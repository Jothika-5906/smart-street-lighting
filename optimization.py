import pandas as pd
import matplotlib.pyplot as plt

# Load the original dataset
DATASET = r"C:\SmartStreetLighting\dataset\street_light_data.csv"

df = pd.read_csv(DATASET)

print("============================================")
print("SMART STREET LIGHTING - ENERGY OPTIMIZATION")
print("============================================")

# Remove duplicate records
df = df.drop_duplicates()

# Convert required columns
df["power_consumption"] = pd.to_numeric(
    df["power_consumption"], errors="coerce"
)

df["brightness_level"] = pd.to_numeric(
    df["brightness_level"], errors="coerce"
)

df["motion_detected"] = pd.to_numeric(
    df["motion_detected"], errors="coerce"
)

# Remove invalid values
df = df.dropna(
    subset=[
        "power_consumption",
        "brightness_level",
        "motion_detected",
        "traffic_level"
    ]
)

# Keep only normal lights for optimization
normal_df = df[df["fault_status"] == "Normal"].copy()

# --------------------------------------------
# INTELLIGENT BRIGHTNESS RULES
# --------------------------------------------

def calculate_optimized_brightness(row):

    traffic = row["traffic_level"]
    motion = row["motion_detected"]

    if traffic == "High":
        return 100

    elif traffic == "Medium":
        return 70

    elif traffic == "Low" and motion == 1:
        return 50

    else:
        return 30


normal_df["optimized_brightness"] = normal_df.apply(
    calculate_optimized_brightness,
    axis=1
)

# --------------------------------------------
# ESTIMATE OPTIMIZED POWER
# --------------------------------------------

normal_df["optimized_power"] = (
    normal_df["power_consumption"]
    * normal_df["optimized_brightness"]
    / normal_df["brightness_level"].replace(0, 1)
)

# Avoid optimized power being greater than original
normal_df["optimized_power"] = normal_df[
    ["optimized_power", "power_consumption"]
].min(axis=1)

# --------------------------------------------
# ENERGY CALCULATION
# --------------------------------------------

current_power = normal_df["power_consumption"].sum()

optimized_power = normal_df["optimized_power"].sum()

energy_saved = current_power - optimized_power

saving_percentage = (
    energy_saved / current_power
) * 100

# --------------------------------------------
# RESULTS
# --------------------------------------------

print("\n========== OPTIMIZATION RESULTS ==========")

print(f"\nRecords analyzed: {len(normal_df):,}")

print(
    f"\nCurrent power consumption: "
    f"{current_power:,.3f} W"
)

print(
    f"Optimized power consumption: "
    f"{optimized_power:,.3f} W"
)

print(
    f"Estimated power saved: "
    f"{energy_saved:,.3f} W"
)

print(
    f"Estimated energy saving: "
    f"{saving_percentage:.2f}%"
)

print("\n--- OPTIMIZED BRIGHTNESS ---")

print(
    normal_df["optimized_brightness"]
    .value_counts()
    .sort_index()
)

# --------------------------------------------
# GRAPH 1: CURRENT VS OPTIMIZED POWER
# --------------------------------------------

plt.figure(figsize=(8, 5))

plt.bar(
    ["Current Power", "Optimized Power"],
    [current_power, optimized_power]
)

plt.ylabel("Power Consumption (W)")
plt.title("Current vs Optimized Power Consumption")

plt.tight_layout()

plt.savefig(
    r"C:\SmartStreetLighting\current_vs_optimized_power.png"
)

plt.show()

# --------------------------------------------
# GRAPH 2: OPTIMIZED BRIGHTNESS
# --------------------------------------------

brightness_counts = (
    normal_df["optimized_brightness"]
    .value_counts()
    .sort_index()
)

plt.figure(figsize=(8, 5))

plt.bar(
    brightness_counts.index.astype(str),
    brightness_counts.values
)

plt.xlabel("Optimized Brightness (%)")
plt.ylabel("Number of Records")
plt.title("Intelligent Brightness Distribution")

plt.tight_layout()

plt.savefig(
    r"C:\SmartStreetLighting\optimized_brightness_distribution.png"
)

plt.show()

# --------------------------------------------
# GRAPH 3: FAULT STATUS
# --------------------------------------------

fault_counts = df["fault_status"].value_counts()

plt.figure(figsize=(8, 5))

plt.bar(
    fault_counts.index,
    fault_counts.values
)

plt.xlabel("Fault Status")
plt.ylabel("Number of Records")
plt.title("Street Light Fault Analysis")

plt.tight_layout()

plt.savefig(
    r"C:\SmartStreetLighting\fault_status.png"
)

plt.show()

# --------------------------------------------
# GRAPH 4: LIGHT STATUS
# --------------------------------------------

status_counts = df["light_status"].value_counts()

plt.figure(figsize=(8, 5))

plt.bar(
    status_counts.index,
    status_counts.values
)

plt.xlabel("Light Status")
plt.ylabel("Number of Records")
plt.title("Street Light ON/OFF Analysis")

plt.tight_layout()

plt.savefig(
    r"C:\SmartStreetLighting\light_status.png"
)

plt.show()

print("\n============================================")
print("ENERGY OPTIMIZATION COMPLETED")
print("============================================")