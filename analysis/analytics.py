from kafka import KafkaConsumer
import json
import pandas as pd
import matplotlib.pyplot as plt

TOPIC = "street-light-data"
BOOTSTRAP_SERVER = "localhost:9092"

consumer = KafkaConsumer(
    TOPIC,
    bootstrap_servers=BOOTSTRAP_SERVER,
    auto_offset_reset="earliest",
    enable_auto_commit=False,
    consumer_timeout_ms=5000
)

records = []

print("Reading data from Kafka...")

for message in consumer:
    try:
        # Decode Kafka message
        data = json.loads(message.value.decode("utf-8"))

        # Accept only dictionary records
        if isinstance(data, dict):
            records.append(data)

    except (json.JSONDecodeError, UnicodeDecodeError):
        # Ignore old test messages / non-JSON messages
        continue

consumer.close()

print(f"\nValid JSON records received: {len(records)}")

if len(records) == 0:
    print("No valid street-light JSON records found.")
    exit()

# Convert to DataFrame
df = pd.DataFrame(records)

# Remove duplicate records
before = len(df)
df = df.drop_duplicates()
after = len(df)

print(f"Duplicate records removed: {before - after}")
print(f"Records after cleaning: {after}")

# Convert numeric columns
numeric_columns = [
    "ldr_value",
    "motion_detected",
    "brightness_level",
    "voltage",
    "current",
    "power_consumption",
    "temperature"
]

for column in numeric_columns:
    df[column] = pd.to_numeric(df[column], errors="coerce")

# -----------------------------
# BASIC ANALYSIS
# -----------------------------

print("\n========== STREET LIGHT ANALYSIS ==========")

print("\n--- DATASET SIZE ---")
print(f"Total records: {len(df)}")

print("\n--- AVERAGE POWER CONSUMPTION ---")
print(f"{df['power_consumption'].mean():.3f} W")

print("\n--- TOTAL POWER CONSUMPTION ---")
print(f"{df['power_consumption'].sum():.3f} W")

print("\n--- POWER CONSUMPTION BY LOCATION ---")
location_power = (
    df.groupby("location")["power_consumption"]
    .mean()
    .sort_values(ascending=False)
)

print(location_power)

print("\n--- LIGHT STATUS ---")
print(df["light_status"].value_counts())

print("\n--- TRAFFIC LEVEL ---")
print(df["traffic_level"].value_counts())

print("\n--- FAULT STATUS ---")
print(df["fault_status"].value_counts())

print("\n--- AVERAGE POWER BY TRAFFIC LEVEL ---")
traffic_power = df.groupby("traffic_level")["power_consumption"].mean()

print(traffic_power)

print("\n--- AVERAGE BRIGHTNESS BY TRAFFIC LEVEL ---")
traffic_brightness = df.groupby("traffic_level")["brightness_level"].mean()

print(traffic_brightness)

# -----------------------------
# GRAPH 1
# -----------------------------

location_power.plot(kind="bar")

plt.title("Average Power Consumption by Location")
plt.xlabel("Location")
plt.ylabel("Power Consumption (W)")
plt.xticks(rotation=45)
plt.tight_layout()

plt.savefig(
    r"C:\SmartStreetLighting\power_by_location.png"
)

plt.show()

# -----------------------------
# GRAPH 2
# -----------------------------

traffic_power.plot(kind="bar")

plt.title("Average Power Consumption by Traffic Level")
plt.xlabel("Traffic Level")
plt.ylabel("Power Consumption (W)")
plt.xticks(rotation=0)
plt.tight_layout()

plt.savefig(
    r"C:\SmartStreetLighting\traffic_vs_power.png"
)

plt.show()

print("\n============================================")
print("Analytics completed successfully!")
print("============================================")
