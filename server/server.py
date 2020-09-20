#!/usr/bin/env python3

from datetime import datetime
from flask import Flask, request, jsonify
import dateparser
from flask import send_from_directory
from db_gateway import DBGateway
from data_fetcher import DataFetcher
from flask import Flask
from flask_cors import CORS
import sched, time
import logging
import threading

db_gateway = DBGateway()
data_fetcher = DataFetcher(db_gateway)

app = Flask(__name__)
CORS(app)
logging.basicConfig(level=logging.ERROR)
log = logging.getLogger(__name__)

@app.route('/map-data', methods=['GET'])
def get_map_data():
    query_date_string = request.args.get('date')

    if query_date_string:
        query_date = dateparser.parse(query_date_string)
    else:
        query_date = datetime.today().utcnow()

    data = data_fetcher.fetch(query_date)
    
    return jsonify(data)

def update_db(db_updater, delay):
    app.logger.error("Running updater")
    data = data_fetcher.fetch_new_data()
    db_gateway.insert(data)
    app.logger.error("Update successful. Scheduling the next one...")
    db_updater.enter(delay, 2, update_db, argument=(db_updater, delay))
    app.logger.error("Update scheduled.")
    db_updater.run()

def run_updater():
    delay = 7200
    db_updater = sched.scheduler(time.time, time.sleep)
    db_updater.enter(0, 2, update_db, argument=(db_updater, delay))
    db_updater.run()


if __name__ == "__main__":
    updater_thread = threading.Thread(target=run_updater)

    updater_thread.start()
    app.run(debug=True)