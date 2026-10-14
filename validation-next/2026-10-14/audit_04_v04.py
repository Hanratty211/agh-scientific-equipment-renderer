"""Saved-scene independent boundary/endpoint check for explicit 04 v04 exterior paths.
Runs inside Blender on the saved scene, not on unsaved construction state.
"""
import bpy,json,math,sys,hashlib
from pathlib import Path
from mathutils import Vector
args=sys.argv[sys.argv.index('--')+1:]
if len(args)!=1:raise SystemExit('expected JSON path')
out=Path(args[0]);scene=bpy.context.scene
bpy.context.view_layer.update();dg=bpy.context.evaluated_depsgraph_get();dg.update()
chip=bpy.data.objects['Transparent_microfluidic_chip']
bounds=[(chip.matrix_world@Vector(c)).x for c in chip.bound_box]
xmin,xmax=min(bounds),max(bounds)
results=[];fails=[]
for i,y in enumerate((-.69,-.87,-1.05,-1.23,-1.41)):
 def co(n):
  o=bpy.data.objects[n];s=o.data.splines[0];return [tuple(o.matrix_world@Vector(p.co[:3])) for p in s.points]
 inlet=co(f'Blue_inlet_exterior_{i}');outlet=co(f'Green_outlet_exterior_{i}')
 a=bpy.data.objects[f'Right_panel_fitting_{i}'];b=bpy.data.objects[f'Left_outlet_fitting_{i}']
 # Cylinders rotated about X; their local z extends along world x. Their world-space mesh bounding x is authoritative.
 a_x=[(a.matrix_world@v.co).x for v in a.data.vertices];b_x=[(b.matrix_world@v.co).x for v in b.data.vertices]
 pump=bpy.data.objects[f'Syringe_hub_connector_{i}'];pys=[(pump.matrix_world@v.co).y for v in pump.data.vertices]
 checks={'syringe_hub_to_blue':math.dist(inlet[0],(.62+i*.63,min(pys),.85))<.002,
 'blue_to_outer_fitting':math.dist(inlet[-1],(max(a_x),y,.145))<.002,
 'right_fitting_to_chip':abs(min(a_x)-xmax)<.002,
 'chip_to_left_fitting':abs(max(b_x)-xmin)<.002,
 'left_outer_fitting_to_green':math.dist(outlet[0],(min(b_x),y,.145))<.002,
 'five_y_distinct':sum(abs(y-z)<.001 for z in (-.69,-.87,-1.05,-1.23,-1.41))==1}
 results.append({'channel':i,'checks':checks,'inlet_endpoints':[inlet[0],inlet[-1]],'outlet_start':outlet[0],
 'chip_x':[xmin,xmax],'right_x':[min(a_x),max(a_x)],'left_x':[min(b_x),max(b_x)],'pump_outer_y':min(pys)})
 fails +=[f'{i}:{k}' for k,v in checks.items() if not v]
report={'source_scene':str(Path(bpy.data.filepath).resolve()),'scene_sha256':hashlib.sha256(Path(bpy.data.filepath).read_bytes()).hexdigest(),'results':results,'fails':fails,
'unknown':'No bores/internal fluid channel or joint seal checks; pixel visibility and scientific correctness not tested'}
out.write_text(json.dumps(report,indent=2,ensure_ascii=False));print('BOUNDARY_AUDIT',json.dumps({'fails':fails}),flush=True)
if fails:raise SystemExit(2)
