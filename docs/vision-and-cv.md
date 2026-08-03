# Computer Vision & Photogrammetry

This document outlines the computer vision architectures, image processing tools, and model inference pipelines developed for MATE ROV 2026.

---

## 1. Photogrammetric Pipe Length Measurement (`src/pipe_measurement/`)

### Purpose
Task 1.2 requires measuring unknown PVC pipe dimensions of underwater structures from ROV camera feeds using a known reference object (e.g. 10.0 cm coral base tile or reference pipe diameter).

### Core Scripts
- `measurement_tool.py`: Main interactive measurement interface.
- `measure.py`: Standalone calculation and coordinate transformation routines.

### Key Capabilities
- **Sub-Pixel Magnification Loupe:** Implements a dynamic `300×300` pixel zoom window centered on the mouse cursor with a 4× scaling factor, allowing millimetric vertex placement despite water turbidity.
- **Reference Calibration:** User selects two endpoints on a known object (e.g., standard tile) and enters the physical length in centimeters to establish the `pixels_per_metric` ratio.
- **Sequential Multi-Segment Tracking:** Once calibrated, users click successive segment endpoints to instantly compute Euclidean lengths and export results into structured CSV logs.

### Usage Example
```bash
python3 src/pipe_measurement/measurement_tool.py
```
- **Left Click:** Mark point
- **Right Click:** Reset current point selection
- **Key `c`:** Clear all measurements
- **Key `q`:** Save and exit

---

## 2. Invasive Crab Detection (`src/crab_detection/`)

### Purpose
Task 4.2 focuses on automated monitoring of invasive European Green Crabs (*Carcinus maenas*) in benthic environments.

### Model Architecture & Training
- **Backbone:** Ultralytics YOLOv8 object detection model.
- **Weights:** Fine-tuned weights stored in `assets/crab_detection/models/best.pt`.
- **Dataset:** Formatted according to YOLO specifications (`assets/crab_detection/data.yaml`), annotated across varied lighting conditions, water columns, and substrate textures.
- **Training Script (`train.py`):** Configured with AdamW optimizer, augmentations (hue/saturation jitter, mosaic), and automatic device targeting (Apple Silicon MPS or NVIDIA CUDA).

### Inference Modes
1. **Single Image Inference (`inference.py`):**
   - Loads image from `assets/images/` or user input.
   - Applies non-maximum suppression (IoU threshold 0.70, confidence threshold 0.45).
   - Draws labeled bounding boxes and saves annotated images to `output/`.
2. **Real-Time Video Stream (`live_inference.py`):**
   - Connects to USB/UVC ROV onboard camera.
   - Overlays real-time detection bounding boxes, confidence tags, and FPS counter.
   - Supports key shortcuts: `s` to freeze and export frame, `q` to quit stream.

### Running Inference
```bash
# Run single test inference
python3 src/crab_detection/inference.py

# Launch live webcam/tether stream
python3 src/crab_detection/live_inference.py
```
