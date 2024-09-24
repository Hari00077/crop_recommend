from flask import Flask, render_template, request
import pickle
import numpy as np

app = Flask(__name__)

# Load the model and data
model2 = pickle.load(open("cmodel.pkl", "rb"))
acrops = pickle.load(open("crops.pkl", "rb"))
district_li = acrops["district"]

# Define mappings
soil_types = {"loamy": 2, "sandyloamy": 4, "sandy": 3, "clay": 1, "alluvial": 0}
states = {"Uttar Pradesh": 10, "Madhya Pradesh": 5, "Maharashtra": 8, "Rajasthan": 6, "Bihar": 9, "Karnataka": 1, "Tamil Nadu": 4, "Gujarat": 2, "Haryana": 3, "Punjab": 7, "West Bengal": 11, "Andhra Pradesh": 0}
crop_mapping = {
    'rice': 20, 'maize': 11, 'chickpea': 3, 'kidneybeans': 9, 'pigeonpeas': 18, 'mothbeans': 13,
    'mungbean': 14, 'blackgram': 2, 'lentil': 10, 'pomegranate': 19, 'banana': 1, 'mango': 12,
    'grapes': 7, 'watermelon': 21, 'muskmelon': 15, 'apple': 0, 'orange': 16, 'papaya': 17,
    'coconut': 4, 'cotton': 6, 'jute': 8, 'coffee': 5
}

@app.route('/')
def index():
    return render_template('index.html', states=states.keys(), soil_types=soil_types.keys())

@app.route('/recommend', methods=['POST'])
def recommend():
    if request.method == 'POST':
        try:
            # Get data from the form
            state = request.form['state']
            district = request.form['district']
            soil_type = request.form['soil_type']
            temp = float(request.form['temperature'])
            humidity = float(request.form['humidity'])
            rainfall = float(request.form['rainfall'])

            # Get state, district, soil type values
            state_value = states[state]
            filtered_df = acrops[acrops['state'] == state]
            district_value = filtered_df[filtered_df["district"] == district]["district_code"].values[0]
            soil_type_value = soil_types[soil_type]

            # Reshape the input into a 2D array
            input_data = np.array([state_value, district_value, soil_type_value, temp, humidity, rainfall]).reshape(1, -1)

            # Make predictions
            result = model2.predict(input_data)[0]

            # Map prediction result to crop name
            def get_key(val):
                for key, value in crop_mapping.items():
                    if value == val:
                        return key
                return "Unknown crop"

            recommended_crop = get_key(result)

            return render_template('index.html', recommended_crop=recommended_crop, states=states.keys(), soil_types=soil_types.keys())

        except ValueError:
            return render_template('index.html', error="Please enter valid numerical values.", states=states.keys(), soil_types=soil_types.keys())

if __name__ == '__main__':
    app.run(debug=True)
