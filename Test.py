import random
import time
import matplotlib.pyplot as plt

# Simulation config
duration = 30  # seconds
refresh_rate = 1  # Hz (1 update/sec)
safe_ttc_threshold = 2.0  # seconds

# Data storage
timestamps = []
ttcs = []
brake_flags = []

# Real-time plotting setup
plt.ion()
fig, ax = plt.subplots()
line1, = ax.plot([], [], label='TTC (sec)')
line2, = ax.plot([], [], label='Braking Triggered')
ax.set_ylim(0, 10)
ax.set_xlabel('Time (s)')
ax.set_ylabel('TTC / Braking')
ax.legend()
plt.title("Real-Time Time-To-Collision Simulation")

start_time = time.time()

while time.time() - start_time < duration:
    current_time = time.time() - start_time

    # Simulated sensor readings
    lidar_distance = random.uniform(5.0, 50.0)  # meters
    radar_speed = random.uniform(5.0, 25.0)     # m/s (obstacle)
    gps_speed = random.uniform(10.0, 30.0)      # m/s (vehicle)

    # Relative speed calculation
    relative_speed = max(gps_speed - radar_speed, 0.1)

    # Time-To-Collision (TTC)
    ttc = lidar_distance / relative_speed

    # Braking decision
    should_brake = 1 if ttc < safe_ttc_threshold else 0

    # Store data
    timestamps.append(current_time)
    ttcs.append(ttc)
    brake_flags.append(should_brake)

    # Live plot update
    line1.set_xdata(timestamps)
    line1.set_ydata(ttcs)
    line2.set_xdata(timestamps)
    line2.set_ydata(brake_flags)
    ax.relim()
    ax.autoscale_view()
    plt.pause(0.05)

    print(f"[{current_time:.1f}s] Distance: {lidar_distance:.1f}m | GPS Speed: {gps_speed:.1f}m/s | Radar Speed: {radar_speed:.1f}m/s | TTC: {ttc:.2f}s | BRAKE: {'YES' if should_brake else 'NO'}")

    time.sleep(1.0 / refresh_rate)

plt.ioff()
plt.show()
