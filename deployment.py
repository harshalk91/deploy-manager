from utils import *
from database import *
import logging
from jinja2 import Template
import os
from python_terraform import *
from shutil import copyfile
import json
import boto3

logging.basicConfig(
    filename="deploymanager-workflow",
    filemode='a',
    level=logging.DEBUG,
    format='%(asctime)s.%(msecs)03d %(levelname)s %(module)s - %(funcName)s: %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
)

logging.info("Started...")
logger = logging.getLogger(__name__)


class deployment:

    def create_json(self, data):
        data['start_time'] = get_current_timestamp()
        data['end_time'] = ""
        data['user'] = "Harshal"
        data['status'] = "InProgress"
        data['deployment_id'] = get_uuid()
        logger.debug(data)
        return data

    def get_data(self, collection, deployment_id):
        query = {"deployment_id": deployment_id}
        return database.getData(collection, query)

    def get_deployments(self, collection):
        database.initialize()
        result = database.getAllDeployments(collection)
        re = []
        for i in result:
            logger.debug(i)
            re.append(i)
        return re

    def get_deployment_status(self, collection, query):
        logger.debug("Request came for /status/")

        logger.debug("Initializing DB")
        database.initialize()
        logger.debug("Initialized DB")
        logger.debug("Getting Deployment Status for %s", data)
        result = database.getData(collection, query)
        return result

    @staticmethod
    def getCloudCredentials(cloud_provider):
        logger.debug("Fetching DB Credentials")
        database.initialize()
        collection = "cloudvault"
        query = {"profile": "default", "cloud": "aws"}
        result = database.getData(collection, query)
        re = []
        for i in result:
            re.append(i)
        return re

    @staticmethod
    def jinjaLoader(template_data, deployment_id):
        """

        :param template_data: Terraform tfvars in json format
        :param deployment_id:
        :return:
        """
        logger.debug("Copying template")
        original_file = os.path.join(os.getcwd(), "aws-terraform/terraform.tfvars.j2")
        newfile = os.path.join(os.getcwd(), "aws-terraform/" + deployment_id + "-terraform.tfvars")
        copyfile(original_file, newfile)
        logger.debug("Rendering template")
        with open(newfile, "r+") as f:
            data = f.read()
            j2_template = Template(data)
            f.seek(0)
            f.write(j2_template.render(template_data))
            f.truncate()
        return newfile

    @staticmethod
    def createInstanceTF(terraform_path, collection, deployment_id, tfvars_file):
        """

        :param terraform_path: Terraform Directory absolute path
        :param collection: deployment collection name
        :param deployment_id: deployment_id generated from create_json function
        :param tfvars_file: absolute path for terraform variable file
        :return:
        """
        try:
            database.initialize()
            deploy_id = {"deployment_id": deployment_id}
            tf = Terraform(working_dir=terraform_path, var_file=tfvars_file)

            return_code, stdout, stderr = tf.init()
            if stderr:
                query = {"$set": {'status': 'Terraform Initialization Failed'}}
                database.updateone(collection, deploy_id, query)
                logger.debug(stderr)
                raise ValueError('Terraform Initialization Failed')
            else:
                query = {"$set": {'status': 'Terraform Initialization Complete'}}
                database.updateone(collection, deploy_id, query)

            return_code, stdout, stderr = tf.cmd("apply", "-state=" + deployment_id + ".tfstate",
                                                 "-state-out=" + deployment_id + ".tfstate", "-var-file=" + tfvars_file,
                                                 "-auto-approve")
            # return_code, stdout, stderr = tf.apply(no_color=IsFlagged, refresh=False, skip_plan=True)
            if return_code != 0:
                query = {"$set": {'status': 'Terraform Apply Failed'}}
                database.updateone(collection, deploy_id, query)
                logger.debug(stderr)
                raise ValueError('Terraform Apply Failed')
            else:

                query = {"$set": {'status': 'Terraform Apply Successful'}}
                database.updateone(collection, deploy_id, query)

                tfstate_file = terraform_path + "/" + deployment_id + ".tfstate"
                with open(tfstate_file, 'r') as tfstate_obj:
                    tfstate_json = json.loads(tfstate_obj.read())

                tfstate_data = {"deployment_id": deployment_id, "tfstate": tfstate_json}
                collection = "tfstate"
                database.insert(collection, tfstate_data)
                return "Terraform Apply Successful"
        except ValueError as err:
            logger.debug(err.args)

    @staticmethod
    def readStateFile(tfstate_file):
        instance_ids = []
        tf = Terraform()
        tf.init()
        tfstate_tuple = tf.cmd('show', '-json', tfstate_file)
        tfstate_json = json.loads(tfstate_tuple[1])

        for child_module in tfstate_json['values']['root_module']['child_modules']:
            for resource in child_module['resources']:
                instance_ids.append(resource['values']['instance_state'])
        return instance_ids
    
    @staticmethod
    def check_instance_status(instance_ids, cloud_credentials):
        re = []
        os.environ["aws_access_key_id"] = cloud_credentials[0]['aws_access_key']
        os.environ["aws_secret_access_key "] = cloud_credentials[0]['aws_secret_key']
        os.environ['region'] = cloud_credentials[0]['aws_region']
        ec2 = boto3.resource('ec2', os.environ.get('region'))
        for instance in ec2.instances.get_all_instances(instance_id=instance_ids):
            re.append(instance.state)

        logger.debu(re)
        return re

    @staticmethod
    def insertToDB(collection, data_json):
        database.initialize()
        database.insert(collection, data_json)

    @staticmethod
    def celeryTriggerDeployment(data_json, collection):
        """

        :param data_json: Data Received from User
        :param collection: Mongo db collection
        :return: list of instance ids or error
        """
        data = data_json
        logger.debug("Async Task Started for Triggering Deployment")
        logger.debug(data)
        cloud_credentials = deployment.getCloudCredentials(data['cloud_provider'])
        logger.debug("Triggering deployment for %s", data['name'])
        template_data = {
            "aws_access_key": cloud_credentials[0]['aws_access_key'],
            "aws_secret_key": cloud_credentials[0]['aws_secret_key'],
            "aws_region": cloud_credentials[0]['aws_region'],
            "ami": cloud_credentials[0]['ami'],
            "instance_count": data['instance_count'],
            "instance_type": cloud_credentials[0]['template'][data['template']],
            "key_name": "jumpbox-kepair",
            "subnet_id": "subnet-022ab974e8cce7e1d",
            "security_group_id": "sg-0639f1fc8e91af47e",
            "instance_name": data['name']
        }
        tfvars_file = deployment.jinjaLoader(template_data, data['deployment_id'])
        logger.debug(tfvars_file)
        if os.path.exists(tfvars_file):

            deploy_id = {"deployment_id": data['deployment_id']}
            query = {"$set": {'status': 'Instance Creation Started"'}}
            database.updateone(collection, deploy_id, query)
            logger.debug("DB Updated and deployment status changed")

            terraform_dir = os.path.join(os.getcwd() + "/aws-terraform")
            logger.debug("Instance Created Started")
            inst_status = deployment.createInstanceTF(terraform_dir, collection, data['deployment_id'], tfvars_file)
            if inst_status == "Terraform Apply Successful":
                tfstate_file = terraform_dir + "/" + data['deployment_id'] + '.tfstate'
                instance_ids = deployment.readStateFile(tfstate_file)
                logger.debug(instance_ids)
                #inst_status = deployment.check_instance_status(instance_ids, cloud_credentials)
                #return inst_status
        else:
            logger.error("Error!! File Does Not exist")
            return "Error"
