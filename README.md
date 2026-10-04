# 💡 Smart Street Lighting Energy Optimization System

A Big Data-based smart street lighting system for monitoring and analyzing street-light energy consumption, traffic, motion, brightness, and faults using Python, Apache Kafka, Hadoop HDFS, Pandas, Plotly, and Streamlit.

## 📌 Project Overview

Traditional street lighting systems often operate using fixed schedules and do not consider real-time traffic, motion, lighting conditions, or equipment faults.

This project uses a Big Data architecture to collect, store, process, analyze, and visualize street-light data.

The system generates simulated street-light sensor data, streams the data using Apache Kafka, stores it using Hadoop HDFS, performs data analysis, and presents the results through an interactive Streamlit dashboard.

## 🎯 Objectives

- Monitor street-light energy consumption
- Analyze traffic and motion patterns
- Identify faulty street lights
- Analyze location-wise energy usage
- Study the relationship between traffic and power consumption
- Monitor brightness and lighting behaviour
- Provide an interactive visualization dashboard

## 🏗️ System Architecture

```text
Street Light Sensor Data
          │
          ▼
    Python Data Generator
          │
          ▼
       Apache Kafka
   street-light-data
          │
          ▼
      Hadoop HDFS
          │
          ▼
 Data Processing & Analysis
          │
          ▼
      Pandas / Python
          │
          ▼
   Streamlit + Plotly
       Dashboard
## 🛠️ Technologies Used

| Technology | Purpose |
|---|---|
| Python | Data generation, processing, and analysis |
| Apache Kafka | Real-time street-light data streaming |
| Hadoop HDFS | Distributed storage of street-light data |
| Pandas | Data cleaning and analysis |
| Plotly | Interactive data visualization |
| Streamlit | Interactive dashboard development |

## 📊 Dataset

The project uses a simulated street-light sensor dataset containing **100,000 records**.

### Dataset Attributes

- Timestamp
- Light ID
- Location
- Latitude
- Longitude
- LDR Value
- Motion Detected
- Traffic Level
- Brightness Level
- Voltage
- Current
- Power Consumption
- Temperature
- Light Status
- Fault Status

The dataset is generated using Python to simulate street-light sensor readings for different locations and operating conditions.

## 📈 Dashboard Features

The Streamlit dashboard provides an interactive view of the street-light system.

### 🔹 Energy Monitoring
- Total power consumption
- Average power consumption
- Location-wise energy analysis
- Power consumption trends

### 🔹 Traffic Analysis
- Traffic-level distribution
- Traffic vs power consumption
- Analysis of Low, Medium, and High traffic conditions

### 🔹 Smart Lighting Analysis
- Motion detection analysis
- Motion vs power consumption
- Brightness-level analysis
- Light status monitoring

### 🔹 System Health
- Faulty street-light monitoring
- Fault status analysis
- Active light monitoring
- Location-wise status analysis

### 🔹 Interactive Features
- Location filters
- Traffic filters
- Light status filters
- Fault status filters
- Recent records view
- CSV data download

## 📁 Project Structure

```text
smart-street-lighting/
│
├── analysis/
│   ├── analytics.py
│   └── optimization.py
│
├── dashboard/
│   └── dashboard.py
│
├── data/
│   ├── street_light_data.csv
│   ├── energy_saving.csv
│   ├── motion_power.csv
│   ├── power_by_location.csv
│   └── status_by_location.csv
│
├── kafka/
│   └── producer.py
│
├── scripts/
│   └── generate_data.py
│
├── visualizations/
│   ├── current_vs_optimized_power.png
│   ├── fault_status.png
│   ├── light_status.png
│   ├── motion_power.png
│   ├── optimized_brightness_distribution.png
│   ├── power_by_location.png
│   └── traffic_vs_power.png
│
├── README.md
└── requirements.txt
````

## 🔄 Project Workflow

```text
Generate Street-Light Data
          ↓
     Apache Kafka
          ↓
      Hadoop HDFS
          ↓
   Data Processing
          ↓
     Data Analysis
          ↓
 Streamlit + Plotly
          ↓
 Interactive Dashboard
```

## 🚀 Live Dashboard

🔗 https://smart-street-lighting-gcbmqvtrasqmajhrowgdfm.streamlit.app/


## ▶️ Run the Dashboard

Install the required dependencies:

```bash
pip install -r requirements.txt
```

Run the Streamlit dashboard:

```bash
streamlit run dashboard/dashboard.py
```

## 📌 Key Outcomes

The system provides a centralized platform for monitoring and analyzing street-light operations.

It helps identify:

* Energy consumption patterns
* Traffic and motion patterns
* Location-wise power usage
* Lighting behaviour
* Fault conditions
* Street-light operating status

## 🔮 Future Enhancements

* Integration with real IoT sensors
* Real-time Kafka-based dashboard updates
* Automated fault alerts
* Predictive maintenance
* Machine learning-based energy optimization
* Cloud deployment

 
