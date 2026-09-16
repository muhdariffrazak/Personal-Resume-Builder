<!-- Generated from data/*.yaml by scripts/render_docs.py — edit the YAML, not this file. -->

# Projects

## Capstone (MET4004) — Acoustic Noise Reduction for Drones
*Project Lead — Software & Electronics | KLASS | Aug 2026 – Apr 2027*

- Leading a 3-person team to deliver a proof-of-concept indoor drone for industry sponsor KLASS, targeting a 78 dBA ceiling at a 1 m reference during steady hover, 10-minute hover endurance, and a 370 mm square airframe envelope.
- Owning the software and electronics workstream, selecting a low-noise propulsion stack of 5-inch injection-molded toroidal propellers, custom ducts with acoustic lining and serrated trailing edges, 1300 KV low-RPM motors, and AM32 ESC PWM frequency tuning to shift tonal whine into less perceptible bands.
- Specified the avionics and power architecture (Holybro Pixhawk 6C Mini, PM02 V2 power module, dedicated 150 A power distribution board), yielding a derated 3.3:1 thrust-to-weight ratio at 1,200 g all-up weight for stable station-keeping in GPS-denied indoor flight.
- Designed the acoustic validation campaign to the Von Karman Institute four-microphone methodology with TU Berlin distance normalization to a 1 m reference, enabling direct benchmarking against HKUST's 90.52 dBA commercial quadcopter baseline and VKI's DJI Phantom 3 SE measurements.
- Specified psychoacoustic post-processing in Python (MoSQITo) under both Zwicker (ISO 532-1) and Moore–Glasberg (ISO 532-2) loudness standards, quantifying perceived annoyance beyond raw sound-pressure level.

## Autonomous Trolley Collection Robot

- Developed an autonomous robot for collecting stray trolleys on an STM32F7 microcontroller running an RTOS, implementing concurrent tasks for obstacle detection and joystick control over a custom serial communication protocol.

## Custom 3D Printer Development

- Built a custom 3D printer from off-the-shelf modules, developing custom firmware in C++ (Marlin) and tuning it for print reliability and dimensional accuracy.

## AI-Generated Video & Audio Forensics Benchmarking
*Sep 2025 – Aug 2026*

- Reproduced and benchmarked state-of-the-art AI-generated video and audio detectors (NSG-VD, D3, ReStraV, SpeechForensics) on SLURM-based HPC, achieving 90.03 AUROC on the NSG-VD replication.
- Integrated optical flow (RAFT), segmentation (SAM 2), and point-tracking (CoTracker) algorithms to analyze physical motion derivatives in video sequences for mission-critical data.
- Evaluated audio-visual synchronization as a deepfake detection signal, selecting a ~0.3 operating threshold through ROC analysis.

**Source:** pulled from [Machine Learning & Fullstack Engineer (Intern), KLASS Engineering and Solutions](experience.md#machine-learning-fullstack-engineer-intern-klass-engineering-and-solutions)

## Synthetic Multimodal Deepfake Dataset Pipeline
*Sep 2025 – Aug 2026*

- Engineered a data generation pipeline chaining video extension (Wan2.2), voice cloning (Chatterbox), and lip-synchronization (LatentSync) models to curate a balanced 1,200-video benchmark dataset.

**Source:** pulled from [Machine Learning & Fullstack Engineer (Intern), KLASS Engineering and Solutions](experience.md#machine-learning-fullstack-engineer-intern-klass-engineering-and-solutions)

## Multi-Model AI Endpoint Platform
*Sep 2025 – Aug 2026*

- Built React frontend components and FastAPI backend services with WebSockets for real-time streaming responses, deploying multi-model AI endpoints for an internal AI chatbot platform.
- Managed GPU-accelerated experimentation on shared SLURM clusters (NVIDIA H200 nodes) via Docker containers, running sanity-check protocols on custom validation splits before committing cluster time to full-scale benchmarking runs.

**Source:** pulled from [Machine Learning & Fullstack Engineer (Intern), KLASS Engineering and Solutions](experience.md#machine-learning-fullstack-engineer-intern-klass-engineering-and-solutions)

## Stair-Climbing Robot Fall-Risk Prediction (LSTM)
*Aug 2022 – May 2024*

- Built a predictive safety model to detect a stair-climbing robot's fall risk, deploying Long Short-Term Memory networks (LSTMs) over sensor time-series data.

**Source:** pulled from [Research Assistant (Full Time / Volunteer), SUTD – ROAR Lab](experience.md#research-assistant-full-time-volunteer-sutd-roar-lab)

## Panthera Autonomous Vehicle — Intelligent Lighting System
*Aug 2022 – May 2024*

- Led the design of the full intelligent lighting control system for Panthera, an autonomous vehicle developed under National Robotics Programme funding, implementing it as a rosserial node on an Arduino that subscribed to cmd_vel, IMU, and vehicle-state topics under an RTOS to drive turn, warning, and hazard signaling; the platform passed T1 autonomous testing at CETRAN.

**Source:** pulled from [Research Assistant (Full Time / Volunteer), SUTD – ROAR Lab](experience.md#research-assistant-full-time-volunteer-sutd-roar-lab)

## Experimental Thermal Chamber for Embodied AI Testing
*Aug 2024 – May 2025*

- Designed and built an experimental temperature chamber simulating human body heat signatures and extreme physical environments for faculty-led embodied AI and robotics hardware testing.
- Engineered a closed-loop, thermistor-based IoT control system to hold chamber temperature at setpoint, enabling high-fidelity data collection.

**Source:** pulled from [Student Research Engineer, Singapore Institute of Technology (SIT)](experience.md#student-research-engineer-singapore-institute-of-technology-sit)
