# session_loader.py

import fastf1
from fastf1 import plotting
import matplotlib.pyplot as plt

# Enable cache to avoid re-downloading every time
fastf1.Cache.enable_cache('cache')  # FastF1 will create this folder automatically

# Load the session
session = fastf1.get_session(2024, 'Monza', 'Q')  # You can change this to any race/session
session.load()

# Pick a driver's fastest lap
laps = session.laps.pick_driver('VER')  # VER = Max Verstappen
fastest_lap = laps.pick_fastest()

# Get telemetry for that lap
car_data = fastest_lap.get_car_data().add_distance()

# Plot speed over distance
plt.plot(car_data['Distance'], car_data['Speed'], color='red')
plt.title("Speed vs Distance – Verstappen (Fastest Lap)")
plt.xlabel("Distance (m)")
plt.ylabel("Speed (km/h)")
plt.grid(True)
plt.show()
