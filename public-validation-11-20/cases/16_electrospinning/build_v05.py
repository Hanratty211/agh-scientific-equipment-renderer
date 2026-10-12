"""R2 narrow repair: preserve v04 whole chamber and exterior power boundaries.
Convert ONLY the two existing HV/return leads from hard POLY to a coaxial
source boot → relaxed exterior Bezier → source-visible chamber occlusion.
No pinout, feedthrough, hidden internal route, or new device asserted.
"""
import bpy,sys
from pathlib import Path
from mathutils import Vector
p=Path(__file__).resolve().parent;sys.path.insert(0,str(p.parent))
from scene_parts_v03 import *
from physical_parts_v01 import bind_existing_materials
from physical_parts_r1 import bent_cable
bpy.ops.wm.open_mainfile(filepath=str(p/'scene_v04.blend'));bind_existing_materials()
for name,z,mat,via,end in [
 ('positive HV',.81,'red',(-2.06,-.65,1.31),(-1.64,-.51,1.16)),
 ('return/ground',.51,'mint',(-2.08,-.71,.45),(-1.64,-.51,.56))]:
 route_name=name+' visible external lead'
 old=bpy.data.objects.get(route_name);assert old and old.type=='CURVE'
 start=Vector((-2.817,-.508,z))
 # Existing physical source plug and short black boot, no added plug identity.
 plug=bpy.data.objects[name+' insulated source plug']
 boot=bpy.data.objects[name+' short strain relief']
 assert abs(plug.location.x-start.x)<1e-5 and abs(plug.location.z-start.z)<1e-5
 assert (boot.location-Vector((-2.817,-.558,z))).length<.005
 bpy.data.objects.remove(old,do_unlink=True)
 # Axial -Y departure at source; relaxed loop farther outboard before reaching
 # same chamber boundary. Last approach ends on visible occlusion, not inside.
 bent_cable(route_name,[start,(-2.817,-.608,z),(-2.80,-.77,z),
  (-2.51,-.84,z+.035),via,(-1.79,-.67,end[2]),end],.018,mat,.18)
scene=bpy.context.scene;scene.render.filepath=str(p/'overview_v05_build_only.png');scene.render.resolution_x=1090;scene.render.resolution_y=850
bpy.context.preferences.filepaths.save_version=0
bpy.ops.wm.save_as_mainfile(filepath=str(p/'scene_v05.blend'))
# Deliberately NO render here: final pixels are made only by independent reload.
