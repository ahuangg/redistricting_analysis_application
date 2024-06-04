import os
import pickle
import multiprocessing
import mmap
import time
import numpy as np
import datetime
import matplotlib.pyplot as plt
import copy
from gerrychain import (GeographicPartition, Graph, updaters)
from OFFICIAL_OptimalTransport import *
from multiprocessing import Value, Lock
from sklearn.manifold import MDS
from sklearn.cluster import KMeans
from kneed import KneeLocator
from data_utils import *
from scipy.optimize import linear_sum_assignment
from scipy.sparse import csr_matrix
from gerrychain.partition.assignment import Assignment

# NOTE: Change vars here
STATE = "NC"
OFFSET_ID = 100000
ENSEMBLE_DIR = "Ensemble_250_Steps_10000"
# huge time sink, if already calculated, set to false.
RUN_GEOMETRIES_OVERRIDE = True
WORKING_DIR = os.path.dirname(os.path.abspath(__file__)) + \
    "/SeaWulf_Output/" + STATE + "/"

OPTIMAL_TRANSPORT_THRESHOLD = 251
# Threshold used to create somewhat interesting data, and still a reasonable percentage.
OPPORTUNITY_DISTRICT_THRESHOLD = 0.37
# Maximum points to sample for ensemble size vs number of clusters plot.
MAX_SAMPLE_POINTS = 20

# Distance measure names, set as constants to avoid typos.
OPTIMAL_TRANSPORT_STR = "Optimal Transport"
HAMMING_DISTANCE_STR = "Hamming Distance"
ENTROPY_DISTANCE_STR = "Entropy Distance"
# Other names
MDS_X_STR = "MDS_X"
MDS_Y_STR = "MDS_Y"
R_D_SPLIT_STR = "R/D Split"
R_D_SPLIT_RANGE_STR = R_D_SPLIT_STR + " Range"
graph = None
my_updaters = None
if __name__ == "__main__":
    # try to load unified_buffered.geojson
    print("Loading unified.geojson...")
    try:
        state_gdf = load_geojson_as_gdf(f"{WORKING_DIR}/unified_buffered.geojson")
        if state_gdf is None:
            raise Exception()
    except:
        print("Buffered unified.geojson not found. Creating...")
        state_gdf = load_geojson_as_gdf(f"{WORKING_DIR}/unified.geojson")
        state_gdf["geometry"] = state_gdf["geometry"].buffer(0)
        state_gdf["geometry"] = state_gdf["geometry"].buffer(0.0004)
        # write to unified_buffered.geojson
        state_gdf.to_file(f"{WORKING_DIR}/unified_buffered.geojson", driver="GeoJSON")
        print("Created unified_buffered.geojson")
    print("Loading Graph...")
    graph = Graph.from_json(f"{WORKING_DIR}/adjacency_data.json")
    # drop all columns except population
    my_updaters = { "population": updaters.Tally("Population", alias="population"),
                    "republican": updaters.Tally("R", alias="republican"),
                    "democrat": updaters.Tally("D", alias="democrat"),
                    "american_indian": updaters.Tally("American Indian and Alaska Native", alias="american_indian"),
                    "pacific_islander": updaters.Tally("Native Hawaiian and Other Pacific Islander", alias="pacific_islander"),
                    "asian": updaters.Tally("Asian", alias="asian"),
                    "black": updaters.Tally("Black or African American", alias="black"),
                    "white": updaters.Tally("White", alias="white"),
                    "other_race": updaters.Tally("Other Race", alias="other_race"),
                    "more_than_one_race": updaters.Tally("MORE THAN ONE RACE", alias="more_than_one_race"),
                    # "land_area": updaters.Tally("Land Area", alias="land_area"),
                    # "water_area": updaters.Tally("Water Area", alias="water_area"),
                    "hispanic": updaters.Tally("Hispanic", alias="hispanic"),
                    "not_hispanic": updaters.Tally("Not Hispanic", alias="not_hispanic"),
                }

print("Calculating stats...")
def make_opp_district_str(race):
    return f"Opportunity districts for {race}(>"+str(OPPORTUNITY_DISTRICT_THRESHOLD*100)+"%)"


def geo_partition_from_assignment(assignment):
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
        # "land_area": updaters.Tally("Land Area", alias="land_area"),
        # "water_area": updaters.Tally("Water Area", alias="water_area"),
        "hispanic": updaters.Tally("Hispanic", alias="hispanic"),
            "not_hispanic": updaters.Tally("Not Hispanic", alias="not_hispanic"),
        }
    return GeographicPartition(graph, assignment=assignment, updaters=my_updaters)


'''Distance measure calculation methods'''
def create_mmap_file(index, assignment, folder):
    # Serialize assignment
    data = json.dumps(assignment, cls=NumpyEncoder).encode('utf-8')

    # Create a memory-mapped file
    mmap_path = os.path.join(folder, f"assignment-{index}.mmap")
    with open(mmap_path, "wb") as f:
        f.write(b'\x00' * len(data))  # Preallocate file size

    with open(mmap_path, "r+b") as f:
        mmapped_file = mmap.mmap(f.fileno(), 0)
        mmapped_file.write(data)
        mmapped_file.flush()
    
    return mmap_path
def read_from_mmap_file(mmap_path):
    with open(mmap_path, "r+b") as f:
        mmapped_file = mmap.mmap(f.fileno(), 0)
        data = mmapped_file.read()
    
    return json.loads(data.decode('utf-8'))
def calc_optimal_transport_distance(outer_idx, inner_idx, outer_mmap_path, inner_mmap_path,shared_counter, lock):
    outer_assignment = read_from_mmap_file(outer_mmap_path)
    inner_assignment = read_from_mmap_file(inner_mmap_path)
    # convert all keys to ints
    outer_assignment = Assignment.from_dict({int(k): v for k, v in outer_assignment.items()})
    inner_assignment = Assignment.from_dict({int(k): v for k, v in inner_assignment.items()})
    outer_partition = geo_partition_from_assignment(outer_assignment)
    inner_partition = geo_partition_from_assignment(inner_assignment)
    distance = Pair(outer_partition, inner_partition,
                    indicator='population', pop_col="Population").distance
    with lock:
        shared_counter.value += 1
        current_value = shared_counter.value
        print(f"Process ID: {os.getpid()},Counter: {current_value} Time: {time.time()}")
    return outer_idx, inner_idx, distance


def get_district_correspondence(partition1, partition2,max_num_precinct,max_num_district):
    # Create cost matrix for hungarian algorithm
    if len(partition1) != len(partition2):
        print("ERROR: correspondence invalid")
    cost_matrix = np.zeros((max_num_district, max_num_district))

    for precinct in range(max_num_precinct+1):
        # See which district each partition assigns the precinct to.
        # NOTE: this means edge cost is not completely based on area, but
        # more closely based on population. This is significantly faster.
        # -1 due to districts being 1-indexed.
        first_partition_district = partition1[precinct]-1
        second_partition_district = partition2[precinct]-1
        cost_matrix[first_partition_district][second_partition_district] += 1
        cost_matrix[second_partition_district][first_partition_district] += 1
    row_ind, col_ind = linear_sum_assignment(cost_matrix, maximize=True)
    district_correspondence = {}
    for i in range(len(row_ind)):
        district_correspondence[row_ind[i]] = col_ind[i]
    return district_correspondence


def calc_hamming_distance(outer_idx, inner_idx, outer_mmap_path, inner_mmap_path,shared_counter, lock):
    outer_assignment = read_from_mmap_file(outer_mmap_path)
    inner_assignment = read_from_mmap_file(inner_mmap_path)
    # convert all keys to ints
    outer_assignment = {int(k): v for k, v in outer_assignment.items()}
    inner_assignment = {int(k): v for k, v in inner_assignment.items()}
    max_num_precinct = 0
    max_num_district = 0
    # see highest key in partition1 or partition2
    for k, v in outer_assignment.items():
        max_num_precinct = max(max_num_precinct, k)
        max_num_district = max(max_num_district, v)
    outer_to_corresponding_inner = get_district_correspondence(
        outer_assignment, inner_assignment,max_num_precinct,max_num_district)
    distance = 0
    for precinct in range(max_num_precinct+1):
        # -1 since districts are 1-indexed, and mapping is 0-indexed.
        outer_district = outer_assignment[precinct]-1
        inner_district = outer_to_corresponding_inner[outer_district]+1
        if inner_assignment[precinct] != inner_district:
            distance += 1
    with lock:
        shared_counter.value += 1
        current_value = shared_counter.value
        if current_value % 1000 == 0:
            print(f"Process ID: {os.getpid()},Counter: {current_value} Time: {time.time()}")
    return outer_idx, inner_idx, distance


def calc_entropy_distance(outer_idx, inner_idx, outer_mmap_path, inner_mmap_path,shared_counter, lock):
    def Ent_D_C(gdf, district_column, county_column, population_column):
        entropy = 0
        totalpop = gdf[population_column].sum()
        district_county_intersections = gdf.groupby(by=[district_column,county_column]).sum()
        county_populations = gdf.groupby(by=county_column).sum()[population_column]
        for i, row in district_county_intersections.iterrows():
            if row[population_column] > 0:
                entropy += 1/totalpop*row[population_column]*np.log2(
                    county_populations[row.name[1]]/row[population_column]
            )
        return entropy

    def Ent_D_D(gdf, district_column_1, district_column_2, population_column):
        return Ent_D_C(gdf, district_column_1, district_column_2, population_column)
    
    global graph, counter
    outer_assignment = read_from_mmap_file(outer_mmap_path)
    inner_assignment = read_from_mmap_file(inner_mmap_path)
    outer_assignment = {int(k): v for k, v in outer_assignment.items()}
    inner_assignment = {int(k): v for k, v in inner_assignment.items()}
    dp_1_dict = outer_assignment
    dp_2_dict = inner_assignment
    if graph is None:
        graph = Graph.from_json(f"{WORKING_DIR}/adjacency_data.json")
    pop_col = {i: graph.nodes[i]['Population'] for i in graph.nodes}
    
    series1 = pd.Series(dp_1_dict, name='dp_1')
    series2 = pd.Series(dp_2_dict, name='dp_2')
    series3 = pd.Series(pop_col, name='totpop')
    df = pd.concat([series1, series2, series3], axis=1)
    df = df.sort_index()
    distance = Ent_D_D(df,'dp_1','dp_2','totpop')
    with lock:
        shared_counter.value += 1
        current_value = shared_counter.value
        if current_value % 1000 == 0:
            print(f"Process ID: {os.getpid()},Counter: {current_value} Time: {time.time()}")
    return outer_idx, inner_idx, distance    


def calc_similarity(matrix1, matrix2):
    correlation_matrix = np.corrcoef(matrix1.flatten(), matrix2.flatten())
    correlation_coefficient = correlation_matrix[0, 1]
    # normalize result
    similarity = (correlation_coefficient + 1) / 2
    return similarity


def calc_dist_measure(measure, partitions, distance_function, ensemble_folder):
    num_partitions = len(partitions)
    distances = np.zeros((num_partitions, num_partitions))
    runtime = 0

    try:
        distances = np.load(f"{ensemble_folder}/{measure}_distances.npy")
        runtime = float(open(f"{ensemble_folder}/{measure}_time.txt", "r").read())
        print(f"Loaded {measure} from file")
    except:
        print(f"Started Calculating {measure}")

        inputs = []
        # reset counter
        # global counter
        # with counter.get_lock():
        #     counter.value = 0
        # delete tmp folder if it exists
        if os.path.exists(f"{ensemble_folder}/tmp"):
            for filename in os.listdir(f"{ensemble_folder}/tmp"):
                os.remove(f"{ensemble_folder}/tmp/{filename}")
            os.rmdir(f"{ensemble_folder}/tmp")
        os.makedirs(f"{ensemble_folder}/tmp")
        for i, partition in enumerate(partitions):
            mmap_path = create_mmap_file(i, partition.assignment.to_dict(), f"{ensemble_folder}/tmp")
            partitions[i].mmap_path = mmap_path
        with multiprocessing.Manager() as manager:
            counter = manager.Value('i', 0)
            lock = manager.Lock()
            for i in range(num_partitions):
                for j in range(i + 1, num_partitions):
                    inputs.append((i, j, partitions[i].mmap_path, partitions[j].mmap_path, counter, lock))
            print(f"Calculating {measure}...")
            ctime = time.time()
            num_inputs = len(inputs)
            print(f"Number of inputs: {num_inputs}")
            with multiprocessing.Pool(processes=multiprocessing.cpu_count()) as pool:
                results = pool.starmap(distance_function, inputs)

                for outer_idx, inner_idx, distance in results:
                    distances[outer_idx, inner_idx] = distance
                    distances[inner_idx, outer_idx] = distance

        runtime = time.time() - ctime
        distances = distances / np.max(distances)

    np.save(f"{ensemble_folder}/{measure}_distances.npy", distances)
    with open(f"{ensemble_folder}/{measure}_time.txt", "w") as f:
        f.write(str(runtime))

    return distances, runtime

def add_dist_measure_to_dist_results(measure, partitions, dist_measure_results, ensemble_folder, ideal_distances=None):
    MEASURE_NAME_TO_DIST_FUNC = {
        OPTIMAL_TRANSPORT_STR: calc_optimal_transport_distance,
        HAMMING_DISTANCE_STR: calc_hamming_distance,
        ENTROPY_DISTANCE_STR: calc_entropy_distance,
    }
    dist_func = MEASURE_NAME_TO_DIST_FUNC[measure]
    distances, runtime = calc_dist_measure(
        measure, partitions, dist_func, ensemble_folder)

    quantiles = np.quantile(distances, [0.0, 0.25, 0.5, 0.75, 1.0])
    optimality = 1.0
    if ideal_distances is not None:
        optimality = calc_similarity(distances, ideal_distances)

    dist_measure_results[measure] = {
        "min": quantiles[0],
        "Q1": quantiles[1],
        "median": quantiles[2],
        "Q3": quantiles[3],
        "max": quantiles[4],
        "average": np.mean(distances),
        "optimality": optimality,
        "timeToRun": runtime
    }
    return distances


def add_distances_to_ensemble_summary(partitions, ensemble_summary, ensemble_directory):
    num_partitions = len(partitions)
    ideal_dist_matrix = None
    dist_measure_results = ensemble_summary["distanceMeasureResults"]

    SHOULD_RUN_OPTIMAL_TRANSPORT = num_partitions <= OPTIMAL_TRANSPORT_THRESHOLD
    if SHOULD_RUN_OPTIMAL_TRANSPORT:
        optimal_dist_matrix = add_dist_measure_to_dist_results(
            OPTIMAL_TRANSPORT_STR, partitions, dist_measure_results, ensemble_directory)
        ideal_dist_matrix = optimal_dist_matrix

    hamming_dist_matrix = add_dist_measure_to_dist_results(
        HAMMING_DISTANCE_STR, partitions, dist_measure_results, ensemble_directory, ideal_dist_matrix)

    if SHOULD_RUN_OPTIMAL_TRANSPORT:
        average_distance_between_pairs = dist_measure_results[OPTIMAL_TRANSPORT_STR]["average"]
    else:
        ideal_dist_matrix = hamming_dist_matrix
        average_distance_between_pairs = dist_measure_results[HAMMING_DISTANCE_STR]["average"]
    entropy_dist_matrix = add_dist_measure_to_dist_results(
        ENTROPY_DISTANCE_STR, partitions, dist_measure_results, ensemble_directory, ideal_dist_matrix)
    dist_measure_results["averageDistanceBetweenPlans"] = average_distance_between_pairs
    return ideal_dist_matrix


'''Statistics Calculation and Aggregation Methods'''


def get_district_plan_measures(current_district_plan):
    opportunity_district_count = {}
    global OPPORTUNITY_DISTRICT_RACES
    for race in OPPORTUNITY_DISTRICT_RACES:
        opportunity_district_count[race] = 0
    opportunity_district_count["hispanic"] = 0
    R_wins = 0
    D_wins = 0
    for district in current_district_plan.parts:
        republican_votes = current_district_plan["republican"][district]
        democrat_votes = current_district_plan["democrat"][district]
        if republican_votes > democrat_votes:
            R_wins += 1
        elif (democrat_votes == republican_votes) and (np.random.rand() < 0.5):
            R_wins += 1

        district_pop = current_district_plan["population"][district]
        hispanic_pop = current_district_plan["hispanic"][district]
        not_hispanic_pop = current_district_plan["not_hispanic"][district]
        # print(f"Hispanic pop: {hispanic_pop}, not hispanic pop: {not_hispanic_pop}, ExpPop: {district_pop-hispanic_pop-not_hispanic_pop}")
        # treat like special case.
        if hispanic_pop / (hispanic_pop + not_hispanic_pop) >= OPPORTUNITY_DISTRICT_THRESHOLD:
            opportunity_district_count["hispanic"] += 1
        required_opportunity_district_pop = OPPORTUNITY_DISTRICT_THRESHOLD * district_pop
        for key in opportunity_district_count:
            if current_district_plan[key][district] > required_opportunity_district_pop:
                opportunity_district_count[key] += 1
    # check if hispanic is an opportunity district
    if OPPORTUNITY_DISTRICT_RACES[-1] != "hispanic":
        OPPORTUNITY_DISTRICT_RACES.append("hispanic")
    
    D_wins = len(current_district_plan.parts) - R_wins
    measureData = {}
    for key in opportunity_district_count:
        measureData[make_opp_district_str(
            key)] = opportunity_district_count[key]
    measureData[R_D_SPLIT_STR] = f"{R_wins}R | {D_wins}D"
    measureData[R_D_SPLIT_RANGE_STR] = f"{R_wins}R | {D_wins}D" + " - " + f"{R_wins}R | {D_wins}D"
    measureData["R"] = R_wins
    measureData["D"] = D_wins
    return measureData


def process_per_partition_info(ensemble_name, ensemble_folder, offset_id=0):
    partitions = []
    partition_summaries = []
    plan_id = 0
    # see how many files end in .pkl or .pkl.json
    num_files = len([name for name in os.listdir(ensemble_folder)
                     if name.endswith(".pkl") or name.endswith(".pkl.json")])
    filecnt = 0
    PRECOMPUTED_PARTITION_SUMMARIES = False
    # check if you can load from partition_summaries.json
    try:
        partition_summaries = load_json_as_dict(
            ensemble_folder, "district_plans")
        print("Loaded partition summaries from file")
        PRECOMPUTED_PARTITION_SUMMARIES = True
    except:
        print("Calculating partition summaries...")
    for filename in os.listdir(ensemble_folder):
        '''ASSIGNMENT: PICKLE FORMAT'''
        if not filename.endswith(".pkl") and not filename.endswith(".pkl.json"):
            continue
        print(f"Processing {filename} ({filecnt}/{num_files})...")
        if filename.endswith(".pkl"):
            file_path = os.path.join(ensemble_folder, filename)
            with open(file_path, "rb") as f:
                cur_assignment = pickle.load(f)
        elif filename.endswith(".pkl.json"):
            file_path = os.path.join(ensemble_folder, filename)
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
        
        if not PRECOMPUTED_PARTITION_SUMMARIES:
            partition_summaries.append(
                {
                    "id": offset_id+plan_id,
                    "name": f"{ensemble_name}-{plan_id}",
                    "availability": False,
                    "measureData": get_district_plan_measures(current_district_plan),
                })
        partitions.append(current_district_plan)
        plan_id += 1
        filecnt += 1
    # save partition summaries to file
    write_dict_as_json(ensemble_folder, f"district_plans",
                       partition_summaries)
    return partitions, partition_summaries


def aggregate_median_r_d_split(partition_summaries, key):
    r_district_counts = []
    total_districts = partition_summaries[0]["measureData"]["R"] + \
        partition_summaries[0]["measureData"]["D"]
    for partition_summary in partition_summaries:
        r_district_counts.append(partition_summary["measureData"]["R"])
    median_r = np.median(r_district_counts)
    # convert to int if possible
    if median_r == int(median_r):
        median_r = int(median_r)
    median_d = total_districts - median_r
    return f"{median_r}R | {median_d}D"
def aggregate_range_r_d_split(partition_summaries, key):
    r_district_counts = []
    total_districts = partition_summaries[0]["measureData"]["R"] + \
        partition_summaries[0]["measureData"]["D"]
    for partition_summary in partition_summaries:
        r_district_counts.append(partition_summary["measureData"]["R"])
    min_r = np.min(r_district_counts)
    max_r = np.max(r_district_counts)
    low_str = f"{min_r}R | {total_districts-min_r}D"
    high_str = f"{max_r}R | {total_districts-max_r}D"
    return f"{low_str} - {high_str}"

def aggregate_median_generic(partition_summaries, key):
    counts = []
    for partition_summary in partition_summaries:
        counts.append(partition_summary["measureData"][key])
    median = np.median(counts)
    return median


def aggregate_mean_generic(partition_summaries, key):
    counts = []
    for partition_summary in partition_summaries:
        counts.append(partition_summary["measureData"][key])
    mean = np.mean(counts)
    return mean


'''Clustering methods'''


def find_optimal_k(data, max_k=20, show_plots = False):
    distortions = np.zeros(max_k-1)

    K = range(1, max_k)
    for k in K:
        if k > len(data):
            break
        kmeans = KMeans(n_clusters=k, tol=0.00005,max_iter=6000,n_init='auto')
        kmeans.fit(data)
        distortions[k-1] = kmeans.inertia_

    # NOTE: kneed can output None if the elbow point is not found(due to low amount of data).
    kneedle = KneeLocator(K, distortions, S=1.0,
                          curve="convex", direction="decreasing")
    elbow_point = kneedle.knee
    if show_plots:
        # also draw vertical line at elbow point
        if elbow_point is None:
            plt.plot(K, distortions, 'bx-')
            plt.xlabel('k')
            plt.ylabel('Distortion')
            plt.title('The Elbow Method showing the optimal k')
            plt.show()
        else:
            kneedle.plot_knee()
            plt.show()


    return elbow_point

def create_ensemble_vs_cluster_size(ensemble_summary, num_partitions, points):
    SAMPLE_POINTS = min(MAX_SAMPLE_POINTS, num_partitions//2)
    for i in range(1, SAMPLE_POINTS+1):
        ensemble_size = int(num_partitions*(i/SAMPLE_POINTS))
        elbow_point = find_optimal_k(points[:ensemble_size])
        if elbow_point == None:
            print("Warning: elbow point not found. Setting to 1.")
            elbow_point = 1
        ensemble_summary["ensembleClusterSizeAssociation"].append(
            {"Number of clusters":elbow_point, "Ensemble size":ensemble_size})


def calculate_cluster_info(cluster_to_plan_index, partition_summaries, ensemble_name, offset_id, distance_matrix):
    global AGGREGATION_OPERATION
    cluster_summaries = []
    num_clusters = len(cluster_to_plan_index)
    typeical_plan_idx = []
    for i in range(num_clusters):
        cluster_measure_data = {}
        cluster_name = ensemble_name+"-Cluster-"+str(i)
        cluster_id = i+offset_id
        partition_ids_in_cluster = cluster_to_plan_index[i]
        offsetted_partition_ids = []
        cluster_partition_summaries = []
        cluster_size = len(partition_ids_in_cluster)
        for partition_id in partition_ids_in_cluster:
            cluster_partition_summaries.append(partition_summaries[partition_id])
            offsetted_partition_ids.append(partition_summaries[partition_id]["id"])
        for key in AGGREGATION_OPERATION:
            cluster_measure_data[AGGREGATION_OPERATION[key]["name"]] = AGGREGATION_OPERATION[key]["method"](
                cluster_partition_summaries, key)
        typical_plan_id = calc_cluster_typical_plan(partition_ids_in_cluster,distance_matrix)    
        typical_plan_id = partition_summaries[typical_plan_id]["id"]
        # calculate average distance between plans in cluster
        cluster_dist_matrix = []
        # Prune dist matrix to only distances in cluster
        for id in partition_ids_in_cluster:
            pruned_list = []
            for i,dist in enumerate(distance_matrix[id]):
                if i in partition_ids_in_cluster:
                    pruned_list.append(dist)
            cluster_dist_matrix.append(pruned_list)
        avg_distance = np.mean(cluster_dist_matrix)
        cluster_summaries.append({
            "clusterId": cluster_id,
            "clusterName": cluster_name,
            "numberOfPlans": cluster_size,
            "districtPlanIds": offsetted_partition_ids,
            "measureData": cluster_measure_data,
            "averageDistanceBetweenPlans": avg_distance,
            "typicalPlan": typical_plan_id            
        })
        typeical_plan_idx.append(typical_plan_id)
    return cluster_summaries, typeical_plan_idx

def calc_cluster_typical_plan(partition_ids_in_cluster,distance_matrix):
    cluster_dist_matrix = []
    # Prune dist matrix to only distances in cluster
    for id in partition_ids_in_cluster:
        pruned_list = []
        for i,dist in enumerate(distance_matrix[id]):
            if i in partition_ids_in_cluster:
                pruned_list.append(dist)
        cluster_dist_matrix.append(pruned_list)
    # For each row, sum of squares distance
    min_idx = -1
    min_sum = 10000000000000000
    for i,row in enumerate(cluster_dist_matrix):
        cur_sum = sum(row)
        if cur_sum < min_sum:
            min_idx = i
            min_sum = cur_sum
    return partition_ids_in_cluster[min_idx]


def process_available_geometries(partitions, partition_summaries, n_clusters, cluster_to_plan_index, offset_id,typ_plan_idx):
    geojson_outputs = []
    MAX_NUM_AVAILABLE_PLANS = 30
    print(f"Number of clusters: {n_clusters}. Processing available geometries...")
    current_geojson_id = offset_id
    for i in range(n_clusters):
        # Try to make sure that each cluster has at least 1 plan available.
        num_available_in_cluster = MAX_NUM_AVAILABLE_PLANS//n_clusters
        num_available_in_cluster += (i <
                                     (MAX_NUM_AVAILABLE_PLANS % n_clusters))
        num_available_in_cluster = min(
            num_available_in_cluster, len(cluster_to_plan_index[i]))
        # take the plan with the lowest R count and the highest R count
        # also take the plan with the highest hispanic opportunity district count
        # also take the plan with the highest black opportunity district count
        high_r_idx = -1
        high_r = -1
        low_r_idx = -1
        low_r = 10000
        high_hispanic_idx = -1
        high_hispanic = -1
        high_black_idx = -1
        high_black = -1
        rep_idx = typ_plan_idx[i]
        for j in range(len(cluster_to_plan_index[i])):
            plan_index = cluster_to_plan_index[i][j]
            plan = partition_summaries[plan_index]
            r_count = plan["measureData"]["R"]
            if plan["id"] == rep_idx:
                rep_idx = plan_index
            hispanic_count = plan["measureData"][make_opp_district_str("hispanic")]
            black_count = plan["measureData"][make_opp_district_str("black")]
            if r_count > high_r:
                high_r = r_count
                high_r_idx = plan_index
            if r_count < low_r:
                low_r = r_count
                low_r_idx = plan_index
            if hispanic_count > high_hispanic:
                high_hispanic = hispanic_count
                high_hispanic_idx = plan_index
            if black_count > high_black:
                high_black = black_count
                high_black_idx = plan_index
        # append the plans to the geojson_outputs
        # create set of indices to avoid duplicates
        indices = set()
        indices.add(high_r_idx)
        indices.add(low_r_idx)
        indices.add(high_hispanic_idx)
        indices.add(high_black_idx)
        indices.add(rep_idx)
        for plan_index in indices:
            district_assignment = partitions[plan_index].assignment
            # district assignment:
            # [(index in unified.json, district_id),...]
            state_gdf["DISTRICT"] = state_gdf.index.map(
                district_assignment)
            dissolved = state_gdf.dissolve(by="DISTRICT")
            # simplify geometry
            dissolved["geometry"] = dissolved["geometry"].simplify(
                0.00001, preserve_topology=True)
            # drop all columns except geometry
            dissolved = dissolved[["geometry"]]
            geojson_outputs.append({
                "id": current_geojson_id,
                "data": dissolved.__geo_interface__
            })
            partition_summaries[plan_index]["availability"] = True
            partition_summaries[plan_index]["boundaryId"] = current_geojson_id
            current_geojson_id += 1

    return geojson_outputs


def process_ensemble(ensemble_name, offset_id=0, show_plots=False):
    ensemble_directory = f"{WORKING_DIR}/{ensemble_name}/"
    partitions, partition_summaries = process_per_partition_info(
        ensemble_name, ensemble_directory, offset_id)

    num_partitions = len(partitions)
    # get timestamp of oldest file in directory
    oldest_file_timestamp = time.time()
    for filename in os.listdir(ensemble_directory):
        if not filename.endswith(".pkl") and not filename.endswith(".pkl.json"):
            continue
        file_timestamp = os.path.getmtime(
            f"{ensemble_directory}/{filename}")
        if file_timestamp < oldest_file_timestamp:
            oldest_file_timestamp = file_timestamp
    # convert timestamp to date, with hours, minutes, seconds
    timestamp_date = datetime.datetime.fromtimestamp(
        oldest_file_timestamp).strftime("%m/%d/%Y, %H:%M:%S")
    ensemble_summary = {
        "id": offset_id,
        "ensembleName": STATE+ensemble_name,
        "numberOfPlans": num_partitions,
        "clusterIds": [],
        "dateCreated": timestamp_date,
        "distanceMeasureResults": {
            "averageDistanceBetweenPlans": 0,
        },
        "ensembleClusterSizeAssociation": [],
    }
    print("Runing distance measures...")
    # Populates averageDistanceBetweenPlans and distanceMeasureResults
    distance_matrix = add_distances_to_ensemble_summary(
        partitions, ensemble_summary, ensemble_directory)
    if show_plots:
        print("Distance measure calculation done. Distance Matrix:")
        # create a figure and a subplot
        fig, ax = plt.subplots()
        # create heatmap
        im = ax.imshow(distance_matrix)
        # create colorbar with label
        cbar = ax.figure.colorbar(im, ax=ax)
        cbar.ax.set_ylabel("Distance", rotation=-90, va="bottom")
        # set title
        ax.set_title("Distance Matrix")
        # show all ticks and label them with the respective list entries.
        # limit to 20 ticks, otherwise it gets too crowded
        num_ticks = min(20, num_partitions)
        # create list of ticks
        ticks = np.linspace(0, num_partitions-1, num_ticks, dtype=int)
        # set ticks
        ax.set_xticks(ticks)
        ax.set_yticks(ticks)
        # set tick labels
        ax.set_xticklabels(ticks)
        ax.set_yticklabels(ticks)

        plt.show()
        
    print("Runninng MDS...")
    # check if mds_coords.npy exists
    if os.path.exists(f"{ensemble_directory}/mds_coords.npy"):
        print ("Loading MDS coords from file...")
        mds_coords = np.load(f"{ensemble_directory}/mds_coords.npy")
    else:
        mds = MDS(n_components=2, random_state=0, dissimilarity='precomputed')
        print("Doing MDS calculation...")
        mds_coords = mds.fit(distance_matrix).embedding_
        print("Done MDS calculation")
        # save the mds coords into a file
        np.save(f"{ensemble_directory}/mds_coords.npy", mds_coords)
    for i, partition_summary in enumerate(partition_summaries):
        partition_summary["measureData"][MDS_X_STR] = mds_coords[i, 0]
        partition_summary["measureData"][MDS_Y_STR] = mds_coords[i, 1]
    if show_plots:
        plt.title("MDS")
        plt.scatter(mds_coords[:, 0], mds_coords[:, 1])
        plt.show()

    # Populates ensembleClusterSizeAssociation
    create_ensemble_vs_cluster_size(
        ensemble_summary, num_partitions, mds_coords)

    elbow_point = find_optimal_k(mds_coords,max_k=20, show_plots=show_plots)
    kmeans_res = KMeans(n_clusters=elbow_point, tol=0.00005,max_iter=6000,n_init='auto').fit(mds_coords)
    best_mapping = kmeans_res.labels_
    centers = kmeans_res.cluster_centers_
    if show_plots:
        plt.title("K-Means Clustering")
        plt.scatter(mds_coords[:, 0], mds_coords[:, 1], c=best_mapping)
        # add the cluster centers
        plt.scatter(centers[:, 0], centers[:, 1], c='red', s=200, alpha=0.5)
        plt.show()

    # Create mapping from cluster id to list of plan indices
    cluster_to_plan_index = {}
    for i in range(elbow_point):
        cluster_to_plan_index[i] = []
    for i in range(num_partitions):
        cluster_to_plan_index[best_mapping[i]].append(i)

    # Aggregate measures for each cluster
    cluster_summaries, typical_plans = calculate_cluster_info(
        cluster_to_plan_index, partition_summaries, ensemble_name, offset_id, distance_matrix)
    for summary in cluster_summaries:
        ensemble_summary["clusterIds"].append(summary["clusterId"])
    if not os.path.exists(f"{ensemble_directory}/geometries") or RUN_GEOMETRIES_OVERRIDE == True:
        geojson_outputs = process_available_geometries(
            partitions, partition_summaries, elbow_point, cluster_to_plan_index, offset_id,typical_plans)
        # iterate over key: value pairs in geojson_outputs
        # make geomtries directory if it doesn't exist
        if not os.path.exists(f"{ensemble_directory}/geometries"):
            os.makedirs(f"{ensemble_directory}/geometries")
        else:
            # clear directory if it exists
            for filename in os.listdir(f"{ensemble_directory}/geometries"):
                os.remove(f"{ensemble_directory}/geometries/{filename}")
        for gdf in geojson_outputs:
            # write each value to a file named key.json
            with open(f"{ensemble_directory}/geometries/{gdf['id']}.json", "w") as f:
                json.dump(gdf, f, cls=NumpyEncoder)
    else:
        print("Geometry files already exist. Skipping geometry generation.")
    write_dict_as_json(ensemble_directory,
                       "ensemble_summary", ensemble_summary)
    write_dict_as_json(ensemble_directory, "clusters", cluster_summaries)
    write_dict_as_json(ensemble_directory, "district_plans",
                       partition_summaries)


# NOTE: More races can be added, but often results in zero opp. districts.
OPPORTUNITY_DISTRICT_RACES = ["black"]
'''
Defines how to aggregate measures when clustering
and the name of the measure in the cluster summary.
'''
AGGREGATION_OPERATION = {
    R_D_SPLIT_STR: {
        "method": aggregate_median_r_d_split,
        "name": "Median " + R_D_SPLIT_STR
    },
    R_D_SPLIT_RANGE_STR: {
        "method": aggregate_range_r_d_split,
        "name": R_D_SPLIT_RANGE_STR
    },
    MDS_X_STR: {
        "method": aggregate_mean_generic,
        "name": MDS_X_STR
    },
    MDS_Y_STR: {
        "method": aggregate_mean_generic,
        "name": MDS_Y_STR
    },
}
for race in OPPORTUNITY_DISTRICT_RACES:
    AGGREGATION_OPERATION[make_opp_district_str(race)] = {
        "method": aggregate_mean_generic,
        "name": f"{make_opp_district_str(race)}(avg)"
    }
AGGREGATION_OPERATION[make_opp_district_str("hispanic")] = {
    "method": aggregate_mean_generic,
    "name": f"{make_opp_district_str('hispanic')}(avg)"
}

def show_geoms():
    # go through geometries folder
    geom_folder = f"{WORKING_DIR}/{ENSEMBLE_DIR}/geometries"
    # for each file, load json
    for filename in os.listdir(geom_folder):
        if not filename.endswith(".json"):
            continue
        with open(f"{geom_folder}/{filename}", "r") as f:
            gdf = json.load(f)
            gdf = gdf["data"]
            # convert to geodataframe
            gdf = gpd.GeoDataFrame.from_features(gdf)
        # plot geometry
        draw_geojson(gdf)
        plt.show()

if __name__ == "__main__":
    if not os.path.exists(WORKING_DIR):
        os.makedirs(WORKING_DIR)
    '''
    NOTE: Manually change offset id when running different ensembles in order to ensure unique ids for every district plan.
    Offsets should be greater than 100_000 apart from each other.
    '''
    process_ensemble(ENSEMBLE_DIR, offset_id=OFFSET_ID, show_plots=True)
    # show_geoms()
    # TODO: add process_ensemble calls for other ensembles and combine the output files into one large file.
