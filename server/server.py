from datetime import date
from flask import Flask, request, jsonify
import dateparser

app = Flask(__name__)

@app.route('/map-data', methods=['GET'])
def get_map_data():
    query_date_string = request.args.get('date')

    if query_date_string:
        query_date = dateparser.parse(query_date_string)
        print("Processing for date", query_date)
    else:
        query_date = date.today()
        print("Processing for current date", query_date)

    return jsonify(query_date)