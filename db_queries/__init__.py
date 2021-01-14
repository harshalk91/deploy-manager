from configparser import ConfigParser
import sqlalchemy
from sqlalchemy import MetaData
from sqlalchemy.ext.automap import automap_base

MYSQL_URL = "mysql://admin:admin@localhost:3306/deploymanager"

config_object = ConfigParser()
config_object.read("config.ini")
db_url = config_object['mysql']
engine = sqlalchemy.create_engine(MYSQL_URL, pool_pre_ping=True)
base = automap_base()
metadata = MetaData(bind=engine)
base.prepare(engine, reflect=True)