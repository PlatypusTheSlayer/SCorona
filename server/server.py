#!/usr/bin/env python3

from datetime import datetime
from flask import Flask, request, jsonify
import dateparser
from db_gateway import DBGateway
from data_fetcher import DataFetcher

data_fetcher = DataFetcher()

app = Flask(__name__)

@app.route('/map-data', methods=['GET'])
def get_map_data():
    query_date_string = request.args.get('date')

    if query_date_string:
        query_date = dateparser.parse(query_date_string)
    else:
        query_date = datetime.today().utcnow()

    data = data_fetcher.fetch(query_date)
    
    return jsonify(data)

if __name__ == "__main__":
    app.run(debug=True)