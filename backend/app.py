# Import necessary libraries
import numpy as np
import joblib  # For loading the serialized model
import pandas as pd  # For data manipulation
from flask import Flask, request, jsonify  # For creating the Flask API

# Initialize the Flask application
product_store_sales_predictor_api = Flask("SuperKart Product Store Sales Predictor")

# Load the trained machine learning model
model = joblib.load("superkart_productstoresales_prediction_model_v1_0.joblib")

# Define a route for the home page (GET request)
@product_store_sales_predictor_api.get('/')
def home():
    """
    This function handles GET requests to the root URL ('/') of the API.
    It returns a simple welcome message.
    """
    return "Welcome to the SuperKart Product Store Sales Prediction API!"

# Define an endpoint for single product store sales prediction (POST request)
@product_store_sales_predictor_api.post('/v1/predict')
def predict_product_store_sales():
    """
    This function handles POST requests to the '/v1/predict' endpoint.
    It expects a JSON payload containing product and store details and returns
    the predicted product store sales as a JSON response.
    """
    # Get the JSON data from the request body
    product_store_data = request.get_json()

    # Extract relevant features from the JSON data
    sample = {
        'Product_Weight': product_store_data['Product_Weight'],
        'Product_Sugar_Content': product_store_data['Product_Sugar_Content'],
        'Product_Allocated_Area': product_store_data['Product_Allocated_Area'],
        'Product_MRP': product_store_data['Product_MRP'],
        'Store_Size': product_store_data['Store_Size'],
        'Store_Location_City_Type': product_store_data['Store_Location_City_Type'],
        'Product_Id_char': product_store_data['Product_Id_char'],
        'Store_Type': product_store_data['Store_Type'],
        'Store_Age_Years': product_store_data['Store_Age_Years'],
        'Product_Type_Category': product_store_data['Product_Type_Category']
    }

    # Convert the extracted data into a Pandas DataFrame
    input_data = pd.DataFrame([sample])

    # Make a prediction using the trained model
    prediction = model.predict(input_data).tolist()[0]

    # The conversion above is needed as we convert the model prediction (log price) to actual price using np.exp, which returns predictions as NumPy float32 values.
    # When we send this value directly within a JSON response, Flask's jsonify function encounters a datatype error

    # Return the actual price
    return jsonify({'Predicted Product Store Sales': prediction})


# Define an endpoint for batch prediction (POST request)
@product_store_sales_predictor_api.post('/v1/predictbatch')
def predict_product_store_sales_batch():
    """
    This function handles POST requests to the '/v1/predictbatch' endpoint.
    It expects a CSV file containing property details for multiple properties
    and returns the predicted rental prices as a dictionary in the JSON response.
    """
    # Get the uploaded CSV file from the request
    file = request.files['file']

    # Read the CSV file into a Pandas DataFrame
    input_data = pd.read_csv(file)

    # Make predictions for the batch data
    predictions = model.predict(input_data).tolist()

    # Create an output dictionary mapping row index to predicted sales
    output_dict = {str(i): round(pred, 2) for i, pred in enumerate(predictions)}

    # Make predictions for all product stores in the DataFrame (get log_product_store_sales)
    #predicted_log_product_store_sales = model.predict(input_data).tolist()

    # Calculate actual product store sales
    #predicted_product_store_sales = [round(float(np.exp(log_product_store_sales)), 2) for log_product_store_sales in predicted_log_product_store_sales]

    # Create a dictionary of predictions with product + store IDs as keys
    #product_store_ids = (input_data['Product_Id'] + input_data["Store_Id"]).tolist()  
    #output_dict = dict(zip(product_store_ids, predicted_product_store_sales))  # Use actual prices

    # Return the predictions dictionary as a JSON response
    return output_dict

# Run the Flask application in debug mode if this script is executed directly
if __name__ == '__main__':
    product_store_sales_predictor_api.run(debug=True)
