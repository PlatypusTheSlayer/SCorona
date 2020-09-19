import json

class GeoDataProvider:

    def __init__(self):
        with open('resources/british-cities-to-counties.json') as f:
            cities_to_counties = json.load(f)
        
        county_list = list(cities_to_counties.values())

        with open('resources/british-isles-counties.geojson') as f:
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

            data = {}
            data['type'] = county['type']
            data['properties'] = {
                'name': name
            }
            data['geometry'] = county['geometry']
            
            counties[name] = data

        with open('mykacperekoutput.json', 'w') as outfile:
            json.dump(counties, outfile)


if __name__ == "__main__":
    GeoDataProvider()