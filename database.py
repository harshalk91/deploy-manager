import pymongo
from configparser import ConfigParser
config_object = ConfigParser()
config_object.read("config.ini")
db = config_object['db']


class database(object):
    URI = db["URI"]
    DATABASE = None

    @staticmethod
    def initialize():
        client = pymongo.MongoClient(database.URI)
        database.DATABASE = client['deploymanager']

    @staticmethod
    def getAllDeployments(collection):
        return database.DATABASE[collection].find()

    @staticmethod
    def getData(collection, query):
        return database.DATABASE[collection].find(query)
    
    @staticmethod
    def getLastInsertedDocument(collection):
        return database.DATABASE[collection].find().sort([("_id", -1)]).limit(1)
    

    @staticmethod
    def insert(collection, data):
        return database.DATABASE[collection].insert(data)

    @staticmethod
    def updateDeployment(collection, query):
        return database.DATABASE[collection].update(query)
    
    @staticmethod
    def updateone(collection, old, new):
        return database.DATABASE[collection].update_one(old, new)
