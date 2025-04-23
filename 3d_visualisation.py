import sys
import random
import time
import threading
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

# ---------------- Simulation Settings ----------------
duration = 30
refresh_rate = 1
safe_ttc_threshold = 2.0
collision_distance = 2.0

obstacles = []
vehicle_z = 0
braking_triggered = False
collision_detected = False
current_ttc = 0
current_speed = 0
current_distance = 0

# ---------------- HUD Visibility Flags ----------------
show_speed = True
show_ttc = True
show_distance = True

# ---------------- Kalman Filter ----------------
class KalmanFilter1D:
    def __init__(self, process_variance, measurement_variance):
        self.x = 0.0
        self.P = 1.0
        self.Q = process_variance
        self.R = measurement_variance

    def update(self, measurement):
        self.P += self.Q
        K = self.P / (self.P + self.R)
        self.x += K * (measurement - self.x)
        self.P *= (1 - K)
        return self.x

# ---------------- 3D Setup ----------------
def setup_3d():
    glEnable(GL_DEPTH_TEST)
    glClearColor(0.05, 0.05, 0.05, 1.0)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(60, 1.33, 0.1, 100.0)
    glMatrixMode(GL_MODELVIEW)

# ---------------- Draw Elements ----------------
def draw_road():
    glPushMatrix()
    glColor3f(0.2, 0.2, 0.2)
    glBegin(GL_QUADS)
    glVertex3f(-4, -0.76, 50)
    glVertex3f(4, -0.76, 50)
    glVertex3f(4, -0.76, -100)
    glVertex3f(-4, -0.76, -100)
    glEnd()
    glPopMatrix()

def draw_vehicle():
    glPushMatrix()
    glTranslatef(0, 0, vehicle_z)
    glColor3f(1.0, 0.0, 0.0)
    glutSolidCube(1.5)
    glPopMatrix()

def draw_obstacles():
    for obs in obstacles:
        glPushMatrix()
        glTranslatef(obs['x'], 0, obs['z'])
        glColor3f(0.0, 1.0, 0.0)
        glutSolidSphere(0.8, 20, 20)
        glPopMatrix()

def draw_lidar_range():
    glPushMatrix()
    glColor3f(0.6, 0.6, 0.6)
    glTranslatef(0, 0, vehicle_z)
    glutWireSphere(5, 12, 12)
    glPopMatrix()

def draw_text(x, y, text, size=GLUT_BITMAP_HELVETICA_18, color=(1, 1, 1)):
    glColor3f(*color)
    glRasterPos2f(x, y)
    for ch in text:
        glutBitmapCharacter(size, ord(ch))

def draw_dashboard():
    glMatrixMode(GL_PROJECTION)
    glPushMatrix()
    glLoadIdentity()
    gluOrtho2D(0, 800, 0, 600)
    glMatrixMode(GL_MODELVIEW)
    glPushMatrix()
    glLoadIdentity()

    # Show Speed
    if show_speed:
        draw_text(20, 550, f"Speed: {current_speed:.1f} m/s", color=(0.6, 1, 1))
    # Show TTC
    if show_ttc:
        draw_text(20, 520, f"TTC: {current_ttc:.2f} s", color=(1, 1, 0))
    # Show Obstacle Distance
    if show_distance:
        draw_text(20, 490, f"Obstacle Distance: {current_distance:.2f} m", color=(1, 0.5, 0.5))
    # Show BRAKING alert
    if braking_triggered:
        draw_text(350, 550, "BRAKING", color=(1, 0, 0))

    glPopMatrix()
    glMatrixMode(GL_PROJECTION)
    glPopMatrix()
    glMatrixMode(GL_MODELVIEW)

# ---------------- Visualization ----------------
def visualizer():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()

    # Top-side view
    gluLookAt(10, 12, 20, 0, 0, 0, 0, 1, 0)

    draw_road()
    draw_vehicle()
    draw_obstacles()
    draw_lidar_range()
    draw_dashboard()

    glutSwapBuffers()

# ---------------- Simulation Logic ----------------
def run_simulation():
    global obstacles, braking_triggered, collision_detected
    global current_ttc, current_speed, current_distance
    kf_lidar = KalmanFilter1D(2.0, 10.0)
    kf_radar = KalmanFilter1D(1.0, 5.0)

    # Initialize obstacles
    for _ in range(3):
        obstacles.append({'x': random.uniform(-2, 2), 'z': -random.uniform(10, 25)})

    start_time = time.time()
    while time.time() - start_time < duration:
        braking_triggered = False
        collision_detected = False

        for obs in obstacles:
            obs['z'] += 0.5
            if obs['z'] > 5:
                obs['z'] = -random.uniform(10, 25)
                obs['x'] = random.uniform(-2, 2)

        nearest = min(obstacles, key=lambda o: o['z'])
        distance = abs(nearest['z'])

        # Collision Detection
        if distance < collision_distance:
            collision_detected = True
            print(f"[{time.time() - start_time:.1f}s] 🚨 COLLISION DETECTED at {distance:.2f}m!")
            time.sleep(1.0 / refresh_rate)
            continue

        gps_speed = random.uniform(10, 30)
        radar = kf_radar.update(random.uniform(5, 25) + random.gauss(0, 3))
        lidar = kf_lidar.update(distance + random.gauss(0, 2))
        relative_speed = max(gps_speed - radar, 0.1)
        ttc = lidar / relative_speed

        current_ttc = ttc
        current_speed = gps_speed
        current_distance = distance

        if ttc < safe_ttc_threshold:
            braking_triggered = True
            print(f"[{time.time() - start_time:.1f}s] ⚠️ BRAKE! TTC: {ttc:.2f}s")
        else:
            print(f"[{time.time() - start_time:.1f}s] TTC: {ttc:.2f}s - Safe")

        time.sleep(1.0 / refresh_rate)

# ---------------- Keyboard Controls ----------------
def keyboard_controls(key, x, y):
    global show_speed, show_ttc, show_distance
    if key == b's':  # Toggle Speed
        show_speed = not show_speed
    elif key == b't':  # Toggle TTC
        show_ttc = not show_ttc
    elif key == b'd':  # Toggle Obstacle Distance
        show_distance = not show_distance
    glutPostRedisplay()

# ---------------- Main Function ----------------
def main():
    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
    glutInitWindowSize(800, 600)
    glutCreateWindow(b"3D Safety Simulation with Dashboard HUD")

    setup_3d()
    glutDisplayFunc(visualizer)
    glutIdleFunc(visualizer)
    glutKeyboardFunc(keyboard_controls)  # Register keyboard callback

    threading.Thread(target=run_simulation).start()
    glutMainLoop()

if __name__ == "__main__":
    main()
