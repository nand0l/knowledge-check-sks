import datetime

# Get the current Unix timestamp
unix_timestamp = int(datetime.datetime.now().timestamp())

readable_datetime = datetime.datetime.fromtimestamp(unix_timestamp)
print(unix_timestamp)
print(readable_datetime)
