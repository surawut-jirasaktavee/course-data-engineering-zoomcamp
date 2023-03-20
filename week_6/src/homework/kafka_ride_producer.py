import csv
from json import dumps
from kafka import KafkaProducer
import argparse

parser = argparse.ArgumentParser(prog="TaxiRide")
parser.add_argument("-source_file", "-f")
args = parser.parse_args()

producer = KafkaProducer(
    bootstrap_servers=["localhost:9092"],
    key_serializer=lambda x: dumps(x).encode("utf-8"),
    value_serializer=lambda x: dumps(x).encode("utf-8"),
)

file = open(args.source_file)

csvReader = csv.reader(file)
header = next(csvReader)
for row in csvReader:
    if args.source_file == "../../datasets/fhv_tripdata_2019-01.csv":
        if row[3] == "":
            key = {"pu_location_id": int(999)}
            value = {"pu_location_id": int(999)}
        else:
            key = {"pu_location_id": int(float(row[3]))}
            value = {"pu_location_id": int(float(row[3]))}
    else:
        key = {"pu_location_id": int(row[0])}
        value = {"pu_location_id": int(row[0])}
    producer.send("rides_json", value=value, key=key)
    print("produce the massages...")
