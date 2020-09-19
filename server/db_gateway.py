import pymongo
from datetime import datetime

class DBGateway:
    
    def __init__(self):
        connection_url = 'mongodb+srv://SCorona-user:QeiFrZ23QM7FNStA@scoronacluster.xdyqi.mongodb.net/test?retryWrites=true&w=majority'
        database_name = 'SCoronaDB'
        db_client = pymongo.MongoClient(connection_url)
        self.db = db_client.get_database(database_name)

    def get_everythang(self):
        return ""