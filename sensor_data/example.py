from requests import post, get
import json

# Configurations
api_url_prefix = "<url>"
credential = "<code>"

# Disable 'SubjectAltNameWarning'
import requests
from requests.packages.urllib3.exceptions import SubjectAltNameWarning
requests.packages.urllib3.disable_warnings(SubjectAltNameWarning)

# API url format
#  - http://147.47.220.28:5000/<command>/<sensor type>
#  - command: new, get, get_range, delete, delete_all
#  - sensor type: PM1, PM10, PM25, TEMPERATURE, PRESSURE, HUMIDITY, AIR_SPEED, ...

# Response field (common)
#  - status: if success, "OK". otherwise "ERROR"
#  - message: only for 'ERROR'. Error description

DATA_NAME = "PM25"

#-----------------------------------------------
# 1. Insert new value
#-----------------------------------------------
new_data = """{"sensor_name":"pm2007", "sensor_id":"AABBCCDDEEFF", "timestamp": "2018-05-11 14:00:00.000000", "latitude": 37.45, "longitude": 126.8, "value":12.7}"""
ret = post('{0}/new/{1}'.format(api_url_prefix, "NEAR_IR_LIGHT_INTENSITY"), data={"data": new_data, "credential": credential}, verify='cert.pem').json()
new_id = ret['id']
print("New value is inserted, ID: {0}".format(new_id))

for i in range(5):
    new_data = """{"sensor_name":"pm2007", "sensor_id":"AABBCCDDEEFF", "timestamp": "2018-05-11 14:34:0""" + str(i) + """.382242", "latitude": 37.45, "longitude": 126.8, "value":12.7}"""
    ret = post('{0}/new/{1}'.format(api_url_prefix, DATA_NAME), data={"data": new_data, "credential": credential}, verify='cert.pem').json()
    new_id = ret['id']
    print("New value is inserted, ID: {0}".format(new_id))

# Response field
#  - status
#  - id: id of inserted row(value)

#-----------------------------------------------
# 1-2. Insert new value with invalid data name
#-----------------------------------------------
new_data = """{"sensor_name":"pm2007", "sensor_id":"AABBCCDDEEFF", "timestamp": "2018-05-11 14:00:00.000000", "latitude": 37.45, "longitude": 126.8, "value":12.7}"""
ret = post('{0}/new/{1}'.format(api_url_prefix, "INVALID_DATA_NAME"), data={"data": new_data, "credential": credential}, verify='cert.pem').json()
assert(ret['status'] == "ERROR")
assert(ret['message'] == "Invalid data name")
print("Invalid data name is rejected")

#-----------------------------------------------
# 2. Retrieve last(based on 'timestamp' field) value
#-----------------------------------------------
ret = get('{0}/get/PM25'.format(api_url_prefix), data={"credential": credential}, verify='cert.pem').json()
value = json.loads(ret['data'])
print("Last value is retrieved: {0}".format(value))

# Response field
#  - status
#  - count: number of retrieved row
#  - data: json string of retrieved row

#-----------------------------------------------
# 3. Retrieve values over range: timestamp = [start_ts, end_ts]
#-----------------------------------------------
# timestamp format: "YYYYMMDDhhmmss"
start_ts = "20180511143400"
end_ts = "20180511143403"

ret = get('{0}/get_range/{1}/{2}/{3}'.format(api_url_prefix, DATA_NAME, start_ts, end_ts), data={"credential": credential}, verify='cert.pem').json()
values = json.loads(ret['data'])
print("{0} values are retrieved".format(len(values)))
for v in values:
    print("    {}".format(v))

# Response field
#  - status
#  - count: number of retrieved rows
#  - data: json string of retrieved rows

#-----------------------------------------------
# 4. Delete one value
#-----------------------------------------------
ret = post('{0}/delete/{1}/{2}'.format(api_url_prefix, DATA_NAME, new_id), data={"credential": credential}, verify='cert.pem').json()
print("{0} value is deleted".format(ret['count']))

# Response field
#  - status
#  - count: number of deleted row

#-----------------------------------------------
# 5. Delete all
#-----------------------------------------------
ret = post('{0}/delete_all/{1}'.format(api_url_prefix, DATA_NAME), data={"credential": credential}, verify='cert.pem').json()
print("{0} values are deleted".format(ret['count']))
ret = post('{0}/delete_all/{1}'.format(api_url_prefix, "NEAR_IR_LIGHT_INTENSITY"), data={"credential": credential}, verify='cert.pem').json()
print("{0} values are deleted".format(ret['count']))

# Response field
#  - status
#  - count: number of deleted rows
