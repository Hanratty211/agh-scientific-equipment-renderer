"""Read-only Blender saved-scene R3: actual BORED WALL + annulus/sleeve + boot
+ existing cable end seating, without relying on centroid/tolerance proxy.
No seal, HV rating or internal-path assertion.
Usage blender --background scene_v06.blend --python this.py -- report.json
"""
import bpy,sys,json,math,hashlib
from pathlib import Path
from mathutils import Vector
from mathutils.bvhtree import BVHTree
out=Path(sys.argv[sys.argv.index('--')+1]);O=bpy.data.objects;scene=bpy.context.scene;D=bpy.context.evaluated_depsgraph_get();bpy.context.view_layer.update();D.update();checks=[]
def add(code,ok,value):checks.append({'code':code,'status':'PASS' if ok else 'FAIL','detail':value})
def ray(obj,p,d,extent):
 ev=obj.evaluated_get(D);inv=ev.matrix_world.inverted();hit,co,normal,index=ev.ray_cast(inv@p,(inv.to_3x3()@d).normalized(),distance=extent)
 return (ev.matrix_world@co) if hit else None
def vertices(obj):
 ev=obj.evaluated_get(D);mesh=ev.to_mesh()
 try:return [ev.matrix_world@v.co for v in mesh.vertices]
 finally:ev.to_mesh_clear()
def surf_gap(obj,pt):
 ev=obj.evaluated_get(D);m=ev.to_mesh()
 try:
  v=[ev.matrix_world@x.co for x in m.vertices];f=[tuple(p.vertices) for p in m.polygons];q=BVHTree.FromPolygons(v,f,all_triangles=False).find_nearest(pt);return (pt-q[0]).length if q and q[0] is not None else math.inf
 finally:ev.to_mesh_clear()
wall=O['clear Perspex side'];bounds=[min(v.x for v in vertices(wall)),max(v.x for v in vertices(wall))]
add('actual original left wall remains',abs(wall.location.x+1.64)<.001 and abs(bounds[0]+1.6625)<.003 and abs(bounds[1]+1.6175)<.003,{'x_bounds':bounds})
for name,z,color in [('positive HV',1.16,'red'),('return/ground',.56,'green')]:
 y=-.51;P=Vector((-1.70,y,z));entry=Vector((-1.6625,y,z));inside=Vector((-1.618,y,z));offset=Vector((-1.70,y+.125,z))
 wall_ray=ray(wall,P,Vector((1,0,0)),.2);side_ray=ray(wall,offset,Vector((1,0,0)),.2)
 add(name+' wall bore at actual entry',wall_ray is None or wall_ray.x>-1.60,{'central_wall_ray':list(wall_ray) if wall_ray else None,'outside_start':list(P)})
 add(name+' intact wall near entry',side_ray is not None and abs(side_ray.x+1.6625)<.008,{'offset_y':offset.y,'side_wall_hit':list(side_ray) if side_ray else None})
 sleeve=O[name+' representative insulating mounting sleeve'];boot=O[name+' wall-entry strain relief'];ring=O['chamber '+color+' boundary'];route=O[name+' visible external lead']
 add(name+' distinct seat/boot real meshes',all(x.type=='MESH' for x in (sleeve,boot,ring)) and all(not x.hide_render for x in (sleeve,boot,ring,wall,route)),{'names':[sleeve.name,boot.name,ring.name]})
 # Bore through insulator sleeve itself: face surface at center of left exit must
 # lie deeper than its outermost exterior face (i.e., lumen, not a solid cap).
 left_face=min(v.x for v in vertices(sleeve));p=Vector((left_face-.01,y,z));q=ray(sleeve,p,Vector((1,0,0)),.16)
 add(name+' insulating sleeve actual axial lumen',q is None or q.x-left_face>.045,{'outermost_x':left_face,'first_axis_hit':list(q) if q else None,'meaning':'no hit means an actually open through-lumen, not a filled cap; wall bore checked independently'})
 # Sleeve crosses the real wall plane on both sides; a physical annular mesh is
 # mounted at cable-facing side, not a floating color dot on transparent sheet.
 sverts=vertices(sleeve);add(name+' sleeve straddles bored wall',min(v.x for v in sverts)<bounds[0]-.01 and max(v.x for v in sverts)>bounds[1]+.005,{'sleeve_x':[min(v.x for v in sverts),max(v.x for v in sverts)],'wall_x':bounds})
 b=route.data.splines[0].bezier_points;p_end=route.matrix_world@b[-1].co;p_before=route.matrix_world@b[-2].co
 add(name+' external lead lands inside boot',(p_end-boot.location).length<.05 and surf_gap(boot,p_end)<.04,{'endpoint':list(p_end),'boot_center':list(boot.location),'surface_gap':surf_gap(boot,p_end)})
 add(name+' guide tangent toward bored sidewall',p_end.x>p_before.x and abs(p_end.y-y)<.004 and abs(p_end.z-z)<.004,{'last_pair':[list(p_before),list(p_end)]})
 add(name+' no lead inside wall',p_end.x<bounds[0]-.008,{'endpoint_x':p_end.x,'wall_outer_x':bounds[0]})
 add(name+' no old colored head',not any(o.name==('chamber red boundary old' if color=='red' else 'chamber green boundary old') for o in O),{'note':'old colored marker was removed by build script; annular ivory boundary retained'})
result={'author':'AGH','scene':bpy.data.filepath,'scene_sha256':hashlib.sha256(Path(bpy.data.filepath).read_bytes()).hexdigest(),'status':'FAIL' if any(c['status']=='FAIL' for c in checks) else 'LIMITED_ENTRY_GEOMETRY_PASS','checks':checks,'not_checked':['actual seal or pressure rating','HV insulation/dielectric/safety/creepage','manufacturer connector specifications','hidden routing to needle and collector','pixel readability']}
out.write_text(json.dumps(result,indent=2)+'\n');print('WALL_R3',result['status'],[(x['code'],x['detail']) for x in checks if x['status']=='FAIL'])
if result['status']=='FAIL':raise SystemExit(2)
