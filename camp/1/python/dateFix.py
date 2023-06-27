from datetime import datetime

datetime_string = "2023-06-21T18:40:30.773Z"
datetime_format = "%Y-%m-%dT%H:%M:%S.%fZ"

datetime_obj = datetime.strptime(datetime_string, datetime_format)
absolute_time_ms = datetime_obj.timestamp() * 1000

print(int(absolute_time_ms))