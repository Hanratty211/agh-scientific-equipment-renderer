"""Printer photo arrangement frozen; replace only disconnected laptop slab pair."""
import bpy,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from physical_parts_v01 import bind_existing_materials,laptop
p=Path(__file__).resolve().parent;bpy.ops.wm.open_mainfile(filepath=str(p/'scene_v03.blend'))
bind_existing_materials()
for o in list(bpy.data.objects):
 if o.name.startswith(('laptop keyboard','laptop open screen','laptop display pixels')):bpy.data.objects.remove(o,do_unlink=True)
laptop('adjacent laptop',(3.04,-.80,.30),width=1.84,depth=1.02,angle=1.91,port=False)
s=bpy.context.scene;s.render.filepath=str(p/'overview_v04.png');s.render.resolution_x=1130;s.render.resolution_y=700
bpy.context.preferences.filepaths.save_version=0
bpy.ops.wm.save_as_mainfile(filepath=str(p/'scene_v04.blend'));bpy.ops.render.render(write_still=True)
