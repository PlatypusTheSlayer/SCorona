import pymongo

class DBGateway:
    
    def __init__(self, connection_url, database_name):
        db_client = pymongo.MongoClient(connection_url)
        self.db = db_client.get_database(database_name)

    def get_everythin(self, date_arg):
        factor_collection = self.db.get_collection('corona_factor')
        factor = factor_collection.find_one(date_arg)
        
        area_collection = self.db.get_collection('areas')
        area_list = factor.get('areas')

        data_list = []
        for area in area_list:
            obj = {}
            area_data = area_collection.find_one({'_id': area['id']})
            obj['area'] = area_data
            obj['factor'] = area

            data_list.append(obj)

        return data_list

    def write_everythin(self, data_to_write):
        return data_to_write