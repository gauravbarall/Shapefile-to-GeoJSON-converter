import geopandas as gpd
import streamlit as st
from io import BytesIO
import tempfile
import os

# Title of the app
st.title("Shapefile to GeoJSON Converter By Gaurav")

# Uploading shapefile components
uploaded_files = st.file_uploader("Upload Shapefile components (.shp, .shx, .dbf, etc.)", type=["shp", "shx", "dbf", "prj", "cpg"], accept_multiple_files=True)

# Processing the uploaded files
if uploaded_files:
    with tempfile.TemporaryDirectory() as tmpdir:
        # Save uploaded files to the temporary directory
        file_paths = {}
        for uploaded_file in uploaded_files:
            file_path = os.path.join(tmpdir, uploaded_file.name)
            file_paths[uploaded_file.name] = file_path
            with open(file_path, "wb") as f:
                f.write(uploaded_file.getvalue())
        
        # Identify the shapefile (.shp)
        shapefile_path = None
        for file_name in file_paths:
            if file_name.endswith('.shp'):
                shapefile_path = file_paths[file_name]
                break
        
        if shapefile_path:
            # Read the shapefile using GeoPandas
            gdf = gpd.read_file(shapefile_path)
            gdf = gdf.to_crs(4326)  # Convert to WGS 84 EPSG:4326
            
            # Convert to GeoJSON
            geojson = gdf.to_json()

            # Provide download button for the GeoJSON
            st.download_button(label="Download GeoJSON", data=geojson, file_name="output.geojson", mime="application/json")

            st.success("Conversion completed! Click the button above to download the GeoJSON file.")
        else:
            st.error("No shapefile (.shp) found. Please upload the correct shapefile components.")

