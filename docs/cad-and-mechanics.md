# CAD & Mechanical Components

Overview of the 3D computer-aided design (CAD) workflow, parametric SolidPython generators, and 3D printable mechanical parts for the ROV vehicle.

---

## 1. Parametric Coral Garden Generator (`src/pipe_measurement/`)

### Scripts
- `3D_model_gen.py`: Procedural geometry generator using SolidPython2.
- `coral_garden_gen.py`: Specialized generator for task layout replication.

### Pipeline
1. Takes measurements derived from `measurement_tool.py` (pipe heights, base widths, cross branches).
2. Generates parametric OpenSCAD scripts (`assets/cad/pvc_temp.scad` and `assets/cad/tiles_temp.scad`).
3. Invokes the local OpenSCAD engine via CLI to compile high-resolution triangular mesh STLs (`assets/stl/pvc_frame.stl` and `assets/stl/coral_tiles.stl`).

### Execution
```bash
python3 src/pipe_measurement/3D_model_gen.py
```

---

## 2. 3D Printable Vehicle Components (`3D MODELS/`)

All parts are engineered for FDM 3D printing using rigid, water-resistant filaments (PETG or ASA) with high infill density (40%+).

| File Name | Description | Material / Print Recommendations |
| :--- | :--- | :--- |
| `top_guard_final.stl` | Upper hydrodynamic propeller and debris shroud for vertical and planar thrusters. Prevents tether fouling. | PETG, 0.20 mm layer height, 4 perimeters, 40% infill. |
| `bottom_guard_final.stl` | Lower matching propeller shroud providing 360° intake protection against pool bottom contact. | PETG, 0.20 mm layer height, 4 perimeters, 40% infill. |
| `vertical.stl` | Structural upright bracket securing vertical heave thrusters to the primary chassis frame. | PETG or Polycarbonate, 5 perimeters, 60% infill for rigidity. |
| `camera_holder.stl` | Adjustable mount securing the main HD forward navigation and measurement camera. | PETG, 0.16 mm layer height for tight pivot fit. |

---

## 3. Engineering Reference Assets (`assets/cad/`)

- `Task1.2_CoralGarden REV A.pdf`: Competition blueprint detailing exact nominal specifications, tolerances, and assembly layouts for Task 1.2.
- `Task1.2_CoralGarden REV A.SLDPRT`: SolidWorks master part model used for mechanical clearance simulation and reference checks.
