from requests import post
import json

# Configurations
api_url_prefix = "<url>"
credential = "<code>"

# API url format
#  - http://147.47.220.28:5000/<command>/<sensor type>/<id>
#  - command: new, get, get_all, delete, delete_all
#  - sensor type: PM1, PM10, PM25, HUM

# Response field (common)
#  - status: if success, "OK". otherwise "ERROR"
#  - message: only for 'ERROR'. Error description

#-----------------------------------------------
# 1. Insert new value
#-----------------------------------------------
for i in range(5):
    new_data = """{"sensor_name":"PM25", "name":"pm2007", "timestamp": "18-05-11 14:34:56.382242", "latitude": 37.45, "longitude": 126.8, "value":12.7}"""
    ret = post('{0}/new/PM25'.format(api_url_prefix), data={"data": new_data, "credential": credential}).json()
    print(ret)
    new_id = ret['id']
    print("New value is inserted, ID: {0}".format(new_id))

# Response field
#  - status
#  - id: id of inserted row(value)

#-----------------------------------------------
# 2. Retrieve one value
#-----------------------------------------------
ret = post('{0}/get/PM25/{1}'.format(api_url_prefix, new_id), data={"credential": credential}).json()
value = json.loads(ret['data'])
print("ID {0} value is retrieved: {1}".format(new_id, value))

# Response field
#  - status
#  - count: number of retrieved row
#  - data: json string of retrieved row

#-----------------------------------------------
# 3. Retrieve all values
#-----------------------------------------------
ret = post('{0}/get_all/PM25'.format(api_url_prefix), data={"credential": credential}).json()
values = json.loads(ret['data'])
print("{0} values are retrieved".format(len(values)))

# Response field
#  - status
#  - count: number of retrieved rows
#  - data: json string of retrieved rows

#-----------------------------------------------
# 4. Delete one value
#-----------------------------------------------
ret = post('{0}/delete/PM25/{1}'.format(api_url_prefix, new_id), data={"credential": credential}).json()
print("{0} value is deleted".format(ret['count']))

# Response field
#  - status
#  - count: number of deleted row

#-----------------------------------------------
# 5. Delete all
#-----------------------------------------------
ret = post('{0}/delete_all/PM25'.format(api_url_prefix), data={"credential": credential}).json()
print("{0} values are deleted".format(ret['count']))

# Response field
#  - status
#  - count: number of deleted rows
