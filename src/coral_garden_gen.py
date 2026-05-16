import os
from solid2 import cylinder, cube, sphere, translate, rotate, union, color, set_global_fn
import subprocess
from solid2 import set_global_fa, set_global_fs

pipe_specs = {
    "main_height": 45.0,     
    "base_width": 30.0,       
    "cross_length": 30.0,     
    "pipe_diameter": 2.13,    
    "tile_size": 10.0,        
    "engagement": 1.9         
}

# Paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SCAD_DIR = os.path.join(BASE_DIR, "assets", "cad")
STL_DIR = os.path.join(BASE_DIR, "assets", "stl")
PVC_SCAD = os.path.join(SCAD_DIR, "pvc_temp.scad")
TILES_SCAD = os.path.join(SCAD_DIR, "tiles_temp.scad")
PVC_STL = os.path.join(STL_DIR, "pvc_frame.stl")
TILES_STL = os.path.join(STL_DIR, "coral_tiles.stl")


def generate_geometry(specs):
    set_global_fa(12)
    set_global_fs(1.0)
    pvc_parts = []
    tile_parts = []
    pvc_parts.append(translate([-32.57, 69.19, 46.29])(sphere(r=1.385)))
    pvc_parts.append(translate([-32.57, 0.89, 105.21])(sphere(r=1.385)))
    pvc_parts.append(translate([-31.68, 17.54, 98.83])(sphere(r=1.385)))
    pvc_parts.append(translate([-31.68, 0.00, 98.86])(sphere(r=1.385)))
    pvc_parts.append(translate([-32.57, 0.89, 46.29])(sphere(r=1.385)))
    pvc_parts.append(translate([0.00, 17.54, 47.18])(sphere(r=1.385)))
    pvc_parts.append(translate([-32.57, 17.54, 47.18])(sphere(r=1.385)))
    pvc_parts.append(translate([-31.68, 0.00, -78.86])(sphere(r=1.385)))
    pvc_parts.append(translate([-32.57, 0.89, -85.21])(sphere(r=1.385)))
    pvc_parts.append(translate([-31.68, 27.54, -78.83])(sphere(r=1.385)))
    pvc_parts.append(translate([-32.57, 0.89, -1.29])(sphere(r=1.385)))
    pvc_parts.append(translate([0.00, 27.54, -2.18])(sphere(r=1.385)))
    pvc_parts.append(translate([-32.57, 27.54, -2.18])(sphere(r=1.385)))
    pvc_parts.append(translate([0.00, 69.19, -1.29])(sphere(r=1.385)))
    pvc_parts.append(translate([-31.68, 70.08, 22.52])(sphere(r=1.385)))
    pvc_parts.append(translate([0.00, 0.89, 105.21])(sphere(r=1.385)))
    pvc_parts.append(translate([-0.89, 17.54, 98.83])(sphere(r=1.385)))
    pvc_parts.append(translate([-0.89, 0.00, 98.86])(sphere(r=1.385)))
    pvc_parts.append(translate([0.00, 0.89, 46.29])(sphere(r=1.385)))
    pvc_parts.append(translate([0.00, 0.89, -85.21])(sphere(r=1.385)))
    pvc_parts.append(translate([-0.89, 27.54, -78.83])(sphere(r=1.385)))
    pvc_parts.append(translate([-0.89, 0.00, -78.86])(sphere(r=1.385)))
    pvc_parts.append(translate([0.00, 0.89, -1.29])(sphere(r=1.385)))
    pvc_parts.append(translate([-0.89, 70.08, 22.52])(sphere(r=1.385)))
    pvc_parts.append(translate([-32.57, 8.77, 46.29])(rotate([-90, 0, 0])(cylinder(r=1.065, h=15.00, center=True))))
    pvc_parts.append(translate([-0.00, 8.77, 46.29])(rotate([-90, 0, 0])(cylinder(r=1.065, h=15.00, center=True))))
    pvc_parts.append(translate([0.00, 8.77, 105.21])(rotate([-90, 0, 0])(cylinder(r=1.065, h=15.00, center=True))))
    pvc_parts.append(translate([-32.57, 8.77, 105.21])(rotate([-90, 0, 0])(cylinder(r=1.065, h=15.00, center=True))))
    pvc_parts.append(translate([-32.57, 13.77, -85.21])(rotate([-90, 0, 0])(cylinder(r=1.065, h=25.00, center=True))))
    pvc_parts.append(translate([0.00, 13.77, -1.29])(rotate([-90, 0, 0])(cylinder(r=1.065, h=25.00, center=True))))
    pvc_parts.append(translate([-32.57, 13.77, -1.29])(rotate([-90, 0, 0])(cylinder(r=1.065, h=25.00, center=True))))
    pvc_parts.append(translate([0.00, 13.77, -85.21])(rotate([-90, 0, 0])(cylinder(r=1.065, h=25.00, center=True))))
    pvc_parts.append(translate([0.00, 70.08, 34.52])(cylinder(r=1.065, h=24.00, center=True)))
    pvc_parts.append(translate([0.00, 70.08, 10.75])(cylinder(r=1.065, h=24.00, center=True)))
    pvc_parts.append(translate([-32.57, 70.08, 10.48])(cylinder(r=1.065, h=24.00, center=True)))
    pvc_parts.append(translate([-32.57, 70.08, 34.52])(cylinder(r=1.065, h=24.00, center=True)))
    pvc_parts.append(translate([-16.27, 27.54, -78.83])(rotate([0, 90, 0])(cylinder(r=1.065, h=30.00, center=True))))
    pvc_parts.append(translate([-16.30, 17.54, 98.83])(rotate([0, 90, 0])(cylinder(r=1.065, h=30.00, center=True))))
    pvc_parts.append(translate([-16.27, 70.08, 22.52])(rotate([0, 90, 0])(cylinder(r=1.065, h=30.00, center=True))))
    pvc_parts.append(translate([-16.29, 0.00, 98.86])(rotate([0, 90, 0])(cylinder(r=1.065, h=30.00, center=True))))
    pvc_parts.append(translate([-16.29, 0.00, -78.86])(rotate([0, 90, 0])(cylinder(r=1.065, h=30.00, center=True))))
    pvc_parts.append(translate([0.00, 0.00, 22.50])(cylinder(r=1.065, h=48.00, center=True)))
    pvc_parts.append(translate([-32.57, 0.00, 22.50])(cylinder(r=1.065, h=48.00, center=True)))
    pvc_parts.append(translate([-32.57, 48.81, -1.29])(rotate([-90, 0, 0])(cylinder(r=1.065, h=40.00, center=True))))
    pvc_parts.append(translate([0.00, 48.81, -1.29])(rotate([-90, 0, 0])(cylinder(r=1.065, h=40.00, center=True))))
    pvc_parts.append(translate([-32.57, 0.00, 72.57])(cylinder(r=1.065, h=53.00, center=True)))
    pvc_parts.append(translate([0.00, 0.00, 72.57])(cylinder(r=1.065, h=53.00, center=True)))
    pvc_parts.append(translate([0.00, 17.54, 72.56])(cylinder(r=1.065, h=53.00, center=True)))
    pvc_parts.append(translate([-32.57, 17.54, 72.56])(cylinder(r=1.065, h=53.00, center=True)))
    pvc_parts.append(translate([-32.57, 43.81, 46.29])(rotate([-90, 0, 0])(cylinder(r=1.065, h=50.00, center=True))))
    pvc_parts.append(translate([0.00, 43.81, 46.29])(rotate([-90, 0, 0])(cylinder(r=1.065, h=50.00, center=True))))
    pvc_parts.append(translate([-32.57, 0.00, -40.07])(cylinder(r=1.065, h=78.00, center=True)))
    pvc_parts.append(translate([0.00, 27.54, -40.06])(cylinder(r=1.065, h=78.00, center=True)))
    pvc_parts.append(translate([-32.57, 27.54, -40.06])(cylinder(r=1.065, h=78.00, center=True)))
    pvc_parts.append(translate([0.00, 0.00, -40.07])(cylinder(r=1.065, h=78.00, center=True)))
    pvc_parts.append(translate([1.00, -0.00, 46.29])(sphere(r=1.385)))
    pvc_parts.append(translate([1.00, -0.00, 105.21])(sphere(r=1.385)))
    pvc_parts.append(translate([1.00, 0.00, -85.21])(sphere(r=1.385)))
    pvc_parts.append(translate([1.00, -0.00, -1.29])(sphere(r=1.385)))
    pvc_parts.append(translate([-0.00, 18.54, 98.83])(sphere(r=1.385)))
    pvc_parts.append(translate([0.00, 1.00, 98.86])(sphere(r=1.385)))
    pvc_parts.append(translate([-0.00, 28.54, -78.83])(sphere(r=1.385)))
    pvc_parts.append(translate([0.00, 1.00, -78.86])(sphere(r=1.385)))
    pvc_parts.append(translate([0.00, 71.08, 22.52])(sphere(r=1.385)))

    tile_parts.append(color('pink')(translate([0.50, 65.78, 43.87])(cube([3.79, 10, 10], center=True))))
    tile_parts.append(color('pink')(translate([0.50, 13.24, 101.80])(cube([3.79, 10, 10], center=True))))
    tile_parts.append(color('pink')(translate([-33.07, 13.24, 101.80])(cube([3.79, 10, 10], center=True))))
    tile_parts.append(color('pink')(translate([0.00, 23.24, -81.80])(cube([2.79, 10, 10], center=True))))
    tile_parts.append(color('pink')(translate([-32.57, 23.24, -81.80])(cube([2.79, 10, 10], center=True))))
    tile_parts.append(color('pink')(translate([-33.07, 65.78, 2.13])(cube([3.79, 10, 10], center=True))))

    tile_parts.append(color('pink')(translate([0.57, 5.00, 22.50])(cube([1.00, 10.00, 10.00], center=True))))
    tile_parts.append(color('pink')(translate([-33.14, 5.00, 22.50])(cube([1.00, 10.00, 10.00], center=True))))
    
    # Fill gaps between pillars and base pipes
    pvc_parts.append(translate([-32.57, 0.00, -82.03])(cylinder(r=1.065, h=6.35, center=True)))
    pvc_parts.append(translate([0.00, 0.00, -82.03])(cylinder(r=1.065, h=6.35, center=True)))
    pvc_parts.append(translate([-32.57, 27.54, -82.03])(cylinder(r=1.065, h=6.35, center=True)))
    pvc_parts.append(translate([0.00, 27.54, -82.03])(cylinder(r=1.065, h=6.35, center=True)))
    pvc_parts.append(translate([0.00, 70.08, 22.52])(cylinder(r=1.065, h=3.00, center=True)))
    #right
    pvc_parts.append(translate([-32.57, 0.0, 101.8])(rotate([0, 0, 0])(cylinder(r=1.065, h=6.00, center=True))))
    pvc_parts.append(translate([0.00, 0.0, 101.8])(rotate([0, 0, 0])(cylinder(r=1.065, h=6.00, center=True))))

    return union()(pvc_parts), union()(tile_parts)

def build_and_export():
    print("Generating SolidPython2 geometry...")
    pvc, tiles = generate_geometry(pipe_specs)

    pvc.save_as_scad(PVC_SCAD)
    tiles.save_as_scad(TILES_SCAD)

    openscad_path = "/Applications/OpenSCAD-2021.01.app/Contents/MacOS/OpenSCAD"
    
    print("Exporting PVC frame (this may take a few seconds)...")
    subprocess.run([openscad_path, "-o", PVC_STL, PVC_SCAD], check=True)
    
    print("Exporting coral tiles...")
    subprocess.run([openscad_path, "-o", TILES_STL, TILES_SCAD], check=True)
    
    print("Export complete.")

def view_model():
    import pyvista as pv

    if not os.path.exists(PVC_STL) or not os.path.exists(TILES_STL):
        print("Error: STL files missing. Ensure OpenSCAD compiled the files successfully.")
        return

    plotter = pv.Plotter(window_size=[2560, 1440])

    # Load meshes
    pvc_mesh = pv.read(PVC_STL)
    tiles_mesh = pv.read(TILES_STL)

    # Apply materials/colors
    plotter.add_mesh(pvc_mesh, color='lightgray', smooth_shading=True, name="PVC Frame")
    plotter.add_mesh(tiles_mesh, color='purple', show_edges=False, name="Coral Tiles")

    # Inspection Tools
    plotter.add_axes()
    # plotter.add_measurement_widget()

    # Viewport Settings
    plotter.set_background('white')
    plotter.camera_position = 'iso'
    plotter.show(title="MATE ROV 2026 - Coral Garden Task 1.2")

if __name__ == "__main__":
    build_and_export()
    view_model()