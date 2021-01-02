
import pandas as pd
import configparser
import helper.transform as tf
import numpy as np
import matplotlib.pyplot as plt
import logging
from os import sys


def main_arg_parse():
    import argparse
    parser = argparse.ArgumentParser(description='Noctornal flight calling')
    parser.add_argument('--config_file_path', type=str, help='Provide the path for config file')
    return parser


logging.basicConfig(level=logging.INFO, filename='app.log', format='%(levelname)s - %(asctime)s - %(message)s')
logger = logging.getLogger()

def main(args_lst):
    # Configuration

    parser = main_arg_parse()
    args = parser.parse_args(args_lst)
    # "config/config.ini"
    config_file = args.config_file_path
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
    logger.info("Read the JSON file")
    
    # Clean data 
    chicago_collision_df = tf.clean_chicago_collision(chicago_collision_df)
    flight_call_df = tf.clean_flight_call(flight_call_df)
    light_levels_df = tf.clean_light_level(light_levels_df)
    logger.info("Clean the data")
    
    # Transforn data 
    chicago_collision_flight = pd.merge(chicago_collision_df, flight_call_df, 
                                        how='left', on=['Genus','Species'])
    chicago_collision_flight_light = pd.merge(chicago_collision_flight,
                                              light_levels_df,  how='left', on=['Date'])
    chicago_collision_flight_light["Flight_Call"] = chicago_collision_flight_light["Flight_Call"].apply(lambda x: 1  if x == "yes" else 0)
    print(chicago_collision_flight_light)

    #plt.scatter(chicago_collision_flight_light["Light_Score"], chicago_collision_flight_light["Collisions"], c = chicago_collision_flight_light["Flight_Call"])

    #plt.show()

    d = chicago_collision_flight\
        .groupby(by=["Family","Genus","Species","Flight_Call","Season","Habitat","Stratum"])\
        .agg(collisions=('Species', 'count'), collisions_days =('Date','nunique') )\
        .sort_values(by= "collisions", ascending = False)
    d.reset_index(inplace = True)
    print(d)
    d["Flight_Call"] = d["Flight_Call"].apply(lambda x: 1  if x == "yes" else 0)
    plt.scatter(x = d["Stratum"], y = d["collisions"], c = d["Flight_Call"])

    plt.show()

    # [chicago_collision_flight_light["Locality"]=="MP"]
    e = chicago_collision_flight_light[chicago_collision_flight_light["Locality"]=="MP"]\
        .groupby(by = ["Light_Score","Flight_Call"]).agg(sum_collisions = ("Species","count"), num_species =('Species','nunique'))
    e.reset_index(inplace= True)


    e["collision_per_species"] =  e["sum_collisions"]/e["num_species"]
    e["log_collision_per_species"] = np.log(e["collision_per_species"])
    print(e)

    plt.scatter(x = e["Light_Score"], y = e["log_collision_per_species"], c = e["Flight_Call"])

    plt.show()

if __name__ == "__main__":
    print(sys.argv)
    main(sys.argv[1:])