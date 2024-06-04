import gerrychain
import pickle
import os
from gerrychain import (GeographicPartition, Graph, updaters)
from gerrychain.partition.assignment import Assignment
import json

STATE = "PA"
ENSEMBLE_NAME = "RECOVERED_Ensemble_5_Steps_10"

WORKING_DIR = os.path.dirname(os.path.abspath(__file__)) + \
    "/adj/" + STATE + "/"
ENSEMBLE_DIR = f"{os.path.dirname(os.path.abspath(__file__))}/{ENSEMBLE_NAME}/"

graph = Graph.from_json(f"{WORKING_DIR}/adjacency_data.json")
my_updaters = {"population": updaters.Tally("Population", alias="population"),
               "republican": updaters.Tally("R", alias="republican"),
               "democrat": updaters.Tally("D", alias="democrat"),
               "american_indian": updaters.Tally("American Indian and Alaska Native", alias="american_indian"),
               "pacific_islander": updaters.Tally("Native Hawaiian and Other Pacific Islander", alias="pacific_islander"),
               "asian": updaters.Tally("Asian", alias="asian"),
               "black": updaters.Tally("Black or African American", alias="black"),
               "white": updaters.Tally("White", alias="white"),
               "other_race": updaters.Tally("Other Race", alias="other_race"),
               "more_than_one_race": updaters.Tally("MORE THAN ONE RACE", alias="more_than_one_race"),
            #    "land_area": updaters.Tally("Land Area", alias="land_area"),
            #    "water_area": updaters.Tally("Water Area", alias="water_area"),
               "hispanic": updaters.Tally("Hispanic", alias="hispanic"),
                "not_hispanic": updaters.Tally("Not Hispanic", alias="not_hispanic"),
               }

RECOVERY_FOLDER = f"{os.path.dirname(os.path.abspath(__file__))}/RECOVERED_{ENSEMBLE_NAME}"
if not os.path.exists(RECOVERY_FOLDER):
    os.makedirs(RECOVERY_FOLDER)


for filename in os.listdir(ENSEMBLE_DIR):
    file_path = os.path.join(ENSEMBLE_DIR, filename)
    with open(file_path, "rb") as f:
        dp_dict = json.load(f)
    dp_dict_intkeys = {}
    for key, value in dp_dict.items():
        try:
            dp_dict_intkeys[int(key)] = value
        except ValueError:
            print(f"Key '{key}' cannot be converted to an integer.")

    cur_assignment = Assignment.from_dict(dp_dict_intkeys)
    current_district_plan = GeographicPartition(
        graph, assignment=cur_assignment, updaters=my_updaters)