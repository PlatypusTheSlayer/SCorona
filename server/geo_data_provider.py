import json

class GeoDataProvider:

    def __init__(self):
        with open('resources/county-to-geojson.json') as f:
            self.county_to_geojson = json.load(f)

    def get_geojson_for_county(self, county_name):
        try:
            return self.county_to_geojson[county_name]
        except:
            return self.county_to_geojson['Bedfordshire']

    def get_all_geojsons(self):
        return self.county_to_geojson

if __name__ == "__main__":
    geo_data_provider = GeoDataProvider()
    print(geo_data_provider.get_all_geojsons())