from flask import Flask, g
from flask_restful import Resource, Api, reqparse
import mysql.connector

import json

parser = reqparse.RequestParser()
parser.add_argument('data')
parser.add_argument('credential')

app = Flask(__name__)
api = Api(app)


#############
## Configuration
#############
from dbms_config import *
from credential import *

DATA_NAME_LISTS = [
    "PM1",
    "PM25",
    "PM10",
    "TEMPERATURE",
    "PRESSURE",
    "HUMIDITY",
    "AIR_SPEED",
    "VISIBLE_LIGHT_INTENSITY",
    "NEAR_IR_LIGHT_INTENSITY",
    "TVOC",
    "CO2",
    "SO2",
    "CO",
    "O3",
    "NO2",
    "H2S",
]

#############
## Utilities
#############
def connect_db():
    cnx = mysql.connector.connect(user=DBMS_USER, password=DBMS_PASSWD,
            host=DBMS_HOST,
            database=DBMS_DATABASE,
            port=DBMS_PORT)
    cursor = cnx.cursor()

    return (cnx, cursor)

def get_db():
    if not hasattr(g, 'db_cursor'):
        conn, cursor = connect_db()
        g.db_conn = conn
        g.db_cursor = cursor
    return g.db_cursor

def check_credential(code):
    if code is None:
        return (False, "Please provide your creential code")
    elif code in allowed_codes:
        return (True, "")
    else:
        return (False, "Invalid credential code")

def check_data_name(data_name):
    if data_name is None:
        return (False, "Please provide data name")
    elif data_name in DATA_NAME_LISTS:
        return (True, "")
    else:
        return (False, "Invalid data name")

#############
## API
#############
class NewValue(Resource):
    def post(self, data_name):
        args = parser.parse_args()
        (allowed, msg) = check_credential(args['credential'])
        if not allowed:
            return {"status": "ERROR", "message": msg}, 400

        (allowed, msg) = check_data_name(data_name)
        if not allowed:
            return {"status": "ERROR", "message": msg}, 400

        data = json.loads(args['data'])

        cursor = get_db()
        cursor.execute("""
            INSERT INTO urban (data_name, sensor_name, sensor_id, timestamp, latitude, longitude, value) 
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            """,
            (data_name, data['sensor_name'], data['sensor_id'], data['timestamp'], data['latitude'], data['longitude'], data['value']))

        new_id = cursor.lastrowid

        return {"status": "OK", "id": new_id}

class GetValue(Resource):
    def get(self, data_name):
        args = parser.parse_args()
        (allowed, msg) = check_credential(args['credential'])
        if not allowed:
            return {"status": "ERROR", "message": msg}, 400

        (allowed, msg) = check_data_name(data_name)
        if not allowed:
            return {"status": "ERROR", "message": msg}, 400

        cursor = get_db()
        cursor.execute("""
        SELECT * FROM urban WHERE data_name = %s ORDER BY timestamp DESC LIMIT 1
        """, (data_name,))

        row = cursor.fetchone()
        if row is None:
            return {"status": "ERROR", "message": "Invalid id"}

        (id, data_name, sensor_name, sensor_id, timestamp, latitude, longitude, value) = row
        timestamp = str(timestamp)
        row = {"id": id, "data_name": data_name, "sensor_name": sensor_name, "sensor_id": sensor_id, "timestamp": timestamp, "latitude": latitude, "longitude": longitude, "value": value}

        return {"status": "OK", "count": cursor.rowcount, "data": json.dumps(row)}

class GetRange(Resource):
    def get(self, data_name, start_ts, end_ts):
        args = parser.parse_args()
        (allowed, msg) = check_credential(args['credential'])
        if not allowed:
            return {"status": "ERROR", "message": msg}, 400

        (allowed, msg) = check_data_name(data_name)
        if not allowed:
            return {"status": "ERROR", "message": msg}, 400

        cursor = get_db()
        cursor.execute("""
        SELECT * FROM urban WHERE data_name = %s AND timestamp >= %s AND timestamp <= %s ORDER BY timestamp 
        """, (data_name, start_ts, end_ts))

        rows = cursor.fetchall()
        rows_json = []
        for (id, data_name, sensor_name, sensor_id, timestamp, latitude, longitude, value) in rows:
            timestamp = str(timestamp)
            row = {"id": id, "data_name": data_name, "sensor_name": sensor_name, "sensor_id": sensor_id, "timestamp": timestamp, "latitude": latitude, "longitude": longitude, "value": value}
            rows_json.append(row)

        return {"status": "OK", "count": cursor.rowcount, "data": json.dumps(rows_json)}

class DeleteValue(Resource):
    def post(self, data_name, id):
        args = parser.parse_args()
        (allowed, msg) = check_credential(args['credential'])
        if not allowed:
            return {"status": "ERROR", "message": msg}, 400

        (allowed, msg) = check_data_name(data_name)
        if not allowed:
            return {"status": "ERROR", "message": msg}, 400

        cursor = get_db()
        cursor.execute("""
        DELETE FROM urban WHERE data_name = %s AND id = %s
        """, (data_name, id,))

        if cursor.rowcount == 0:
            return {"status": "ERROR", "message": "Invalid id"}

        return {"status": "OK", "count": cursor.rowcount}

class DeleteAllValues(Resource):
    def post(self, data_name):
        args = parser.parse_args()
        (allowed, msg) = check_credential(args['credential'])
        if not allowed:
            return {"status": "ERROR", "message": msg}, 400

        (allowed, msg) = check_data_name(data_name)
        if not allowed:
            return {"status": "ERROR", "message": msg}, 400

        cursor = get_db()
        cursor.execute("""
        DELETE FROM urban WHERE data_name = %s
        """, (data_name,))

        return {"status": "OK", "count": cursor.rowcount}

api.add_resource(NewValue, '/new/<string:data_name>')
api.add_resource(GetValue, '/get/<string:data_name>')
api.add_resource(GetRange, '/get_range/<string:data_name>/<start_ts>/<end_ts>')
api.add_resource(DeleteValue, '/delete/<string:data_name>/<int:id>')
api.add_resource(DeleteAllValues, '/delete_all/<string:data_name>')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', ssl_context=('cert.pem', 'key.pem'))
