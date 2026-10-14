"""04 v05: targeted repair of v04 failure: blue routes ended on assumed pump port, not real syringe hub face.
Start from saved v04, leave v01-v04 intact. No claimed bore, seal or hidden flow.
"""
import bpy,sys
from pathlib import Path
from mathutils import Vector
root=Path(__file__).resolve().parent
for i in range(5):
 hub=bpy.data.objects[f'Syringe_hub_connector_{i}']
 lo=min((hub.matrix_world@v.co).y for v in hub.data.vertices)
 route=bpy.data.objects[f'Blue_inlet_exterior_{i}'];first=route.data.splines[0].points[0]
 # Only the first point moves from -0.44 assumed cap to the true evaluated hub outer cap (-.01).
 first.co.y=lo
 route['v05_reason']='World-space hub mesh front cap, not assumed nozzle ring; Fig3C external line only'
scene=bpy.context.scene;scene['revision_version']='v05';scene['v05_limit']='Syringe hub face to tube visually linked, five outer fittings meet solid chip boundaries; holes, seals, channel and flow still unverified.';scene['visual_review']='pending_AGH_pixel_review'
bpy.context.view_layer.update();out=root/'cases/04_microfluidics/v05';out.mkdir(exist_ok=True)
bpy.ops.wm.save_as_mainfile(filepath=str(out/'scene.blend'));print('V05_SAVED',out/'scene.blend',flush=True)
