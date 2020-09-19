from rss_fetcher import RssFetcher
from db_gateway import DBGateway
from data_parser import DataParser

class DataFetcher:
    
    def __init__(self):
        self.rss_fetcher = RssFetcher()
        self.db_gateway = DBGateway()
        self.data_parser = DataParser()

    def fetch(self, date_arg):
        db_data = self.db_gateway.get_everythang()

        if db_data:
            return db_data
        else:
            return self.fetch_new_data()

    def fetch_new_data(self):
        news_arr = self.rss_fetcher.fetch_news_data()

        county_dict = {}
        for news in news_arr:
            county_name = self.data_parser.parse_text_for_location(news)
            county_geojson = {}
            # emotions = whatever
            # color = whatever
            
            if county_name in county_dict:
                county = county_dict[county_name]
                county['newscount'] += 1
                county['emotions'] += 1
            else:
                data = {
                    'county': {
                        'name': county_name,
                        'geojson': county_geojson
                    },
                    'newscount': 2,
                    'emotions': 1,
                    'color': '#222222'
                }
            county_dict[county_name] = data

        return list(county_dict.values())

        
