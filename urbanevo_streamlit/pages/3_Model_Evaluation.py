import streamlit as st
import pandas as pd

st.set_page_config(page_title="Model Evaluation")
st.markdown("# Model Evaluation")
st.sidebar.markdown("# Model Evaluation")

tab_year_5, tab_year1 = st.tabs(["5 year model", "1 year model"])
with tab_year_5:
    st.subheader("5 year", divider=True)
    option = str(st.selectbox(
    "Select Evaluation",
    ("Confusion Matrix","Model Comparison - Precision, Recall, F1-score","Year on Year - Comparison - Precision, Recall, F1-score")))

    if option == 'Confusion Matrix':
        col1, col2  = st.columns(2)
        with col1:
            st.markdown("### LGBM Baseline Model ###")
            st.image("urbanevo_streamlit/static/cm_lgbm_base_5.png")
            with st.expander("Conclusion"):
                st.markdown("The model has predominantly predicted the rural class for most instances, likely due to the dataset being imbalanced, with the majority of data points belonging to the rural class.")
        with col2:
            st.markdown("### LGBM weighted sampling ###")
            st.image("urbanevo_streamlit/static/cm_lgbm_weight_5.png")
            with st.expander("Conclusion"):
                st.markdown("When we apply weighted sampling, the model’s performance improves. This approach ensures that underrepresented classes receive more attention during training, reducing the bias caused by the dataset imbalance. By doing so, the model learns to distinguish patterns in both majority and minority classes more effectively, resulting in better overall predictions and improved generalization across all classes.")
        col3, col4  = st.columns(2)
        with col3:
            st.markdown("### LGBM model - weighted sampling & additional features. ###")
            st.image("urbanevo_streamlit/static/cm_lgbm_3_5year.png")
            with st.expander("Conclusion"):
                st.markdown("Now we can see that classwise mis-classification has further reduced with such diverse set of features which includes:")
                st.markdown("- Features strongly correlated with urbanization, such as previous urbanization (prev_urban), night time light (ntl),population density (pop_den), population growth (pop_gt), and total built volume (bn_total).")
                st.markdown("- Features weakly correlated with urbanization but strongly interrelated, such as maximum temperature (tmmx), minimum temperature (tmmn), Normalized Difference Vegetation Index (NDVI), Enhanced Vegetation Index (EVI), landcover (LC_Type1), and health sites, which may indirectly influence urbanization trends and patterns over time.")
        with col4:
            st.markdown("### Hyper-parameter tuned LGBM model - weighted sampling & features ###")
            st.image("urbanevo_streamlit/static/cm_lgbm_4_5year.png")
            with st.expander("Conclusion"):
                st.markdown("Tuning the hyperparameters has further improved the model's accuracy and enhanced its ability to distinguish between closely related classes, such as transitional and low-density urban areas. This optimization has helped the model capture finer distinctions in the data, leading to more precise and reliable predictions.")
    elif option == 'Model Comparison - Precision, Recall, F1-score':
        col11, col22, col33  = st.columns(3)
        with col11:
            st.markdown("### Precision ###")
            st.image("urbanevo_streamlit/static/prec_mc.png")
        with col22:
            st.markdown("### Recall ###")
            st.image("urbanevo_streamlit/static/recall_mc.png")
        with col33:
            st.markdown("### F1-Score ###")
            st.image("urbanevo_streamlit/static/f1score_mc.png")
        
        st.markdown("We can conclude from the above plots that by using weighted sampling, the model is trained with a balanced number of points across classes, enabling it to effectively distinguish between the classes. Furthermore, incorporating additional relevant features enhances the model's ability to differentiate between closely related classes, such as low-density urban and transitional, with greater clarity.It is important to note that the precision for the high-density urban is approximately 0, Similarly, recall for transitional class is approximately 0 and F1_score for transitional classes is approximately 0. As a result, no plots are generated for these classes for baseline.")
    else:
        col111, col222, col333  = st.columns(3)
        with col111:
            st.markdown("### Precision ###")
            st.image("urbanevo_streamlit/static/prec_yy5.png")
        with col222:
            st.markdown("### Recall ###")
            st.image("urbanevo_streamlit/static/recall_yy5.png")
        with col333:
            st.markdown("### F1-Score ###")
            st.image("urbanevo_streamlit/static/f1score_yy5.png")
        
        st.markdown("We trained our model on five train-test dataset pairs on the best performing hyper parameter tunded model. The model was trained on data from a specific year and tested on data of 5th year. This process was repeated for each year between 2010 and 2015. For example, the model trained on the 2010 dataset was tested on the 2015 dataset, and the model trained on the 2011 dataset was tested on the 2016 dataset.Below is the comparison between precision, recall and f1_score for the 5 training-test dataset pairs.Note- We have mentioned the prediction year in the y-label.")        

with tab_year1:
    st.subheader("1 year", divider=True)
    st.markdown("### LGBM model - weighted sampling & additional features. ###")
    col1_1, col2_1  = st.columns(2)
    with col1_1:
            st.markdown("##### Confusion Matrix #####")
            st.image("urbanevo_streamlit/static/cc_1year.png")
    with col2_1:
            st.markdown("##### Precision #####")
            st.image("urbanevo_streamlit/static/prec_1year.png")
    col3_1, col4_1  = st.columns(2)
    with col3_1:
            st.markdown("##### Recall #####")
            st.image("urbanevo_streamlit/static/recall_1year.png")
    with col4_1:
            st.markdown("##### F1 Score #####")
            st.image("urbanevo_streamlit/static/f1score_1year.png")