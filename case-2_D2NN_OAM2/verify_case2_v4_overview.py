#!/usr/bin/env python3
"""Read-only checks on SAVED v4 scene. Geometric checks ≠ visual pass."""
import bpy, math, sys
from pathlib import Path
from mathutils import Vector
from bpy_extras.object_utils import world_to_camera_view
HERE=Path(__file__).resolve().parent
blend=HERE/'render-output'/'scene_case2_v4_overview.blend'
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
log('NOTE: occlusion/readability/reference visual match require inspection of PNG; not established by geometry.')
log(f'GEOMETRY {len(issues)} failed: {issues}')
(HERE/'verify_case2_v4_overview_results.txt').write_text('\n'.join(lines)+'\n',encoding='utf-8')
sys.exit(1 if issues else 0)
