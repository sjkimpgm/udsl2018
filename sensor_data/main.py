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

#############
## API
#############
class NewValue(Resource):
    def post(self, sensor_name):
        args = parser.parse_args()
        (allowed, msg) = check_credential(args['credential'])
        if not allowed:
            return {"status": "ERROR", "message": msg}, 400

        data = json.loads(args['data'])

        cursor = get_db()
        cursor.execute("""
            INSERT INTO {0} (name, timestamp, latitude, longitude, value) 
            VALUES (%s, %s, %s, %s, %s)
            """.format(sensor_name), 
            (data['name'], data['timestamp'], data['latitude'], data['longitude'], data['value']))

        new_id = cursor.lastrowid

        return {"status": "OK", "id": new_id}

class GetValue(Resource):
    def get(self, sensor_name):
        args = parser.parse_args()
        (allowed, msg) = check_credential(args['credential'])
        if not allowed:
            return {"status": "ERROR", "message": msg}, 400

        cursor = get_db()
        cursor.execute("""
        SELECT * FROM {0} ORDER BY timestamp DESC LIMIT 1
        """.format(sensor_name))

        row = cursor.fetchone()
        if row is None:
            return {"status": "ERROR", "message": "Invalid id"}

        (id, name, timestamp, latitude, longitude, value) = row
        timestamp = str(timestamp)
        row = {"id": id, "name": name, "count": 1, "timestamp": timestamp, "latitude": latitude, "longitude": longitude, "value": value}

        return {"status": "OK", "count": cursor.rowcount, "data": json.dumps(row)}

class GetRange(Resource):
    def get(self, sensor_name, start_ts, end_ts):
        args = parser.parse_args()
        (allowed, msg) = check_credential(args['credential'])
        if not allowed:
            return {"status": "ERROR", "message": msg}, 400

        cursor = get_db()
        cursor.execute("""
        SELECT * FROM {0} WHERE timestamp >= %s AND timestamp <= %s ORDER BY timestamp 
        """.format(sensor_name), (start_ts, end_ts))

        rows = cursor.fetchall()
        rows_json = []
        for (id, name, timestamp, latitude, longitude, value) in rows:
            timestamp = str(timestamp)
            rows_json.append({"id": id, "name": name, "timestamp": timestamp, "latitude": latitude, "longitude": longitude, "value": value})

        return {"status": "OK", "count": cursor.rowcount, "data": json.dumps(rows_json)}

class DeleteValue(Resource):
    def post(self, sensor_name, id):
        args = parser.parse_args()
        (allowed, msg) = check_credential(args['credential'])
        if not allowed:
            return {"status": "ERROR", "message": msg}, 400

        cursor = get_db()
        cursor.execute("""
        DELETE FROM {0} where id = %s
        """.format(sensor_name), (id,))

        if cursor.rowcount == 0:
            return {"status": "ERROR", "message": "Invalid id"}

        return {"status": "OK", "count": cursor.rowcount}

class DeleteAllValues(Resource):
    def post(self, sensor_name):
        args = parser.parse_args()
        (allowed, msg) = check_credential(args['credential'])
        if not allowed:
            return {"status": "ERROR", "message": msg}, 400

        cursor = get_db()
        cursor.execute("""
        DELETE FROM {0}
        """.format(sensor_name))

        return {"status": "OK", "count": cursor.rowcount}

api.add_resource(NewValue, '/new/<string:sensor_name>')
api.add_resource(GetValue, '/get/<string:sensor_name>')
api.add_resource(GetRange, '/get_range/<string:sensor_name>/<start_ts>/<end_ts>')
api.add_resource(DeleteValue, '/delete/<string:sensor_name>/<int:id>')
api.add_resource(DeleteAllValues, '/delete_all/<string:sensor_name>')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', ssl_context=('cert.pem', 'key.pem'))
