import geopandas as gpd
import streamlit as st
from io import BytesIO
import zipfile
import tempfile

# Title of the app
st.title("Shapefile to GeoJSON Converter By Gaurav")

# Uploading the shapefile components
uploaded_shapefile = st.file_uploader("Upload a Shapefile (zip all .shp, .shx, .dbf, etc. together)", type=["zip"])

# Processing the uploaded file
if uploaded_shapefile is not None:
    with tempfile.TemporaryDirectory() as tmpdir:
        # Extract files from the uploaded zip to the temporary directory
        with zipfile.ZipFile(BytesIO(uploaded_shapefile.read()), 'r') as zip_ref:
            zip_ref.extractall(tmpdir)
        
        # Find the shapefile in the extracted files
        for file_name in zip_ref.namelist():
            if file_name.endswith('.shp'):
                shapefile_path = f"{tmpdir}/{file_name}"
                break

        # Read the shapefile using GeoPandas
        gdf = gpd.read_file(shapefile_path)
        gdf = gdf.to_crs(4326)  # Convert to WGS 84 EPSG:4326
        
        # Convert to GeoJSON
        geojson = gdf.to_json()

        # Provide download button for the GeoJSON
        st.download_button(label="Download GeoJSON", data=geojson, file_name="output.geojson", mime="application/json")

        st.success("Conversion completed! Click the button above to download the GeoJSON file.")

