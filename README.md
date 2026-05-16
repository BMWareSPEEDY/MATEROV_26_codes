# Pipe Length MATE ROV 2026

Project for calculating pipe lengths and generating 3D models for the MATE ROV 2026 Coral Garden Task 1.2.

## Project Structure

- `src/`: Python source code
  - `main.py`: Precision measurement tool for calculating pipe lengths from images.
  - `3D_model_gen.py`: Parametric 3D model generator using SolidPython2 and PyVista.
  - `coral_garden_gen.py`: Original 3D model generator script.
- `assets/`: Project assets
  - `images/`: Source images for measurement.
  - `stl/`: Generated and reference STL files.
  - `cad/`: CAD source files and intermediate OpenSCAD scripts.
- `output/`: (Optional) Directory for exported results.

## Requirements

- Python 3.x
- OpenCV (`cv2`)
- NumPy
- SolidPython2
- PyVista
- OpenSCAD (installed at `/Applications/OpenSCAD-2021.01.app`)

## Usage

### Measurement Tool
```bash
cd src
python3 main.py
```

### 3D Model Generation
```bash
cd src
python3 3D_model_gen.py
```
