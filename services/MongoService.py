# This service is to perform Mongo tasks using python library.
import pymongo

class MongoService:
    def __init__(self):
        # Write code to setup connection with Mongo
        client = pymongo.MongoClient(database.URI)
        database.DATABASE = client['deploymanager']

    def inset(self):
        pass

    def update(self):
        pass

    def get(self):
        pass

    def delete(self):
        pass