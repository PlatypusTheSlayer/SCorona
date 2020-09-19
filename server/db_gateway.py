import pymongo
import datetime

class DBGateway:
    
    def __init__(self):
        connection_url = 'mongodb+srv://SCorona-user:QeiFrZ23QM7FNStA@scoronacluster.xdyqi.mongodb.net/test?retryWrites=true&w=majority'
        database_name = 'SCoronaDB'
        db_client = pymongo.MongoClient(connection_url)
        db = db_client.get_database(database_name)
        self.collection = db.get_collection('news-analysis')

    def insert(self, data):
        dateobject = datetime.date.today()
        current_date = datetime.datetime.combine(dateobject, datetime.time())
        data = {
            "date": current_date,
            "data": data
        }
        self.collection.update_one({'date': {'$eq': current_date}}, {"$set": data}, upsert=True)

    def get(self, date_param):
        date_param = datetime.datetime.combine(date_param, datetime.time())
        document = self.collection.find_one({'date': {'$eq': date_param}})

        try:
            return document['data']
        except:
            return None

if __name__ == "__main__":
    db_gateway = DBGateway()
    print(db_gateway.get(datetime.date.today()))