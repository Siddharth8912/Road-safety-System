# Adaptive Safety System for High-Speed Driving

This project focuses on developing an adaptive safety system to minimize collision risks during high-speed driving, especially in low-visibility conditions. The system integrates Lidar, Radar, and GPS technologies to achieve real-time obstacle detection, speed monitoring, and automated safety interventions. [cite: 75, 76, 77, 130, 131]
## To Run the following code you need to add some python libraries
* **MatPlotib:**
  ```
  pip install matplotlib
  (To plot graphs for sensor data (like speed, distance, TTC) during initial simulations. It helped visualize how values change over time before moving into real-time 3D rendering).
  
  ```
* **Tkinter:** python -m pip install tk (To build a simple GUI dashboard with real-time labels and controls (like Start/Stop buttons). It was used during the early phase to display simulation outputs in a user-friendly way).
* **PyOpenGL:** pip install PyOpenGL PyOpenGL_accelerate (To create a real-time 3D simulation of the vehicle, road, obstacles, and sensor effects. It allowed us to visualize motion, collision detection, LiDAR range, and HUD overlays from different camera views).
* **
## Objectives

* **Enhance Road Safety:** Reduce collision risks in high-speed and low-visibility environments. [cite: 75]
   
* **Integrate Multi-Sensor Fusion:** Combine Lidar, Radar, and GPS for accurate obstacle detection in all weather. [cite: 76]
   
* **Enable Adaptive Safety Responses:** Implement real-time speed adjustments, alerts, and emergency interventions. [cite: 77]
   
* **Optimize Performance:** Ensure effective operation in challenging conditions like fog, rain, darkness, and high speeds. [cite: 78]

## Methodology

The research methodology includes:

1.  **Literature Review:** Analyzing existing research on Lidar and GPS integration for real-time adaptive systems. [cite: 79, 80, 81]
   
2.  **System Design and Sensor Integration:** Developing the system architecture and integrating Lidar, Radar, and GPS sensors. [cite: 82, 83, 84, 85, 86]
   
3.  **Simulation and Testing:** Testing the system under simulated high-speed and low-visibility conditions using platforms like CarSim. [cite: 87, 88, 89, 90, 91, 92]

## Improvements

The project has undergone several improvements:

* **ESP32 Integration:** Switched from Raspberry Pi to ESP32 for better real-time performance due to lower latency. [cite: 92, 93, 94]
   
* **Radar Integration:** Incorporated Radar with Lidar to enhance object detection accuracy in all weather conditions. [cite: 95, 96, 97]
   
* **Kalman and Median Filtering:** Implemented filtering to improve the accuracy of Lidar data by reducing noise. [cite: 98, 99, 100]
   
* **Automatic Emergency Braking (AEB):** Added AEB functionality using ESP32 and a relay control system to automatically trigger brakes. [cite: 101, 102, 103, 104]

## Automatic Braking System Overview

The automatic braking system works as follows:

* **Inputs:** Lidar for distance, GPS for speed and location. [cite: 105, 106]
   
* **Processing:** ESP32 calculates Time-to-Collision (TTC). [cite: 106, 107]
   
* **Output:** Relay module triggers a servo motor or brake actuator. [cite: 108, 109, 110, 111]

## Research Outcomes

The project aims to achieve:

* **Improved Detection Accuracy:** Accurate obstacle detection in low-visibility. [cite: 112, 113, 114]
   
* **Enhanced Speed Regulation:** Real-time speed monitoring for safety. [cite: 113]
   
* **Reliable Low-Visibility Performance:** Better safety than traditional systems in adverse conditions. [cite: 114]
   
* **Reduced Accident Rates:** Potential decrease in accidents and fatalities. [cite: 115]
   
* **Framework for Future Development:** Foundation for further research in vehicle safety. [cite: 116]

## References

The project references various journal publications and software:

* **Journal Publications:** \[cite: 117, 118, 119, 120, 121, 122, 123, 124, 125, 126]
   
* **Software:** \[cite: 127, 128]

## Introduction

The project addresses the problem of increased accident risks during high-speed driving, especially in low visibility. The solution is an adaptive safety system that integrates Lidar, GPS, and AI to enhance driver safety through real-time object detection, speed monitoring, and automated alerts. [cite: 128, 129, 130, 131, 132, 133]

## Motivation

The research is motivated by the need to:

* Develop a system for real-time obstacle detection and speed adjustment. [cite: 134, 135, 136]
   
* Integrate a real-time safety intervention mechanism. [cite: 135]
   
* Test the effectiveness of Lidar-GPS integration in low-visibility conditions. [cite: 136]

## Review of Literature

The literature review covers:

* **Lidar for Autonomous Vehicles:** Lidar's limitations in weather and reflective surfaces. [cite: 137, 138]
   
* **Limitations of GPS-Based Safety Systems:** GPS's inability to detect real-time obstacles. [cite: 138, 139, 140, 141]
   
* **Radar-Based Object Detection:** Radar's reliability in all weather but limitations in object classification. [cite: 142, 143, 144, 145]

## Research Gap

Existing systems have limitations:

* Lidar fails in fog, rain, and on reflective surfaces. [cite: 146, 147, 148]
   
* Radar cannot classify objects. [cite: 147]
   
* GPS lacks real-time obstacle detection. [cite: 147]

This project aims to fill the gap by creating a system that ensures accurate, real-time detection in all conditions and provides high-speed adaptability. [cite: 147, 148]
