import geopandas as gpd
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import json

'''Generic utility functions for loading and plotting data'''

def load_geojson_as_gdf(filename):
    if not filename.endswith(".geojson"):
        print(f"Warning: {filename} is not a geojson file")
        return None
    try:
        gdf = gpd.read_file(filename)
        if gdf.crs != "EPSG:4326":
            gdf = gdf.to_crs("EPSG:4326")
            gdf.to_file(filename, driver='GeoJSON')
        return gdf
    except Exception as e:
        print(f"Error loading geojson file: {e}")
        return None


def load_csv_as_df(filename):
    if not filename.endswith(".csv"):
        print(f"Warning: {filename} is not a csv file")
        return None

    try:
        df = pd.read_csv(filename)
        return df
    except Exception as e:
        print(f"Error loading csv file: {e}")
        return None


def draw_shape(geometry, fill_color, alpha, hatch=None):
    if geometry.geom_type == 'MultiPolygon':
        for polygon in geometry.geoms:
            plt.fill(*polygon.exterior.xy, color=fill_color, alpha=alpha, hatch=hatch)
    else:
        plt.fill(*geometry.exterior.xy, color=fill_color, alpha=alpha, hatch=hatch)


def draw_geojson(geodataframe, color='blue', alpha=0.5, hatch=None):
    # Color of each geometry can be specified by a column named 'color'
    for _, row in geodataframe.iterrows():
        fill_color = row.get(
            'color', color) if 'color' in geodataframe.columns else color
        draw_shape(row['geometry'], fill_color, alpha, hatch)


def try_cast_columns_to_numeric(df):
    for column in df.columns:
        try:
            df[column] = pd.to_numeric(df[column], errors='ignore')
        except:
            pass
    return df


class NumpyEncoder(json.JSONEncoder):
    # Numpy encoder used for allowing numpy datatypes to be serialized into json.
    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        elif isinstance(obj, np.floating):
            return float(obj)
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        else:
            return super(NumpyEncoder, self).default(obj)


def write_dict_as_json(ensemble_directory, filename, dictionary):
    with open(f"{ensemble_directory}/{filename}.json", "w") as f:
        json.dump(dictionary, f, cls=NumpyEncoder)

def load_json_as_dict(ensemble_directory, filename):
    with open(f"{ensemble_directory}/{filename}.json", "r") as f:
        return json.load(f)


def remove_unwanted_columns(df,unwanted_columns=[]):
    for column in unwanted_columns:
        if column in df.columns:
            del df[column]
    df.dropna(axis=1, how='all', inplace=True)


def reverse_mapping(dictionary):
    reverse_dict = {}
    for k, v in dictionary.items():
        if v not in reverse_dict:
            reverse_dict[v] = []
        reverse_dict[v].append(k)
    return reverse_dict