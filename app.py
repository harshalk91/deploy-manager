import logging
from flask import Flask, render_template, request
from database import database
from utils import get_uuid, get_current_timestamp
from flask_api import status
from workflow import *
from flask_celery import make_celery
import time

logging.basicConfig(
    filename="deploymanager",
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
    CELERY_RESULT_BACKEND='redis://localhost:6379'
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


@app.route("/createdeployment", methods=['POST'])
def createDeployment():
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
        cloud_credentials = getCloudCredentials(data['cloud_provider'])
        logger.debug("Triggering Async Task to create deployment)"
        celeryTriggerDeployment.delay(data['name'],
                          data['template'],
                          data['instance_count'],
                          cloud_credentials,
                          collection,
                          data['deployment_id'])
        #if not str(data['deployment_id']) or res == "Error":
        #    return status.HTTP_500_INTERNAL_SERVER_ERROR
        #else:
        return render_template('show_deployments.html',
                                title='overview',
                                result=result), status.HTTP_200_OK


@celery.task(name='celery_example.celery')
def insertToDB(collection, data):
    logger.debug("Async Task Started for Inserting deployment recrord into DB")
    database.initialize()
    database.insert(collection, data)

@celery.task(name='celery_example.celery_trigger_deployment')
def celeryTriggerDeployment(name, template, instance_count, cloud_credentials, collection, deployment_id):
    logger.debug("Async Task Started for Trigerring Deployment")
    triggerDeployment(name, template, instance_count, cloud_credentials, collection, deployment_id)


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
