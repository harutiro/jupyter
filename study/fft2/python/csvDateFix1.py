import csv
from datetime import datetime

input_file = "study/fft2/data/3回目/ans.csv"
output_file = "study/fft2/data/3回目/ans.csv"

datetime_format = "%Y-%m-%dT%H:%M:%S.%fZ"

with open(input_file, "r", newline="") as file:
    reader = csv.DictReader(file)
    rows = list(reader)

    for row in rows:
        datetime_str = row["time"]
        datetime_obj = datetime.strptime(datetime_str, datetime_format)
        absolute_time_ms = int(datetime_obj.timestamp() * 1000)
        row["time"] = absolute_time_ms

with open(output_file, "w", newline="") as file:
    fieldnames = reader.fieldnames
    writer = csv.DictWriter(file, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(rows)

print("変換が完了しました。")