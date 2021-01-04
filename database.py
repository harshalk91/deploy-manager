import pymongo


class database(object):
    URI = "mongodb://mongoadmin:secret@192.168.100.2:27017"
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
    def insert(collection, data):
        return database.DATABASE[collection].insert(data)

    @staticmethod
    def updateDeployment(collection, query):
        return database.DATABASE[collection].update(query)
