"""Only left Genvolt 73030 source housing/visible terminal geometry upgraded.
External termination representative: no confirmed Genvolt legacy connector pinout.
"""
import bpy,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from scene_parts_v03 import *
from physical_parts_v01 import bind_existing_materials,hv_supply
p=Path(__file__).resolve().parent;bpy.ops.wm.open_mainfile(filepath=str(p/'scene_v03.blend'))
bind_existing_materials()
for o in list(bpy.data.objects):
 if o.name.startswith(('external LEFT high voltage DC supply','DC red output terminal','DC green output terminal','visible red DC lead','visible green DC lead')):bpy.data.objects.remove(o,do_unlink=True)
hv_supply('representative Genvolt 73030 body',(-3.09,0,.67),(1.10,.77,.91))
# Connection to source-specified needle/collector is NOT visible through the whole chamber;
# preserve only the exterior lead to the source-visible occlusion boundary.
for name,z,mat,end,via in [('positive HV',.81,'red',(-1.64,-.51,1.16),(-2.06,-.65,1.31)),('return/ground',.51,'mint',(-1.64,-.51,.56),(-2.08,-.71,.45))]:
 start=(-2.817,-.508,z)
 cylinder(name+' insulated source plug',(start[0],start[1]+.025,start[2]),.048,.074,mat,rotation=(1.5707963,0,0))
 tube(name+' short strain relief',start,(start[0],start[1]-.10,start[2]),.031,'black')
 polyline(name+' visible external lead',[start,(start[0],start[1]-.10,start[2]),via,end],.019,mat)
 # Anchor on the actual seated plug, not the distant case shell; the case-to-plug
 # mechanical relation is independently inspected and not a claim about pinout.
 marker('HV '+name+' QA owner',name+' insulated source plug',start,.012,mat)
s=bpy.context.scene;s.render.filepath=str(p/'overview_v04.png');s.render.resolution_x=1090;s.render.resolution_y=850
bpy.context.preferences.filepaths.save_version=0
bpy.ops.wm.save_as_mainfile(filepath=str(p/'scene_v04.blend'));bpy.ops.render.render(write_still=True)
