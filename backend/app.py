# Import necessary libraries
import numpy as np
import joblib  # For loading the serialized model
import pandas as pd  # For data manipulation
from flask import Flask, request, jsonify  # For creating the Flask API

# Initialize the Flask application
superkart_sale_predictor_api = Flask("Superkart Sale Predictor")

# Load the trained machine learning model
model = joblib.load("superkart_model_v1.joblib")

# Define a route for the home page (GET request)
@superkart_sale_predictor_api.get('/')
def home():
    """
    This function handles GET requests to the root URL ('/') of the API.
    It returns a simple welcome message.
    """
    return "Welcome to the Superkart Sale Prediction API!"

# Define an endpoint for single product sale (POST request)
@superkart_sale_predictor_api.post('/v1/superkart')
def predict_rental_price():
    """
    This function handles POST requests to the '/v1/superkart' endpoint.
    It expects a JSON payload containing property details and returns
    the predicted sale as a JSON response.
    """
    # Get the JSON data from the request body
    product_data = request.get_json()

    # Extract relevant features from the JSON data
    sample = {
        'Product_Weight': product_data['Product_Weight'],
        'Product_Sugar_Content': product_data['Product_Sugar_Content'],
        'Product_Allocated_Area': product_data['Product_Allocated_Area'],
        'Product_MRP': product_data['Product_MRP'],
        'Store_Size': product_data['Store_Size'],
        'Store_Location_City_Type': product_data['Store_Location_City_Type'],
        'Store_Type': product_data['Store_Type'],
        'Product_Id_char': product_data['Product_Id_char'],
        'Store_Age_Years': product_data['Store_Age_Years'],
        'Product_Type_Category': product_data['Product_Type_Category']
    }

    # Convert the extracted data into a Pandas DataFrame
    input_data = pd.DataFrame([sample])

    # Make prediction (get sale volume)
    predicted_sale = model.predict(input_data)[0]

    # Convert predicted_sale to Python float
    predicted_sale = round(float(predicted_sale), 2)

    # Return the actual price
    return jsonify({'Predicted Sale (in dollars)': predicted_sale})


# Define an endpoint for batch prediction (POST request)
@superkart_sale_predictor_api.post('/v1/superkartbatch')
def predict_rental_price_batch():
    """
    This function handles POST requests to the '/v1/superkartbatch' endpoint.
    It expects a CSV file containing product and store details for multiple products
    and returns the predicted sale as a dictionary in the JSON response.
    """
    # Get the uploaded CSV file from the request
    file = request.files['file']

    # Read the CSV file into a Pandas DataFrame
    input_data = pd.read_csv(file)

    # Make predictions
    predicted_sales = model.predict(input_data)

    # Add prediction as a new column
    input_data['Predicted_Sales'] = predicted_sales

    # Convert complete DataFrame to JSON
    output_dict = input_data.to_dict(orient='records')

    return output_dict


# Run the Flask application in debug mode if this script is executed directly
if __name__ == '__main__':
    superkart_sale_predictor_api.run(debug=True)
