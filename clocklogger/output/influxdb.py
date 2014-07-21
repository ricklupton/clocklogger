from __future__ import print_function
from datetime import datetime
from influxdb import client as influxdb


def datetime_to_epoch(d):
    return int((d - datetime(1970, 1, 1)).total_seconds())


class InfluxDBWriter(object):
    def __init__(self, columns):
        self.columns = columns
        self.db = influxdb.InfluxDBClient('localhost', 8086,
                                          'clocklogger', 'pendulum', 'clock')
        print("Opened connection to InfluxDB")

    def write(self, data):
        data = dict(data)
        data['time'] = datetime_to_epoch(data['time'])
        points = [
            {
                "name":    "clock",
                "columns": self.columns,
                "points":  [[data[k] for k in self.columns]],
            }
        ]
        self.db.write_points_with_precision(points, 's')