"""Physical hardware pass: preserve v03 optical/fluid layout, replace pump camera laptop
with structural bodies and representative unverified camera/data plug semantics.
"""
import bpy,sys
from pathlib import Path
from mathutils import Vector
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from scene_parts_v03 import *
from physical_parts_v01 import bind_existing_materials,laptop,camera_body,syringe_drive,representative_data_seat
p=Path(__file__).resolve().parent
bpy.ops.wm.open_mainfile(filepath=str(p/'scene_v03.blend'))
bind_existing_materials()
def remove(prefixes):
 for o in list(bpy.data.objects):
  if any(o.name==s or o.name.startswith(s) for s in prefixes):bpy.data.objects.remove(o,do_unlink=True)
remove(('upper pump','lower pump','high speed camera','laptop ','camera to laptop visible lead','top camera objective','upper syringe','lower syringe'))
for label,loc in [('upper',(-3.0,0,2.02)),('lower',(-3.0,0,.57))]:
 x,y,z=loc;syringe_drive(label+' syringe pump',loc,(1.10,.70,.51),'ivory')
 # Keep old feed tube endpoint and source-supported fitting at x=-2.49; new pump tip inside it.
 cylinder(label+' visible syringe tip',(-2.48,0,z+.40),.057,.17,'silver',rotation=(0,1.5707963,0))
 marker(label+' pump exit',label+' visible syringe tip',(-2.49,0,z+.40),.020,'silver')
# Restore named source-visible fluid feed curves after replacing pump housings.
route('upper pump to capillary',(-2.49,0,2.42),(-.78,0,1.10),'fluid',.023,[(-1.75,0,2.28),(-1.20,0,1.37)])
route('lower pump to capillary',(-2.49,0,.97),(-.43,0,1.10),'fluid',.023,[(-1.74,0,.74),(-.74,0,.76)])
camera_body('high speed camera',(0,0,2.55),(.68,.53,.50))
cylinder('top camera objective',(0,0,2.14),.16,.35,'dark')
# Camera rear face at y=+.265; unverified data port model distinctly NOT C mount.
camplug=representative_data_seat('camera representative DATA',(.235,.278,2.59),axis='left')
camport=(.235,.278,2.59)
# Physical laptop base occupies v03 desk footprint; hinge rooted on base rear edge.
lap=laptop('laptop',(3.50,-.24,.23),width=1.18,depth=.95,port=True)
lapplug=representative_data_seat('laptop DATA',lap['socket_center'],axis='left')
polyline('camera to laptop exterior DATA cable',[camport,camplug,(.83,.70,2.58),(1.84,.95,2.12),(2.76,.74,1.60),(3.10,.27,.67),lapplug,lap['socket_center']],.016,'black')
# Keep complete v03 composition/framing and apparatus; save after camera/geometry.
scene=bpy.context.scene;scene.render.filepath=str(p/'overview_v04.png');scene.render.resolution_x=1140;scene.render.resolution_y=720
bpy.context.preferences.filepaths.save_version=0
bpy.ops.wm.save_as_mainfile(filepath=str(p/'scene_v04.blend'));bpy.ops.render.render(write_still=True)
