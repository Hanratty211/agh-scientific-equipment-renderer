"""R1 bounded repair: start from frozen v04 scene; replace disconnected pump
assemblies with coaxial barrel→nozzle→tube; retain feed tubes; cut open laptop
side port into the actual metal base and route DATA outside its lid.
"""
import sys
from pathlib import Path
import bpy
from mathutils import Vector
p=Path(__file__).resolve().parent
sys.path.insert(0,str(p.parent))
from scene_parts_v03 import *
from physical_parts_v01 import bind_existing_materials
from physical_parts_r1 import bent_cable,true_data_port,syringe_axis_chain
bpy.ops.wm.open_mainfile(filepath=str(p/'scene_v04.blend'));bind_existing_materials()
# Earlier broad-prefix deletion removed original feed tubes. v04 restores curves;
# here assert BOTH surviving; never use pump prefix to remove a connected route.
for label in ('upper','lower'):
 assert bpy.data.objects.get(label+' pump to capillary') is not None, 'source feed route lost'
 # Source-facing v04 barrel and v04 tip are genuinely separated; move barrel to
 # route-facing axis at y=0,z=old nozzle z while keeping chassis/outer layout.
 barrel=bpy.data.objects[label+' syringe pump mounted syringe barrel']
 assert barrel.type=='MESH'
 # Old cylinders used local Z and rotation Y=pi/2; x length is local Z,
 # so set native cylinder dimensions BEFORE rotation, not world-axis dimensions.
 barrel.rotation_euler=(0,0,0)
 route_obj=bpy.data.objects[label+' pump to capillary'];spline=route_obj.data.splines[0]
 outlet=Vector(spline.points[0].co[:3]);length=.66;barrel.location=(outlet.x-.215-length/2,0,outlet.z)
 # v04 barrel was already X-oriented. Its old length was only 0.495;
 # X scaling is applied to a real mesh, not stored as a custom declaration.
 barrel.dimensions=(.146,.146,length);barrel.rotation_euler[1]=1.57079632679;bpy.context.view_layer.update()
 for name in (label+' visible syringe tip',label+' pump exit'):
  o=bpy.data.objects.get(name)
  if o:bpy.data.objects.remove(o,do_unlink=True)
 chain=syringe_axis_chain(label+' pump',barrel.location,length,tuple(outlet),axis_sign=1)
 # Keep a small *non-rendering* audit point on actual nozzle metal surface. The
 # port itself in record binds to open metal outlet seat, not an isolated proxy.
 # Both fluid feeds continue from nozzle interior to previous capillary inlets.
# Remove v04's black data-pad and solid silver port-block; create real aperture.
base=bpy.data.objects['laptop base']
for name in ('laptop representative DATA receptacle','laptop DATA port surround','laptop DATA data socket','laptop DATA seated data plug','laptop DATA cable boot','camera to laptop exterior DATA cable'):
 o=bpy.data.objects.get(name)
 if o:bpy.data.objects.remove(o,do_unlink=True)
assert bpy.data.objects.get('laptop left rim')
bpy.data.objects.remove(bpy.data.objects['laptop left rim'],do_unlink=True)
left=base.location.x-base.dimensions.x/2
socket=true_data_port('laptop DATA',base,(left,-.18,.234),axis='left')
# Camera socket/plug: retain original body but route starts from actual boot,
# not arbitrarily from visual body center. Camera rear-facing socket is on +X.
cam=bpy.data.objects['camera representative DATA data socket'];boot=bpy.data.objects['camera representative DATA cable boot']
# Exterior cable first heads along camera plug's -X axis; then behind apparatus
# on +Y until far left of laptop; approach its LEFT socket along +X.
cam_outer=Vector((boot.location.x-.05,boot.location.y,boot.location.z))
lap_outer=Vector(socket['boot_end'])
anchors=[tuple(cam.location),tuple(boot.location),tuple(cam_outer),(-.50,1.02,2.78),
 (1.54,1.20,2.39),(2.25,1.23,1.36),(2.43,1.22,.58),
 (2.44,.44,.35),(lap_outer.x-.18,lap_outer.y,.234),tuple(lap_outer),tuple(socket['seat'])]
bent_cable('camera to laptop exterior DATA cable',anchors,.014,'black',tension=.20)
s=bpy.context.scene;s.render.filepath=str(p/'overview_v05.png');s.render.resolution_x=1140;s.render.resolution_y=720
bpy.context.preferences.filepaths.save_version=0
bpy.ops.wm.save_as_mainfile(filepath=str(p/'scene_v05.blend'));bpy.ops.render.render(write_still=True)
