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



def createInstancetf(terraform_path, collection, deployment_id):
    try:
       database.initialize()
       deploy_id = { "deployment_id": deployment_id }

       tf = Terraform(working_dir=terraform_path)
    
       return_code, stdout, stderr = tf.init()
       if stderr:
          query = {"$set": {'status': 'Terraform Initialization Failed'}}
          database.updateone(collection, deploy_id, query) 
          logger.debug(stderr)
          raise ValueError('Terraform Initialization Failed')
             
       
       return_code, stdout, stderr = tf.plan()
       if stderr:
          query = {"$set": {'status': 'Terraform Plan Failed'}}
          database.updateone(collection, deploy_id, query)
          logger.debug(stderr)
          raise ValueError('Terraform Plan Failed')



       return_code, stdout, stderr = tf.apply(no_color=IsFlagged, refresh=False, skip_plan=True)
       if stderr:
          query = {"$set": {'status': 'Terraform Apply Failed'}}
          database.updateone(collection, deploy_id, query)
          logger.debug(stderr)
          raise ValueError('Terraform Apply Failed')

       return "Terraform Apply Successfull"
       #read_state_file = tf.read_state_file()
       #logger.debug(read_state_file)

    except ValueError as err:
       logger.debug(err.args)
