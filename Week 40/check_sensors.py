# Student: Christian Bjørklund Seeberg
# Week 40 assignment

# Task 2

# Importing libraries
import yaml
import json
import pandas as pd

# Reading the configuration
with open("data/config.yml", "r") as f:
    config = yaml.safe_load(f)


max_days = config["max_days_since_calibration"]
output_file = config["output_file"]

# Reading the data
sensors_df = pd.read_excel("data/sensors.xlsx")        
calib_df = pd.read_csv("data/calibrations.csv")       


# Merging the dataframes on sensor_id
merged = sensors_df.merge(calib_df, on="sensor_id", how="left")


# Filtering the sensors
overdue = merged[merged["days_since_calibration"] > max_days]


# Getting ready to export the data
records = overdue[["sensor_id", "lab_room", "owner", "days_since_calibration"]].to_dict(orient="records")


with open(output_file, "w") as f:
    json.dump(records, f, indent=2)

