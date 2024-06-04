import geopandas as gpd

# File should be discarded after project is finished, will only be run to convert file formats.
# Read the shapefile
shapefile_path = '..\data\TX\Districts_TX_Raw\\PLANC2193.shp'
gdf = gpd.read_file(shapefile_path)
# convert crs to wgs84
gdf = gdf.to_crs('EPSG:4326')
gdf.name = "Districts_TX"
# Convert and save to GeoJSON
geojson_path = '../data/TX/Districts_TX.geojson'
gdf.to_file(geojson_path, driver='GeoJSON')

