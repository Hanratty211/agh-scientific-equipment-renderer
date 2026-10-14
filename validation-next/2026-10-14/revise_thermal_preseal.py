"""20 optional PRE-SEAL process-state detail based on v02 final sealed scene.
Same copper wick geometry; exposed interior is preparation cutaway, not final-state transparency.
"""
import bpy,sys
from pathlib import Path
from mathutils import Vector
root=Path(__file__).resolve().parent;sys.path.insert(0,str(root))
import render_core as r
r.M.clear()
for m in bpy.data.materials:
 if m.name.startswith('MAT_'):r.M[m.name[4:]]=m
# Parent is saved v02 final. Remove ONLY final fourth/east seal; fold top foil upwards as preparatory view.
east=bpy.data.objects['Heat_seal_east_final'];bpy.data.objects.remove(east,do_unlink=True)
foil=bpy.data.objects['Flexible_al_plastic_top_foil'];foil.location=(0,.25,1.02);foil.rotation_euler[0]=-.26
foil['prep_state']='lifted top layer for editable 200-mesh wick visibility, not final as-used AHP'
for n in list(bpy.data.objects):
 if n.type=='CAMERA':bpy.data.objects.remove(n,do_unlink=True)
r.camera((4.4,-8.5,5.2),(0,0,.44),7.7)
sc=bpy.context.scene;sc['revision_version']='v02_preseal_detail';sc['view_state']='EXPOSED PRE-SEAL CUTAWAY ONLY, not final product';sc['process_source']='Methods p10-11: three sides sealed, one side open; vacuum/DI-water fill then fourth side sealed';sc['unknown']='Interior wick path and vapor liquid circuit not pictured or functionally verified'
bpy.context.view_layer.update();out=root/'cases/20_thermal/v02_preseal_detail';out.mkdir(exist_ok=True)
bpy.ops.wm.save_as_mainfile(filepath=str(out/'scene.blend'));print('PRESEAL_SAVED',out/'scene.blend',flush=True)
