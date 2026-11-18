<!-- Generated from data/*.yaml by scripts/render_docs.py — edit the YAML, not this file. -->

# Projects

## Capstone (MET4004): Acoustic Noise Reduction for Drones
*Project Lead, Software & Electronics | Sponsored by KLASS | Aug 2026 – Apr 2027*

- Leading a 3-person team, working from an approved proposal, to build a proof-of-concept indoor drone for end user MHA that is harder to detect by sound, targeting a 78 dBA ceiling at a 1 m reference during steady hover, 10-minute hover endurance, and a 370 mm square airframe envelope.
- Selected a low-noise propulsion stack: 5-inch injection-molded toroidal propellers, custom ducts with acoustic lining and serrated trailing edges, 1300 KV low-RPM motors, and AM32 ESC PWM frequency tuning to shift tonal whine into less perceptible bands.
- Specified the avionics and power architecture (Holybro Pixhawk 6C Mini, PM02 V2 power module, dedicated 150 A power distribution board), sized to preserve control headroom for manually piloted indoor flight.
- Planned the acoustic validation to the Von Karman Institute four-microphone methodology with TU Berlin distance normalization to a 1 m reference; the tests will benchmark against HKUST's 90.52 dBA commercial quadcopter baseline and VKI's DJI Phantom 3 SE measurements.

## Autonomous Airport Trolley Return Robot (SIT–DigiPen Coursework)
*Firmware & Perception*

- Built LiDAR-based perception in C++ and ROS for a robot that autonomously returns airport trolleys, integrating obstacle detection, SLAM mapping, and localization with IMU and wheel-odometry sensor fusion on an onboard computer; the robot completed the final demo task.
- Developed RTOS firmware on an STM32F7 microcontroller with concurrent tasks for obstacle detection and joystick control, and a custom serial protocol linking it to ROS for reliable motor control.

## Custom 3D Printer Development
*2019*

- Built a custom 3D printer from off-the-shelf modules as a personal project and extended its Marlin firmware in C++ with auto bed levelling and filament runout detection, which improved first-layer adhesion and print quality and cut failed prints.

## AI-Generated Video & Audio Forensics Benchmarking
*Sep 2025 – Aug 2026*

- Reproduced and benchmarked four state-of-the-art detectors for AI-generated video and audio (NSG-VD, D3, ReStraV, SpeechForensics) on a SLURM-based HPC cluster, treating AI-generated media as a public-safety threat, and reached 90.03 AUROC on the NSG-VD replication.
- Ran ablation studies integrating optical flow (RAFT), segmentation (SAM 2), and point tracking (CoTracker) to test whether physical-motion signals in video sequences can distinguish AI-generated content, and found mixed evidence of a usable signal.
- Evaluated audio-visual synchronization as a deepfake detection signal and selected a ~0.3 operating threshold through ROC analysis.

**Source:** pulled from [Machine Learning & Fullstack Engineer (Intern), KLASS Engineering and Solutions](experience.md#machine-learning-fullstack-engineer-intern-klass-engineering-and-solutions)

## Synthetic Multimodal Deepfake Dataset Pipeline
*Sep 2025 – Aug 2026*

- Built a data generation pipeline chaining video extension (Wan2.2), voice cloning (Chatterbox), and lip-sync (LatentSync) models to produce a balanced 1,200-video real/fake dataset, used to compare all four detectors on equal terms and to test models at small scale before committing larger compute.

**Source:** pulled from [Machine Learning & Fullstack Engineer (Intern), KLASS Engineering and Solutions](experience.md#machine-learning-fullstack-engineer-intern-klass-engineering-and-solutions)

## Multi-Model AI Endpoint Platform
*Sep 2025 – Aug 2026*

- Built React frontend components and FastAPI backend services, with WebSockets for real-time streaming responses, for a company-wide internal AI chatbot that serves multiple models and searches internal documents, giving staff a secure alternative to public AI tools.
- Ran GPU experiments on shared SLURM clusters (NVIDIA H200 nodes) in Docker containers, with sanity checks on custom validation splits that caught pipeline errors before training and synthetic-deepfake generation runs of up to 5 hours each.

**Source:** pulled from [Machine Learning & Fullstack Engineer (Intern), KLASS Engineering and Solutions](experience.md#machine-learning-fullstack-engineer-intern-klass-engineering-and-solutions)

## Stair-Climbing Robot Fall-Risk Prediction (LSTM)
*Aug 2022 – May 2024*

- Trained and evaluated Long Short-Term Memory (LSTM) networks on a stair-climbing robot's sensor time-series data, showing that its fall risk could be predicted.

**Source:** pulled from [Research Assistant (volunteer until Nov 2022, then full time), SUTD ROAR Lab](experience.md#research-assistant-volunteer-until-nov-2022-then-full-time-sutd-roar-lab)

## Panthera Autonomous Vehicle — Intelligent Lighting System
*Aug 2022 – May 2024*

- Led the design of the lighting control system that signals the Panthera autonomous vehicle's intent to pedestrians, as required for safety testing, with a rosserial node on an Arduino under an RTOS mapping cmd_vel, IMU, and vehicle-state topics to turn, warning, and hazard signals; the vehicle passed T1 autonomous testing at CETRAN.

**Source:** pulled from [Research Assistant (volunteer until Nov 2022, then full time), SUTD ROAR Lab](experience.md#research-assistant-volunteer-until-nov-2022-then-full-time-sutd-roar-lab)

## Body-Temperature Test Chamber for Food Chewing Research
*Aug 2024 – May 2025*

- Designed and built a temperature-controlled enclosure around a compression testing machine for faculty research on how foods behave during chewing, including the electrical architecture and component selection, and handed the completed chamber over to the research team.
- Engineered closed-loop temperature control with a thermistor and standalone temperature controller, holding the chamber within ±2 °C of a 37 °C body-temperature setpoint for consistent test conditions.

**Source:** pulled from [Student Research Engineer, Singapore Institute of Technology (SIT)](experience.md#student-research-engineer-singapore-institute-of-technology-sit)
