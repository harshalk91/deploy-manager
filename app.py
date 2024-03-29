from flask import Flask, render_template, request
from flask_api import status

from deployment import *
from flask_celery import make_celery
from configparser import ConfigParser

config_object = ConfigParser()
config_object.read("config.ini")
redis = config_object['redis']

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
    CELERY_BROKER_URL=redis['CELERY_BROKER_URL'],
    CELERY_RESULT_BACKEND=redis['CELERY_RESULT_BACKEND'],
    CELERY_TASK_SERIALIZER='json',
    CELERY_RESULT_SERIALIZER='json'
)

celery = make_celery(app)
celery_trigger_deployment = make_celery(app)


@app.route("/getdeployments", methods=['GET'])
def getDeployments():
    if request.method == "GET":
        collection = "deployment"
        deployment_obj = deployment()
        re = deployment_obj.get_deployments(collection)
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
        collection = "deployment"
        deployment_obj = deployment()
        deployment_json = deployment_obj.create_json(request.get_json())
        celeryTriggerDeployment.apply_async(
            args=[deployment_json, collection], countdown=2, expires=180)
        deployment.insertToDB(collection, deployment_json)
        result = deployment_obj.get_data(collection, deployment_json['deployment_id'])
        return render_template('show_deployments.html',
                               title='overview',
                               result=result), status.HTTP_200_OK


@app.route("/status", methods=['GET'])
def get_deployment_status():
    if request.method == "GET":
        deployment_obj = deployment()
        query = dict(deployment_id=request.args.get("deployment_id"))
        collection = "deployment"
        result = deployment_obj.get_deployment_status(collection, query)
        if not result:
            return status.HTTP_500_INTERNAL_SERVER_ERROR
        else:
            return render_template('show_deployments.html',
                                   title='overview',
                                   result=result)


@celery.task(name='celery_example.celery_trigger_deployment', serializer='json')
def celeryTriggerDeployment(deployment_json, collection):
    logger.debug("Hello from celeryTriggerDeployment")
    logger.debug(deployment_json)
    logger.debug(type(deployment_json))
    deployment.celeryTriggerDeployment(deployment_json, collection)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5005, debug=True)
