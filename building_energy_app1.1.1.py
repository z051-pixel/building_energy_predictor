import streamlit as st
import pandas as pd
import pickle
import numpy as np

def load_model():

    with open("building_pipeline_app1.1.pkl", "rb") as f:        
        model = pickle.load(f)
    return model

pipeline = load_model()

st.title("Building Energy Prediction App")
st.write("Predict energy usage based on building and weather data")


with st.sidebar:
            
            st.subheader("Weather Information & Temperature Features")

            air_temperature = st.slider("Air Temperature (°C)", -30.0, 50.0, 25.0)
            cloud_coverage = st.slider("Cloud Coverage ( 0 to 9 scale )", 0.0, 9.0, 4.0)
            dew_temperature = st.slider("Dew Temperature (°C)", -30.0, 30.0, 10.0)
            precip_depth_1_hr = st.slider("Precipitation Depth in Millimeters (1 hr)", 0.0, 100.0, 0.0)
            sea_level_pressure = st.slider("Sea Level Pressure (Millibar/hectopascals)", 900.0, 1100.0, 1013.0)
            wind_direction = st.slider("Wind Direction ( 0 to 360° )", 0.0, 360.0, 180.0)
            wind_speed = st.slider("Wind Speed ( Meters per second )", 0.0, 50.0, 5.0)



with st.container(): 
            
            st.subheader("Building Information")

            site_id = st.number_input("Site ID", min_value=0, max_value=16, value=0, step=1)
            square_feet = st.slider("Square Feet", min_value=300, max_value=500000, value=50000, step=100)
            year_built = st.number_input("Year Built", min_value=1900, max_value=2025, value=2000, step=1)
            floor_count = st.number_input("Floor Count", min_value=1, max_value=30, value=5, step=1)

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

            month = st.selectbox(
                "Select your Preferred Month For Energy Prediction",
                ["January", "February", "March", "April", "May", "June",
                "July", "August", "September", "October", "November", "December"]
            )

            month_mapping = {
                "January": 1, "February": 2, "March": 3, "April": 4,
                "May": 5, "June": 6, "July": 7, "August": 8,
                "September": 9, "October": 10, "November": 11, "December": 12
            }
            month = month_mapping[month]


            hour_label = st.selectbox(
                "Time of Day",
                [
                    "12 AM", "1 AM", "2 AM", "3 AM", "4 AM", "5 AM",
                    "6 AM", "7 AM", "8 AM", "9 AM", "10 AM", "11 AM",
                    "12 PM", "1 PM", "2 PM", "3 PM", "4 PM", "5 PM",
                    "6 PM", "7 PM", "8 PM", "9 PM", "10 PM", "11 PM"
                ]
            )

            hour_mapping = {
                "12 AM": 0, "1 AM": 1, "2 AM": 2, "3 AM": 3, "4 AM": 4, "5 AM": 5,
                "6 AM": 6, "7 AM": 7, "8 AM": 8, "9 AM": 9, "10 AM": 10, "11 AM": 11,
                "12 PM": 12, "1 PM": 13, "2 PM": 14, "3 PM": 15, "4 PM": 16, "5 PM": 17,
                "6 PM": 18, "7 PM": 19, "8 PM": 20, "9 PM": 21, "10 PM": 22, "11 PM": 23
            }

            hour = hour_mapping[hour_label]

            active_hours = st.slider("Active Hours Energy Usage per Day ( For Monthly Energy Prediction)", 1, 24, 10)


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
    "month": [month],
    "primary_use": [primary_use]
})

if st.button("Predict Meter Reading"):
    try:
        prediction = pipeline.predict(input_data)[0]
        prediction = np.expm1(prediction)
        st.success(f"Estimated Hourly Meter Reading: **{prediction:,.2f} Kwh**")

        monthly_kwh = prediction * active_hours * 30
        st.info(f"Estimated Monthly Energy Consumption: **{monthly_kwh:,.2f} kWh**")

        cost_per_kwh = 0.15
        monthly_bill = monthly_kwh * cost_per_kwh
        st.info(f"Estimated Monthly Bill for Energy Consumption: **{monthly_bill:,.2f} US$**")

        st.markdown(f"""
         <div style="
         background-color:#e6f0fa; 
         padding:20px; 
         border-radius:10px; 
         border:1px solid #e0e0e0;
            max-width:500px;
            font-family: 'Arial', sans-serif;
            line-height:1.5;
             ">
        <h3 style="color:#0d6efd;">Monthly Energy Bill</h3>
        <p style="font-size:14px; color:#333;">
            <b>Location Site_ID:</b> {site_id}<br>
            <b>Meter Type:</b> {meter_label}<br>
            <b>Month:</b> {month}<br>
            <b>Active Hours per Day:</b> {active_hours} hrs
        </p>
        <hr style="border-top:1px solid #dee2e6;">
        <p style="font-size:14px; color:#333;">
            <b>Hourly Consumption:</b> {prediction:,.2f} kWh<br>
            <b>Monthly Consumption:</b> {monthly_kwh:,.2f} kWh<br>
            <b>Cost per kWh:</b> ${cost_per_kwh:.2f}
        </p>
        <hr style="border-top:1px solid #dee2e6;">
        <h4 style="color:#198754;">Estimated Monthly Bill: US${monthly_bill:,.2f}</h4>
    </div>
    """, unsafe_allow_html=True)
        
    except Exception as e:
        st.error(f"Prediction failed: {e}")

st.markdown("""
    <style>
    body {background-color:#f7f7f7;}
    h1,h2,h3{color:#004b87;}
    .stButton>button {background-color:#0d6efd; color:white;}
    </style>
""", unsafe_allow_html=True)

#cd "/Users/mac/Downloads/Building Energy/"
#streamlit run building_energy_app1.1.py