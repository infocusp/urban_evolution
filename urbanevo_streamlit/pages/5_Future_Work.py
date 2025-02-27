import streamlit as st

st.markdown("# Future Work")
#st.header("Future Work ", divider=True)
st.sidebar.markdown("# Future Work")

st.markdown("### Better Label Definition ###")
st.markdown("- Currently, to calculate the labels, we use population data and the urban built-up surface. This at a high level serves our purpose as we are correctly able to classify the urban regions as we need. But these are not 100% accurate and lack some precision.The generation of labels is very subjective and can be improved by accounting more factors for urbanization. This would give us even more accurate labels and help us get better predictions.")

st.markdown("### Model Exploration ###")
st.markdown("- Currently, the model training is based on LightGBM (LGBM), which provides efficiency and interpretability for structured geospatial data. However, future improvements can be explored by experimenting with different models, particularly deep learning architectures like neural networks. We can use Convolutional Neural Networks (CNNs) to  Leverage spatial patterns in raster data for improved feature extraction. Also try combining the LGBM with neural network features to enhance feature selection and predictive accuracy.")

st.markdown("### Additional features ###")
st.markdown("- To improve model performance and enhance predictive accuracy, additional features can be explored in future iterations. These features can provide a more comprehensive understanding of urbanization patterns: Socioeconomic Data, Infrastructure accessibility Data, Land Use and Zoning Data")


