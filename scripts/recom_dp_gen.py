from gerrychain import (GeographicPartition, Partition, Graph, MarkovChain,
                        proposals, updaters, constraints, accept, Election)
from gerrychain.proposals import recom
from functools import partial
from gerrychain import MarkovChain
import pickle
import os
import random
from multiprocessing import Process
from datetime import datetime

# Magic numbers and values.
# TODO: Move these to a config file.
PROGRAM_FOLDER = os.path.dirname(os.path.realpath(__file__))
OUTPUT_FOLDER = f"{PROGRAM_FOLDER}/Seawulf_Output"
INPUT_FOLDER = f"{PROGRAM_FOLDER}/Seawulf_Input"
ENSEMBLE_SIZES = [5]
POPULATION_CONSTRAINT_PERCENTAGE = 0.12
COMPACTNESS_BOUND_FACTOR = 2
DEFAULT_NUMBER_OF_STEPS = 100


def generate_default_proposal(graph):
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
                #    "land_area": updaters.Tally("Land Area", alias="land_area", dtype=float),
                #    "water_area": updaters.Tally("Water Area", alias="water_area", dtype=float),
                   "hispanic": updaters.Tally("Hispanic", alias="hispanic"),
                   "not_hispanic": updaters.Tally("Not Hispanic", alias="not_hispanic"),
                   }
    initial_partition = GeographicPartition(
        graph, assignment="DISTRICT", updaters=my_updaters)
    ideal_population = sum(
        initial_partition["population"].values()) / len(initial_partition)
    proposal = partial(recom,
                       pop_col="Population",
                       pop_target=ideal_population,
                       epsilon=0.02,
                       node_repeats=2
                       )
    return proposal, initial_partition


def generate_district_plans(graph, number_of_plans, total_steps, output_folder):
    # For each process, set seed to ensure different partitions are generated.
    process_id = os.getpid()
    random.seed(process_id + datetime.now().microsecond)

    proposal, initial_partition = generate_default_proposal(graph)
    compactness_bound = constraints.UpperBound(
        lambda p: len(p["cut_edges"]),
        COMPACTNESS_BOUND_FACTOR*len(initial_partition["cut_edges"])
    )
    pop_constraint = constraints.within_percent_of_ideal_population(
        initial_partition, POPULATION_CONSTRAINT_PERCENTAGE)
    while True:
        markov_chain = MarkovChain(
            proposal=proposal,
            constraints=[
                pop_constraint,
                compactness_bound
            ],
            accept=accept.always_accept,
            initial_state=initial_partition,
            total_steps=total_steps 
        ).with_progress_bar()
        for partition in markov_chain:
            pass
        generated_dp = partition

        plans_generated = 1 + len([name for name in os.listdir(output_folder)
                                  if name.endswith(".pkl")])
        if plans_generated > number_of_plans:
            break

        # NOTE: There might be a race condition
        # if two processes read the same value of plans_generated.
        print(
            f"[{process_id}]Generated partition: {plans_generated} / {number_of_plans}")
        filename = f"{output_folder}/pid{process_id}assignment{plans_generated}.pkl"
        with open(filename, "wb") as file:
            # Save assignment, the whole partition object cannot be pickled.
            pickle.dump(generated_dp.assignment, file)


def generate_ensemble(graph, number_of_plans, total_steps, output_folder):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    plans_generated = len([name for name in os.listdir(
        output_folder) if name.endswith(".pkl")])
    if plans_generated >= number_of_plans:
        print(
            f"Already generated enough plans for ensemble size {number_of_plans}.")
        return
    NUM_CORES = min(os.cpu_count(), number_of_plans)
    processes = []
    for _ in range(NUM_CORES):
        p = Process(target=generate_district_plans, args=(
            graph, number_of_plans, total_steps, output_folder))
        processes.append(p)
        p.start()
    for process in processes:
        process.join()

    for i, filename in enumerate(os.listdir(output_folder)):
        # Remove extra plans possibly caused by race condition.
        if i >= number_of_plans:
            os.remove(f"{output_folder}/{filename}")

    print("Finished generating ensemble in folder: ", output_folder)


def generate_state_ensembles(state, ensemble_sizes, total_steps=DEFAULT_NUMBER_OF_STEPS):
    if not os.path.exists(f"{INPUT_FOLDER}/{state}/adjacency_data.json"):
        print(
            f"Error: {INPUT_FOLDER}/{state}/adjacency_data.json does not exist. Please generate the input files first.")
        return
    input_graph = Graph.from_json(
        f"{INPUT_FOLDER}/{state}/adjacency_data.json")

    if not os.path.exists(f"{OUTPUT_FOLDER}/{state}"):
        os.makedirs(f"{OUTPUT_FOLDER}/{state}")

    for ensemble_size in ensemble_sizes:
        generate_ensemble(input_graph, ensemble_size, total_steps,
                          f"{OUTPUT_FOLDER}/{state}/Ensemble_{ensemble_size}_Steps_{total_steps}")

    print(f"Finished generating ensembles for {state}.")


if __name__ == "__main__":
    # generate_state_ensembles("NC", ENSEMBLE_SIZES)
    # generate_state_ensembles("PA", ENSEMBLE_SIZES)
    generate_state_ensembles("NC", ENSEMBLE_SIZES)