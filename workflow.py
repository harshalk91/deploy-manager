from database import database
from wsgi import logger
from python_terraform import *
from jinja2 import Template
import os
from shutil import copyfile
import subprocess
import time


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
    logger.debug(StringIO(output))
    tf_state = subprocess.check_output(["sh", + os.getcwd() + "/scripts/read-state.sh", os.path.join(os.getcwd(), "terraform")])
    logger.debug(tf_state)
    return tf_state


def triggerDeployment(deployment_name, template, instance_count, cloud_credentials):
    try:
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
        if os.path.exists(tfvars_file):
            logger.debug("Instance Creation Triggered")
            instance_creation_status = createInstance()
            return instance_creation_status
        else:
            logger.error("Error!! File Does Not exist" )
            return "Error"

    except Exception as e:
        return "Error"
