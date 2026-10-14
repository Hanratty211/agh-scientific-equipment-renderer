"""Audit saved 04 v06 real exterior surfaces and spline endpoints, not chip internals/pixel quality."""
import bpy,sys,json,hashlib,math
from pathlib import Path
from mathutils import Vector
args=sys.argv[sys.argv.index('--')+1:];out=Path(args[0]);bpy.context.view_layer.update();bpy.context.evaluated_depsgraph_get().update()
def ends(n):
 o=bpy.data.objects[n];sp=o.data.splines[0]
 if sp.type=='BEZIER':p=[sp.bezier_points[0].co,sp.bezier_points[-1].co]
 else:p=[sp.points[0].co.xyz,sp.points[-1].co.xyz]
 return [o.matrix_world@x for x in p]
def bound(n,axis):
 o=bpy.data.objects[n];return [min((o.matrix_world@v.co)[axis] for v in o.data.vertices),max((o.matrix_world@v.co)[axis] for v in o.data.vertices)]
cb=bound('Transparent_microfluidic_chip',0);res=[];fail=[]
for i,y in enumerate((-.69,-.87,-1.05,-1.23,-1.41)):
 blue=ends(f'Blue_inlet_exterior_{i}');green=ends(f'Green_outlet_exterior_{i}')
 hub=bound(f'Syringe_hub_connector_{i}',1);rh=bound(f'Right_panel_fitting_{i}',0);lh=bound(f'Left_outlet_fitting_{i}',0);balloon=bound(f'Green_balloon_schematic_{i}',0)
 checks={'syringe_cap_blue':(blue[0]-Vector((.62+i*.63,hub[0],.85))).length<.003,
 'blue_fitting_lip':(blue[1]-Vector((rh[1],y,.145))).length<.003,
 'right_fitting_chip_wall':abs(rh[0]-cb[1])<.003,
 'left_fitting_chip_wall':abs(lh[1]-cb[0])<.003,
 'left_fitting_green':(green[0]-Vector((lh[0],y,.145))).length<.003,
 'green_to_balloon_body':balloon[0]<green[1].x<balloon[1] and abs(green[1].y-y)<.003,
 'balloon_reach':balloon[0]<-3.7,
 'distinct_channel':sum(abs(y-z)<.001 for z in (-.69,-.87,-1.05,-1.23,-1.41))==1}
 res.append({'channel':i,'checks':checks,'blue_start':list(blue[0]),'blue_end':list(blue[1]),'green_start':list(green[0]),'green_end':list(green[1]),'chip_x':cb,'right_fitting_x':rh,'left_fitting_x':lh,'balloon_x':balloon})
 fail.extend(f'{i}:{k}' for k,v in checks.items() if not v)
scene=Path(bpy.data.filepath);report={'scene_sha256':hashlib.sha256(scene.read_bytes()).hexdigest(),'results':res,'fails':fail,'scope':'External visible mesh-surface and curve-world endpoint geometry only. Spline tangents, overlaps/occlusion, chip bores, seals and flow NOT VALIDATED.'}
out.write_text(json.dumps(report,indent=2));print('V06_EXTERIOR_AUDIT',json.dumps({'fails':fail}),flush=True)
if fail:raise SystemExit(2)
