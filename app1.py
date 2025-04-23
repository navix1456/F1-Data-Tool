import streamlit as st
import fastf1

# Example for checking available attributes
st.title("🏁 F1 Telemetry Viewer")

# Select season, race, and session
year = st.selectbox("Season", list(range(2018, 2025))[::-1])  # Show seasons from 2024 to 2018
race = st.text_input("Race (e.g., 'Monza')", "Monza")
session_type = st.selectbox("Session", ["Q", "R", "FP1", "FP2", "FP3"])

# Button to load data (only loads once)
if st.button("Load Data"):
    try:
        with st.spinner('Loading data...'):
            session = fastf1.get_session(year, race, session_type)
            session.load()

        # Debug: Check session attributes
        st.write("Session Attributes:")
        st.write(dir(session))  # List all attributes of session to check if weather exists

        # Try to print weather data if available
        if hasattr(session, 'weather'):
            st.write("Weather Data:")
            st.write(session.weather)
        else:
            st.write("Weather data is not available for this session.")

    except Exception as e:
        st.error(f"Error loading session: {str(e)}")
