import json
import numpy as np

class GeoDataProvider:

    def __init__(self):
        # with open('british-cities-to-counties.json') as f:
        #     cities_to_counties = json.load(f)
        with open('british-cities-to-counties-clean.json') as f:
            cities_to_counties = json.load(f)
        
        # county_list = np.unique(np.array(list(cities_to_counties.values())))
        # print("County count from british-cities-to-counties.json:", len(county_list))

        county_list = list(cities_to_counties.values())

        with open('british-isles-counties.geojson') as f:
            counties_geojsons = json.load(f)

        features = counties_geojsons['features']
        counties = {}
        for county in features:
            name = ""
            properties = county['properties']
            for prop in properties.values():
                if prop in county_list:
                    name = prop

            if not name:
                continue

            data = {
                'type': 'geojson',
                'data': {
                    'type': 'Feature',
                    'geometry': county['geometry']
                }
            }

            counties[name] = data

        with open('county-to-geojson.json', 'w') as outfile:
            json.dump(counties, outfile)


if __name__ == "__main__":
    GeoDataProvider()