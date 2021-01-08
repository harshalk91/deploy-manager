from datetime import datetime
import uuid


def get_current_timestamp():
    dateTimeObj = datetime.now()
    return dateTimeObj.strftime("%d-%b-%Y-%H-%M-%S-%f")


def get_uuid():
    deployment_id = uuid.uuid1()
    return str(deployment_id)
