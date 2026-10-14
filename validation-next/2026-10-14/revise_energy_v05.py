"""Fix saved 16 v04 source cap audit FAIL without mutating v04.
Cap was y=start-.0415, but Bezier start in saved scene failed exact face check.
Re-anchor both source curves to actual world-mesh cap and leave MFC/cell paths untouched.
"""
import bpy
from pathlib import Path
root=Path(__file__).resolve().parent
if bpy.context.scene.get('revision_version')!='v04':raise RuntimeError('expected 16 v04 scene')
for gas in ('CO2_cathode','Ar_anode'):
 socket=bpy.data.objects[gas+'_source_visible_socket']
 low=min((socket.matrix_world@v.co).y for v in socket.data.vertices)
 route=bpy.data.objects[gas+'_gas_source_to_MFC'];p=route.data.splines[0].bezier_points[0]
 # Curve local/world identity at this scene; use inverse matrix once to avoid double transformation.
 from mathutils import Vector
 local=route.matrix_world.inverted()@Vector((socket.location.x,low,socket.location.z))
 p.co=local;route['v05_fix']='visible source cap world mesh to curve world endpoint, no sealed ingress claim'
sc=bpy.context.scene;sc['revision_version']='v05';sc['visual_review']='pending_external_pixel_review';sc['revision_reason']='v04 independent audit found both source ends FAIL; move endpoints only'
bpy.context.view_layer.update();out=root/'cases/16_energy_nature/v05'
if out.exists():raise RuntimeError('no overwrite')
out.mkdir();bpy.ops.wm.save_as_mainfile(filepath=str(out/'scene.blend'));print('ENERGY_V05_SAVED',flush=True)
