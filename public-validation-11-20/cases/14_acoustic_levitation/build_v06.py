"""R1 limited correction, source Fig.5(b) actually inspected: microphone→amp→
scope signal input, camera→laptop. No array→amp line in source drawing;
array's electrical drive is unknown, and must not be attached to microphone amp.
"""
import bpy,sys
from pathlib import Path
p=Path(__file__).resolve().parent;sys.path.insert(0,str(p.parent))
from scene_parts_v03 import *
from physical_parts_v01 import bind_existing_materials
from physical_parts_r1 import true_data_port,bent_cable
bpy.ops.wm.open_mainfile(filepath=str(p/'scene_v05.blend'));bind_existing_materials()
# Delete ONLY corrected trajectories and obsolete incorrectly interpreted amp-array
# input. Do not delete the array itself or diaphragm/reflector/photo orientation.
for name in ('array-to-amplifier exterior cable','amplifier array representative input ring','amplifier array seated plug',
 'microphone-to-amplifier exterior cable','camera-to-laptop exterior DATA cable','representative amplifier-to-scope signal lead',
 'laptop representative DATA receptacle','laptop DATA port surround','laptop DATA data socket','laptop DATA seated data plug','laptop DATA cable boot','laptop left rim'):
 o=bpy.data.objects.get(name)
 if o:bpy.data.objects.remove(o,do_unlink=True)
base=bpy.data.objects['laptop base'];left=base.location.x-base.dimensions.x/2
lap=true_data_port('laptop DATA',base,(left,-.12,.174),axis='left')
# The amp outlet (ring at x2.27,y.116,z.43) feeds scope analog input
# at x3.59,y.079,z.35 via plug with tangent in +Y (scope inward). Use
# microphone signal as amp INPUT; array electrical drive not drawn in source.
ampin=(1.68,.116,.70);ampout=(2.27,.116,.43);scope=(3.59,.079,.35)
bent_cable('microphone-to-amplifier exterior cable',[(.08,-1.35,2.42),(.23,-1.37,2.41),
 (.48,-1.55,2.15),(1.12,-1.15,1.17),(1.54,-.44,.82),(1.68,-.13,.70),ampin],.014,'black',.20)
bent_cable('representative amplifier-to-scope signal lead',[ampout,(2.27,-.005,.43),
 (2.27,-.23,.43),(2.61,-.36,.41),(3.17,-.35,.35),(3.59,-.29,.35),
 (3.59,-.172,.35),scope],.014,'black',.19)
# Optical camera's data line passes BEHIND scene and enters laptop from its
# left outward axis, not across its display front. Details remain representative.
cam=bpy.data.objects['camera DATA output data socket'];boot=bpy.data.objects['camera DATA output cable boot']
outer=lap['boot_end']
bent_cable('camera-to-laptop exterior DATA cable',[
 tuple(cam.location),tuple(boot.location),(-3.10,-.25,1.63),(-3.34,-1.68,1.68),
 (-2.90,-2.28,1.48),(-.20,-2.36,1.33),(2.53,-2.31,1.14),
 (3.86,-2.12,.52),(4.00,-.90,.30),(outer[0]-.18,outer[1],outer[2]),outer,lap['seat']],.013,'black',.18)
s=bpy.context.scene;s.render.filepath=str(p/'overview_v06.png');s.render.resolution_x=1140;s.render.resolution_y=830
bpy.context.preferences.filepaths.save_version=0
bpy.ops.wm.save_as_mainfile(filepath=str(p/'scene_v06.blend'));bpy.ops.render.render(write_still=True)
