import os
import math
import subprocess
from solid2 import cylinder, cube, sphere, translate, rotate, union, color, set_global_fn
from solid2 import set_global_fa, set_global_fs

pipe_specs = {
    "main_height": 45.0,     
    "base_width": 30.0,       
    "cross_length": 30.0,     
    "pipe_diameter": 2.13,    
    "tile_size": 10.0,        
    "engagement": 1.9         
}
specs = { 
    "main_height": 52.0,  
    "left_wing_length": 112.0,  
    "right_wing_length": 121.0,  
}

def generate_geometry(specs):
    set_global_fa(12)
    set_global_fs(1.0)
    pvc_parts = []
    tile_parts = []
    pipe_metadata = []

    H_MAIN = specs.get("left_wing_length", 112.0) 
    L_WING = specs.get("main_height", 78.0)
    R_WING = specs.get("right_wing_length", 78.0)

    delta_rw = R_WING - 78.00

    pipe_radius = pipe_specs["pipe_diameter"] / 2
    joint_radius = pipe_radius * 1.3

    delta_h = H_MAIN - 53.00
    delta_l = L_WING - 40.00
    delta_r = L_WING - 40.00

    def add_p(h, trans, rot=None):
        p = cylinder(r=pipe_radius, h=h, center=True)
        if rot:
            if isinstance(rot[0], list):
                for r in reversed(rot):
                    p = rotate(r)(p)
            else:
                p = rotate(rot)(p)
        if trans:
            p = translate(trans)(p)
        pvc_parts.append(p)
        pipe_metadata.append({'length': h, 'pos': trans})

    def add_s(trans):
        pvc_parts.append(translate(trans)(sphere(r=joint_radius)))

    # --- JOINTS ---
    add_s([-32.57, 69.19 + delta_l, 46.29])
    add_s([-32.57, 0.89, 105.21 + delta_h])
    add_s([-31.68, 17.54, 98.83 + delta_h])
    add_s([-31.68, 0.00, 98.86 + delta_h])
    add_s([-32.57, 0.89, 46.29])
    add_s([-32.57, 17.54, 47.18])
    add_s([-31.68, 0.00, -78.86 - delta_rw])
    add_s([-32.57, 0.89, -85.21 - delta_rw])
    add_s([-31.68, 27.54, -78.83 - delta_rw])
    add_s([-32.57, 0.89, -1.29])
    add_s([-32.57, 27.54, -2.18])
    add_s([-31.68, 70.08 + delta_l, 22.52])
    
    add_s([0.00, 17.54, 47.18])
    add_s([0.00, 27.54, -2.18])
    add_s([0.00, 69.19 + delta_r, -1.29])
    add_s([0.00, 0.89, 105.21 + delta_h])
    add_s([0.00, 0.89, 46.29])
    add_s([0.00, 0.89, -85.21 - delta_rw])
    add_s([0.00, 0.89, -1.29])
    add_s([-0.89, 17.54, 98.83 + delta_h])
    add_s([-0.89, 0.00, 98.86 + delta_h])
    add_s([-0.89, 27.54, -78.83 - delta_rw])
    add_s([-0.89, 0.00, -78.86 - delta_rw])
    add_s([-0.89, 70.08 + delta_r, 22.52])

    add_s([1.00, 0.00, 46.29])
    add_s([1.00, 0.00, 105.21 + delta_h])
    add_s([1.00, 0.00, -85.21 - delta_rw])
    add_s([1.00, 0.00, -1.29])
    add_s([0.00, 18.54, 98.83 + delta_h])
    add_s([0.00, 1.00, 98.86 + delta_h])
    add_s([0.00, 28.54, -78.83 - delta_rw])
    add_s([0.00, 1.00, -78.86 - delta_rw])
    add_s([0.00, 71.08 + delta_r, 22.52])

    # --- PIPES ---
    add_p(15.00, [-32.57, 8.77, 46.29], [-90, 0, 0])
    add_p(15.00, [0.00, 8.77, 46.29], [-90, 0, 0])
    add_p(15.00, [0.00, 8.77, 105.21 + delta_h], [-90, 0, 0])
    add_p(15.00, [-32.57, 8.77, 105.21 + delta_h], [-90, 0, 0])
    
    add_p(30.00, [-16.27, 27.54, -78.83 - delta_rw], [0, 90, 0])
    add_p(30.00, [-16.30, 17.54, 98.83 + delta_h], [0, 90, 0])
    add_p(30.00, [-16.29, 0.00, 98.86 + delta_h], [0, 90, 0])
    add_p(30.00, [-16.29, 0.00, -78.86 - delta_rw], [0, 90, 0])
    
    cc_y_left = 70.08 + delta_l
    cc_y_right = 70.08 + delta_r
    cc_cy = (cc_y_left + cc_y_right) / 2
    cc_l = math.sqrt(32.57**2 + (cc_y_right - cc_y_left)**2)
    cc_angle = math.degrees(math.atan2(cc_y_right - cc_y_left, 32.57))
    add_p(cc_l, [-16.27, cc_cy, 22.52], [[0, 0, cc_angle], [0, 90, 0]])

    add_p(40.00 + delta_l, [-32.57, 48.81 + delta_l/2, -1.29], [-90, 0, 0])
    add_p(40.00 + delta_r, [0.00, 48.81 + delta_r/2, -1.29], [-90, 0, 0])
    add_p(50.00 + delta_l, [-32.57, 43.81 + delta_l/2, 46.29], [-90, 0, 0])
    add_p(50.00 + delta_r, [0.00, 43.81 + delta_r/2, 46.29], [-90, 0, 0])

    add_p(25.00, [-32.57, 13.77, -85.21 - delta_rw], [-90, 0, 0])
    add_p(25.00, [0.00, 13.77, -1.29], [-90, 0, 0])
    add_p(25.00, [-32.57, 13.77, -1.29], [-90, 0, 0])
    add_p(25.00, [0.00, 13.77, -85.21 - delta_rw], [-90, 0, 0])

    # --- VERTICAL PIPES ---
    add_p(53.00 + delta_h, [-32.57, 0.00, 72.57 + delta_h/2])
    add_p(53.00 + delta_h, [0.00, 0.00, 72.57 + delta_h/2])
    add_p(53.00 + delta_h, [0.00, 17.54, 72.56 + delta_h/2])
    add_p(53.00 + delta_h, [-32.57, 17.54, 72.56 + delta_h/2])
    
    add_p(48.00, [0.00, 0.00, 22.50])
    add_p(48.00, [-32.57, 0.00, 22.50])
    
    add_p(R_WING, [-32.57, 0.00, -40.07 - delta_rw / 2])
    add_p(R_WING, [0.00, 27.54, -40.06 - delta_rw / 2])
    add_p(R_WING, [-32.57, 27.54, -40.06 - delta_rw / 2])
    add_p(R_WING, [0.00, 0.00, -40.07 - delta_rw / 2])
    
    add_p(24.00, [0.00, 70.08 + delta_r, 34.52])
    add_p(24.00, [0.00, 70.08 + delta_r, 10.75])
    add_p(24.00, [-32.57, 70.08 + delta_l, 10.48])
    add_p(24.00, [-32.57, 70.08 + delta_l, 34.52])

    add_p(6.35, [-32.57, 0.00, -82.03 - delta_rw])
    add_p(6.35, [0.00, 0.00, -82.03 - delta_rw])
    add_p(6.35, [-32.57, 27.54, -82.03 - delta_rw])
    add_p(6.35, [0.00, 27.54, -82.03 - delta_rw])
    add_p(3.00, [0.00, 70.08 + delta_r, 22.52])
    add_p(6.00, [-32.57, 0.00, 101.8 + delta_h/2])
    add_p(6.00, [0.00, 0.00, 101.8 + delta_h/2])

    # --- TILES ---
    tile_parts.append(color('pink')(translate([0.50, 65.78 + delta_r, 43.87])(cube([3.79, 10, 10], center=True))))
    tile_parts.append(color('pink')(translate([0.50, 13.24, 101.80 + delta_h])(cube([3.79, 10, 10], center=True))))
    tile_parts.append(color('pink')(translate([-33.07, 13.24, 101.80 + delta_h])(cube([3.79, 10, 10], center=True))))
    tile_parts.append(color('pink')(translate([0.00, 23.24, -81.80 - delta_rw])(cube([2.79, 10, 10], center=True))))
    tile_parts.append(color('pink')(translate([-32.57, 23.24, -81.80 - delta_rw])(cube([2.79, 10, 10], center=True))))
    tile_parts.append(color('pink')(translate([-33.07, 65.78 + delta_l, 2.13])(cube([3.79, 10, 10], center=True))))
    tile_parts.append(color('pink')(translate([0.57, 5.00, 22.50])(cube([1.00, 10.00, 10.00], center=True))))
    tile_parts.append(color('pink')(translate([-33.14, 5.00, 22.50])(cube([1.00, 10.00, 10.00], center=True))))

    return union()(pvc_parts), union()(tile_parts), pipe_metadata

def build_and_export():
    print("Generating SolidPython2 geometry...")
    pvc, tiles, pipe_metadata = generate_geometry(specs)

    pvc.save_as_scad("pvc_temp.scad")
    tiles.save_as_scad("tiles_temp.scad")

    openscad_path = "/Applications/OpenSCAD-2021.01.app/Contents/MacOS/OpenSCAD"
    
    print("Exporting PVC frame...")
    subprocess.run([openscad_path, "-o", "pvc_frame.stl", "pvc_temp.scad"], check=True)
    
    print("Exporting coral tiles...")
    subprocess.run([openscad_path, "-o", "coral_tiles.stl", "tiles_temp.scad"], check=True)
    
    print("Export complete.")
    return pipe_metadata

def view_model(pipe_metadata=None):
    import pyvista as pv

    if not os.path.exists("pvc_frame.stl") or not os.path.exists("coral_tiles.stl"):
        print("Error: STL files missing. Ensure OpenSCAD compiled the files successfully.")
        return

    plotter = pv.Plotter(window_size=[2560, 1440])

    pvc_mesh = pv.read("pvc_frame.stl")
    tiles_mesh = pv.read("coral_tiles.stl")

    plotter.add_mesh(pvc_mesh, color='lightgray', smooth_shading=True, name="PVC Frame")
    plotter.add_mesh(tiles_mesh, color='purple', show_edges=False, name="Coral Tiles")

    if pipe_metadata:
        for pipe in pipe_metadata:
            length = pipe['length']
            pos = pipe['pos']
            plotter.add_point_labels([pos], [f"{length:.1f} cm"], 
                                     point_size=0, font_size=15, 
                                     text_color='black', shape_color='white', shape_opacity=0.5)

    plotter.add_axes()
    plotter.set_background('white')
    plotter.camera_position = 'iso'
    plotter.show(title="MATE ROV 2026 - Coral Garden Task 1.2")

if __name__ == "__main__":
    pipe_metadata = build_and_export()
    view_model(pipe_metadata)