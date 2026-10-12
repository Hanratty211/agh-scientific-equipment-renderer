"""Reopen saved .blend and check ACTUAL mesh locations, ownership, collisions and
connector/wire alignment for physical-model batch. Checks limited to listed geometries.
blender --background scene.blend --python script -- case_id result.json
"""
import bpy,sys,json,math
from mathutils import Vector
from mathutils.bvhtree import BVHTree
n=int(sys.argv[sys.argv.index('--')+1]);dest=sys.argv[sys.argv.index('--')+2]
O=bpy.data.objects;D=bpy.context.evaluated_depsgraph_get();checks=[]
def check(name,ok,detail=None):checks.append({'name':name,'status':'PASS' if ok else 'FAIL','detail':detail})
def gap(obj,point):
 ev=obj.evaluated_get(D);me=ev.to_mesh()
 try:
  pts=[ev.matrix_world@v.co for v in me.vertices];faces=[tuple(p.vertices) for p in me.polygons];q=BVHTree.FromPolygons(pts,faces,all_triangles=False).find_nearest(Vector(point));return (q[0]-Vector(point)).length if q and q[0] is not None else None
 finally:ev.to_mesh_clear()
def loc(name):return (O[name] if isinstance(name,str) else name).matrix_world.translation
def bbox(obj):return [obj.matrix_world@Vector(c) for c in obj.bound_box]
def route(name):
 o=O.get(name)
 if not o or o.type!='CURVE':check(name+' exists',False);return None
 p=[o.matrix_world@Vector(q.co[:3]) for q in o.data.splines[0].points];return p
def mesh_gap_pair(a,b):
 # Nearest face-to-sampled-vertices, on both directions; avoids confusing the
 # center of a long mated plug with its front-end insertion depth.
 ev=a.evaluated_get(D);me=ev.to_mesh()
 try:pa=[ev.matrix_world@v.co for v in me.vertices]
 finally:ev.to_mesh_clear()
 ev=b.evaluated_get(D);me=ev.to_mesh()
 try:pb=[ev.matrix_world@v.co for v in me.vertices]
 finally:ev.to_mesh_clear()
 return min(min(gap(a,v) for v in pb),min(gap(b,v) for v in pa))
def near(name,a,b,limit=.07):
 x,y=loc(a),loc(b);d=(x-y).length;check(name,d<limit,{'distance':d,'limit':limit,'parts':[a,b]})
def connected(route_name,start,end):
 p=route(route_name)
 if not p:return
 a=loc(start);b=loc(end);e=[(p[0]-a).length,(p[-1]-b).length];check(route_name+' endpoints',max(e)<.046,{'distances':e,'start':start,'end':end})
for prefix in (('adjacent laptop',) if n==13 else ('laptop',) if n in (12,14) else ()):
 base=O[prefix+' base'];lid=O[prefix+' lid'];hinge=O[prefix+' full hinge axle'];tip=loc(hinge)
 check(prefix+' hinge contacts base',gap(base,tip)<.08,{'mesh_gap':gap(base,tip)})
 corners=bbox(lid);bottom=min(v.z for v in corners)
 check(prefix+' lid meets hinge',abs(bottom-tip.z)<.08,{'bottom_z':bottom,'hinge_z':tip.z})
 if n in (12,14):
  socket=O[prefix+' representative DATA receptacle'];plug=O[prefix+' DATA seated data plug'];sx=loc(socket);px=loc(plug)
  check(prefix+' socket occupies sidewall',gap(base,sx)<.027,{'gap_to_base_mesh':gap(base,sx)})
  check(prefix+' plug meets socket',mesh_gap_pair(socket,plug)<.027,{'sampled_mesh_gap':mesh_gap_pair(socket,plug)})
  check(prefix+' data not on display',(sx-loc(lid)).length>.25,{'separation_to_display_center':(sx-loc(lid)).length})
if n in (12,14):
 cam='camera representative DATA' if n==12 else 'camera DATA output';camerahousing=O['high speed camera' if n==12 else 'LEFT high speed camera']
 seat=O[cam+' data socket'];plug=O[cam+' seated data plug'];sx=loc(seat);px=loc(plug)
 check('camera socket at housing',gap(camerahousing,sx)<.04,{'mesh_gap':gap(camerahousing,sx)})
 check('camera plug mating',mesh_gap_pair(seat,plug)<.034,{'sampled_mesh_gap':mesh_gap_pair(seat,plug)})
 r='camera to laptop exterior DATA cable' if n==12 else 'camera-to-laptop exterior DATA cable'
 connected(r,cam+' data socket','laptop DATA data socket')
if n==12:
 for label in ('upper','lower'):
  near(label+' pump tube tip',label+' pump exit',label+' visible syringe tip',.03)
  p=route(label+' pump to capillary')
  if p:check(label+' feed at syringe tip',(p[0]-loc(O[label+' pump exit'])).length<.02,{'delta':(p[0]-loc(O[label+' pump exit'])).length})
if n==14:
 for label,readout,output in [('microphone','microphone-to-amplifier exterior cable','microphone cable surface'),('array','array-to-amplifier exterior cable','array upper signal boundary')]:connected(readout,output,'amplifier '+label+' representative input ring')
 connected('representative amplifier-to-scope signal lead','amp representative signal output ring','representative oscilloscope ANALOG INPUT BNC input ring')
if n in (14,19):
 name='representative oscilloscope' if n==14 else 'representative Keysight DSOX1204A front';base=O[name];stem=name+' ANALOG INPUT';ring=O[stem+' BNC input ring'];shell=O[stem+' coax mating shell'];boot=O[stem+' plug strain relief'];p=loc(ring);q=loc(shell);f=min(v.y for v in bbox(base))
 check('scope input is on FRONT not screen',abs(p.y-f)<.06,{'input_y':p.y,'chassis_front_y':f})
 check('scope input and plug coaxial',abs(p.x-q.x)<.002 and abs(p.z-q.z)<.002 and .025<abs(p.y-q.y)<.085,{'ring':list(p),'shell':list(q)})
 check('scope plug and boot inline',(loc(boot)-q).length<.10,{'boot_to_shell':(loc(boot)-q).length})
 cable='representative amplifier-to-scope signal lead' if n==14 else 'glass to analog input exterior coax';pts=route(cable)
 if pts:
  t=pts[-2]-pts[-3];check('scope final cable tangent along connector axis',t.y>0 and abs(t.y)>.7*max(abs(t.x),abs(t.z)),{'approach_vector':list(t)})
  check('scope cable enters actual socket',(pts[-1]-p).length<.025,{'gap':(pts[-1]-p).length})
if n==16:
 for name in ('positive HV','return/ground'):
  shell=O[name+' insulated source plug'];body=O['representative Genvolt 73030 body'];r=route(name+' visible external lead')
  check(name+' plug on supply',gap(body,loc(shell))<.15,{'gap_to_housing':gap(body,loc(shell))})
  if r:check(name+' cable starts at plug',(r[0]-loc(shell)).length<.04,{'gap':(r[0]-loc(shell)).length})
if n==17:
 check('DC supply panel and pneumatic pump distinct',O.get('representative EA-PSI9200-25T body') is not None and O.get('right syringe pump') is not None)
 for name in ('sample to pump visible pneumatic segment','sample to pressure sensor visible segment'):check('source pneumatic route preserved '+name,route(name) is not None)
if n==19:
 connected('glass to resistance exterior lead','QA glass left contact','resistance actual terminal ring')
 connected('glass to analog input exterior coax','QA glass right contact','representative Keysight DSOX1204A front ANALOG INPUT BNC input ring')
result={'scene':bpy.data.filepath,'case':n,'status':'FAIL' if any(q['status']=='FAIL' for q in checks) else 'LIMITED_INTERFACE_GEOMETRY_PASS','checks':checks,'unverified':['pixel legibility and occlusion','exact commercial connector ID if unknown','electrical/flow function and hidden topology']}
open(dest,'w').write(json.dumps(result,indent=2)+'\n');print('INTERFACE',result['status'],'FAIL',sum(q['status']=='FAIL' for q in checks))
if result['status']=='FAIL':raise SystemExit(2)
