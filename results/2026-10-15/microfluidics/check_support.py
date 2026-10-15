"""Supplemental post-revision contact probes. Frozen original 141 contract is unchanged."""
import bpy,sys,json,hashlib
from pathlib import Path
from mathutils import Vector
from mathutils.bvhtree import BVHTree
out=Path(sys.argv[sys.argv.index('--')+1]).resolve();out.parent.mkdir(parents=True,exist_ok=True)
bpy.context.view_layer.update();dg=bpy.context.evaluated_depsgraph_get();checks=[]
def tree(n):
 o=bpy.data.objects[n];ev=o.evaluated_get(dg);m=ev.to_mesh();vs=[ev.matrix_world@v.co for v in m.vertices];t=BVHTree.FromPolygons(vs,[list(p.vertices) for p in m.polygons]);ev.to_mesh_clear();return t
for i in range(5):
 x=.62+.63*i;frame=tree(f'Pump_{i}_frame');barrel=tree(f'Pump_{i}_barrel');gaps=[]
 for y in [.56,.60,.64]:
  a=frame.ray_cast(Vector((x,y,2)),Vector((0,0,-1)),3)[0];b=barrel.ray_cast(Vector((x,y,.25)),Vector((0,0,1)),3)[0]
  gaps.append(b.z-a.z if a is not None and b is not None else None)
 checks.append({'id':f'barrel{i}.support_surface','status':'PASS' if all(g is not None and -.04<=g<=.015 for g in gaps) else 'FAIL','surface_gaps':gaps,'maximum_gap':.015,'maximum_schematic_overlap':.04,'method':'3 evaluated-mesh ray pairs per support; no force/strength claim'})
src=Path(bpy.data.filepath);d={'scene':str(src),'sha256':hashlib.sha256(src.read_bytes()).hexdigest(),'checks':checks,'counts':{s:sum(x['status']==s for x in checks) for s in ['PASS','FAIL']},'scope':'New support probes for visual-revision regression, separate from original 141 contract'};out.write_text(json.dumps(d,indent=2)+'\n');print(d['counts'])
