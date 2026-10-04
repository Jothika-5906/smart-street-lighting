import csv
import random
from datetime import datetime, timedelta

import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

OUTPUT_FILE = os.path.join(
    BASE_DIR,
    "dataset",
    "street_light_data.csv"
)

os.makedirs(
    os.path.dirname(OUTPUT_FILE),
    exist_ok=True
)

NUMBER_OF_RECORDS = 100000

locations = [
    ("Chennai_Central", 13.0827, 80.2707),
    ("T_Nagar", 13.0418, 80.2341),
    ("Anna_Nagar", 13.0850, 80.2101),
    ("Adyar", 13.0012, 80.2565),
    ("Velachery", 12.9815, 80.2180),
    ("Tambaram", 12.9249, 80.1000),
    ("Guindy", 13.0067, 80.2206),
    ("OMR", 12.9165, 80.2300)
]

start_time = datetime(2026, 8, 1, 0, 0, 0)

with open(OUTPUT_FILE, "w", newline="") as file:

    writer = csv.writer(file)

    writer.writerow([
        "timestamp",
        "light_id",
        "location",
        "latitude",
        "longitude",
        "ldr_value",
        "motion_detected",
        "traffic_level",
        "brightness_level",
        "voltage",
        "current",
        "power_consumption",
        "temperature",
        "light_status",
        "fault_status"
    ])

    for i in range(NUMBER_OF_RECORDS):

        timestamp = start_time + timedelta(seconds=i)

        light_number = random.randint(1, 10000)

        location = random.choice(locations)

        hour = timestamp.hour

        # Daytime
        if 6 <= hour < 18:

            ldr_value = random.randint(500, 900)
            motion = 0
            brightness = 0
            light_status = "OFF"

        # Night
        else:

            ldr_value = random.randint(50, 250)

            motion = random.choice([0, 1])

            if motion == 1:
                brightness = 100
            else:
                brightness = 30

            light_status = "ON"

        traffic = random.choice([
            "Low",
            "Medium",
            "High"
        ])

        voltage = round(
            random.uniform(11.8, 12.2),
            2
        )

        current = round(
            (brightness / 100) *
            random.uniform(0.7, 0.9),
            3
        )

        power = round(
            voltage * current,
            3
        )

        temperature = round(
            random.uniform(25, 38),
            1
        )

        # Small probability of a fault
        if random.random() < 0.002:
            fault_status = "Fault"
        else:
            fault_status = "Normal"

        writer.writerow([
            timestamp,
            f"SL_{light_number:05d}",
            location[0],
            location[1],
            location[2],
            ldr_value,
            motion,
            traffic,
            brightness,
            voltage,
            current,
            power,
            temperature,
            light_status,
            fault_status
        ])

        if (i + 1) % 10000 == 0:
            print(
                f"Generated {i + 1:,} records..."
            )

print()
print("Dataset generation completed!")
print(f"File created: {OUTPUT_FILE}")