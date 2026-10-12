"""R2 narrow repair: preserve v05 tilted glass, sample, real film contacts,
resistor/scope bodies; smooth two external leads with coaxial plug boots.
Actual probe attenuator/ground and channel number remain unknown.
"""
import bpy,sys
from pathlib import Path
from mathutils import Vector
p=Path(__file__).resolve().parent;sys.path.insert(0,str(p.parent))
from scene_parts_v03 import *
from physical_parts_v01 import bind_existing_materials
from physical_parts_r1 import bent_cable
bpy.ops.wm.open_mainfile(filepath=str(p/'scene_v05.blend'));bind_existing_materials()
film=bpy.data.objects['TeRC transparent coating'];bpy.context.view_layer.update()
left=tuple(film.matrix_world@Vector((-1.00,-.55,.005)))
right=tuple(film.matrix_world@Vector((1.00,-.55,.005)))
res=(1.0,-.287,.77);analog=(2.58,-.294,.34)
assert (bpy.data.objects['resistance actual terminal ring'].location-Vector(res)).length<1e-5
assert (bpy.data.objects['representative Keysight DSOX1204A front ANALOG INPUT BNC input ring'].location-Vector(analog)).length<1e-5
for name in ('glass to resistance exterior lead','glass to analog input exterior coax'):
 obj=bpy.data.objects[name];assert obj.type=='CURVE';bpy.data.objects.remove(obj,do_unlink=True)
# Exterior begins on actual film surface; a short lifted arch bends toward a
# mated resistor plug and its -Y boot, never enters back of display/panel.
boot=(1.0,-.406,.77)
tube('resistance plug strain relief',(1.0,-.383,.77),(1.0,-.443,.77),.022,'black')
bent_cable('glass to resistance exterior lead',[
 left,(-1.68,-.66,.69),(-1.46,-.89,.86),(-.85,-.99,1.12),
 (-.16,-1.03,1.11),(.46,-.81,.89),(1.0,-.58,.77),boot,res],.014,'gold',.19)
# The existing scope front analog input center is the ONLY chosen receiver.
# Last three controls are coaxial +Y through the plug boot into BNC ring.
bent_cable('glass to analog input exterior coax',[
 right,(.13,-.69,1.54),(.38,-1.08,1.26),(1.17,-1.22,.78),
 (1.97,-1.10,.41),(2.49,-.80,.34),(2.58,-.466,.34),analog],.014,'black',.19)
s=bpy.context.scene;s.render.filepath=str(p/'overview_v06_build_only.png');s.render.resolution_x=1100;s.render.resolution_y=800
bpy.context.preferences.filepaths.save_version=0
bpy.ops.wm.save_as_mainfile(filepath=str(p/'scene_v06.blend'))
# Independent saved-scene reload renders versioned pixels separately.
