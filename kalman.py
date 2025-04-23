import random
import time
import matplotlib.pyplot as plt

# ---------------- Kalman Filter Class ----------------
class KalmanFilter1D:
    def __init__(self, process_variance, measurement_variance):
        self.x = 0.0  # initial estimate
        self.P = 1.0  # initial estimate uncertainty
        self.Q = process_variance  # process (model) noise
        self.R = measurement_variance  # measurement noise

    def update(self, measurement):
        # Prediction update
        self.P += self.Q

        # Measurement update
        K = self.P / (self.P + self.R)
        self.x += K * (measurement - self.x)
        self.P *= (1 - K)
        return self.x

# ---------------- Simulation Setup ----------------
duration = 30  # seconds
refresh_rate = 1  # Hz
safe_ttc_threshold = 2.0  # seconds

timestamps = []
ttcs = []
brake_flags = []

# Kalman filters for LiDAR and Radar
kf_lidar = KalmanFilter1D(process_variance=2.0, measurement_variance=10.0)
kf_radar = KalmanFilter1D(process_variance=1.0, measurement_variance=5.0)

# Plot Setup
plt.ion()
fig, ax = plt.subplots()
line1, = ax.plot([], [], label='TTC (sec)')
line2, = ax.plot([], [], label='Braking Triggered')
ax.set_ylim(0, 10)
ax.set_xlabel('Time (s)')
ax.set_ylabel('TTC / Braking')
ax.legend()
plt.title("Real-Time TTC with Kalman Filtering")

start_time = time.time()

while time.time() - start_time < duration:
    current_time = time.time() - start_time

    # Simulated noisy sensor inputs
    lidar_true = random.uniform(5.0, 50.0)
    radar_true = random.uniform(5.0, 25.0)
    gps_speed = random.uniform(10.0, 30.0)

    # Add random noise
    lidar_noisy = lidar_true + random.gauss(0, 5.0)
    radar_noisy = radar_true + random.gauss(0, 3.0)

    # Filter noisy values
    lidar_filtered = kf_lidar.update(lidar_noisy)
    radar_filtered = kf_radar.update(radar_noisy)

    # Relative speed
    relative_speed = max(gps_speed - radar_filtered, 0.1)
    ttc = lidar_filtered / relative_speed

    # Braking logic
    should_brake = 1 if ttc < safe_ttc_threshold else 0

    # Store for graph
    timestamps.append(current_time)
    ttcs.append(ttc)
    brake_flags.append(should_brake)

    # Plot update
    line1.set_xdata(timestamps)
    line1.set_ydata(ttcs)
    line2.set_xdata(timestamps)
    line2.set_ydata(brake_flags)
    ax.relim()
    ax.autoscale_view()
    plt.pause(0.05)

    print(f"[{current_time:.1f}s] Lidar(raw): {lidar_noisy:.1f} | Radar(raw): {radar_noisy:.1f} | Lidar(filtered): {lidar_filtered:.1f} | Radar(filtered): {radar_filtered:.1f} | TTC: {ttc:.2f} | BRAKE: {'YES' if should_brake else 'NO'}")

    time.sleep(1.0 / refresh_rate)

plt.ioff()
plt.show()
