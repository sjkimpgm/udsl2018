from datetime import date

# import storage API
import udsl_storage

# load storage configuration
from udsl_storage_config import *

# Init API
api = udsl_storage.API(DBMS_HOST, DBMS_PORT, DBMS_DATABASE, DBMS_USER, DBMS_PASSWD)

# Insert new records
#   args: SENSOR, SENSOR_NAME, TIMESTAMP, LATITUDE, LONGITUDE, DATA
#   possible SENSOR: HUM, PM25, PM10, PM1
api.add_record("PM25", "pm2007", "18-05-11 14:34:56.382242", 37.450269, 126.9523002, 91)
api.add_record("PM25", "pm2007", "18-05-11 14:34:56.582242", 37.450269, 126.9523002, 91)
api.add_record("PM25", "pm2007", "18-05-11 14:34:56.782242", 37.450269, 126.9523002, 90)
api.add_record("PM25", "pm2007", "18-05-11 14:34:56.982242", 37.450269, 126.9523002, 90)
api.add_record("PM25", "sen0177", "18-05-11 14:34:56.914707", 37.450269, 126.9523002, 74)

# Get newest records. Use 'count' parameter to limit fetched records
print(api.get_records("PM25", count=5))
