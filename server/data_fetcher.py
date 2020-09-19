from rss_fetcher import RssFetcher
from db_gateway import DBGateway
from data_parser import DataParser
from geo_data_provider import GeoDataProvider

class DataFetcher:
    
    def __init__(self):
        self.rss_fetcher = RssFetcher()
        self.db_gateway = DBGateway()
        self.data_parser = DataParser()
        self.geo_data_provider = GeoDataProvider()

    def fetch(self, date_arg):
        db_data = self.db_gateway.get_everythang()

        if db_data:
            return db_data
        else:
            return self.get_mock_data()
            # return self.fetch_new_data()

    def fetch_new_data(self):
        # news_arr = self.rss_fetcher.fetch_news_data()
        news_arr = self.rss_fetcher.get_news_from_file()

        global_news_count = 0
        county_dict = {}
        for news in news_arr:
            county_name = self.data_parser.parse_text_for_location(news)

            if county_name == 'NO_LOCATION':
                global_news_count += 1
            elif county_name in county_dict:
                county = county_dict[county_name]
                county['newscount'] += 1
            else:
                county_geojson = self.geo_data_provider.get_geojson_for_county(county_name)
                county_data = {
                    'county': {
                        'name': county_name,
                        'geojson': county_geojson
                    },
                    'newscount': 1,
                    'emotions': 1,
                    'opacity': 0.8,
                    'color': '#00ff00'
                }
                county_dict[county_name] = county_data

        for county in county_dict.values():
            county['newscount'] += global_news_count

        return list(county_dict.values())


    def get_mock_data(self):
        geojsons = self.geo_data_provider.get_all_geojsons()
        county_dict = {}

        for geojson in geojsons:
            county_name = geojson['properties']['name']

            county_data = {
                'county': {
                    'name': county_name,
                    'geojson': geojson
                },
                'newscount': 1,
                'emotions': 1,
                'opacity': 0.8,
                'color': '#00ff00'
            }
            county_dict[county_name] = county_data

        return list(county_dict.values())