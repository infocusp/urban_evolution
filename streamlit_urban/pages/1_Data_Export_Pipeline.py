# Urban Evo - Demo - Data Pipeline

import streamlit as st
import pandas as pd
st.markdown("# Data Export Pipeline")
st.sidebar.markdown("# Data Export Pipeline")

#st.header("Data Pipeline", divider=True)
st.markdown("""The feature datasets used for modelling are all available on Earth Engine and consists of different climatic data, built-up data, population data and related datasets.
""")

tab_label, tab_features, tab_custom_features, tab_corr ,tab_storage = st.tabs(["Label Generation", "Data Features","Custom Features", "Data Corelation", "Data Storage"])


with tab_label:
    st.subheader("Label Generation", divider=True)
    st.markdown("""Labels for urbanization prediction are generated with a hybrid approach using below earth engine datasets:""")

    col1, col2  = st.columns(2)

    with col1:
        st.subheader("[GPWv411: Population Density](https://developers.google.com/earth-engine/datasets/catalog/CIESIN_GPWv411_GPW_Population_Density#description)", divider=True)

        st.markdown(
    """
    - Contains estimates of the number of persons per square kilometer
    - Updated after every 5 years
    - Can use the population density to classify regions into urban and rural.
    - Band used is 'population_density'
"""
)
        #st.image("static/CIESIN_GPWv411_GPW_Population_Density_sample.png")

    with col2:
         st.subheader("[MCD12Q1.061 MODIS Land Cover Global 500m](https://developers.google.com/earth-engine/datasets/catalog/MODIS_061_MCD12Q1#bands)", divider=True)
         st.markdown(
        """
        - Represents the land surface that is covered by man-made structures such as buildings, roads & other forms of infrastructurewhich show human habitation 
        - Updated every year
        - Use only classes denoting the urban and built up lands (`LC_Type1` band from the data set,value 13)
        - Data is binary, which means it denotes 1 if there is impervious surface else 0.
        
    """
)
        # st.markdown("""[MCD12Q1.061 MODIS Land Cover Type Yearly Global 500m](https://developers.google.com/earth-engine/datasets/catalog/MODIS_061_MCD12Q1#bands)
        # - Represents the land surface that is covered by man-made structures such as buildings, roads & other forms of infrastructurewhich show human habitation 
        # - Updated every year, 
        # - Use only classes enoting the urban and built up lands (`LC_Type1` band from the data set,value 13)
        # - This data is binary, which means it denotes 1 if there is impervious surface else 0.
        # """)
        
        #st.image("static/MODIS_061_MCD12Q1_sample.png")
     
    #chart_data = pd.DataFrame([[0,400],[1,400],[0,900],[1,900],[0,1200],[1,1200]])
    #chart_data = pd.DataFrame([[400,0],[400,1],[900,0],[900,1],[1200,0],[1200,1]],columns = ['built-up','population'])
    #st.scatter_chart(chart_data)
    df = pd.DataFrame(
    {
        "Class Name": ["0", "1","2","3"],
        "Class Description": ["High Density urban grid cell", "Low Density urban grid cell", "Peri urban grid cell(transitional)","Rural grid cell"],
        "Definition": [
            "population density >= 1200/km^2 & Built up surface area = 1",
            "population density >= 900/km^2 & Built up surface area = 1",
            "population density >= 400/km^2 & Built up surface area = 1",
            "population density < 400/km^2 OR Built up surface area = 0"
        ],
    }
    )
    st.table(df)
    st.image("static/class_distribution.png")
    st.image("static/label_main.png",caption="Ground truth labels spread in Northern India")

with tab_features:
     st.subheader("Data Features", divider=True)
     st.markdown("""Features are either bands from Earth Engine Datastes or custome features derived from them. Below columns describe the features used to train the model. """)
     col_terra, col2_modis  = st.columns(2)
     with col_terra:
        st.subheader("[TerraClimate: Monthly Climate](https://developers.google.com/earth-engine/datasets/catalog/IDAHO_EPSCOR_TERRACLIMATE)", divider=True)
        st.image("static/TERRACLIMATE.png")
        with st.expander("Bands Details"):
            st.markdown("**pdsi**- Palmer Drought Severity Index: Its a standardized index that measures the severity and duration of drought using temperature and precipitation data to estimate the dryness of a region. Updated monthly. ")
            st.markdown("**pr** - Precipitation accumulation is the total amount of precipitation over a certain period of time in a specified place.Updated monthly.")
            st.markdown("**tmmn**-Minimum temperature recorded over a certain period in a specified place. Updated monthly.")
            st.markdown("**tmmx**-Maximum temperature recorded over a certain period in a specified place. Updated monthly.")
     with col2_modis:
        st.subheader("[MOD13A2.061 Terra Vegetation ](https://developers.google.com/earth-engine/datasets/catalog/MODIS_061_MOD13A2)", divider=True)
        st.image("static/MODIS_061.png")
        with st.expander("Bands Details"):
            st.markdown("**NDVI**- 16 Day Normalized Difference Vegetation Index is a measure of the amount of and vigor of vegetation on the land surface. This metric is developed to more easily distinguish between green vegetation from bare soils. Updated monthly.")
            st.markdown("**EVI** - 16 Day Enhanced Vegetation Index. Updated monthly.")
        
     col_srtm, col2_mcd  = st.columns(2)
     with col_srtm:
        st.subheader("[SRTM Digital Elevation](https://developers.google.com/earth-engine/datasets/catalog/CGIAR_SRTM90_V4)", divider=True)
        st.image("static/srtm.png")
        with st.expander("Bands Details"):
            st.markdown("**Elevation**-  Contains information about the elevation of a region in meters(m).")
     with col2_mcd:
        st.subheader("[MODIS Land Cover Type](https://developers.google.com/earth-engine/datasets/catalog/MODIS_061_MCD12Q1)", divider=True)
        st.image("static/MODIS_061_MCD12Q1_sample.png")
        with st.expander("Bands Details"):
            st.markdown("**LC_Type1**- Annual International Geosphere-Biosphere Programme (IGBP) classification: IGBP classifies the surface types of ecosystems. For e.g. Grasslands, Permanent wetlands, Mixed forests, Fresh snow, water bodies etc.")
     col_pop, col2_build  = st.columns(2)
     with col_pop:
        st.subheader("[GPWv411: Population Density](https://developers.google.com/earth-engine/datasets/catalog/CIESIN_GPWv411_GPW_Population_Density)", divider=True)
        st.image("static/CIESIN_GPWv411_GPW_Population_Density_sample.png")
        with st.expander("Bands Details"):
            st.markdown("**population density** - It estimates number of persons per square kilometer. Updated every 5 years.")
     with col2_build:
        st.subheader("[GHSL: Global building volume](https://developers.google.com/earth-engine/datasets/catalog/JRC_GHSL_P2023A_GHS_BUILT_V)", divider=True)
        st.image("static/ghsl.png")
        with st.expander("Bands Details"):
            st.markdown("**bv_total**- Total building volume per grid cell. Updated every 5 year.")
            st.markdown("**bv_nres**- Non-residential building volume per grid cell. Updated every 5 year.")
    

     col_custom,col_road = st.columns(2)
     with col_custom:
        st.subheader("Custom Features", divider=True)
        #st.image("static/roads.png")
        with st.expander("Bands Details"):
            st.markdown("**urb_6**- It calculates the number of pixels within a  6×6 pixel grid that is better urbanized than the specific pixel being evaluated.")
            st.markdown("**urb_10**- It calculates the number of pixels within a 10×10 pixel grid that is  better urbanized than the pixel under consideration.")
            st.markdown("**urb_20**- It calculates the number of pixels within a 20×20  pixel grid that is better urbanized than the pixel under consideration.")
            st.markdown("**population growth**- Change in population over the last five years to understand how this growth has affected the current urbanization.")
            st.markdown("**prev_urban**- Previous 5 year urbanization.")
     with col_road:
        st.subheader("[Global Roads Inventory ](https://gee-community-catalog.org/projects/grip/)", divider=True)
        #st.image("static/roads.png")
        with st.expander("Bands Details"):
            st.markdown("**Roads**- This dataset is a vector dataset, which contains the Global Roads and highways data.")
     
     col2_heatlh,col_ntl  = st.columns(2)
     with col2_heatlh:
        st.subheader("[Global Healthsites Mapping](https://gee-community-catalog.org/projects/health_sites/)", divider=True)
        #st.image("static/roads.png")
        with st.expander("Bands Details"):
            st.markdown("**Health Sites**- This vector dataset provides information about different health facilities across the world.")
     with col_ntl:
        st.subheader("[GAN based Synthetic VIIRS (NTL) India](https://gee-community-catalog.org/projects/syn_ntl/)", divider=True)
        #st.image("static/roads.png")
        with st.expander("Bands Details"):
            st.markdown("**ntl**- This Dataset contains monthly Night time light data Globally. The unit used is radiance.")
with tab_custom_features:
    st.subheader("More About Custom Features", divider=True)
    st.markdown("**1. Counting More Urbanized Pixels in 6×6 Surrounding Pixel Grid(urb_6).** For each pixel, we examine its surrounding 6×6 pixel grid and count the number of neighboring pixels that exhibit a higher level of urbanization than the central pixel. This count provides insights into the relative urbanization density within the local area. The count of more urbanized pixels in the surrounding provides insights about the urban growth patterns. If urbanization has already occurred in neighboring areas, it is highly likely that the given area will also undergo urbanization in the future.")
    st.markdown("**2. Counting More Urbanized Pixels in 10×10 Surrounding Pixel Grid(urb_10).** For each pixel, we examine its surrounding 10×10 pixel grid and count the number of neighboring pixels that exhibit a higher level of urbanization than the central pixel. This count provides insights into the relative urbanization density within the local neighborhood. As we increase the size of the surrounding pixel grid, a larger area is considered when assessing urbanization.")
    st.markdown("**3. Counting More Urbanized Pixels in a 20×20 Surrounding Pixel  Grid(urb_20).** For each pixel, we examine its surrounding 20×20 pixel grid and count the number of neighboring pixels that exhibit a higher level of urbanization than the central pixel. This count provides insights into the relative urbanization density within the local neighborhood.")
    st.markdown("**4. Population Growth Over the Last 5 Years(pg)** We compute the change in population over the last five years to understand how this growth has affected the current urbanization.")
    st.markdown("**5. Urbanization in the Last 5 Years(prev_urban)** We have incorporated a band representing urbanization over the last 5 years. This provides prior information to the model, helping it to understand historical trends and predict accordingly.")

with tab_corr:
    st.subheader("Features correlation Matrix:", divider=True)
    st.image("static/featcorr.png")
    st.markdown("### Conclusion drawn from the correlation matrix: ###")
    st.markdown("- Features such as night time light(ntl), prev_urban, population density(pop_den), population growth(pop_gt), built_volume_total(bv_total) are highly correlated with urbanization.")
    st.markdown("- Features such as  max_temperature(tmmx), min_temperature(tmmn), Normalized Difference Vegetation Index(NDVI), enhanced vegetation index(EVI), landcover(LC_Type1) and roads form another cluster that are correlated with each other, but not strongly correlates with urbanization. However,  we included them because they provide information that might indirectly influence urbanization trends or patterns.")
    st.markdown("- Some features like health sites show relatively weaker correlations with urbanization, included to account for potential variations in health care accessibility, which may affect or be affected by urbanization over time.")

with tab_storage:
    st.subheader("Data Storage", divider=True)
    st.markdown("The data for this project is exported from Google Earth Engine (GEE) scripts and stored in a Google Cloud Storage (GCS) bucket. All the data is in raster format and hence it is stored as GeoTiff files. The spatial resolution for both label and feature data is 1500m.")
    st.markdown("**Sample gcs path:** `gs://earth-engine-seminar/urbanization/data/export_16012025/2005-01-01/urban_feat.tif`")
    st.markdown("Below is the Directory structure which is followed to export the data into the bucket.")
    st.image("static/dir.png")
    st.markdown("This directory structure is designed to ensure efficient organization, easy access, and scalability of the data which can be exported in the bucket.")
    st.markdown("The base path for storing the data is `gs://earth-engine-seminar/urbanization/data`.")
    st.markdown("Whenever we export the data from the earth engine code editor, we append a new folder name to this directory, preferably export_DDMMYYYY representing the date of export. This would ensure we export unique data on a particular day.")
    st.markdown("Inside this folder we have folders for the years the data was exported, and it contains the labels as urban_label.tif and feature data as urban_feat.tif for that particular year respectively. This makes the data easily accessible, whenever we want to read and use the data using gcloud cli/sdk.")

    
    
    