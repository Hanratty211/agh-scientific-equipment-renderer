"""Codex independent read-only probe of the saved v01 electrolyzer geometry."""
import bpy, bmesh, json
from pathlib import Path
from mathutils import Vector
from mathutils.bvhtree import BVHTree
root=Path(__file__).resolve().parents[1]
obj=bpy.data.objects['exploded 2 silicone gasket']
deps=bpy.context.evaluated_depsgraph_get(); ev=obj.evaluated_get(deps); mesh=ev.to_mesh()
pts=[ev.matrix_world @ v.co for v in mesh.vertices]
tree=BVHTree.FromPolygons(pts,[tuple(p.vertices) for p in mesh.polygons])
center=obj.matrix_world.translation
out={'scene':bpy.data.filepath,'object':obj.name,
     'world_extent':[max(p[i] for p in pts)-min(p[i] for p in pts) for i in range(3)],
     'probe_meaning':'For the vertical plate silhouette, the intended thin normal is y. A central y ray should be open for a window gasket; this is a directional aperture check only.'}
for axis in [(0,1,0),(0,0,1)]:
 d=Vector(axis);loc,norm,index,dist=tree.ray_cast(center-d*3,d,6)
 out['central_ray_'+str(axis)]={'hits_surface':loc is not None,'hit':list(loc) if loc is not None else None}
bm=bmesh.new();bm.from_mesh(mesh)
out['nonmanifold_edges']=sum(not e.is_manifold for e in bm.edges)
out['edge_count']=len(bm.edges)
bm.free();ev.to_mesh_clear()
(root/'codex-review/probe_v01_stack_results.json').write_text(json.dumps(out,indent=2))
print(json.dumps(out,indent=2))
