
import streamlit as st
import pandas as pd
import requests

# Base URL of the Flask backend
BACKEND_URL = "http://backend:7860"

# Streamlit UI for Product Store Sales Prediction
st.title("SuperKart Product Store Sales Prediction App")
st.write("This tool predicts the product store sales of a product in a given store based on store and product details.")

st.subheader("Enter the product and store details:")

# Collect user input
product_weight = st.number_input("Product Weight", min_value=0.00, max_value=100.00, value=0.00)
product_sugar_content = st.selectbox("Sugar Content", ["No Sugar", "Low Sugar", "Regular"])
product_allocated_area = st.number_input("Product Allocated Area", min_value=0.000, step=.001, value=1.000)
product_MRP = st.number_input("Maximum Retail Price", min_value=0.00, max_value=500.00, value=0.01)
store_size = st.selectbox("Store Size", ["Small", "Medium", "High"])
store_location_city_type = st.selectbox("Store Location City Type", ["Tier 1", "Tier 2", "Tier 3"])
store_type = st.selectbox("Store Type", ["Food Mart", "Departmental Store", "Supermarket Type1", "Supermarket Type2", "Supermarket Type3"])
product_id_char = st.selectbox("Product ID Char", ["FD", "DR", "NC"])
store_age = st.number_input("Store Age", min_value=0, step=1, value=200)
product_type_category = st.selectbox("Product Type Category", ["Perishables", "Non-Perishables"])

# Convert user input into a DataFrame
input_data = {
    'Product_Weight': product_weight,
    'Product_Sugar_Content': product_sugar_content,
    'Product_Allocated_Area': product_allocated_area,
    'Product_MRP': product_MRP,
    'Store_Size': store_size,
    'Store_Location_City_Type': store_location_city_type,
    'Store_Type': store_type,
    'Product_Id_char': product_id_char,
    'Store_Age_Years': store_age,
    'Product_Type_Category': product_type_category
}

# Make prediction when the "Predict" button is clicked
if st.button("Predict", type="primary"):
    response = requests.post(f"{BACKEND_URL}/v1/predict", json=input_data)  # Send data to Flask API
    if response.status_code == 200:
        prediction = response.json()['Predicted Product Store Sales']
        st.success(f"Predicted Rental Price (in dollars): {prediction}")
    else:
        st.error("Unable to connect to the prediction API.")

# Section for batch prediction
st.subheader("Batch Prediction")

# Allow users to upload a CSV file for batch prediction
uploaded_file = st.file_uploader("Upload CSV file for batch prediction", type=["csv"])

# Make batch prediction when the "Predict Batch" button is clicked
if uploaded_file is not None:
    if st.button("Predict Batch", type="primary"):
        response = requests.post(f"{BACKEND_URL}/v1/predictbatch", files={"file": uploaded_file})  # Send file to Flask API
        if response.status_code == 200:
            predictions = response.json()
            st.success("Batch predictions completed!")
            st.write(predictions)  # Display the predictions
        else:
            st.error("Unable to connect to the prediction API.")   

