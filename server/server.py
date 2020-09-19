#!/usr/bin/env python3

from datetime import date
from flask import Flask, request, jsonify
import dateparser
import logging

from db_gateway import DBGateway
from data_fetcher import DataFetcher

connection_url = 'mongodb+srv://SCorona-user:QeiFrZ23QM7FNStA@scoronacluster.xdyqi.mongodb.net/test?retryWrites=true&w=majority'
database_name = 'SCoronaDB'
db = DBGateway(connection_url, database_name)

data_fetcher = DataFetcher()

app = Flask(__name__)
logger = logging.getLogger('werkzeug')

@app.route('/map-data', methods=['GET'])
def get_map_data():
    query_date_string = request.args.get('date')

    if query_date_string:
        query_date = dateparser.parse(query_date_string)
    else:
        query_date = date.today()

    try:
        map_data = db.get_everythin(query_date)
    except:
        map_data = data_fetcher.fetch_news_data(query_date)
        db.write_everythin(map_data)
        
    return jsonify(map_data)

if __name__ == "__main__":
    app.run(debug=True)