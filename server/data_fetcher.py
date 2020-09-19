from rss_fetcher import RssFetcher
from db_gateway import DBGateway
from data_parser import DataParser
from geo_data_provider import GeoDataProvider
from twitter_fetcher import TwitterFetcher
from sentiment_evaluator import predict_sentiment
import datetime

class DataFetcher:
    
    def __init__(self, db_gateway):
        self.rss_fetcher = RssFetcher()
        self.db_gateway = db_gateway
        self.data_parser = DataParser()
        self.geo_data_provider = GeoDataProvider()
        self.twitter_fetcher = TwitterFetcher()

    def fetch(self, date_arg):
        db_data = self.db_gateway.get(date_arg)

        if db_data:
            return db_data
        else:
            db_data = self.db_gateway.get(datetime.date.today())
            if db_data:
                return db_data
            else:
                data = self.fetch_new_data()
                self.db_gateway.insert(data)
                return data

    def fetch_new_data(self):
        # news_arr = self.rss_fetcher.fetch_news_data()
        news_arr = self.rss_fetcher.get_news_from_file()

        global_sentiment = {
            'positive': 0,
            'negative': 0
        }
        county_dict = self.get_all_county_data()
        for news in news_arr:
            county_name = self.data_parser.parse_text_for_location(news)
            sentiment = predict_sentiment(news)

            if county_name == 'NO_LOCATION':
                global_news_count += 1
                global_sentiment[sentiment] += 1
            elif county_name in county_dict:
                county = county_dict[county_name]
                county['newscount'] += 1
                county['emotions'][sentiment] += 1
            else:
                county_geojson = self.geo_data_provider.get_geojson_for_county(county_name)
                county_data = {
                    'county': {
                        'name': county_name,
                        'geojson': county_geojson
                    },
                    'newscount': 1,
                    'emotions': {
                        'positive': 0
                        'negative': 0
                    },
                    'color': '#00ff00'
                }
                county_data['emotions'][sentiment] += 1
                county_dict[county_name] = county_data

        tweets = self.twitter_fetcher.get_yesterday_twitter_data(300)
        for tweet in tweets:
            county_name = self.data_parser.parse_text_for_location(tweet)
            sentiment = predict_sentiment(tweet)

            if county_name == 'NO_LOCATION':
                global_news_count += 1
                global_sentiment[sentiment] += 1
            elif county_name in county_dict:
                county = county_dict[county_name]
                county['newscount'] += 1
                county['emotions'][sentiment] += 1
            else:
                county_geojson = self.geo_data_provider.get_geojson_for_county(county_name)
                county_data = {
                    'county': {
                        'name': county_name,
                        'geojson': county_geojson
                    },
                    'newscount': 1,
                    'emotions': {
                        'positive': 0
                        'negative': 0
                    },
                    'color': '#00ff00'
                }
                county_data['emotions'][sentiment] += 1
                county_dict[county_name] = county_data

        max_newscount = -1
        for county in county_dict.values():
            county['newscount'] += 1
            county['emotions']['positive'] += global_sentiment['positive']
            county['emotions']['negative'] += global_sentiment['negative']

            if county['newscount'] > max_newscount:
                max_newscount = county['newscount']
            
        for county in county_dict.values():
            county['opacity'] = county['newscount'] / max_newscount

        return list(county_dict.values())


    def get_all_county_data(self):
        geojsons = self.geo_data_provider.get_all_geojsons()
        county_dict = {}
        for key, geojson in geojsons.items():
            county_name = key

            county_data = {
                'county': {
                    'name': county_name,
                    'geojson': geojson
                },
                'newscount': 0,
                'emotions': 0,
                'opacity': 1,
                'color': '#00ff00'
            }
            county_dict[county_name] = county_data

        return county_dict

if __name__ == "__main__":
    data_fetcher = DataFetcher()
    data_fetcher.fetch_new_data()