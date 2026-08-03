# MATE ROV 2026 — Competition Software & Telemetry Suite

Software, embedded control firmware, computer vision pipelines, and CAD generation tools built for the **MATE ROV 2026 Competition** (Ranger Class).

> **Note:** For educational and competition evaluation purposes.

---

## Overview

This repository houses the full software stack supporting mission tasks across robotics control, computer vision, photogrammetry, and telemetry:

- **Task 1.2 — Coral Garden Measurement & CAD Modeling:** Sub-pixel photogrammetric measurement tool to calculate unknown pipe dimensions from underwater optical reference frames, alongside parametric OpenSCAD/STL generator scripts for structural reproduction.
- **Task 4.2 — Invasive Species Detection:** Custom YOLOv8 pipeline for identifying European Green Crabs with single-image inference and real-time live camera streams (Metal Performance Shaders / CUDA / CPU compatible).
- **Vehicle Control Firmware (`code.ino`):** ESP32 flight controller software implementing a 6-thruster holonomic drive vector mixer from 4-channel RC PWM inputs with interrupt-driven pulse width timing.
- **Autonomous Profiling Float Firmware (`buoy_30sechold.ino`):** Dual-cycle depth profiling buoy running MS5837 pressure sensor feedback via I2C, staged thruster depth-hold state machine, and Bluetooth telemetry streaming.
- **Ranger Class Mission Scorer (`mate_scorer.html`):** Standalone zero-dependency HTML5/CSS/JS mission score tracking and penalty calculation cockpit.
- **3D Printable Components (`3D MODELS/`):** Production STLs for thruster propeller guards, vertical supports, and camera mounts.

---

## Repository Structure

```
├── 3D MODELS/              # Production ROV STL models (thruster guards, mounts)
├── assets/
│   ├── cad/                # OpenSCAD source scripts and CAD references
│   ├── crab_detection/     # Training dataset, data.yaml, and trained model weights (best.pt)
│   ├── images/             # High-resolution underwater camera test captures
│   └── stl/                # Reference coral garden and frame STLs
├── buoy_30sechold.ino      # ESP32 autonomous profiling float firmware
├── code.ino                # ESP32 6-thruster vector mixer firmware
├── docs/                   # Detailed subsystem documentation
│   ├── hardware-and-firmware.md  # Thruster mapping, pinouts, and float state machine
│   ├── vision-and-cv.md          # YOLOv8 pipeline and photogrammetric measurement
│   └── cad-and-mechanics.md      # Parametric models and 3D printable parts
├── mate_scorer.html        # Interactive MATE Ranger Class mission scoring tool
├── README.md               # Repository entry point
└── src/
    ├── main.py             # Interactive CLI launcher
    ├── crab_detection/     # YOLOv8 training and inference scripts
    └── pipe_measurement/   # Photogrammetry and parametric OpenSCAD scripts
```

---

## Quickstart

### Prerequisites

- Python 3.9+
- [OpenSCAD](https://openscad.org/) (optional, required only for parametric STL compilation)
- Arduino IDE or CLI with `esp32` board definitions and `ESP32Servo`, `MS5837` libraries

### Environment Setup

```bash
# Clone the repository
git clone https://github.com/BMWareSPEEDY/MATEROV_26_codes.git
cd MATEROV_26_codes

# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install opencv-python numpy ultralytics torch pyvista solidpython2
```

### Launch Interactive Suite

```bash
python3 src/main.py
```

This launches the top-level menu to trigger:
1. `measurement_tool.py` — Optical calibration and pipe measurement
2. `inference.py` — YOLOv8 single image crab detection
3. `live_inference.py` — Camera feed inference with real-time HUD
4. `3D_model_gen.py` — Parametric SolidPython generation of Coral Garden structures

---

## Subsystem Details

### 1. Computer Vision & Photogrammetry (`src/`)
- **Pipe Length Measurement:** Interactive OpenCV tool (`measurement_tool.py`) applying a 4× magnification sub-pixel magnifier. Users calibrate reference scale (e.g. 10 cm tile) and accurately calculate target pipe lengths in the pool.
- **YOLOv8 Crab Detection:** Target detection (`inference.py` / `live_inference.py`) fine-tuned on custom datasets for underwater European Green Crab recognition. Exports bounding box metrics, confidence scores, and detection snapshots.

### 2. Embedded & ROV Control (`*.ino`)
- **Vector Thruster Mixer (`code.ino`):** Interrupt-based RC PWM reader (channels 1–4) driving 6 ESCs. Computes forward/back, strafe, yaw, and vertical thrust components with deadzone filtering and signal safety clamps.
- **Autonomous Profiling Float (`buoy_30sechold.ino`):** Simulates an oceanographic profiling float across two dive cycles: submerging to 1.0 m, holding for 30 seconds via dynamic thruster pulsing, ascending to 0.4 m, holding, resurfacing, and offloading log packets over Bluetooth Serial.

### 3. Mission Scorer (`mate_scorer.html`)
Open `mate_scorer.html` directly in any modern browser to calculate score tallies across:
- Primary missions (Coral Garden, Biofouling & Invasive Species, Floats)
- Safety checks, run times, and penalty points
- Live breakdown with instant reset and print-ready summary

---

## Documentation

For deep-dive documentation on individual subsystems, see:
- [Hardware & Firmware Guide](file:///Users/ashishpaliwal/MATEROV_26_codes/docs/hardware-and-firmware.md)
- [Vision & Photogrammetry Guide](file:///Users/ashishpaliwal/MATEROV_26_codes/docs/vision-and-cv.md)
- [CAD & Mechanical Design](file:///Users/ashishpaliwal/MATEROV_26_codes/docs/cad-and-mechanics.md)

---

## License

Created for the MATE ROV Competition 2026. Code and design files are shared for educational and competitive review.
