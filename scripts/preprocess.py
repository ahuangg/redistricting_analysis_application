from rtree import index
from shapely.geometry import shape
from data_utils import *
import pandas as pd
from gerrychain import Graph
import networkx as nx
import json
import maup
import os

'''
state: string

Precincts should be stored in:                    ../data/{state}/Precincts_{state}.geojson
2022 Congressional Districts should be stored in: ../data/{state}/Districts_{state}.geojson
Voting data(by vtd) should be stored in:          ../data/{state}/Voting_{state}.csv
Census data(by vtd) should be stored in:          ../data/{state}/Census/Voting_Age_Demographics.csv
VTD geojson should be stored in:                  ../data/{state}/VTDs_{state}.geojson
'''
DATA_DIR = os.path.dirname(os.path.abspath(__file__)) + "/../data"
RUN_FROM_SCRATCH = True
states = ["NC"]
cur_state = None


def join_gdfs(main, other):
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
    voting = load_geojson_as_gdf(
        f'{DATA_DIR}/{cur_state}/Voting_{cur_state}.geojson')
    D_column = pd.Series(np.zeros(len(voting)), index=voting.index)
    R_column = pd.Series(np.zeros(len(voting)), index=voting.index)
    for column in voting.columns:
        if column[:4] == "GCON":
            party = column[-4]
            if party == 'D':
                D_column += voting[column]
            elif party == 'R':
                R_column += voting[column]
    # Keep only geometry and add votes.
    voting = voting[['geometry']]
    voting['D'] = D_column
    voting['R'] = R_column
    return voting


def calculate_income():
    income = load_csv_as_df(
        f'{DATA_DIR}/{cur_state}/Income_Tracts_{cur_state}.csv')
    # Remove first row describing columns.
    income = income.iloc[1:]
    # remove the first 9 characters of the GEOID column
    income['GEOID'] = income['GEOID'].str[9:]
    unwanted_columns = ["NAME", "LSAD", "C24010_001E", "C24010_001M"]
    remove_unwanted_columns(income, unwanted_columns)

def get_hispanic():
    hispanic = load_csv_as_df(
        f'{DATA_DIR}/{cur_state}/Census/Hispanic.csv')
    # Remove first row describing columns.
    hispanic = hispanic.iloc[1:]
    # Keep only "P4_002N","P4_003N", and "GEO_ID"
    hispanic = hispanic[["GEO_ID","P4_002N","P4_003N"]]
    # rename columns
    hispanic.rename(columns={"P4_002N": "Hispanic", "P4_003N": "Not Hispanic"}, inplace=True)
    return hispanic

def calculate_demographics():
    demographics = load_csv_as_df(
        f'{DATA_DIR}/{cur_state}/Census/Voting_Age_Demographics.csv')
    # Remove first row describing columns.
    demographics = demographics.iloc[1:]
    unwanted_columns = ["STATEFP20", "COUNTYFP20", "GEOID20",
                        "VTDI20", "NAME20", "LSAD20", "NAMELSAD20", "NAME",
                        "P3_002N"]
    remove_unwanted_columns(demographics, unwanted_columns)
    try_cast_columns_to_numeric(demographics)
    demographics_remap = {
        "P3_001N": "Population",
        "P3_003N": "White",
        "P3_004N": "Black or African American",
        "P3_005N": "American Indian and Alaska Native",
        "P3_006N": "Asian",
        "P3_007N": "Native Hawaiian and Other Pacific Islander",
        "P3_008N": "Other Race",
    }
    demographics["More than 1 Race"] = 0
    for column in demographics.columns:
        if column[:4] == "P3_0":
            # Ignores annotation columns like P3_002NA
            # Ignores populations that are not > 1 race.
            if column[-1] == 'N' and (int(column[3:6])) > 8:
                demographics["More than 1 Race"] += demographics[column]
                del demographics[column]
    demographics.rename(columns=demographics_remap, inplace=True)
    # calculate hispanic
    hispanic = get_hispanic()
    demographics = demographics.merge(hispanic, on="GEO_ID")
    return demographics


def load_and_clean_vtd_gdf():
    vtds = load_geojson_as_gdf(
        f'{DATA_DIR}/{cur_state}/VTDs_{cur_state}.geojson')
    unwanted_columns = ["STATEFP20", "COUNTYFP20", "GEOID20",
                        "VTDI20", "NAME20", "LSAD20", "NAMELSAD20", "NAME","ALAND20","AWATER20"]
    vtds_remap = {
        "AFFGEOID20": "GEO_ID",
        # "ALAND20": "Land Area (m^2)",
        # "AWATER20": "Water Area (m^2)",
    }
    # check if AFFGEOID20 column exists
    if "AFFGEOID20" not in vtds.columns:
        # If not, just prepend "7000000US" to the GEOID20 column data
        vtds["AFFGEOID20"] = "7000000US" + vtds["GEOID20"]
    remove_unwanted_columns(vtds, unwanted_columns)
    vtds.rename(columns=vtds_remap, inplace=True)
    return vtds


def load_and_clean_precincts_gdf():
    precincts = load_geojson_as_gdf(
        f'{DATA_DIR}/{cur_state}/Precincts_{cur_state}.geojson')
    if precincts is None:
        return None
    unwanted_columns = ["prec_id", "enr_desc",
                        "county_nam", "of_prec_id", "county_id"]
    remove_unwanted_columns(precincts, unwanted_columns)
    precincts.rename(columns={"id": "PRECINCT"}, inplace=True)
    return precincts


def load_merged_precinct_data(from_scratch=False):
    if not from_scratch and os.path.isfile(f'{DATA_DIR}/{cur_state}/unified.geojson'):
        print("Found unified file, skipping preprocessing")
        unified = load_geojson_as_gdf(
            f'{DATA_DIR}/{cur_state}/unified.geojson')
        return unified
    demographics_df = calculate_demographics()
    vtds_gdf = load_and_clean_vtd_gdf()
    if set(vtds_gdf['GEO_ID']) != set(demographics_df['GEO_ID']):
        print("VTDS and demographics GEO_IDs do not match.")
        return None
    vtds_and_demographics_gdf = vtds_gdf.merge(demographics_df, on="GEO_ID")
    r_d_splits_gdf = calculate_r_d_split()
    precincts_gdf = load_and_clean_precincts_gdf()
    if precincts_gdf is None:
        unified = r_d_splits_gdf
    else:
        unified = join_gdfs(precincts_gdf, r_d_splits_gdf)
    unified = join_gdfs(unified, vtds_and_demographics_gdf)
    unified.to_file(
        f'{DATA_DIR}/{cur_state}/unified.geojson', driver='GeoJSON')
    return unified


def map_district_to_precincts(precincts, districts):
    '''
    NOTE: This assignment from mggg maup is purely based on indices
    of the precincts and districts.
    Anything related to precinct ids or district ids is ignored.
    maup also requires that the precincts and districts to be in a
    projected coordinate system. (In this case, Mercator)
    '''
    precincts_copy = precincts.copy().to_crs("EPSG:3857")
    districts_copy = districts.copy().to_crs("EPSG:3857")
    precinct_to_district_assignment = maup.assign(
        precincts_copy, districts_copy)
    district_to_precincts = {}
    # see if 'DISTRICT' column exists
    district_column_name = 'DISTRICT'
    if district_column_name not in districts.columns:
        # use 'District' instead
        district_column_name = 'District'
    for _, district in districts.iterrows():
        district_id = district[district_column_name]
        district_to_precincts[district_id] = []
    for precinct_index, _ in precincts.iterrows():
        district_index = precinct_to_district_assignment[precinct_index]
        district_id = districts.loc[district_index][district_column_name]
        district_to_precincts[district_id].append(precinct_index)
    return district_to_precincts


def create_precinct_graph(precincts):
    G = Graph.from_geodataframe(precincts)

    return G


if __name__ == '__main__':
    for state in states:
        cur_state = state
        # Group all data sources for precincts into one unified geojson file.
        unified_gdf = load_merged_precinct_data(from_scratch=RUN_FROM_SCRATCH)
        districts = load_geojson_as_gdf(
            f'{DATA_DIR}/{cur_state}/Districts_{cur_state}.geojson')
        districts = try_cast_columns_to_numeric(districts)
        mapping = map_district_to_precincts(unified_gdf, districts)
        precinct_series = pd.Series(
            {precinct: district for district, precincts in mapping.items() for precinct in precincts})
        unified_gdf['DISTRICT'] = unified_gdf.index.map(precinct_series)
        # plot the precincts, color by district
        unified_gdf.plot(column='DISTRICT', cmap='tab20')
        plt.show()
        # fix geometry
        unified_gdf['geometry'] = unified_gdf['geometry'].buffer(0)
        graph = create_precinct_graph(unified_gdf)
        # drop geometry column from each node
        for node in graph.nodes:
            graph.nodes[node].pop('geometry', None)
        # sum up R and D votes for each node
        total_R = 0
        total_D = 0
        total_black = 0
        total_hispanic = 0
        total_population = 0
        for node in graph.nodes:
            total_R += graph.nodes[node]['R']
            total_D += graph.nodes[node]['D']
            total_black += graph.nodes[node]['Black or African American']
            total_hispanic += graph.nodes[node]['Hispanic']
            total_population += graph.nodes[node]['Population']
        total_votes = total_R + total_D
        print(f"Total population: {total_population}")
        print(f"Total votes: {total_votes}")
        print(f"R percentage: {total_R / total_votes}")
        print(f"D percentage: {total_D / total_votes}")
        print(f"Black percentage: {total_black / total_population}")
        print(f"Hispanic percentage: {total_hispanic / total_population}")
        



        adjacency_data = nx.adjacency_data(graph)
        with open(f'{DATA_DIR}/{cur_state}/adjacency_data.json', 'w') as f:
            json.dump(adjacency_data, f)
        print(f"Finished preprocessing {cur_state}")
