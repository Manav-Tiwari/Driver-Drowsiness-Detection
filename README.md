# Edge-Based Driver Drowsiness & Distraction Alert System

## Overview
This repository contains the source code for an edge-based, real-time Driver Drowsiness and Distraction Detection system. It uses computer vision and geometric analysis of facial landmarks to monitor a driver's state and issue audio warnings when signs of fatigue or distraction are detected.

## Features
- **Facial Landmark Extraction**: Utilizes MediaPipe Face Mesh for robust, lightweight, CPU-efficient facial tracking.
- **Drowsiness Detection**: Calculates Eye Aspect Ratio (EAR) with temporal smoothing to detect micro-sleeps.
- **Yawn Detection**: Calculates Mouth Aspect Ratio (MAR) to catch early signs of fatigue.
- **Distraction Detection**: Uses Perspective-n-Point (PnP) geometry to calculate head pitch and yaw.
- **Incident Logging**: Automatically records incidents locally into an SQLite database (`incidents.db`).
- **Cross-Platform Audio**: Uses `pygame` to issue non-blocking audio alerts.

## Tech Stack
- **Python 3.x**
- **OpenCV**: Image acquisition and PnP pose estimation.
- **MediaPipe**: Real-time facial landmark inference.
- **SciPy & NumPy**: Geometric distance calculations and array manipulations.
- **SQLite3**: Local incident logging.
- **Pygame**: Cross-platform audio alerting.
- **Pytest**: Unit testing framework.

## Project Structure (5-10 Meaningful Modules)
- `main.py`: The entry point for the application.
- `src/camera.py`: Module for image acquisition and hardware interfacing.
- `src/landmarks.py`: Module encapsulating the MediaPipe ML model.
- `src/metrics.py`: Module containing pure geometric logic (EAR, MAR, PnP).
- `src/evaluator.py`: Module managing the state machine and temporal smoothing triggers.
- `src/logger.py`: Module interfacing with the SQLite database.
- `src/alerter.py`: Module for threaded audio alerts.
- `src/config.py`: Centralized configuration and thresholds.

## NFRs & Evaluation Metrics
- **Real-Time Latency**: The system is designed to run $> 15$ FPS on a standard laptop CPU.
- **Reliability/Error Handling**: Gracefully handles lost tracking (face occlusions) without crashing.
- **Resource Efficiency**: Proper teardown of OpenCV capture objects and Pygame mixer to prevent memory leaks.
- **Model Selection**: MediaPipe Face Mesh was chosen over Dlib because it leverages BlazeFace, an architecture optimized specifically for mobile/edge CPUs.

## Setup & Run Commands

### 1. Install Dependencies
Ensure you have Python 3.8+ installed. 
Run the following command to install the required libraries:
```bash
pip install -r requirements.txt
```

### 2. Run the Application
Execute the main script to start the webcam feed and monitoring system:
```bash
python main.py
```
*(Press 'q' inside the video window to quit)*

### 3. Testing Instructions
Unit tests are provided for the metric computations and the state evaluator logic.
Run the tests using `pytest`:
```bash
pytest tests/
```
