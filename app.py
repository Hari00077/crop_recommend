import streamlit as st
import pickle
import numpy as np

# Load the model and data
model2 = pickle.load(open("cmodel.pkl", "rb"))
acrops = pickle.load(open("crops.pkl", "rb"))
district_li = acrops["district"]

# Streamlit title
st.title("Crop Recommendations")

# Define mappings
soil_types = {"loamy": 2, "sandyloamy": 4, "sandy": 3, "clay": 1, "alluvial": 0}
states = {"Uttar Pradesh": 10, "Madhya Pradesh": 5, "Maharashtra": 8, "Rajasthan": 6, "Bihar": 9, "Karnataka": 1, "Tamil Nadu": 4, "Gujarat": 2, "Haryana": 3, "Punjab": 7, "West Bengal": 11, "Andhra Pradesh": 0}
districts = {
    # District mappings
}

# State selection
state = st.selectbox("Select the state", list(states.keys()))

# Filter districts based on the selected state
filtered_df = acrops[acrops['state'] == state]
districts_ = filtered_df["district"].unique()  # Ensure unique districts are shown

# District selection
district = st.selectbox("Select the district", districts_)

# Input fields
soil_type = st.selectbox("Select Soil Type", list(soil_types.keys()))
temp = st.text_input("Enter Temperature:")
humidity = st.text_input("Enter Humidity:")
rainfall = st.text_input("Enter Rainfall in mm:")

# Recommendation button
if st.button("Recommend Crop"):
    if state and district and soil_type and temp and humidity and rainfall:
        try:
            # Convert inputs to float
            state_value = states[state]
            district_value = districts.get(district, None)  # Use .get() to avoid KeyError if district is not found
            soil_type_value = soil_types[soil_type]
            temp = float(temp)
            humidity = float(humidity)
            rainfall = float(rainfall)

            # Mapping of crop types to values
            crop_mapping = {
                'rice': 20, 'maize': 11, 'chickpea': 3, 'kidneybeans': 9, 'pigeonpeas': 18, 'mothbeans': 13,
                'mungbean': 14, 'blackgram': 2, 'lentil': 10, 'pomegranate': 19, 'banana': 1, 'mango': 12,
                'grapes': 7, 'watermelon': 21, 'muskmelon': 15, 'apple': 0, 'orange': 16, 'papaya': 17,
                'coconut': 4, 'cotton': 6, 'jute': 8, 'coffee': 5
            }

            # Reshape the input into a 2D array
            input_data = np.array([state_value, district_value, soil_type_value, temp, humidity, rainfall]).reshape(1, -1)

            # Make predictions
            result = model2.predict(input_data)[0]

            def get_key(val):
                for key, value in crop_mapping.items():
                    if value == val:
                        return key
                return "Key not found"

            ans = get_key(result)
            st.write("Recommended crop is:", ans)

        except ValueError:
            st.write("Please enter valid numerical values for all inputs.")
    else:
        st.write("Please fill in all the input fields.")
