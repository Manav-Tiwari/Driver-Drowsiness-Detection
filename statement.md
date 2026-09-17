# Problem Statement

## Title
Edge-Based Driver Drowsiness & Distraction Alert System

## Overview
Driver fatigue and distraction are among the leading causes of fatal traffic accidents worldwide. Many existing drowsiness detection systems require high-end computational hardware or cloud connectivity to process deep learning models, making them unsuitable for embedded environments or edge devices typically found in vehicles.

This project addresses the need for a **lightweight, offline, and real-time** drowsiness and distraction detection system. By leveraging geometric analysis of facial landmarks (via Google's MediaPipe), the system calculates specific metrics (Eye Aspect Ratio, Mouth Aspect Ratio, and Head Pose) to infer driver fatigue and attention levels, alerting them before micro-sleep occurs.

## Scope
The scope of this project is to develop a Python-based software application that:
1. Captures live video feed from a standard webcam.
2. Extracts 468 3D facial landmarks in real-time.
3. Computes EAR (Eye Aspect Ratio), MAR (Mouth Aspect Ratio), and PnP-based head pose (pitch/yaw/roll).
4. Evaluates these metrics over time-windows (temporal smoothing) to trigger audio alerts when drowsiness, yawning, or distraction is detected.
5. Logs all incident metadata to a local SQLite database for post-trip reporting.

## Target Audience
- **Everyday Commuters and Commercial Drivers**: Individuals looking for an accessible, low-cost safety enhancement using standard in-cabin cameras or dashcams.
- **Fleet Management Companies**: Organizations requiring offline driver monitoring solutions that log incidents (via SQLite) without transmitting sensitive live video streams to the cloud.

## High-Level Features
- **Real-Time Inference**: Achieves $> 15$ FPS on standard CPU hardware by avoiding heavy convolutional neural networks.
- **Drowsiness & Blink Detection**: Alerts if eyes remain closed (EAR $< 0.25$) for longer than a specified duration ($2.5$s).
- **Yawn Detection**: Detects early signs of fatigue by tracking mouth aspect ratio.
- **Distraction Tracking**: Computes head orientation (PnP) to detect if the driver is looking away from the road for extended periods.
- **Incident Logging**: Maintains an offline SQLite database tracking the timestamps and severity of each event.
