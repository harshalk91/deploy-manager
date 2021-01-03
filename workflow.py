from database import database
from app import logger
from python_terraform import *
from jinja2 import Template
import os
from shutil import copyfile


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


def triggerDeployment(deployment_name, template, instance_count, cloud_credentials):
    try:
        logger.debug("Triggering deployment for %s", deployment_name)
        template_data = {
            "aws_access_key": cloud_credentials[0]['aws_access_key'],
            "aws_secret_key": cloud_credentials[0]['aws_secret_key'],
            "aws_region": "ap-south-1",
            "ami": "ami-0e306788ff2473ccb",
            "instance_count": instance_count,
            "instance_type": template,
            "key_name": "test-key",
            "subnet_id": "subnet-022ab974e8cce7e1d",
            "security_group_id": "sg-0639f1fc8e91af47e"
        }
        tfvars_file = jinjaLoader(template_data)
        if os.path.exists(tfvars_file):
            t = Terraform()
            return_code, stdout, stderr = t.apply()

        return template_data
    except Exception as e:
        return "Error"
