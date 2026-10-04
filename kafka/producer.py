import csv
import json
import time
from kafka import KafkaProducer

CSV_FILE = r"C:\SmartStreetLighting\dataset\street_light_data.csv"
KAFKA_TOPIC = "street-light-data"
KAFKA_SERVER = "localhost:9092"

producer = KafkaProducer(
    bootstrap_servers=KAFKA_SERVER,
    value_serializer=lambda value: json.dumps(value).encode("utf-8")
)

print("Connected to Kafka.")
print("Sending CSV records...\n")

with open(CSV_FILE, mode="r", newline="", encoding="utf-8") as file:
    reader = csv.DictReader(file)

    for row in reader:
        producer.send(KAFKA_TOPIC, value=row)

        print(
            f"Sent: {row['timestamp']} | "
            f"{row['light_id']} | "
            f"{row['location']} | "
            f"Power: {row['power_consumption']} W"
        )

       # No delay - send records continuously

producer.flush()
producer.close()

print("\nAll CSV records sent successfully.")
