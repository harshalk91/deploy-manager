from database import database
#from app import logger
import logging
from python_terraform import *
from jinja2 import Template
import os
from shutil import copyfile
import subprocess
import time
from database import database

logging.basicConfig(
    filename="deploymanager-workflow",
    filemode='a',
    level=logging.DEBUG,
    format='%(asctime)s.%(msecs)03d %(levelname)s %(module)s - %(funcName)s: %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
)
logging.info("Started...")
logger = logging.getLogger(__name__)


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


def jinjaLoader(template_data):
    logger.debug("Copying template")
    original_file = os.path.join(os.getcwd(), "terraform/terraform.tfvars.j2")
    newfile = os.path.join(os.getcwd(), "terraform/terraform.tfvars")
    copyfile(original_file, newfile)
    logger.debug("Rendering template")
    with open(newfile, "r+") as f:
        data = f.read()
        j2_template = Template(data)
        f.seek(0)
        f.write(j2_template.render(template_data))
        f.truncate()
    return newfile


def createInstance():
    command = "sh " + os.getcwd() + "/scripts/create-instance.sh " + os.path.join(os.getcwd(), "terraform") + " >> " + os.path.join(os.getcwd()) + "/deploymanager " + "2>&1"
    logger.debug(command)
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    process.wait()
    output, error = process.communicate()
    logger.debug(output)
    #command = "sh " + os.getcwd() + "/scripts/read-state,sh " + os.path.join(os.getcwd(), "terraform")
    #tf_state = subprocess.check_output(["sh", + os.getcwd() + "/scripts/read-state.sh", os.path.join(os.getcwd(), "terraform")])
    #logger.debug(tf_state)
    #return tf_state

def createInstancetf(terraform_path):
    tf = Terraform(working_dir=terraform_path)
    
    tf_init = tf.init()
    logger.debug(tf_init)
    
    tf_plan = tf.plan()
    logger.debug(tf_plan)


    tf_apply = tf.apply(no_color=IsFlagged, refresh=False, skip_plan=True)
    logger.debug(tf_apply)


    read_state_file = tf.read_state_file()
    logger.debug(read_state_file)
    return read_state_file

def triggerDeployment(deployment_name, template, instance_count, collection, deployment_id, cloud_provider):
    try:
        logger.debug("Inside triggerDeployment")
        database.initailize()
        logger.debug("Database initialized")
        cloud_credentials = getCloudCredentials(cloud_provider)        
        logger.debug(cloud_credentials)
        logger.debug("Triggering deployment for %s", deployment_name)
        template_data = {
            "aws_access_key": cloud_credentials[0]['aws_access_key'],
            "aws_secret_key": cloud_credentials[0]['aws_secret_key'],
            "aws_region": cloud_credentials[0]['aws_region'],
            "ami": cloud_credentials[0]['ami'],
            "instance_count": instance_count,
            "instance_type": cloud_credentials[0]['template'][template],
            "key_name": "jumpbox-kepair",
            "subnet_id": "subnet-022ab974e8cce7e1d",
            "security_group_id": "sg-0639f1fc8e91af47e"
        }
        tfvars_file = jinjaLoader(template_data)
        logger.debug(tfvars_file)
        if os.path.exists(tfvars_file):
            instance_creation_status = createInstance()
            logger.debug(tfvars_file)
            newvalues = '{"deployment_id": deployment_id}, {$set: {"status": "Instance Creation Started"}}'
            database.updateDeployment(collection, newvalues)

            logger.debug("DB Updated and deployment status changed")
            #database.updateDeployment(collection, query={"deployment_id": deployment_id, {$set: {"status": "Instance Creation Started"}}))
            return instance_creation_status
        else:
            logger.error("Error!! File Does Not exist" )
            return "Error"

    except Exception as e:
        return "Error"
