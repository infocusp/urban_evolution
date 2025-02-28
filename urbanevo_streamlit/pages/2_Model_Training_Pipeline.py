import streamlit as st
import pandas as pd

st.set_page_config(page_title="Training Pipeline")
st.markdown("# Model Training Pipeline")
st.sidebar.markdown("# Model Training Pipeline")

tab_design, tab_data, tab_model_year, tab_model = st.tabs(["Pipeline Design", "Data Preparation","Data Selection", "Model Selection"])
with tab_design:
    st.subheader("Model Training Pipeline Design", divider=True)
    st.image("urbanevo_streamlit/static/hld.png")

with tab_data:
    st.subheader("Data Preparation", divider=True)
    st.markdown("The Data pre-processing involves mainly three major steps to create the input dataset. This involves stacking tiffs, creating spatial windows and train-test splits.")
    st.markdown("### Stacking tiffs ###")
    st.markdown("We have separate tiff files for each year's label data and features in the GCS bucket. We need to convert these files into a single multi-band raster tiff file. In this step, we handle the missing values and concatenate the data accordingly for each year.This results in a stacked single raw tiff which contains labels and features for each year.")
    st.image("urbanevo_streamlit/static/Stacked.drawio.png")
    st.markdown("### Creating Spatial Windows ###")
    st.markdown("As the Geospatial data can be very large depending on the resolution. Processing this data might require higher memory. To make this efficient, we can divide the raw stacked data into several smaller windows depending on the block size we need. This will also ensure that the spatial context is preserved. This also helps us create the input training and validation data independently, thus not causing any data leakage.")
    st.markdown("### Train-Test Splits ###")
    st.markdown("To maintain spatial independence, raw data is split into training and validation datasets. Here we are using a 70:30 data split for training and validation datasets.This would give us the processed data, which can be used as an input to the model.")
    st.image("urbanevo_streamlit/static/splitting_stacked_features.drawio.png")

with tab_model_year:
    st.subheader("Data Selection for Model Training", divider=True)
    st.markdown("For model training the target labels contain the data for the next 5 years or 1 year, whereas the feature data contains the data one year prior to the model training date.")
    st.markdown("1 year model training")
    #1 year table
    df_1 = pd.DataFrame(
    {
        "Model trained": ["2010", "2011","2012","2013", "2014", "2015", "2016", "2017", "2018", "2019", "2020", "2021", "2022", "2023"],
        "Training data year range": ["2009-2010", "2010-2011", "2011-2012","2012-2013", "2013-2014", "2014-2015", "2015-2016", "2016-2017", "2017-2018", "2018-2019", "2019-2020", "2020-2021", "2021-2022", "2022-2023"],
        "Prev_label year": ["2009", "2010", "2011", "2012", "2013", "2014", "2015", "2016", "2017", "2018", "2019", "2020", "2021", "2022"],
        "Predictions year range": ["2011-2012", "2012-2013", "2013-2014", "2014-2015", "2015-2016", "2016-2017", "2017-2018", "2018-2019", "2019-2020", "2020-2021", "2021-2022", "2022-2023", "2023-2024", "2024-2025"],
    }
    )
    st.table(df_1)
    st.markdown("5 year model training")
    # 5 year table
    df_5 = pd.DataFrame(
    {
        "Model trained": ["2010", "2011","2012","2013", "2014", "2015"],
        "Training data year range": ["2009-2010", "2010-2011", "2011-2012","2012-2013", "2013-2014", "2014-2015"],
        "Prev_label year": ["2005", "2006", "2007", "2008", "2009", "2010"],
        "Predictions year range": ["2015-2020", "2016-2021", "2017-2022", "2018-2023", "2019-2024", "2020-2025"],
    }
    )
    st.table(df_5)

with tab_model:
    st.subheader("Models Trained", divider=True)
    st.markdown("### LGBM (Baseline) ###")
    st.markdown("LGBM trained with only 3 features as baseline model. The features on which the model was trained are Landcover(LC_Type1), population_density(pop_den) and prev_urban.")
    st.markdown("### LGBM model with weighted sampling ###")
    st.markdown("Given that the dataset is highly imbalanced, with the majority of labels belonging to the rural class, we implemented weighted sampling by assigning each class a weight inversely proportional to its frequency and applying these weights to each data point accordingly.")
    st.markdown("### LGBM model with weighted sampling and additional features ###")
    st.markdown("We have added a diverse set of features which includes:")
    st.markdown("- ***Features strongly correlated*** with urbanization, such as previous urbanization (prev_urban), night time light (ntl), population density (pop_den), population growth (pop_gt), and total built volume (bn_total).")
    st.markdown("- ***Features weakly correlated*** with urbanization but strongly interrelated, such as maximum temperature (tmmx), minimum temperature (tmmn), Normalized Difference Vegetation Index (NDVI), Enhanced Vegetation Index (EVI), landcover (LC_Type1), and health sites, which may indirectly influence urbanization trends and patterns over time.")
    st.markdown("### Hyper-parameter tuned LGBM model with weighted sampling and additional features ###")
    st.markdown("Although the model can be tuned on numerous parameters, due to limited computational resources and time constraints, we focused on optimizing the following key parameters:")
    st.markdown(" - ***Learning rate:*** Determines the step size at which the model’s weights are updated during training.")
    st.markdown(" - ***Num_leaves:*** Specifies the maximum number of nodes per tree.")
    st.markdown(" - ***Min_child_samples:*** Regulates the minimum number of samples required to create a node, effectively controlling the tree depth and preventing overfitting by reducing the model's sensitivity to noise in the training data.")
    st.markdown(" - ***Min_child_weight:*** Controls the minimum sum of instance weights needed for a child node, influencing the tree structure and the contribution of individual data points to the model.")
    st.markdown(" - ***Max_depth:*** Sets the maximum depth of the tree, helping to manage overfitting by limiting model complexity.")

   
      