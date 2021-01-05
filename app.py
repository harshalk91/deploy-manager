import logging
from flask import Flask, render_template, request, redirect
from database import database
from utils import get_uuid, get_current_timestamp
from flask_api import status
from workflow import *
from flask_celery import make_celery
import time

logging.basicConfig(
    filename="deploymanager-workflow",
    filemode='a',
    level=logging.DEBUG,
    format='%(asctime)s.%(msecs)03d %(levelname)s %(module)s - %(funcName)s: %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
)
logging.info("Started...")
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.config.update(
    CELERY_BROKER_URL='redis://localhost:6379',
    CELERY_RESULT_BACKEND='redis://localhost:6379',
    CELERY_TASK_SERIALIZER='json',
    CELERY_RESULT_SERIALIZER='json'
)
celery = make_celery(app)
celery_trigger_deployment = make_celery(app)
celery_2 = make_celery(app)


@app.route("/getdeployments", methods=['GET'])
def getDeployments():
    if request.method == "GET":
        collection = "deployment"
        logger.debug("Initializing DB")
        database.initialize()
        logger.debug("Initialized DB")
        logger.debug("Getting results from DB")
        result = database.getAllDeployments(collection)
        logging.debug(result)
        re = []
        for i in result:
            logger.debug(i)
            re.append(i)
        if not re:
            return status.HTTP_500_INTERNAL_SERVER_ERROR
        else:
            return render_template('show_deployments.html',
                                   title='overview',
                                   result=re), status.HTTP_200_OK


@app.route("/createdeployment", methods=['POST', 'GET'])
def createDeployment():
    if request.method == "GET":
        database.initialize()
        result = database.getLastInsertedDocument("deployment")
        re = []
        for i in result:
            logger.debug(i)
            re.append(i)

        return render_template('show_deployments.html',
                               title='overview',
                               result=re), status.HTTP_200_OK

    if request.method == "POST":
        logger.debug("Request Came for inserting data")
        data = request.get_json()
        data['start_time'] = get_current_timestamp()
        data['end_time'] = ""
        data['user'] = "Harshal"
        data['status'] = "InProgress"
        data['deployment_id'] = get_uuid()
        collection = "deployment"
        logger.debug("Initializing DB")

        insertToDB.delay(collection, data)
        query = {"deployment_id": data['deployment_id']}
        database.initialize()
        time.sleep(1)
        result = database.getData(collection, query)
        # cloud_credentials = getCloudCredentials(data['cloud_provider'])
        logger.debug("Triggering Async Task to create deployment")
        celeryTriggerDeployment.apply_async(
            args=[data['name'], data['template'], data['instance_count'], collection, data['deployment_id'],
                  data['cloud_provider']], countdown=2, expires=180)
        return render_template('show_deployments.html',
                               title='overview',
                               result=result), status.HTTP_200_OK


@celery.task(name='celery_example.celery')
def insertToDB(collection, data):
    logger.debug("Async Task Started for Inserting deployment record into DB")
    database.initialize()
    database.insert(collection, data)


@celery.task(name='celery_example.celery_trigger_deployment', serializer='json')
def celeryTriggerDeployment(name, template, instance_count, collection, deployment_id, cloud_provider):
    logger.debug("Async Task Started for Triggering Deployment")
    database.initialize()
    logger.debug("Database initialized")
    cloud_credentials = getCloudCredentials(cloud_provider)
    logger.debug(cloud_credentials)
    logger.debug("Triggering deployment for %s", name)
    template_data = {
        "aws_access_key": cloud_credentials[0]['aws_access_key'],
        "aws_secret_key": cloud_credentials[0]['aws_secret_key'],
        "aws_region": cloud_credentials[0]['aws_region'],
        "ami": cloud_credentials[0]['ami'],
        "instance_count": instance_count,
        "instance_type": cloud_credentials[0]['template'][template],
        "key_name": "jumpbox-kepair",
        "subnet_id": "subnet-022ab974e8cce7e1d",
        "security_group_id": "sg-0639f1fc8e91af47e",
        "instance_name": name
    }
    tfvars_file = jinjaLoader(template_data)
    logger.debug(tfvars_file)
    if os.path.exists(tfvars_file):

        deploy_id = {"deployment_id": deployment_id}
        query = {"$set": {'status': 'Instance Creation Started"'}}
        database.updateone(collection, deploy_id, query)
        logger.debug("DB Updated and deployment status changed")

        terraform_dir = os.path.join(os.getcwd() + "/aws-terraform")
        logger.debug("Instance Created Started")
        inst_status = createInstancetf(terraform_dir, collection, deployment_id)
        logger.debug(inst_status)
    else:
        logger.error("Error!! File Does Not exist")
        return "Error"


@app.route("/status", methods=['GET'])
def get_deployment_status():
    if request.method == "GET":
        logger.debug("Request came for /status/")
        data = request.args.get("deployment_id")
        logger.debug("data: %s", data)
        query = dict(deployment_id=data)
        collection = "deployment"
        logger.debug("Initializing DB")
        database.initialize()
        logger.debug("Initialized DB")
        logger.debug("Getting Deployment Status for %s", data)
        result = database.getData(collection, query)
        if not result:
            return status.HTTP_500_INTERNAL_SERVER_ERROR
        else:
            return render_template('show_deployments.html',
                                   title='overview',
                                   result=result)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5005, debug=True)
