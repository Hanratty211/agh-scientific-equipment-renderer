"""R1 repair: physical pump interface derives from actual X-oriented barrel.
No new hidden fluid/coil topology; sample/pump/sensor visible routes preserved.
"""
import bpy,sys
from pathlib import Path
from mathutils import Vector
p=Path(__file__).resolve().parent;sys.path.insert(0,str(p.parent))
from scene_parts_v03 import *
from physical_parts_v01 import bind_existing_materials
from physical_parts_r1 import syringe_axis_chain,bent_cable
bpy.ops.wm.open_mainfile(filepath=str(p/'scene_v04.blend'));bind_existing_materials()
barrel=bpy.data.objects['right syringe pump mounted syringe barrel'];r=bpy.data.objects['sample to pump visible pneumatic segment']
assert barrel.type=='MESH' and r.type=='CURVE'
# Body stays right; moving only mounted syringe into the REAL source-facing left
# nozzle chain. Sample's tube end moves from detached proxy to the real nozzle.
barrel.location=(2.98,.05,1.42)
barrel.rotation_euler=(0,0,0);barrel.dimensions=(.146,.146,.58)
barrel.rotation_euler[1]=1.57079632679;bpy.context.view_layer.update()
for name in ('red pump syringe interface','pump syringe pneumatic ferrule','pump visible tube fitting','sample to pump visible pneumatic segment'):
 obj=bpy.data.objects.get(name)
 if obj:bpy.data.objects.remove(obj,do_unlink=True)
outlet=(2.47,.05,1.42)
chain=syringe_axis_chain('right pump',tuple(barrel.location),.58,outlet,axis_sign=-1)
# Keep original sample fitting and waypoints, but land route on nozzle action
# face. This is a source-facing minimal end adjustment; original tube topology.
bent_cable('sample to pump visible pneumatic segment',[
 (.315,-.03,1.00),(.72,.08,1.02),(1.27,.27,1.10),
 (1.85,.26,1.38),(2.30,.11,1.42),(2.38,.05,1.42),outlet],.020,'fluid',.24)
# Real nozzle annulus itself owns the record's pump interface. Nothing ending at
# the discontinued ferrule sphere or independent old barrel.
chamber=bpy.data.objects.get('front pressure sensor')
assert chamber and bpy.data.objects.get('sample to pressure sensor visible segment')
s=bpy.context.scene;s.render.filepath=str(p/'overview_v05.png');s.render.resolution_x=1120;s.render.resolution_y=800
bpy.context.preferences.filepaths.save_version=0
bpy.ops.wm.save_as_mainfile(filepath=str(p/'scene_v05.blend'));bpy.ops.render.render(write_still=True)
