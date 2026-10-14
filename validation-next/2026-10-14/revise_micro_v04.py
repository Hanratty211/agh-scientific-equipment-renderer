"""04 v04: five Fig.3C exterior paths meet visible fittings/solid chip boundary.
Run from v01 blend, not v03: v03 had a known failed layout. No hidden channel or seal claim.
"""
import sys,math
from pathlib import Path
import bpy
from mathutils import Vector
root=Path(__file__).resolve().parent
sys.path.insert(0,str(root))
import render_core as r
r.M.clear()
for mat in bpy.data.materials:
 if mat.name.startswith('MAT_'):r.M[mat.name[4:]]=mat
# Green is a figure-3C schematic code, not a claim about dyed fluid or material.
green_mat=bpy.data.materials.new('MAT_schematic_green');green_mat.diffuse_color=(.23,.64,.34,1)
green_mat.use_nodes=True
green_mat.node_tree.nodes.clear();bs=green_mat.node_tree.nodes.new('ShaderNodeBsdfPrincipled');outnode=green_mat.node_tree.nodes.new('ShaderNodeOutputMaterial')
green_mat.node_tree.links.new(bs.outputs['BSDF'],outnode.inputs['Surface'])
bs.inputs['Base Color'].default_value=(.23,.64,.34,1);r.M['schematic_green']=green_mat
def remove(name):
 ob=bpy.data.objects.get(name)
 if ob:bpy.data.objects.remove(ob,do_unlink=True)
# Delete only v01 defective rings/paths and unused old camera, keep pump/barrel/chip.
for ob in list(bpy.data.objects):
 if ob.name.startswith(('Chip_inlet_','Chip_outlet_','External_fluid_tube_','Overview_Camera')):bpy.data.objects.remove(ob,do_unlink=True)
chip=bpy.data.objects['Transparent_microfluidic_chip'];chip['v04_boundary_note']='Solid exterior. No holes, channels, fluid continuity, seal or real input port demonstrated.'
# v01 chip bounds: x[-1.915,-.485], y[-1.53,-.57], z[.1025,.1775].
# Fittings are outside the chip, their flat end disks touch the actual chip boundary.
# Routes contact the outer face of their fitting; polyline points can be independently checked.
rows=[-.69,-.87,-1.05,-1.23,-1.41]
for i,y in enumerate(rows):
 x=.62+i*.63;z=.145
 # Pump hub is centered y=-.38, depth .12: its outward cap is y=-.44.
 # Visible blue route begins exactly there and ends at right fitting's y-facing open lip.
 fitting=r.cyl(f'Right_panel_fitting_{i}',(-.44,y,z),.046,.09,'metal',axis='X',evidence='assumption')
 fitting['physical_owner']=chip.name;fitting['face_contact']='x=-.485 chip outside / x=-.395 exterior';fitting['port_status']='representative external fitting only, no hole'
 route=r.route(f'Blue_inlet_exterior_{i}',[(x,-.44,.85),(x,-.75,.87),(x-.23,-.88,.62),(-.35,y,.33),(-.395,y,z)],.023,'blue','source-visible')
 route['source']='Fig.3C five right inlet paths; shape/coordinates are modeling assumptions';route['termination']='exterior metal fitting, chip internal connection UNKNOWN'
 # Left chip boundary x=-1.915; fitting center=-1.96 with radius of its axial half-depth .045.
 out=r.cyl(f'Left_outlet_fitting_{i}',(-1.96,y,z),.046,.09,'metal',axis='X',evidence='assumption')
 out['physical_owner']=chip.name;out['face_contact']='x=-1.915 chip outside / x=-2.005 exterior';out['port_status']='representative external fitting only, no hole'
 green=r.route(f'Green_outlet_exterior_{i}',[(-2.005,y,z),(-2.28,y,z+.03),(-2.66,y,z+.09),(-3.08,y,z+.12)],.030,'schematic_green','source-visible')
 green['source']='Fig.3C five green outlet paths';green['termination']='left schematic green segment; terminal reservoir/seal UNKNOWN'
 # Small terminal silhouette is a schematic bulb, not a tank/reservoir asserted as hardware.
 bulb=r.cyl(f'Green_schematic_terminal_{i}',(-3.17,y,z+.12),.068,.20,'schematic_green',axis='X',evidence='assumption')
 bulb['shape_note']='diagram terminal illustration, not sealed fluid reservoir'
# No camera is inherited from v01, making overview target deterministic.
r.camera((4.8,-7.8,5.4),(-.75,-.30,.46),8.3)
sc=bpy.context.scene;sc['revision_version']='v04';sc['visual_review']='pending_AGH_pixel_review';sc['source_location']='Fig.3C PDF p4, five right inlets, central chip, five green left outlets; Fig.3A pump shape only';sc['v04_limit']='External fittings touch chip bounds; no Boolean bore or hidden channel/seal; not fluid-functional CAD.'
bpy.context.view_layer.update()
out=root/'cases/04_microfluidics/v04';out.mkdir(exist_ok=True)
bpy.ops.wm.save_as_mainfile(filepath=str(out/'scene.blend'))
print('V04_SAVED',out/'scene.blend',flush=True)
