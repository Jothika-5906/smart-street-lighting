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
