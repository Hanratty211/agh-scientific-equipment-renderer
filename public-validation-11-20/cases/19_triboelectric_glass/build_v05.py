"""Preserve existing tilted film/real matrix anchors/regulator and lead start points.
Replace only readout boxes, make scope analog BNC-like input with mated plug.
"""
import bpy,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from scene_parts_v03 import *
from physical_parts_v01 import bind_existing_materials,signal_scope,resistance_substituter
p=Path(__file__).resolve().parent;bpy.ops.wm.open_mainfile(filepath=str(p/'scene_v04.blend'))
bind_existing_materials()
for o in list(bpy.data.objects):
 if o.name.startswith(('resistance substituter','resistance selector knob','oscilloscope','scope side controls','QA resistor terminal','QA scope terminal','visible signal to resistance socket','visible signal to scope socket')):bpy.data.objects.remove(o,do_unlink=True)
resistance_substituter('resistance substituter',(1.32,.10,.53),(1.24,.75,.79))
scope=signal_scope('representative Keysight DSOX1204A front',(3.0,.10,.63),(1.33,.76,1.04),(2.58,-.294,.34),'black')
# Actual CH number not in source: one representative analog input, not knob/screen.
# Visible electrode to substituter and visible other electrode to scope; unknown
# hidden ground and exact 1:10 GTP-100A-4 probe positioning stay unresolved.
film=bpy.data.objects['TeRC transparent coating'];from mathutils import Vector
bpy.context.view_layer.update();left=tuple(film.matrix_world@Vector((-1.00,-.55,.005)));right=tuple(film.matrix_world@Vector((1.00,-.55,.005)))
ring=flat_ring('resistance actual terminal ring',(1.0,-.287,.77),.047,.023,.018,'gold');ring.rotation_euler[0]=1.5707963
cylinder('resistance actual seated plug',(1.0,-.341,.77),.029,.075,'black',rotation=(1.5707963,0,0))
polyline('glass to resistance exterior lead',[left,(-.70,-.83,1.20),(.25,-.87,.96),(.94,-.47,.78),(1.0,-.38,.77),(1.0,-.287,.77)],.014,'gold')
polyline('glass to analog input exterior coax',[right,(.36,-.86,1.28),(1.34,-.96,.65),(2.26,-.82,.40),scope['signal']['cable_start'],scope['signal']['input_center']],.014,'black')
s=bpy.context.scene;s.render.filepath=str(p/'overview_v05.png');s.render.resolution_x=1100;s.render.resolution_y=800
bpy.context.preferences.filepaths.save_version=0
bpy.ops.wm.save_as_mainfile(filepath=str(p/'scene_v05.blend'));bpy.ops.render.render(write_still=True)
