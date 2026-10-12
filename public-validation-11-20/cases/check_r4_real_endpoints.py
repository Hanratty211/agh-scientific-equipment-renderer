"""Read-only physical scene geometry probe, not a visual/functional certificate.
Blender --background <saved scene> --python this -- <case-id> <report.json>
Examine mesh surface via evaluated triangles, actual oriented body rear face and
Bezier world matrix/handles/sampled true cubic path. Never accept custom props.
"""
import bpy,json,sys,hashlib,math
from pathlib import Path
from mathutils import Vector
from mathutils.bvhtree import BVHTree
case=int(sys.argv[sys.argv.index('--')+1]);out=Path(sys.argv[sys.argv.index('--')+2]);O=bpy.data.objects;D=bpy.context.evaluated_depsgraph_get();bpy.context.view_layer.update();D.update();C=[]
def check(label,condition,detail):C.append({'check':label,'status':'PASS' if condition else 'FAIL','detail':detail})
def verts(obj):
 e=obj.evaluated_get(D);mesh=e.to_mesh()
 try:return [e.matrix_world@v.co for v in mesh.vertices]
 finally:e.to_mesh_clear()
def bounds(obj):
 v=verts(obj);return [(min(p[i] for p in v),max(p[i] for p in v)) for i in range(3)]
def gap(obj,p):
 e=obj.evaluated_get(D);m=e.to_mesh()
 try:
  v=[e.matrix_world@x.co for x in m.vertices];q=BVHTree.FromPolygons(v,[tuple(poly.vertices) for poly in m.polygons]).find_nearest(p);return (p-q[0]).length if q and q[0] is not None else math.inf
 finally:e.to_mesh_clear()
def cable(name):
 ob=O[name];s=ob.data.splines[0];assert ob.type=='CURVE' and s.type=='BEZIER'
 return [(ob.matrix_world@q.handle_left,ob.matrix_world@q.co,ob.matrix_world@q.handle_right) for q in s.bezier_points],ob.data.bevel_depth
def bezier(a,b,t):return a[2]*(1-t)**3+3*a[2]*(1-t)**2*t+3*b[0]*(1-t)*t*t+b[1]*t**3
def seg_points(a,b,N=100):return [bezier(a,b,i/N) for i in range(N+1)]
if case==12:
 body=O['high speed camera'];s=O['camera representative DATA data socket'];p=O['camera representative DATA seated data plug'];boot=O['camera representative DATA cable boot'];c,r=cable('camera to laptop exterior DATA cable')
 B,S,P,T=[bounds(o) for o in (body,s,p,boot)];center=Vector((sum(S[0])/2,sum(S[1])/2,sum(S[2])/2));rear=B[1][1];front=S[1][0]
 check('actual camera housing rear plane +Y',abs(rear-.265)<.002 and gap(body,Vector((center.x,rear,center.z)))<.002,{'rear_y':rear,'surface_mesh_gap':gap(body,Vector((center.x,rear,center.z))),'socket_front_y':front})
 check('data socket seated on true housing rear',front<=rear+.003 and S[1][1]>rear+.01 and abs(center.x)<B[0][1] and B[2][0]<center.z<B[2][1],{'body':B,'socket':S})
 check('plug enters socket real volume',P[1][0]<S[1][1]-.005 and P[1][1]>S[1][1]+.02 and all(abs(sum(P[i])/2-sum(S[i])/2)<.003 for i in (0,2)),{'socket':S,'plug':P})
 check('boot physically mates plug',T[1][0]<P[1][1]-.003 and T[1][1]>P[1][1]+.03 and all(abs(sum(T[i])/2-sum(P[i])/2)<.003 for i in (0,2)),{'plug':P,'boot':T})
 start=c[0][1];dir0=(c[0][2]-start).normalized();tail=[q for i in range(2) for q in seg_points(c[i],c[i+1])]
 check('cable center begins inside boot volume',all(T[i][0]+.006<start[i]<T[i][1]-.006 for i in range(3)) and gap(boot,start)>.006,{'start_world':list(start),'boot_aabb':T,'boot_surface_gap':gap(boot,start)})
 check('cable exits boot on rear normal +Y',dir0.dot(Vector((0,1,0)))>.995 and c[1][1].y>T[1][1]+.005 and all(abs(q.x-center.x)<.003 and abs(q.z-center.z)<.003 for q in tail[:50]),{'world_handle_tangent':list(dir0),'exterior_waypoint':list(c[1][1]),'boot_exit_y':T[1][1],'max_first_curve_xy':max(abs(q.x-center.x) for q in tail[:50])})
 check('old off-axis wire start removed',abs(start.x-.235)>.01 and start.y>rear+.10,{'world_start':list(start),'old_start':[.235,.278,2.59]})
if case==16:
 wall=O['clear Perspex side'];W=bounds(wall)
 for name,z in [('positive HV',1.16),('return/ground',.56)]:
  boot=O[name+' wall-entry strain relief'];sleeve=O[name+' representative insulating mounting sleeve'];T=bounds(boot);S=bounds(sleeve);c,r=cable(name+' visible external lead');end=c[-1][1];tangent=(end-c[-1][0]).normalized()
  penetration=end.x-T[0][0];center=Vector((sum(T[0])/2,sum(T[1])/2,sum(T[2])/2));approach=seg_points(c[-2],c[-1]);inside=[q for q in approach if T[0][0]<=q.x<=end.x];outside=[q for q in approach if q.x<T[0][0]-.006]
  check(name+' last segment world +X axial',tangent.dot(Vector((1,0,0)))>.995 and abs(c[-2][1].y-center.y)<.002 and abs(c[-2][1].z-center.z)<.002 and all(abs(q.y-center.y)<.003 and abs(q.z-center.z)<.003 for q in approach),{'world_endpoint':list(end),'world_tangent':list(tangent),'predecessor':list(c[-2][1]),'max_radial_curve_offset':max((Vector((0,q.y-center.y,q.z-center.z))).length for q in approach)})
  check(name+' colored end inside actual black boot',T[0][0]+.025<end.x<T[0][1]-.025 and abs(end.y-center.y)<.002 and abs(end.z-center.z)<.002 and gap(boot,end)>.012 and penetration>.04,{'world_endpoint':list(end),'boot_aabb':T,'penetration':penetration,'boot_surface_gap':gap(boot,end),'lead_radius':r})
  check(name+' continuous exterior visible path into boot',len(outside)>1 and len(inside)>4 and all(abs(q.y-center.y)<.003 and abs(q.z-center.z)<.003 for q in inside),{'outside_samples':len(outside),'inside_samples':len(inside),'predecessor_world':list(c[-2][1]),'boot_entrance_x':T[0][0]})
  check(name+' stays outside bored wall; sleeve remains',end.x<W[0][0]-.025 and S[0][0]<W[0][0] and S[0][1]>W[0][1],{'end_x':end.x,'wall_x':W[0],'sleeve_x':S[0]})
status='LIMITED_REAL_GEOMETRY_PASS' if all(x['status']=='PASS' for x in C) else 'FAIL';report={'author':'AGH','case':case,'saved_scene':bpy.data.filepath,'scene_sha256':hashlib.sha256(Path(bpy.data.filepath).read_bytes()).hexdigest(),'status':status,'checks':C,'method':'Evaluated real meshes world-space vertices/BVH, actual cubic Bezier world samples and transformed handles; independent reload. No authored metadata trusted.','not_checked':['Rendered pixel visual acceptance','CAD connector specifications','electrical contact or HV safety','sealed function','hidden line paths']};out.write_text(json.dumps(report,indent=2)+'\n');print('R4_REAL_GEOMETRY',case,status,[x['check'] for x in C if x['status']=='FAIL']);
if status=='FAIL':raise SystemExit(2)
