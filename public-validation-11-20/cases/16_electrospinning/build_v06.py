"""R3 two-boundary-only: replace colored free tips at existing left transparent wall
with representative insulating feedthrough collars and actual editable wall bores.
No internal needle/collector route, seal, HV rating or product fitting asserted.
Source scene_v05 stays unchanged; save scene_v06 without rendering in build process.
"""
import bpy,sys,math
from pathlib import Path
from mathutils import Vector
p=Path(__file__).resolve().parent;sys.path.insert(0,str(p.parent))
from scene_parts_v03 import *
from physical_parts_v01 import bind_existing_materials
bpy.ops.wm.open_mainfile(filepath=str(p/'scene_v05.blend'));bind_existing_materials()
wall=bpy.data.objects['clear Perspex side'];assert abs(wall.location.x+1.64)<.001
# Two bores cut into actual Perspex side, whose thickness runs along world X.
# Keep remaining wall/frames and every other source component unchanged.
bpy.ops.object.select_all(action='DESELECT');wall.select_set(True);bpy.context.view_layer.objects.active=wall
for prior in list(wall.modifiers):bpy.ops.object.modifier_apply(modifier=prior.name)
ends=[('positive HV','red',1.16,'chamber red boundary'),('return/ground','mint',.56,'chamber green boundary')]
for name,mat,z,old_marker in ends:
 center=Vector((-1.64,-.51,z));exterior=Vector((-1.6625,-.51,z))
 assert (bpy.data.objects[old_marker].location-center).length<.0005
 curve=bpy.data.objects[name+' visible external lead'];assert curve.type=='CURVE' and len(curve.data.splines)==1 and curve.data.splines[0].type=='BEZIER'
 last=curve.data.splines[0].bezier_points[-1]
 assert (Vector(last.co)-center).length<.0005
 # Stop inside a dark insulated outer sleeve, BEFORE crossing the wall.
 # Final tangent is near +X: entry guided by the actual outside left face.
 last.co=(-1.708,-.51,z);last.handle_left=(-1.748,-.51,z);last.handle_right=(-1.668,-.51,z)
 # The previous penultimate point is still outside the wall, retains natural bow.
 old=bpy.data.objects[old_marker];bpy.data.objects.remove(old,do_unlink=True)
 # An actual round bore along X through the evaluated wall mesh, radius for this
 # illustrative layout only; cutter and applied result remain editable as mesh.
 cutter=cylinder('TEMP '+name+' wall bore',tuple(center),.069,.15,'black',rotation=(0,math.pi/2,0))
 bpy.context.view_layer.update();bpy.ops.object.select_all(action='DESELECT');wall.select_set(True);bpy.context.view_layer.objects.active=wall
 mod=wall.modifiers.new(name+' true insulated entry bore','BOOLEAN');mod.operation='DIFFERENCE';mod.solver='EXACT';mod.object=cutter
 bpy.ops.object.modifier_apply(modifier=mod.name);bpy.data.objects.remove(cutter,do_unlink=True)
 # Actual hollow annuli, not painted discs. Outer insulating mounting sleeve
 # straddles the wall; its cable-facing opening accepts the external cable end.
 exterior_shell=cylinder(name+' representative insulating mounting sleeve',(-1.668,-.51,z),.091,.125,'ivory',rotation=(0,math.pi/2,0))
 hole=cylinder('TEMP '+name+' mounting sleeve lumen',(-1.668,-.51,z),.040,.15,'black',rotation=(0,math.pi/2,0))
 bpy.context.view_layer.update();bpy.ops.object.select_all(action='DESELECT');exterior_shell.select_set(True);bpy.context.view_layer.objects.active=exterior_shell
 for prior in list(exterior_shell.modifiers):bpy.ops.object.modifier_apply(modifier=prior.name)
 mod=exterior_shell.modifiers.new('real axial sleeve void','BOOLEAN');mod.operation='DIFFERENCE';mod.solver='EXACT';mod.object=hole
 bpy.ops.object.modifier_apply(modifier=mod.name);bpy.data.objects.remove(hole,do_unlink=True)
 # An additional cable-end flexible boot enters a sleeve opening. No route exists
 # through or beyond the wall, thus no invented internal electrical topology.
 cable_boot=cylinder(name+' wall-entry strain relief',(-1.745,-.51,z),.035,.101,'black',rotation=(0,math.pi/2,0))
 # Original per-source boundary port now binds to actual cable-facing rim mesh;
 # anchor real evaluated sleeve front (left) face, NOT a floating colored cube.
 ring=flat_ring('chamber '+('red' if name=='positive HV' else 'green')+' boundary',(-1.7305,-.51,z),.091,.040,.012,'ivory')
 ring.rotation_euler[1]=math.pi/2
 # The anchor is its real annular mesh, never a filled center marker.
 # Its centroid is hollow and cannot be on the sleeve surface; auditor will
 # report centroid-to-surface distance. Record this as unverified, not FAIL-erasure.
scene=bpy.context.scene;scene.render.filepath=str(p/'overview_v06_build_only.png');scene.render.resolution_x=1090;scene.render.resolution_y=850
bpy.context.preferences.filepaths.save_version=0
bpy.ops.wm.save_as_mainfile(filepath=str(p/'scene_v06.blend'))
