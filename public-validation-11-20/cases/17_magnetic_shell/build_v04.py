"""Preserve field-axis/hemisphere/fixture. Distinguish DC supply, pump and sensor;
existing visible pneumatic routes remain; coil-current internals unknown.
"""
import bpy,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from scene_parts_v03 import *
from physical_parts_v01 import bind_existing_materials,dc_supply,syringe_drive,chassis
p=Path(__file__).resolve().parent;bpy.ops.wm.open_mainfile(filepath=str(p/'scene_v03.blend'))
bind_existing_materials()
for o in list(bpy.data.objects):
 if o.name.startswith(('left compact DC supply','right red syringe pump','front pressure sensor','red pump syringe interface')):bpy.data.objects.remove(o,do_unlink=True)
dc_supply('representative EA-PSI9200-25T body',(-3.05,0,.50),(1.06,.70,.77))
syringe_drive('right syringe pump',(3.02,.05,.82),(1.10,.81,1.01),'red')
cylinder('red pump syringe interface',(2.44,.05,1.42),.10,.18,'glass',rotation=(0,1.5707963,0))
chassis('front pressure sensor',(2.42,-.91,.34),(.44,.31,.41),'black',screen=False)
# Existing probe of sample→pump & sample→sensor remains at previous owner faces.
# Additional ferrule collar represents visible tube seating rather than hidden pneumatic circuit.
for name,point in [('pressure sensor pneumatic ferrule',(2.23,-.91,.42)),('pump syringe pneumatic ferrule',(2.50,.05,1.42))]:
 sphere(name,point,.045,'silver')
s=bpy.context.scene;s.render.filepath=str(p/'overview_v04.png');s.render.resolution_x=1120;s.render.resolution_y=800
bpy.context.preferences.filepaths.save_version=0
bpy.ops.wm.save_as_mainfile(filepath=str(p/'scene_v04.blend'));bpy.ops.render.render(write_still=True)
