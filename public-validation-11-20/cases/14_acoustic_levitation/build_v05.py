"""Whole source layout untouched. Physical camera/amp/scope and coherent laptop;
representative data and analog input plugs, no invented waveform or hidden circuit.
"""
import bpy,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from scene_parts_v03 import *
from physical_parts_v01 import bind_existing_materials,laptop,camera_body,signal_scope,representative_data_seat,chassis,analog_input
p=Path(__file__).resolve().parent;bpy.ops.wm.open_mainfile(filepath=str(p/'scene_v04.blend'))
bind_existing_materials()
for o in list(bpy.data.objects):
 if o.name.startswith(('LEFT high speed camera','LEFT inward camera lens','camera lead owner surface',
 'amplifier electronics','oscilloscope instrument','scope controls','laptop base','laptop open screen','laptop viewing panel',
 'amp microphone socket','amp array socket','laptop input socket','camera-to-laptop visible wire',
 'microphone-to-amplifier visible wire','array-to-amplifier visible wire')):bpy.data.objects.remove(o,do_unlink=True)
camera_body('LEFT high speed camera',(-3.12,-.26,1.55),(.72,.57,.48),front_axis='x')
camplug=representative_data_seat('camera DATA output',(-3.10,.037,1.63),axis='front')
amp=chassis('microphone/array amplifier',(1.93,.48,.51),(1.03,.70,.78),'black',screen=False)
# Distinguish two small signal INPUTs on amp left and one signal OUTPUT right;
# manufacturer and cable standard unknown. Physically recessed/plugged boundaries.
for name,x,z in [('microphone',(1.68),.70),('array',(1.95),.43)]:
 ring=flat_ring('amplifier '+name+' representative input ring',(x,.116,z),.044,.025,.019,'silver');ring.rotation_euler[0]=1.5707963
 cylinder('amplifier '+name+' seated plug',(x,.052,z),.031,.081,'black',rotation=(1.5707963,0,0))
ampmic=(1.68,.116,.70);amparray=(1.95,.116,.43)
ring=flat_ring('amp representative signal output ring',(2.27,.116,.43),.049,.025,.016,'silver');ring.rotation_euler[0]=1.5707963
cylinder('amp OUTPUT mating plug',(2.27,.052,.43),.033,.082,'black',rotation=(1.5707963,0,0))
ampout=(2.27,.116,.43)
scope=signal_scope('representative oscilloscope',(3.22,.48,.55),(1.18,.73,.84),(3.59,.079,.35),'blue')
lap=laptop('laptop',(4.68,-.18,.17),width=1.09,depth=.80,port=True)
lapplug=representative_data_seat('laptop DATA',lap['socket_center'],'left')
polyline('camera-to-laptop exterior DATA cable',[(-3.10,.037,1.63),camplug,(-2.7,.85,1.94),(.2,1.52,1.89),(3.54,1.18,1.14),(4.00,.42,.54),lapplug,lap['socket_center']],.013,'black')
polyline('microphone-to-amplifier exterior cable',[(.08,-1.35,2.42),(.42,-1.33,2.28),(1.17,-.69,1.11),ampmic],.015,'black')
polyline('array-to-amplifier exterior cable',[(-.58,0,2.745),(.66,.84,2.38),(1.74,.72,.99),amparray],.014,'black')
# Drawing supports instrument readout; this representative amp→scope segment is
# explicitly illustrative, not hidden measured waveform or documented cable type.
polyline('representative amplifier-to-scope signal lead',[ampout,(2.52,-.33,.40),(3.53,-.43,.35),(3.59,-.31,.35),scope['signal']['cable_start'],scope['signal']['input_center']],.014,'black')
s=bpy.context.scene;s.render.filepath=str(p/'overview_v05.png');s.render.resolution_x=1140;s.render.resolution_y=830
bpy.context.preferences.filepaths.save_version=0
bpy.ops.wm.save_as_mainfile(filepath=str(p/'scene_v05.blend'));bpy.ops.render.render(write_still=True)
