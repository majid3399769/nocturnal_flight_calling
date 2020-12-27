
import pandas as pd 
import configparser
import os

# Configuration
config_file = "config/config.ini"
cp = configparser.ConfigParser()
cp.read(config_file)

# Environment 
env = cp["Env"]["env"]
input_path = cp["Input"]["path"]
chicago_collision = input_path + cp["Input"]["chicago_collision"]
flight_call = input_path + cp["Input"]["flight_call"]
light_levels = input_path + cp["Input"]["light_levels"]

# Read data as JSON file 
chicago_collision_df = pd.read_json(chicago_collision)
flight_call_df = pd.read_json(flight_call)
light_levels_df = pd.read_json(light_levels)

print(chicago_collision_df.head())
print(flight_call_df.head())
print(light_levels_df.head())


# Clean Data 
