import pymongo
from datetime import datetime

class DBGateway:
    
    def __init__(self):
        connection_url = 'mongodb+srv://SCorona-user:QeiFrZ23QM7FNStA@scoronacluster.xdyqi.mongodb.net/test?retryWrites=true&w=majority'
        database_name = 'SCoronaDB'
        db_client = pymongo.MongoClient(connection_url)
        db = db_client.get_database(database_name)
        self.collection = db.get_collection('news-analysis')

    def insert(self, data):
        self.collection.insert_one(data)

    def get_everythang(self):
        return ""