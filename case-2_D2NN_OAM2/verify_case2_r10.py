#!/usr/bin/env python3
"""R10 independent Blender counterexamples + read-only saved v3 diagnostics.
Units metres. No edits to saved scene. Exit nonzero on any behavioral-test failure.
"""
import os, math, sys
import bpy, bmesh, bpy_extras
from mathutils import Vector
from pathlib import Path
BASE=Path(__file__).resolve().parent
OUT=BASE/'verify_case2_r10_results.txt'
lines=[]; failures=[]
def emit(s): print(s); lines.append(s)
def check(label, predicate, detail):
    ok=bool(predicate); emit(f"{'PASS' if ok else 'FAIL'} {label}: {detail}")
    if not ok: failures.append(label)

CONTACT_M=0.0005    # 0.5 mm
SURFACE_M=0.000002  # geometric boundary tolerance (2 micrometres)
def cube(name, dims, loc=(0,0,0)):
    bm=bmesh.new(); bmesh.ops.create_cube(bm, size=1)
    bmesh.ops.scale(bm, vec=Vector(dims), verts=bm.verts)
    me=bpy.data.meshes.new(name); bm.to_mesh(me); bm.free()
    ob=bpy.data.objects.new(name,me); bpy.context.scene.collection.objects.link(ob)
    ob.location=loc; bpy.context.view_layer.update(); return ob

def world_faces(obj):
    """Return largest actual evaluated face's world point/normal, inverse transpose.
    Face selection is by transformed polygon area, not local area or a property.
    """
    dep=bpy.context.evaluated_depsgraph_get()
    ev=obj.evaluated_get(dep)
    mesh=ev.to_mesh()
    try:
        m=ev.matrix_world; nmat=m.inverted().transposed().to_3x3()
        best=(-1,None,None)
        for poly in mesh.polygons:
            vs=[m @ mesh.vertices[j].co for j in poly.vertices]
            area=sum((vs[k]-vs[0]).cross(vs[k+1]-vs[0]).length/2
                     for k in range(1,len(vs)-1))
            if area>best[0]:
                best=(area,vs[0],(nmat @ poly.normal).normalized())
        return best
    finally: ev.to_mesh_clear()

def closest_distance(obj, point):
    """Distance to actual mesh surface, not a bbox extreme; None if unsupported."""
    if obj.type!='MESH': return None
    dep=bpy.context.evaluated_depsgraph_get(); ev=obj.evaluated_get(dep)
    im=ev.matrix_world.inverted(); hit, loc, norm, index=ev.closest_point_on_mesh(im @ Vector(point))
    return ((ev.matrix_world @ loc)-Vector(point)).length if hit else None

def target_hits(obj, origin, direction, distance=5):
    """Ray cast a single evaluated mesh, local direction normalized; return world distance.
    Does not move the starting point into a lens. Used for parity and occlusion.
    """
    dep=bpy.context.evaluated_depsgraph_get(); ev=obj.evaluated_get(dep)
    if ev.type!='MESH': return None
    im=ev.matrix_world.inverted(); start=im @ Vector(origin)
    local=(im.to_3x3() @ Vector(direction)).normalized()
    if local.length<1e-12:return None
    hit,p,n,face=ev.ray_cast(start,local,distance=1e6)
    if not hit:return None
    w=ev.matrix_world @ p; d=(w-Vector(origin)).length
    along=(w-Vector(origin)).dot(Vector(direction).normalized())
    return (d,w,n,face) if d<=distance and along>=-1e-8 else None

def strictly_inside(obj, point):
    """Boundary is NOT interior. Bbox only an early rejection; mesh parity decides."""
    if obj.type!='MESH':return False
    near=closest_distance(obj,point)
    if near is None or near<=SURFACE_M:return False
    local=obj.matrix_world.inverted() @ Vector(point)
    corners=obj.bound_box
    if any(local[i]<min(c[i] for c in corners)-1e-8 or
           local[i]>max(c[i] for c in corners)+1e-8 for i in range(3)):return False
    direction=Vector((0.934,0.217,0.281)).normalized(); pos=Vector(point); count=0
    for _ in range(128):
        hit=target_hits(obj,pos,direction,1000)
        if hit is None:break
        count+=1; pos=hit[1]+direction*1e-6
    else: raise RuntimeError('ray parity did not converge')
    return count%2==1

def classify(origin, direction, target, source=None, limit=5):
    """Five exclusive outcomes: contact/gap/penetration/miss/other-first.
    Skip only the specific illustrative beam source; every real obstruction remains.
    """
    origin=Vector(origin); direction=Vector(direction).normalized()
    if direction.length<1e-12:raise ValueError('zero propagation vector')
    target_obj=bpy.data.objects.get(target)
    if target_obj is None:return ('未命中',None,None)
    near=closest_distance(target_obj,origin)
    # At surface, point is contact, never penetration; avoids far-side ray on a lens.
    if near is not None and near<=SURFACE_M:
        return ('接触',target,near)
    if strictly_inside(target_obj,origin):
        return ('穿入',target,near)
    hits=[]
    for obj in bpy.context.scene.objects:
        if obj.name==source or obj.type!='MESH' or obj.hide_render:continue
        got=target_hits(obj,origin,direction,limit)
        if got is not None:hits.append((got[0],obj.name))
    if not hits:return ('未命中',None,None)
    d,name=min(hits)
    if name!=target:return ('先碰其他对象',name,d)
    return ('接触' if d<=CONTACT_M else '间隙',name,d)

def ground_surface_z(ground):
    """Actual transformed opaque planar ground vertices, not object's origin."""
    dep=bpy.context.evaluated_depsgraph_get(); ev=ground.evaluated_get(dep)
    mesh=ev.to_mesh()
    try:return max((ev.matrix_world @ v.co).z for v in mesh.vertices)
    finally:ev.to_mesh_clear()

def projection(camera,obj):
    """All 8 transformed corners. Axial clip and horizontal/vertical separately.
    Occlusion is deliberately a separate check: a visible-switch is not an occlusion test.
    """
    bpy.context.view_layer.update()
    coords=[bpy_extras.object_utils.world_to_camera_view(
        bpy.context.scene,camera,obj.matrix_world @ Vector(v)) for v in obj.bound_box]
    axial=all(camera.data.clip_start <= p.z <= camera.data.clip_end for p in coords)
    horiz=all(0<=p.x<=1 for p in coords)
    vert=all(0<=p.y<=1 for p in coords)
    return axial,horiz,vert

def axis_of_beam(obj):
    """Use CURRENT cylindrical mesh Z axis, sign-aligned with p0→p1 metadata.
    No vector aimed at the target centre, no bbox diagonal or stale p0/p1 axis.
    """
    p0=obj.get('beam_p0'); p1=obj.get('beam_p1')
    if p0 is None or p1 is None or obj.type!='MESH':return None
    axis=obj.matrix_world.to_3x3() @ Vector((0,0,1))
    if axis.length<1e-10:return None
    axis.normalize()
    if axis.dot(Vector(p1)-Vector(p0))<0:axis.negate()
    return axis


def synthetic_checks():
    bpy.ops.wm.read_factory_settings(use_empty=True)
    plate=cube('lens',(.002,.10,.10),(.50,0,0)); front=.499
    emit('Synthetic five-way classifier, all dimensions metres')
    cases=[('surface',(.499,0,0),'接触'),('0.3mm',(.4987,0,0),'接触'),
           ('10mm',(.489,0,0),'间隙'),('inside',(.500,0,0),'穿入')]
    for name,pos,want in cases:
        r=classify(pos,(1,0,0),'lens')
        check(name,r[0]==want,f'expected={want}; got={r}')
    miss=classify((.489,0,0),(-1,0,0),'lens')
    check('miss',miss[0]=='未命中',str(miss))
    # Source indicative beam covers the start; only it is excluded.
    src=cube('beam_source',(.003,.025,.025),(.487,0,0))
    bpy.context.view_layer.update()
    r=classify((.489,0,0),(1,0,0),'lens',source='beam_source')
    check('own illustrative beam excluded',r[0]=='间隙',str(r))
    obstacle=cube('real_obstacle',(.001,.025,.025),(.494,0,0))
    bpy.context.view_layer.update()
    r=classify((.489,0,0),(1,0,0),'lens',source='beam_source')
    check('other obstruction retained',r[0]=='先碰其他对象' and r[1]=='real_obstacle',str(r))
    # Unequal scale & rotation: geometric cross of transformed face edges is independent oracle.
    mirror=cube('mirror',(.003,.08,.08),(-1,0,0))
    mirror.rotation_euler=(.43,.28,.61); mirror.scale=(2.0,.5,1.7)
    bpy.context.view_layer.update()
    area,pt,n=world_faces(mirror)
    poly=max(mirror.data.polygons,key=lambda f:f.area)
    vs=[mirror.matrix_world @ mirror.data.vertices[k].co for k in poly.vertices]
    oracle=(vs[1]-vs[0]).cross(vs[2]-vs[0]).normalized()
    check('inverse-transpose under nonuniform scale', abs(n.dot(oracle))>.99999,
          f'abs dot={abs(n.dot(oracle)):.8f}')
    check('opposite sign same plane',abs(n.dot(-n))>.99999,'abs dot=1')
    ortho=n.cross(Vector((1,0,0)))
    if ortho.length<1e-8:ortho=n.cross(Vector((0,1,0)))
    ortho.normalize()
    check('genuinely perpendicular',abs(n.dot(ortho))<1e-6,f'abs dot={abs(n.dot(ortho)):.8g}')
    wrong=(n+ortho).normalized()
    check('wrong recorded normal rejected',abs(n.dot(wrong))<.95,
          f'abs dot={abs(n.dot(wrong)):.3f}')
    ground=cube('ground_plane',(4,4,.01),(0,0,.1))
    # Change mesh vertices so actual top differs from origin; other objects are test geometry.
    for v in ground.data.vertices:v.co.z+=.05
    below=cube('below_ground',(.03,.03,.03),(0,0,.05))
    bpy.context.view_layer.update()
    top=ground_surface_z(ground)
    check('ground from world vertices, not origin',abs(top-.155)<1e-5 and abs(ground.location.z-.1)<1e-5,
          f'top={top:.9f}, origin={ground.location.z:.9f}')
    check('object hidden below opaque plane',
          max((below.matrix_world @ Vector(v)).z for v in below.bound_box)<top,
          f'object upper bound < ground top={top:.3f}')
    camdata=bpy.data.cameras.new('camera');cam=bpy.data.objects.new('camera',camdata)
    bpy.context.scene.collection.objects.link(cam)
    cam.location=(0,-3,0);cam.rotation_euler=(math.pi/2,0,0)
    camdata.clip_start=.01;camdata.clip_end=10
    centre=cube('centre',(.05,.05,.05),(0,0,0))
    side=cube('offscreen',(.05,.05,.05),(5,0,0))
    behind=cube('behind',(.05,.05,.05),(0,-4,0))
    bpy.context.view_layer.update()
    check('all corners in frame',all(projection(cam,centre)),str(projection(cam,centre)))
    check('offscreen horizontal rejected',not projection(cam,side)[1],str(projection(cam,side)))
    check('behind camera rejected',not projection(cam,behind)[0],str(projection(cam,behind)))

def saved_scene_diagnostics():
    path=BASE/'render-output'/'scene_case2_v3.blend'
    bpy.ops.wm.open_mainfile(filepath=str(path));bpy.context.view_layer.update()
    emit('\nRead-only saved v3 diagnostics; NOT a claim of case-2 correctness')
    for beam,target in [('beam_laser_L1','lens_L1'),('beam_L2_M1','mirror_M1'),
                        ('beam_M2_dmd','dmd'),('beam_slm_M3','mirror_M3')]:
        obj=bpy.data.objects.get(beam)
        if obj is None:emit(f'{beam}: missing');continue
        axis=axis_of_beam(obj)
        if axis is None:emit(f'{beam}: unknown own axis; fail closed');continue
        # Old stored endpoint may be stale after transformations: use current mesh axial end.
        c=Vector((0,0,max(v.co.z for v in obj.data.vertices)))
        endpoint=obj.matrix_world @ c
        result=classify(endpoint,axis,target,source=obj.name)
        emit(f'{beam} → {target}: axis={tuple(round(v,4) for v in axis)}, '
             f'endpoint={tuple(round(v,4) for v in endpoint)}, classification={result}')
    for name in ('mirror_M1','mirror_M2','mirror_M3'):
        obj=bpy.data.objects.get(name)
        if obj is None:continue
        area,p,n=world_faces(obj)
        attr=obj.get('mirror_normal')
        similarity=abs(n.dot(Vector(attr).normalized())) if attr else None
        emit(f'{name} face world n={tuple(round(v,4) for v in n)}; '
             f'recorded abs dot={None if similarity is None else round(similarity,4)}')

# @CHECKS_END@


if __name__=='__main__':
    try:
        synthetic_checks()
        saved_scene_diagnostics()
    except Exception as exc:
        failures.append(f'EXCEPTION: {exc}')
        emit(f'FAIL EXCEPTION: {type(exc).__name__}: {exc}')
        import traceback; emit(traceback.format_exc())
    emit(f'\nASSERTIONS {"PASS" if not failures else "FAIL"}; failures={failures}')
    OUT.write_text('\n'.join(lines)+'\n',encoding='utf-8')
    sys.exit(1 if failures else 0)

