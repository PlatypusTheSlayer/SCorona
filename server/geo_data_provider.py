import json

class GeoDataProvider:

    def __init__(self):
        with open('resources/british-isles-counties.geojson') as f:
            counties_geojsons = json.load(f)

        features = counties_geojsons['features']
        counties = {}
        for county in features:
            data = {}
            data['type'] = county['type']
            name = county['properties']['VARNAME_1']
            data['properties'] = {
                'name': name
            }
            data['geometry'] = county['geometry']
            
            counties[name] = data

        with open('mykacperekoutput.json', 'w') as outfile:
            json.dump(counties, outfile)


if __name__ == "__main__":
    GeoDataProvider()