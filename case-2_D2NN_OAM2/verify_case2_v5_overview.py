#!/usr/bin/env python3
"""Read-only checks on SAVED v5 scene. Geometric checks ≠ visual pass."""
import bpy, math, sys
from pathlib import Path
from mathutils import Vector
from bpy_extras.object_utils import world_to_camera_view
HERE=Path(__file__).resolve().parent
blend=HERE/'render-output'/'scene_case2_v5_overview.blend'
bpy.ops.wm.open_mainfile(filepath=str(blend));bpy.context.view_layer.update()
sc=bpy.context.scene
issues=[];lines=[]
def log(s):lines.append(s);print(s)
def test(label,ok,note=''):
    log(('PASS' if ok else 'FAIL')+' '+label+(' '+note if note else ''))
    if not ok:issues.append(label)
def obj(name):return bpy.data.objects.get(name)
def v_attr(o,name):return Vector(tuple(o[name]))
# Surface intersection: mesh closest surface at declared mirror hit, not bbox face.
for name in ('M1','M2','DMD','BS','SLM','M3'):
    o=obj(name);p=v_attr(o,'optical_hit');inv=o.matrix_world.inverted()
    found,local,normal,idx=o.closest_point_on_mesh(inv @ p)
    distance=(o.matrix_world @ local-p).length if found else float('inf')
    test(name+' optical hit on evaluated mesh',distance<.00005,f'{distance*1000:.4f} mm')
# Compare actual BIG FACE normal to intended optical-plane normal (sign indifferent).
for name in ('M1','M2','M3','SLM','BS'):
    o=obj(name);m=o.matrix_world;nm=m.inverted().transposed().to_3x3()
    poly=max(o.data.polygons,key=lambda f:f.area)
    real=(nm @ poly.normal).normalized()
    expected=v_attr(o,'optical_normal').normalized()
    test(name+' actual plane matches intended',abs(real.dot(expected))>.999,
         f'|dot|={abs(real.dot(expected)):.5f}')
for name,prev,nxt in (('M1','L2','M2'),('M2','M1','DMD'),('M3','BS','L5')):
    o=obj(name);nm=o.matrix_world.inverted().transposed().to_3x3()
    poly=max(o.data.polygons,key=lambda f:f.area)
    n=(nm @ poly.normal).normalized();i=(obj(name).location-obj(prev).location).normalized()
    out=(obj(nxt).location-obj(name).location).normalized()
    r=(i-2*i.dot(n)*n).normalized()
    test(name+' specular direction',r.dot(out)>.999,f'dot={r.dot(out):.5f}')
# SLM is reflective: BS→SLM→BS. No beam through back of SLM.
slm=obj('SLM'); n=(slm.matrix_world.inverted().transposed().to_3x3() @
                   max(slm.data.polygons,key=lambda f:f.area).normal).normalized()
i=(v_attr(slm,'optical_hit')-v_attr(obj('BS'),'optical_hit')).normalized()
r=(i-2*i.dot(n)*n).normalized()
back=(v_attr(obj('BS'),'optical_hit')-v_attr(slm,'optical_hit')).normalized()
test('SLM return toward BS',r.dot(back)>.999,f'dot={r.dot(back):.5f}')
# Three actual renderable coils + BC output fiber + PD cable.
for name in ('MMF_delay_2m_visual_turns','MMF_delay_4m_visual_turns',
             'MMF_delay_6m_visual_turns','MMF_BC_to_PD','PD_to_oscilloscope_electrical'):
    o=obj(name);test(name+' bevelled curve',o is not None and o.type=='CURVE' and o.data.bevel_depth>0,
                     f'bevel={o.data.bevel_depth if o else None}')
# Real ground upper plane, all named device bounding corners must remain above it.
g=obj('ground_table');top=max((g.matrix_world @ v.co).z for v in g.data.vertices)
parts=('laser_housing','L1','L2','M1','M2','DMD','L3','Iris1','L4','HWP',
       'polarizer','BS','SLM','M3','L5','Iris2','L6','L7','Holder','BC_3x1',
       'PD_housing','Oscilloscope')
for name in parts:
    o=obj(name);z=min((o.matrix_world @ Vector(c)).z for c in o.bound_box)
    test(name+' above ground',z>top+1e-5,f'bottom={z:.3f}, ground={top:.3f}')
cam=sc.camera
test('saved overview camera',cam.name=='overview_camera',cam.name)
for name in parts:
    o=obj(name);coords=[world_to_camera_view(sc,cam,o.matrix_world @ Vector(v)) for v in o.bound_box]
    xy=all(0<=p.x<=1 and 0<=p.y<=1 for p in coords)
    depth=all(cam.data.clip_start<=p.z<=cam.data.clip_end for p in coords)
    test(name+' all corners projected and depth',xy and depth,
         f'xy={xy} depth={depth}')
# New v5 changes: actual transmissive lens material and mesh-surface ports.
mat=bpy.data.materials.get('lens_transmissive_ior147')
bs=mat.node_tree.nodes.get('Principled BSDF') if mat else None
trans=bs.inputs['Transmission Weight'].default_value if bs else 0
ior=bs.inputs['IOR'].default_value if bs else 0
test('lens material really transmits',trans>=.9 and 1.4<ior<1.6,
     f'trans={trans:.3f} IOR={ior:.3f}')
for name in ('L1','L2','L3','L4','L5','L6','L7'):
    o=obj(name)
    # Mesh.validate never silently repairs invalid faces in the build script.
    test(name+' biconvex mesh valid',o.type=='MESH' and len(o.data.vertices)>300 and
         not o.data.validate(clean_customdata=False),f'vertices={len(o.data.vertices)}')
    for key in ('entry','exit'):
        p=v_attr(o,key);found,local,n,idx=o.closest_point_on_mesh(o.matrix_world.inverted() @ p)
        delta=(o.matrix_world @ local-p).length if found else 1e9
        test(name+' '+key+' real surface',delta<.00005,f'{delta*1000:.4f} mm')
# Re-derive endpoints from the saved scene, not a beam-axis/bbox proxy.
path=('laser','L1','L2','M1','M2','DMD','L3','Iris1','L4','HWP',
      'polarizer','BS','SLM','BS','M3','L5','Iris2','L6','L7','Holder')
def surface_point(name,typ):
    o=obj(name)
    if name=='laser':
        # The first beam starts at the actual laser-exit box face.
        o=obj('laser_exit'); return None
    if name=='Holder':return None
    if typ in o:return v_attr(o,typ)
    if 'optical_hit' in o:return v_attr(o,'optical_hit')
    return o.matrix_world.translation

def end(o,at_start):
    p=o.data.splines[0].points[0 if at_start else -1]
    return o.matrix_world @ Vector(p.co[:3])
for k,(a,b) in enumerate(zip(path,path[1:])):
    name=f'beam_{k:02d}_{a}_to_{b}';o=obj(name)
    test(name+' exists',o is not None)
    if not o:continue
    p=end(o,True);q=end(o,False)
    for label,part,point,typ in (('source',a,p,'exit'),('target',b,q,'entry')):
        expected=surface_point(part,typ)
        if expected is None:
            surface=obj('laser_exit' if part=='laser' else 'Holder')
            found,loc,n,idx=surface.closest_point_on_mesh(surface.matrix_world.inverted() @ point)
            delta=(surface.matrix_world @ loc-point).length if found else 1e9
        else:delta=(point-expected).length
        test(name+' '+label+' anchor',delta<.00005,f'{delta*1000:.4f} mm')
    r0=o.data.splines[0].points[0].radius*o.data.bevel_depth
    r1=o.data.splines[0].points[-1].radius*o.data.bevel_depth
    test(name+' tapered-end radii',abs(r0-o['width_start_m'])<1e-7 and
         abs(r1-o['width_end_m'])<1e-7,f'{r0*1000:.1f}→{r1*1000:.1f} mm')
    if k+1<len(path)-1:
        nxt=obj(f'beam_{k+1:02d}_{b}_to_{path[k+2]}')
        if nxt:
            if 'entry' in obj(b):
                inside=obj(f'beam_{k:02d}_inside_{b}')
                continuous=(inside is not None and (end(inside,True)-q).length<1e-7 and
                            (end(inside,False)-end(nxt,True)).length<1e-7)
                width=(abs(r1-inside.data.splines[0].points[0].radius*inside.data.bevel_depth)<1e-7 and
                       abs(nxt.data.splines[0].points[0].radius*nxt.data.bevel_depth-r1)<1e-7) if inside else False
            else:
                continuous=(end(nxt,True)-q).length<1e-7
                width=abs(nxt.data.splines[0].points[0].radius*nxt.data.bevel_depth-r1)<1e-7
            test(name+' continues at '+b,continuous and width)
# Cable/fiber positions are saved curve endpoints on actual meshes, not bbox extremes.
for curve,up,dn in (('MMF_delay_2m_visual_turns','Holder','BC_3x1'),
                    ('MMF_delay_4m_visual_turns','Holder','BC_3x1'),
                    ('MMF_delay_6m_visual_turns','Holder','BC_3x1'),
                    ('MMF_BC_to_PD','BC_3x1','PD_optical_input'),
                    ('PD_to_oscilloscope_electrical','PD_output_port','Oscilloscope')):
    o=obj(curve)
    for point,body,where in ((end(o,True),obj(up),'start'),(end(o,False),obj(dn),'end')):
        found,loc,n,idx=body.closest_point_on_mesh(body.matrix_world.inverted() @ point)
        delta=(body.matrix_world @ loc-point).length if found else 1e9
        test(curve+' '+where+' port surface',delta<.00005,f'{delta*1000:.4f} mm')
# Optical body and all flexible lines, including coils, must be fully in camera.
for name in ('MMF_delay_2m_visual_turns','MMF_delay_4m_visual_turns',
             'MMF_delay_6m_visual_turns','MMF_BC_to_PD','PD_to_oscilloscope_electrical'):
    o=obj(name)
    coords=[world_to_camera_view(sc,cam,o.matrix_world @ Vector(p.co[:3]))
            for s in o.data.splines for p in s.points]
    test(name+' every curve point in frame',all(0<=p.x<=1 and 0<=p.y<=1 and p.z>0 for p in coords))
log('NOTE: occlusion/readability/reference visual match require inspection of PNG; not established by geometry.')
log(f'GEOMETRY {len(issues)} failed: {issues}')
(HERE/'verify_case2_v5_overview_results.txt').write_text('\n'.join(lines)+'\n',encoding='utf-8')
sys.exit(1 if issues else 0)
