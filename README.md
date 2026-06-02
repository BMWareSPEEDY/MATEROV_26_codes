# MATE ROV 2026 - Pipe Length & Crab Detection

This repository contains tools developed for the MATE ROV 2026 competition, focusing on Task 1.2 (Coral Garden) and Task 4.2 (Invasive Species Detection).

## Project Structure

- `src/`: Python source code
  - `main.py`: Entry point for all tools.
  - `pipe_measurement/`: Tools for calculating pipe lengths and generating 3D models.
    - `measurement_tool.py`: Precision measurement tool using image processing.
    - `3D_model_gen.py`: Parametric 3D model generator.
  - `crab_detection/`: YOLOv8-based invasive species detection.
    - `inference.py`: Run detection on a test image.
    - `live_inference.py`: Real-time detection from a camera feed.
    - `train.py`: Script for training the YOLOv8 model.
- `assets/`: Project assets
  - `images/`: Source images for measurement.
  - `stl/`: Generated and reference STL files.
  - `cad/`: CAD source files and OpenSCAD scripts.
  - `crab_detection/`: Dataset and trained models (weights).
- `output/`: Directory for exported results (annotated images, CSVs).

## Requirements

- Python 3.x
- OpenCV (`cv2`)
- NumPy
- SolidPython2
- PyVista
- OpenSCAD (installed at `/Applications/OpenSCAD-2021.01.app`)
- Ultralytics (for YOLOv8)
- PyTorch (with MPS support for Apple Silicon recommended)

## Usage

Run the master control script to access all tools:

```bash
python3 src/main.py
```

### 1. Pipe Length Measurement
Used to calculate unknown pipe lengths by setting a scale with a known reference. Features a zoom window for sub-pixel precision.

### 2. Crab Detection
Detects invasive European Green Crabs using a YOLOv8 model trained on custom data.
- Supports single image inference.
- Supports live camera feed with frame capture.

### 3. 3D Model Generation
Generates parametric CAD models and STL files for the ROV components.
