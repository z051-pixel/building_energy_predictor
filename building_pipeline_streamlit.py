import streamlit as st
import pandas as pd
import pickle
from datetime import datetime

def load_model():
    with open("building_pipeline.pkl", "rb") as f:
        model = pickle.load(f)
    return model

pipeline = load_model()

st.title("Building Energy Consumption Prediction App")
st.write("Predict energy usage based on building and weather data")



st.subheader("Building Information")

site_id = st.number_input("Site ID", min_value=0, max_value=16, value=0, step=1)
square_feet = st.slider("Square Feet", min_value=500, max_value=500000, value=50000, step=100)
year_built = st.number_input("Year Built", min_value=1900, max_value=2025, value=2000, step=1)
floor_count = st.number_input("Floor Count", min_value=1, max_value=100, value=5, step=1)

meter_map = {
    "Electricity": 0,
    "Chilled Water": 1,
    "Steam": 2,
    "Hot Water": 3
}
meter_label = st.selectbox("Meter Type", list(meter_map.keys()))
meter = meter_map[meter_label]

primary_use = st.selectbox(
    "Primary Use",
    [
        "Education", "Office", "Residential", "Public services",
        "Healthcare", "Lodging/residential", "Entertainment/public assembly",
        "Retail", "Parking", "Warehouse/storage", "Food sales and service",
        "Religious worship", "Utility", "Technology/science"
    ]
)

st.subheader("Weather Information & Timestamp Features")

air_temperature = st.slider("Air Temperature (°C)", -30.0, 50.0, 25.0)
cloud_coverage = st.slider("Cloud Coverage ( 0 to 9 scale )", 0.0, 9.0, 4.0)
dew_temperature = st.slider("Dew Temperature (°C)", -30.0, 30.0, 10.0)
precip_depth_1_hr = st.slider("Precipitation Depth in Millimeters (1 hr)", 0.0, 100.0, 0.0)
sea_level_pressure = st.slider("Sea Level Pressure (Millibar/hectopascals)", 900.0, 1100.0, 1013.0)
wind_direction = st.slider("Wind Direction ( 0 to 360° )", 0.0, 360.0, 180.0)
wind_speed = st.slider("Wind Speed ( Meters per second )", 0.0, 50.0, 5.0)


now = datetime.now()
hour = now.hour
day = now.day
month = now.month
year = now.year


input_data = pd.DataFrame({
    "meter": [meter],
    "site_id": [site_id],
    "square_feet": [square_feet],
    "year_built": [year_built],
    "floor_count": [floor_count],
    "air_temperature": [air_temperature],
    "cloud_coverage": [cloud_coverage],
    "dew_temperature": [dew_temperature],
    "precip_depth_1_hr": [precip_depth_1_hr],
    "sea_level_pressure": [sea_level_pressure],
    "wind_direction": [wind_direction],
    "wind_speed": [wind_speed],
    "hour": [hour],
    "day": [day],
    "month": [month],
    "year": [year],
    "primary_use": [primary_use]
})

if st.button("Predict Meter Reading"):
    try:
        prediction = pipeline.predict(input_data)[0]
        st.success(f"Estimated Meter Reading: **{prediction:,.2f} Kwh**")
    except Exception as e:
        st.error(f"Prediction failed: {e}")


