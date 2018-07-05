import mysql.connector

class API():
    def __init__(self, host, port, database, user, passwd):
        self.cnx = mysql.connector.connect(user=user, password=passwd,
                                      host=host,
                                      database=database,
                                      port=port)
        self.cursor = self.cnx.cursor()

    def add_record(self, sensor, sensor_name, ts, latitude, longitude, data):
        self.cursor.execute("INSERT INTO {0} VALUES (%s, %s, %s, %s, %s)".format(sensor), 
                (sensor_name, ts, latitude, longitude, data))

    def get_records(self, sensor, count = 1000):
        self.cursor.execute("SELECT * FROM {0} order by ts desc".format(sensor))
        return self.cursor.fetchmany(size=count)
