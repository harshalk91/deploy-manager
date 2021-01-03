import logging
from flask import Flask, render_template, request
from database import database
from utils import get_uuid, get_current_timestamp
from flask_api import status
import workflow

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


@app.route("/getdeployments", methods=['GET'])
def getDeployments():
    if request.method == "GET":
        logger.debug("Initializing DB")
        database.initialize()
        logger.debug("Initialized DB")
        collection = "deployment"
        logger.debug("Getting results from DB")
        result = database.getAllDeployments(collection)
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
        database.initialize()
        result = database.insert(collection, data)
        logger.debug(result)
        cloud_credentials = workflow.getCloudCredentials(data['cloud_provider'])
        res = workflow.triggerDeployment(data['name'],
                                         data['template'],
                                         data['instance_count'],
                                         cloud_credentials)
        if not str(data['deployment_id']) or res == "Error":
            return status.HTTP_500_INTERNAL_SERVER_ERROR
        else:
            return res, status.HTTP_201_CREATED


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
