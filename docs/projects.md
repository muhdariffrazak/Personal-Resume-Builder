<!-- Generated from data/*.yaml by scripts/render_docs.py — edit the YAML, not this file. -->

# Projects

## Capstone (MET4004) — Acoustic Noise Reduction for Drones
*Project Lead, Software & Electronics | Sponsored by KLASS | Aug 2026 – Apr 2027*

- Leading a 3-person team to deliver a proof-of-concept quiet indoor drone for end user MHA to reduce acoustic detectability, targeting a 78 dBA ceiling at a 1 m reference during steady hover, 10-minute hover endurance, and a 370 mm square airframe envelope, with the project proposal approved.
- Owning the software and electronics workstream, selecting a low-noise propulsion stack of 5-inch injection-molded toroidal propellers, custom ducts with acoustic lining and serrated trailing edges, 1300 KV low-RPM motors, and AM32 ESC PWM frequency tuning to shift tonal whine into less perceptible bands.
- Specified the avionics and power architecture (Holybro Pixhawk 6C Mini, PM02 V2 power module, dedicated 150 A power distribution board), yielding a derated 3.3:1 thrust-to-weight ratio at 1,200 g all-up weight to preserve control headroom for manually piloted indoor flight.
- Designed the acoustic validation plan to the Von Karman Institute four-microphone methodology with TU Berlin distance normalization to a 1 m reference, to benchmark directly against HKUST's 90.52 dBA commercial quadcopter baseline and VKI's DJI Phantom 3 SE measurements.
- Specified psychoacoustic post-processing in Python (MoSQITo) under both Zwicker (ISO 532-1) and Moore–Glasberg (ISO 532-2) loudness standards to quantify perceived annoyance beyond raw sound-pressure level.

## Autonomous Airport Trolley Return Robot (SIT–DigiPen Coursework)
*Firmware & Perception*

- Built LiDAR-based perception in C++ and ROS for a robot that autonomously returns airport trolleys, developing and integrating obstacle detection, SLAM mapping, and localization with IMU and wheel-odometry sensor fusion on an onboard computer, completing the final demo task.
- Developed RTOS firmware on an STM32F7 microcontroller with concurrent tasks for obstacle detection and joystick control, and a custom serial protocol linking it to ROS for reliable motor control.

## Custom 3D Printer Development
*2019*

- Built a custom 3D printer from off-the-shelf modules as a personal project, extending Marlin firmware in C++ with auto bed levelling and filament runout detection, improving first-layer adhesion and print quality and reducing failed prints.

## AI-Generated Video & Audio Forensics Benchmarking
*Sep 2025 – Aug 2026*

- Reproduced and benchmarked state-of-the-art AI-generated video and audio detectors (NSG-VD, D3, ReStraV, SpeechForensics) on SLURM-based HPC to assess detection capability against AI-generated media as a public-safety threat, achieving 90.03 AUROC on the NSG-VD replication.
- Ran ablation studies integrating optical flow (RAFT), segmentation (SAM 2), and point tracking (CoTracker) to test whether physical-motion signals in video sequences can distinguish AI-generated content, finding mixed evidence of a usable signal.
- Evaluated audio-visual synchronization as a deepfake detection signal, selecting a ~0.3 operating threshold through ROC analysis.

**Source:** pulled from [Machine Learning & Fullstack Engineer (Intern), KLASS Engineering and Solutions](experience.md#machine-learning-fullstack-engineer-intern-klass-engineering-and-solutions)

## Synthetic Multimodal Deepfake Dataset Pipeline
*Sep 2025 – Aug 2026*

- Engineered a data generation pipeline chaining video extension (Wan2.2), voice cloning (Chatterbox), and lip-sync (LatentSync) models to curate a balanced 1,200-video real/fake dataset, used to compare all four detectors consistently and to test models at small scale before committing larger compute.

**Source:** pulled from [Machine Learning & Fullstack Engineer (Intern), KLASS Engineering and Solutions](experience.md#machine-learning-fullstack-engineer-intern-klass-engineering-and-solutions)

## Multi-Model AI Endpoint Platform
*Sep 2025 – Aug 2026*

- Built React frontend components and FastAPI backend services with WebSockets for real-time streaming responses, deploying multi-model AI endpoints for a company-wide internal AI chatbot platform that gave staff a secure alternative to public AI tools, with search across internal documents.
- Managed GPU-accelerated experimentation on shared SLURM clusters (NVIDIA H200 nodes) via Docker containers, running sanity-check protocols on custom validation splits that caught pipeline errors before committing to training and synthetic-deepfake generation runs of up to 5 hours each.

**Source:** pulled from [Machine Learning & Fullstack Engineer (Intern), KLASS Engineering and Solutions](experience.md#machine-learning-fullstack-engineer-intern-klass-engineering-and-solutions)

## Stair-Climbing Robot Fall-Risk Prediction (LSTM)
*Aug 2022 – May 2024*

- Explored predictive safety for a stair-climbing robot by training and evaluating Long Short-Term Memory (LSTM) networks on its sensor time-series data, showing that fall risk could be predicted.

**Source:** pulled from [Research Assistant, SUTD – ROAR Lab](experience.md#research-assistant-sutd-roar-lab)

## Panthera Autonomous Vehicle — Intelligent Lighting System
*Aug 2022 – May 2024*

- Led the design of Panthera's intelligent lighting control system to signal the autonomous vehicle's intent to pedestrians and meet testing safety requirements, running a rosserial node on an Arduino under an RTOS that mapped cmd_vel, IMU, and vehicle-state topics to turn, warning, and hazard signals; the platform passed T1 autonomous testing at CETRAN.

**Source:** pulled from [Research Assistant, SUTD – ROAR Lab](experience.md#research-assistant-sutd-roar-lab)

## Body-Temperature Test Chamber for Food Chewing Research
*Aug 2024 – May 2025*

- Designed and built a temperature-controlled enclosure around a compression testing machine for faculty research on how foods behave during chewing, defining the electrical architecture and selecting components before handing the completed chamber over to the research team.
- Engineered closed-loop temperature control with a thermistor and standalone temperature controller, holding the chamber within ±2 °C of a 37 °C body-temperature setpoint for consistent test conditions.

**Source:** pulled from [Student Research Engineer, Singapore Institute of Technology (SIT)](experience.md#student-research-engineer-singapore-institute-of-technology-sit)
