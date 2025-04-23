import streamlit as st
import fastf1
import matplotlib.pyplot as plt

# Enable cache for FastF1
fastf1.Cache.enable_cache('cache')

# Streamlit UI
st.title("🏁 F1 Telemetry Viewer")

# Select season, race, and session
year = st.selectbox("Season", list(range(2018, 2025))[::-1])  # Show seasons from 2024 to 2018
race = st.text_input("Race (e.g., 'Monza')", "Monza")
session_type = st.selectbox("Session", ["Q", "R", "FP1", "FP2", "FP3"])

# Initialize session state variables
if 'session' not in st.session_state:
    st.session_state.session = None  # Store the session object in session_state
if 'driver' not in st.session_state:
    st.session_state.driver = None  # Store the selected driver

# Button to load data (only loads once)
if st.button("Load Data") and st.session_state.session is None:
    try:
        with st.spinner('Loading data...'):
            # Load session only once and store it in session state
            session = fastf1.get_session(year, race, session_type)
            session.load()
            st.session_state.session = session  # Save the session in session state

        st.success(f"Session loaded: {year} - {race} - {session_type}")

    except Exception as e:
        st.error(f"Error loading session: {str(e)}")

# If session is already loaded, allow changing the driver without reloading the data
if st.session_state.session:
    try:
        # Use the already loaded session from session state
        session = st.session_state.session

        # Select driver (this will not reload the session)
        drivers = session.laps['Driver'].unique()
        driver = st.selectbox("Pick Driver", drivers, index=list(drivers).index(st.session_state.driver) if st.session_state.driver else 0)

        # Update the session state when driver is changed
        st.session_state.driver = driver

        # Filter laps for the selected driver and pick the fastest lap
        laps = session.laps.pick_driver(driver)
        
        # Debug: Check the columns of the laps dataframe
        st.write(f"Laps Data Columns: {laps.columns.tolist()}")  # This will print out the available columns

        # Plot the telemetry (Speed vs Distance)
        fastest_lap = laps.pick_fastest()
        telemetry = fastest_lap.get_car_data().add_distance()

        fig, ax = plt.subplots()
        ax.plot(telemetry['Distance'], telemetry['Speed'], color='red')
        ax.set_title(f"Speed vs Distance – {driver} (Fastest Lap)")
        ax.set_xlabel("Distance (m)")
        ax.set_ylabel("Speed (km/h)")
        ax.grid(True)
        st.pyplot(fig)  # Display the plot in Streamlit

        # Add pit stop analysis if pit stops data is available (using PitInTime and PitOutTime)
        pit_stops = laps[laps['PitInTime'].notnull() & laps['PitOutTime'].notnull()]
        if not pit_stops.empty:
            st.write(f"Pit Stops for {driver}:")
            st.dataframe(pit_stops[['LapNumber', 'PitInTime', 'PitOutTime']])  # Show pit stop times and lap number
        else:
            st.write(f"No pit stops data available for {driver} in this session.")

        # Add tyre strategy analysis
        tyre_strategy = laps[['LapNumber', 'Compound', 'Stint']].drop_duplicates()  # Include 'Stint' for detailed strategy
        tyre_strategy_summary = tyre_strategy.groupby(['Stint', 'Compound']).size().reset_index(name='Lap Count')

        st.write(f"Tyre Strategy for {driver}:")
        st.dataframe(tyre_strategy_summary)  # Show tyre compounds and stint laps during the session

    except Exception as e:
        st.error(f"Error updating data for the selected driver: {str(e)}")

