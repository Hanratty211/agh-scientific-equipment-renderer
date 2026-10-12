"""R4 only two exterior lead-end tails on existing R3 seated wall connectors.
Keep actual bores/sleeves/black boots/whole chamber and all source wiring scope.
Curve ends are now inside boot, with last two controls coaxial +X and colored
portion entering the black boot lumen instead of a lateral bright endcap.
"""
import bpy,sys
from pathlib import Path
from mathutils import Vector
p=Path(__file__).resolve().parent;sys.path.insert(0,str(p.parent))
bpy.ops.wm.open_mainfile(filepath=str(p/'scene_v06.blend'))
for name,z in [('positive HV',1.16),('return/ground',.56)]:
 lead=bpy.data.objects[name+' visible external lead'];boot=bpy.data.objects[name+' wall-entry strain relief'];sleeve=bpy.data.objects[name+' representative insulating mounting sleeve']
 assert lead.type=='CURVE' and boot.type=='MESH' and sleeve.type=='MESH'
 assert abs(boot.location.x+1.745)<.002 and abs(boot.location.y+.51)<.002 and abs(boot.location.z-z)<.002
 spline=lead.data.splines[0];assert spline.type=='BEZIER' and len(spline.bezier_points)==7
 pts=spline.bezier_points
 # Old penultimate y=-.67 forces the last Bezier to emerge beside the boot.
 # Replace only this short end approach; previous five points/path untouched.
 pts[-2].co=(-1.88,-.51,z)
 pts[-2].handle_left=(-1.92,-.51,z);pts[-2].handle_right=(-1.84,-.51,z)
 # Actual black boot extends x=[-1.7955,-1.6945]. Lead center ends x=-1.724
 # inside it (>=.0295 insertion), short of wall outer x=-1.6625.
 pts[-1].co=(-1.724,-.51,z)
 pts[-1].handle_left=(-1.756,-.51,z);pts[-1].handle_right=(-1.692,-.51,z)
 # Blend from previous waypoint; explicitly reset its incoming approach into
 # the now-coaxial penultimate point rather than leaving a misplaced hook.
 pts[-3].handle_right=(pts[-3].co+Vector((.044,.028,0)))
bpy.context.view_layer.update();bpy.context.preferences.filepaths.save_version=0
scene=bpy.context.scene;scene.render.filepath=str(p/'overview_v07_build_only.png')
bpy.ops.wm.save_as_mainfile(filepath=str(p/'scene_v07.blend'))
