from rtree import index
from shapely.geometry import shape
from matplotlib import pyplot as plt
from data_utils import *
import pandas as pd
import numpy as np
import networkx as nx
import time
import json
import maup
import os

# state: string
# Precincts should be stored in:                    ../data/{state}/Precincts_{state}.geojson
# 2022 Congressional Districts should be stored in: ../data/{state}/Districts_{state}.geojson
# Voting data(by vtd) should be stored in:          ../data/{state}/Voting_{state}.csv
# Census data(by vtd) should be stored in:          ../data/{state}/Census/Voting_Age_Demographics.csv
# VTD geojson should be stored in:                  ../data/{state}/VTDs_{state}.geojson
state = "NC"
DATA_DIR = os.path.dirname(os.path.abspath(__file__)) + "/../data"


def join_geojsons(main, other):
    other = try_cast_columns_to_numeric(other)
    main = try_cast_columns_to_numeric(main)
    other_to_main = {}
    idx = index.Index()
    for i, main_geom in enumerate(main['geometry']):
        idx.insert(i, main_geom.bounds)
    for i, other_geom in enumerate(other['geometry']):
        other_to_main[i] = []
        other_area = other_geom.area
        for main_id in idx.intersection(other_geom.bounds):
            main_geom = main['geometry'][main_id]
            intersection = other_geom.intersection(main_geom)
            overlap = intersection.area / other_area
            other_to_main[i].append((main_id, overlap))

    # Add columns that are in other but not in main, sum based on linear interpolation of overlaps.
    columns_to_add = other.select_dtypes(
        include='number').columns.difference(main.columns)
    main = main.reindex(columns=main.columns.union(
        columns_to_add), fill_value=0)
    updates_df = pd.DataFrame(
        index=main.index, columns=columns_to_add).fillna(0)
    for i, other_shape in other.iterrows():
        for main_id, overlap in other_to_main[i]:
            updates_df.loc[main_id] += (other_shape[columns_to_add]
                                        * overlap).astype(int)
    main[updates_df.columns] += updates_df.astype(int)
    return main


def calculate_r_d_split():
    voting = load_geojson_as_gdf(f'{DATA_DIR}/{state}/Voting_{state}.geojson')
    voting['D'] = 0
    voting['R'] = 0
    for column in voting.columns:
        if column == 'D' or column == 'R':
            continue
        if column[:4] == "GCON":
            party = column[-4]
            if party == 'D':
                voting['D'] += voting[column]
            elif party == 'R':
                voting['R'] += voting[column]
        # Other than R,D and geometry, delete all columns.
        if column != "geometry":
            del voting[column]
    return voting


def calculate_demographics():
    demographics = load_csv_as_df(
        f'{DATA_DIR}/{state}/Census/Voting_Age_Demographics.csv')
    # Remove first row describing columns.
    demographics = demographics.iloc[1:]
    unwanted_columns = ["STATEFP20", "COUNTYFP20", "GEOID20",
                        "VTDI20", "NAME20", "LSAD20", "NAMELSAD20", "NAME",
                        "P3_002N"]
    remove_unwanted_columns(demographics, unwanted_columns)
    try_cast_columns_to_numeric(demographics)

    # create new column to aggregate remaining columns dealing with >1 race.
    demographics["More than 1 Race"] = 0
    for column in demographics.columns:
        if column[:4] == "P3_0":
            if column[-1] == 'N' and (int(column[3:6])) > 8:
                demographics["More than 1 Race"] += demographics[column]
                del demographics[column]
    demographics_remap = {
        "P3_001N": "Population",
        "P3_003N": "White",
        "P3_004N": "Black or African American",
        "P3_005N": "American Indian and Alaska Native",
        "P3_006N": "Asian",
        "P3_007N": "Native Hawaiian and Other Pacific Islander",
        "P3_008N": "Other Race",
    }
    demographics.rename(columns=demographics_remap, inplace=True)
    return demographics


def get_vtd_gdf():
    vtds = load_geojson_as_gdf(f'{DATA_DIR}/{state}/VTDs_{state}.geojson')
    unwanted_columns = ["STATEFP20", "COUNTYFP20", "GEOID20",
                        "VTDI20", "NAME20", "LSAD20", "NAMELSAD20", "NAME"]
    remove_unwanted_columns(vtds, unwanted_columns)
    vtds_remap = {
        "AFFGEOID20": "GEO_ID",
        "ALAND20": "Land Area (m^2)",
        "AWATER20": "Water Area (m^2)",
    }
    vtds.rename(columns=vtds_remap, inplace=True)
    return vtds


def get_precincts_gdf():
    precincts = load_geojson_as_gdf(
        f'{DATA_DIR}/{state}/Precincts_{state}.geojson')
    unwanted_columns = ["prec_id", "enr_desc",
                        "county_nam", "of_prec_id", "county_id"]
    remove_unwanted_columns(precincts, unwanted_columns)
    precincts.rename(columns={"id": "PRECINCT"}, inplace=True)
    return precincts


def load_merged_census_data(from_scratch=False):
    if not from_scratch and os.path.isfile(f'{DATA_DIR}/{state}/unified.geojson'):
        print("Found unified file, skipping preprocessing")
        unified = load_geojson_as_gdf(f'{DATA_DIR}/{state}/unified.geojson')
        return unified
    demographics_df = calculate_demographics()
    # TODO: Get age data, join with demographics.
    vtds_gdf = get_vtd_gdf()
    if set(vtds_gdf['GEO_ID']) != set(demographics_df['GEO_ID']):
        print("VTDS and demographics GEO_IDs do not match.")
        return None
    vtds_and_demographics_gdf = vtds_gdf.merge(demographics_df, on="GEO_ID")
    # TODO: Get block group income data from ACS. Join with vtds.
    r_d_splits_gdf = calculate_r_d_split()
    precincts_gdf = get_precincts_gdf()
    unified = join_geojsons(precincts_gdf, r_d_splits_gdf)
    unified = join_geojsons(unified, vtds_and_demographics_gdf)
    unified.to_file(f'{DATA_DIR}/{state}/unified.geojson', driver='GeoJSON')
    return unified


def map_district_to_precincts(precincts, districts, get_plot_data=False):
    # NOTE: This assignment from mggg maup is purely based on indices
    # of the precincts and districts.
    # Anything related to precinct ids or district ids is ignored.
    # maup also requires that the precincts and districts to be in a
    # projected coordinate system. (In this case, Mercator)
    precincts_copy = precincts.copy().to_crs("EPSG:3857")
    districts_copy = districts.copy().to_crs("EPSG:3857")
    precinct_to_district_assignment = maup.assign(
        precincts_copy, districts_copy)
    district_to_precincts = {}
    precinct_colors = {}
    district_colors = {}
    for _, district in districts.iterrows():
        district_id = district['DISTRICT']
        district_colors[district_id] = np.random.rand(3,)
        district_to_precincts[district_id] = []
    for precinct_index, _ in precincts.iterrows():
        district_index = precinct_to_district_assignment[precinct_index]
        district_id = districts.loc[district_index]['DISTRICT']
        district_to_precincts[district_id].append(precinct_index)
        precinct_colors[precinct_index] = district_colors[district_id]
    if get_plot_data:
        return district_to_precincts, precinct_colors, district_colors
    else:
        return district_to_precincts


def create_precinct_graph(precincts, get_suspect_precincts=False, debug=False):
    """
    Creates a graph of precincts, with edges between precincts that are neighbors.

    Parameters:
    precincts (GeoDataFrame): The precincts.
    get_suspect_precincts (bool): Whether or not to return a map of suspect precincts.
    debug (bool): Whether or not to plot debug data.

    Returns:
    G (Graph): The graph.
    precinct_colors (dict): A map from precinct id to a color.
    suspect_precincts (dict): A map from precinct id to whether or not it is suspect.
    """

    # Create spatial index for fast lookup.
    idx = index.Index()
    for i, precinct in precincts.iterrows():
        idx.insert(i, shape(precinct['geometry']).bounds)

    # Thresholds
    GAP_THRESHOLD = 0.0003
    POINT_INTERSECTION_AREA = 3.141592653589793 * GAP_THRESHOLD**2
    POINT_THRESHOLD = POINT_INTERSECTION_AREA*1.1

    # map of all suspect precincts
    suspect_precincts = {}
    precinct_to_district = {}
    precinct_colors = {}
    district_colors = {}

    G = nx.Graph()
    # Do an initial pass to find neighbors whose bounding boxes intersect.
    neighbors = {}
    for i, precinct in precincts.iterrows():
        precinct_neighbors = list(idx.intersection(
            shape(precinct['geometry']).bounds))
        precinct_neighbors.remove(i)
        neighbors[i] = precinct_neighbors

    # Do a second pass to find neighbors whose geometries intersect.
    for i, precinct in precincts.iterrows():
        centroid = precinct['geometry'].centroid
        if not precinct['geometry'].contains(centroid):
            centroid = precinct['geometry'].representative_point()
        precinct_colors[i] = np.random.rand(3,)
        G.add_node(i, pos=(centroid.x, centroid.y))
        # add info about this precinct to the graph
        for column in precincts.columns:
            if column != "geometry":
                G.nodes[i][column] = precinct[column]

    # Add edges.
    for i, precinct_neighbor_list in neighbors.items():
        current_precinct = precincts.loc[i, 'geometry']
        current_precinct_buffered = current_precinct.buffer(GAP_THRESHOLD)
        for neighbor in precinct_neighbor_list:
            neighbor_precinct = precincts.loc[neighbor, 'geometry']
            shared_borderline_length = 0
            # check if the two precincts their borders are gapped by less than a threshold
            if i < neighbor and current_precinct_buffered.intersects(neighbor_precinct):
                intersection_strict = current_precinct.intersection(
                    neighbor_precinct)
                intersection_buffered = current_precinct_buffered.intersection(
                    neighbor_precinct)
                # see if they only intersect at a point
                if intersection_strict.geom_type == 'Point':
                    continue
                # if they don't intersect at all, it could just be a line gap, or a gap shaped like a dot.
                if intersection_strict.is_empty:
                    if intersection_buffered.geom_type == 'LineString':
                        if intersection_buffered.length < POINT_THRESHOLD:
                            if debug:
                                print("sus:", i, "and",
                                      neighbor, "no intersect")
                            suspect_precincts[i] = True
                            suspect_precincts[neighbor] = True
                            continue
                        # take medial axis of intersection polygon to estimate shared border length
                        shared_borderline_length = intersection_buffered.length
                    elif intersection_buffered.geom_type == 'Polygon':
                        if intersection_buffered.area - POINT_INTERSECTION_AREA < POINT_THRESHOLD:
                            if debug:
                                print("sus:", i, "and",
                                      neighbor, "no intersect")
                                plt.fill(*intersection_buffered.exterior.xy,
                                         color='red', alpha=0.5)
                            suspect_precincts[i] = True
                            suspect_precincts[neighbor] = True
                            continue
                        else:
                            shared_borderline_length = intersection_buffered.minimum_rotated_rectangle.length
                            if debug:
                                # implies overlap considered, and good!
                                plt.fill(*intersection_buffered.exterior.xy,
                                         color='blue', alpha=0.5)
                    else:
                        if debug:
                            print("sus:", i, "and", neighbor, "no intersect")
                        suspect_precincts[i] = True
                        suspect_precincts[neighbor] = True
                        continue
                elif intersection_strict.geom_type == 'Polygon':
                    # possible intersection might just be a dot/rounding error
                    if intersection_buffered.area - POINT_INTERSECTION_AREA < POINT_THRESHOLD:
                        if debug:
                            print("sus:", i, "and", neighbor, "no intersect")
                            plt.fill(*intersection_buffered.exterior.xy,
                                     color='red', alpha=0.5)
                        suspect_precincts[i] = True
                        suspect_precincts[neighbor] = True
                        continue
                    shared_borderline_length = intersection_strict.minimum_rotated_rectangle.length
                else:
                    shared_borderline_length = intersection_strict.length
                G.add_edge(i, neighbor)
                G[i][neighbor]['shared_perim'] = shared_borderline_length

    if get_suspect_precincts:
        return G, precinct_colors, suspect_precincts
    return G, suspect_precincts


if __name__ == '__main__':
    SHOW_PLOTS = True
    RUN_FROM_SCRATCH = True
    start = time.time()
    # Group all data sources for precincts into one unified geojson file.
    unified_geojson = load_merged_census_data(from_scratch=RUN_FROM_SCRATCH)
    districts = load_geojson_as_gdf(
        f'{DATA_DIR}/{state}/Districts_{state}.geojson')
    districts = try_cast_columns_to_numeric(districts)
    mapping, precinct_colors, district_colors = map_district_to_precincts(
        unified_geojson, districts, get_plot_data=SHOW_PLOTS)
    if SHOW_PLOTS:
        plt.title("Mapping between precincts and districts")
        unified_geojson['color'] = unified_geojson.index.map(precinct_colors)
        draw_geojson(unified_geojson, color=None, alpha=0.5)
        districts['color'] = districts['DISTRICT'].map(district_colors)
        draw_geojson(districts, color=None, alpha=0.5)
        plt.show()
        del unified_geojson['color']
        del districts['color']

    precinct_series = pd.Series(
        {precinct: district for district, precincts in mapping.items() for precinct in precincts})
    unified_geojson['DISTRICT'] = unified_geojson.index.map(precinct_series)
    graph_results = create_precinct_graph(
        unified_geojson, get_suspect_precincts=False, debug=True)
    # plot_data(Graph, unified_geojson, graph_results[1], None)
    Graph = graph_results[0]
    adjacency_data = nx.adjacency_data(Graph)
    with open(f'{DATA_DIR}/{state}/adjacency_data.json', 'w') as f:
        json.dump(adjacency_data, f)
