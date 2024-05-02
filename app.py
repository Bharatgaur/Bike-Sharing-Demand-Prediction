import streamlit as st
import joblib
import numpy as np

# Load the trained model
model = joblib.load('xgboost_bike_demand_model.joblib')

# Define the input features
input_features = ['Seasons', 'Month', 'Day', 'Hour', 'Holiday', 'Functioning Day', 
                  'Temperature(°C)', 'Wind speed (m/s)', 'Visibility (10m)', 
                  'Solar Radiation (MJ/m2)', 'Rainfall(mm)', 'Snowfall (cm)']

# Define the limits for each feature based on the dataset description
feature_limits = {
    'Seasons': (1, 4),
    'Month': (1, 12),
    'Day': (1, 31),
    'Hour': (0, 23),
    'Holiday': (0, 1),
    'Functioning Day': (0, 1),
    'Temperature(°C)': (-17.8, 39.4),
    'Wind speed (m/s)': (0, 1.686399),
    'Visibility (10m)': (1, 44.429720),
    'Solar Radiation (MJ/m2)': (0, 1.201470),
    'Rainfall(mm)': (0, 3.583519),
    'Snowfall (cm)': (0, 2.282382),
}

# Season options
season_options = {
    1: "Spring",
    2: "Summer",
    3: "Autumn",
    4: "Winter"
}

# Month options
month_options = {
    1: "January",
    2: "February",
    3: "March",
    4: "April",
    5: "May",
    6: "June",
    7: "July",
    8: "August",
    9: "September",
    10: "October",
    11: "November",
    12: "December"
}

# Render the Streamlit app
def main():
    st.title('Bike Sharing Demand Prediction')
    st.write('This app predicts the demand for bike sharing based on various features.')

    # Collect user input
    features = {}
    for feature in input_features:
        min_val, max_val = feature_limits[feature]
        if feature == 'Seasons':
            features[feature] = st.selectbox(f'Select {feature}', options=list(season_options.values()))
        elif feature == 'Month':
            selected_month = st.selectbox(f'Select {feature}', options=list(month_options.values()))
            features[feature] = list(month_options.keys())[list(month_options.values()).index(selected_month)]
        else:
            features[feature] = st.number_input(f'Enter {feature} ({min_val} to {max_val})', min_value=float(min_val), max_value=float(max_val), value=float(min_val))

    # Validate user input
    valid_input = True
    for feature, value in features.items():
        min_val, max_val = feature_limits[feature]
        if feature != 'Seasons' and feature != 'Month':
            if not (float(min_val) <= float(value) <= float(max_val)):
                st.error(f'Invalid input for {feature}. Please enter a value between {min_val} and {max_val}.')
                valid_input = False
                break

    # Predict the demand if input is valid
    if valid_input and st.button('Predict Demand'):
        # Convert seasons back to numerical values
        features['Seasons'] = list(season_options.keys())[list(season_options.values()).index(features['Seasons'])]
        input_data = np.array([list(features.values())])
        prediction = model.predict(input_data)
        st.write(f'Predicted demand: {prediction[0]}')

if __name__ == '__main__':
    main()



