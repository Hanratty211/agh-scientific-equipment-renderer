#!/usr/bin/env python3
"""Read-only checks on SAVED v10 scene. Geometric checks ≠ visual pass."""
import bpy, math, sys, hashlib, json
from pathlib import Path
from mathutils import Vector
from bpy_extras.object_utils import world_to_camera_view
HERE=Path(__file__).resolve().parent
blend=HERE/'render-output'/'scene_case2_v10_overview.blend'
base=HERE/'render-output'/'scene_case2_v9_overview.blend'
def frozen_fingerprint():
    # Shape/pose/anchors of frozen devices, plus ALL beam centerline samples.
    # Deliberately exclude material and beam radius: those are this round's edits.
    def rnd(values):return [round(float(x),9) for x in values]
    data={}
    for ob in bpy.data.objects:
        if ob.name.startswith('beam_'):continue
        item={'matrix':rnd(x for row in ob.matrix_world for x in row),'type':ob.type}
        if ob.type=='MESH':item['vertices']=[rnd(v.co) for v in ob.data.vertices]
        if ob.type=='CURVE':
            item['splines']=[[rnd(p.co)+[round(p.radius,9)] for p in sp.points]
                              for sp in ob.data.splines]
            item['bevel_depth']=round(ob.data.bevel_depth,9)
        if ob.type=='CAMERA':
            item['ortho_scale']=round(ob.data.ortho_scale,9)
        for key in ('entry','exit','optical_hit','optical_normal','aperture_center'):
            if key in ob:item[key]=rnd(ob[key])
        data[ob.name]=item
    data['__camera_render__']=(bpy.context.scene.camera.name,
        bpy.context.scene.render.resolution_x,bpy.context.scene.render.resolution_y,
        round(bpy.context.scene.view_settings.exposure,9))
    for ob in bpy.data.objects:
        if ob.name.startswith('beam_'):
            data[ob.name]={'axis_points':[rnd(p.co) for p in ob.data.splines[0].points]}
    return data
bpy.ops.wm.open_mainfile(filepath=str(base));bpy.context.view_layer.update()
old_geometry=frozen_fingerprint()
bpy.ops.wm.open_mainfile(filepath=str(blend));bpy.context.view_layer.update()
new_geometry=frozen_fingerprint()
sc=bpy.context.scene
issues=[];lines=[]
def log(s):lines.append(s);print(s)
def test(label,ok,note=''):
    log(('PASS' if ok else 'FAIL')+' '+label+(' '+note if note else ''))
    if not ok:issues.append(label)
def obj(name):return bpy.data.objects.get(name)
def v_attr(o,name):return Vector(tuple(o[name]))
old_hash=hashlib.sha256(json.dumps(old_geometry,sort_keys=True).encode()).hexdigest()
new_hash=hashlib.sha256(json.dumps(new_geometry,sort_keys=True).encode()).hexdigest()
test('v9 nonbeam scene geometry, camera and all beam centerlines frozen',
     old_geometry==new_geometry,f'v9={old_hash[:16]} v10={new_hash[:16]}')
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
test('only one camera and one image render configured',
     len([o for o in bpy.data.objects if o.type=='CAMERA'])==1 and
     (sc.render.resolution_x,sc.render.resolution_y)==(1280,660))
screen=[]
for name in parts:
    o=obj(name);coords=[world_to_camera_view(sc,cam,o.matrix_world @ Vector(v)) for v in o.bound_box]
    screen.extend(coords)
    xy=all(0<=p.x<=1 and 0<=p.y<=1 for p in coords)
    depth=all(cam.data.clip_start<=p.z<=cam.data.clip_end for p in coords)
    test(name+' all corners projected and depth',xy and depth,
         f'xy={xy} depth={depth}')
occupancy=max(p.y for p in screen)-min(p.y for p in screen)
test('vertical frame occupancy improved while whole parts fit',occupancy>.70,
     f'v10_y_range={min(p.y for p in screen):.4f}..{max(p.y for p in screen):.4f}; occupancy={occupancy:.4f}')
# Orthographic corner rays must reach the top surface inside the extended
# ground plane, otherwise a desk edge may remain in frame.
frame=cam.data.view_frame(scene=sc)
direction=-(cam.matrix_world.to_3x3() @ Vector((0,0,1))).normalized()
plane=obj('ground_table');world_corners=[plane.matrix_world @ Vector(v) for v in plane.bound_box]
lo_x=min(p.x for p in world_corners);hi_x=max(p.x for p in world_corners)
lo_y=min(p.y for p in world_corners);hi_y=max(p.y for p in world_corners)
for j,corner in enumerate(frame):
    source=cam.matrix_world @ Vector((corner.x,corner.y,0))
    t=(top-source.z)/direction.z
    hit=source+direction*t
    test('table footprint covers camera corner '+str(j),
         t>0 and lo_x+.01<hit.x<hi_x-.01 and lo_y+.01<hit.y<hi_y-.01,
         f'ground_hit=({hit.x:.3f},{hit.y:.3f})')
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
    test(name+' plano-convex mesh valid',o.type=='MESH' and len(o.data.vertices)>300 and
         not o.data.validate(clean_customdata=False),f'vertices={len(o.data.vertices)}')
    for key in ('entry','exit'):
        p=v_attr(o,key);found,local,n,idx=o.closest_point_on_mesh(o.matrix_world.inverted() @ p)
        delta=(o.matrix_world @ local-p).length if found else 1e9
        test(name+' '+key+' real surface',delta<.00005,f'{delta*1000:.4f} mm')
# Re-derive endpoints from the saved scene, not a beam-axis/bbox proxy.
def nozzle_ring_centres():
    o=obj('laser_exit');n=len(o.data.vertices)//4;m=o.matrix_world
    centre=lambda lo:sum((m @ o.data.vertices[k].co for k in range(lo,lo+n)),Vector((0,0,0)))/n
    return centre(0),centre(n)

path=('laser','L1','L2','M1','M2','DMD','L3','Iris1','L4','HWP',
      'polarizer','BS','SLM','BS','M3','L5','Iris2','L6','L7','Holder')
def surface_point(name,typ):
    o=obj(name)
    if name=='laser':
        # The ray begins at the middle of the saved open annular mouth.
        return nozzle_ring_centres()[1]
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
# v10: collinearity is tested on actual saved centres AND surface anchors.
def line_error_mm(p,a,b):
    u=(b-a).normalized();return ((p-a)-u*((p-a).dot(u))).length*1000
def require_axis(title,a,b,names,additional=()):
    probes=[(name,obj(name).matrix_world.translation) for name in names]
    for name in names:
        o=obj(name)
        for attr in ('entry','exit'):
            if attr in o:probes.append((name+' '+attr,v_attr(o,attr)))
    probes+=list(additional)
    for name,p in probes:
        err=line_error_mm(p,a,b)
        test(title+' '+name+' collinear',err<.01,f'{err:.5f} mm')
laser_start=end(obj('beam_00_laser_to_L1'),True)
m1=v_attr(obj('M1'),'optical_hit')
require_axis('laser→M1',laser_start,m1,('L1','L2'))
require_axis('DMD→BS',v_attr(obj('DMD'),'optical_hit'),v_attr(obj('BS'),'optical_hit'),
             ('L3','Iris1','L4','HWP','polarizer'))
require_axis('M3→Holder',v_attr(obj('M3'),'optical_hit'),
             end(obj('beam_18_L7_to_Holder'),False),('L5','Iris2','L6','L7'))
require_axis('BS→SLM',v_attr(obj('BS'),'optical_hit'),v_attr(obj('SLM'),'optical_hit'),())
# Actual planar-versus-curved lens vertices, not name/material-only validation.
for name in ('L1','L2','L3','L4','L5','L6','L7'):
    ob=obj(name);vs=ob.data.vertices;front=[v.co.z for v in vs[:193]]
    plane=max(front)-min(front)
    sag=vs[385].co.z-vs[337].co.z
    test(name+' real plano-convex profile',plane<1e-7 and sag>.003,
         f'front flatness={plane*1000:.6f} mm rear sag={sag*1000:.3f} mm')
# BS is the saved single-quad active surface, NOT its separately named frame.
plate=obj('BS');test('BS active mesh is one quad',plate.type=='MESH' and
                     len(plate.data.polygons)==1 and len(plate.data.vertices)==4)
poly=plate.data.polygons[0]
normal=(plate.matrix_world.inverted().transposed().to_3x3() @ poly.normal).normalized()
hit=v_attr(plate,'optical_hit')
def mesh_ray(ob,origin,target):
    direction=(target-origin).normalized();m=ob.matrix_world;inv=m.inverted()
    v=(inv.to_3x3() @ direction).normalized()
    found,local,n,idx=ob.ray_cast(inv @ origin,v,distance=3)
    world=m @ local if found else None
    return found,world
for label,start_name,end_name in (
    ('forward','beam_10_polarizer_to_BS','beam_11_BS_to_SLM'),
    ('return','beam_12_SLM_to_BS','beam_12_SLM_to_BS')):
    origin=end(obj(start_name),True) if label=='forward' else end(obj(start_name),True)
    dest=end(obj(end_name),False)
    found,where=mesh_ray(plate,origin,dest)
    test('BS '+label+' ray hits SAVED active quad',found and (where-hit).length<.00005,
         f'offset mm={((where-hit).length*1000) if found else float("inf"):.5f}')
inc=end(obj('beam_12_SLM_to_BS'),False)-end(obj('beam_12_SLM_to_BS'),True)
out=end(obj('beam_13_BS_to_M3'),False)-end(obj('beam_13_BS_to_M3'),True)
reflected=(inc.normalized()-2*inc.normalized().dot(normal)*normal).normalized()
test('BS reflection from actual quad polygon normal',reflected.dot(out.normalized())>.999999,
     f'dot={reflected.dot(out.normalized()):.8f}')
frame=[o for o in bpy.data.objects if o.name.startswith('BS_open_frame_')]
test('BS has four separate open frame rails',len(frame)==4)
# Chief and edge sample rays. A frame collision is a hard failure; do not hide segments.
for label,origin,target in (
    ('forward',end(obj('beam_10_polarizer_to_BS'),True),end(obj('beam_11_BS_to_SLM'),False)),
    ('return',end(obj('beam_12_SLM_to_BS'),True),hit)):
    direction=(target-origin).normalized();perp=Vector((-direction.y,direction.x,0))
    offsets=(Vector((0,0,0)),perp*.008,-perp*.008,Vector((0,0,.008)),Vector((0,0,-.008)))
    for j,offset in enumerate(offsets):
        blocked=any(mesh_ray(rail,origin+offset,target+offset)[0] for rail in frame)
        test('BS '+label+' frame-clear sample '+str(j),not blocked)
# v10: independent geometry review of the corrected laser outlet and housing.
housing=obj('laser_housing');nozzle=obj('laser_exit');first=obj('beam_00_laser_to_L1')
base,tip=nozzle_ring_centres();axis=(tip-base).normalized()
first_point=end(first,True);beam_dir=(end(first,False)-first_point).normalized()
test('laser nozzle open valid mesh',nozzle.type=='MESH' and
     len(nozzle.data.vertices)==192 and len(nozzle.data.polygons)==192 and
     not nozzle.data.validate(clean_customdata=False))
test('beam starts at actual open mouth centre',(first_point-tip).length<.00002,
     f'offset mm={(first_point-tip).length*1000:.5f}')
test('nozzle axis matches emitted ray',axis.dot(beam_dir)>.999999,
     f'dot={axis.dot(beam_dir):.8f}')
test('outlet→L1→L2→M1 same axis',max(line_error_mm(p,tip,m1) for p in
     (obj('L1').location,obj('L2').location,v_attr(obj('L1'),'entry'),
      v_attr(obj('L1'),'exit'),v_attr(obj('L2'),'entry'),v_attr(obj('L2'),'exit')))<.01)
nv=nozzle.data.vertices;n=len(nv)//4
inner_r=[(nozzle.matrix_world @ nv[k].co-tip).length for k in range(3*n,4*n)]
width=first.data.splines[0].points[0].radius*first.data.bevel_depth
test('real opening clears red beam',min(inner_r)>width+.001,
     f'inner radius={min(inner_r)*1000:.2f}mm beam radius={width*1000:.2f}mm')
flange=obj('laser_mount_collar');inv=housing.matrix_world.inverted()
found,loc,norm,idx=housing.closest_point_on_mesh(inv @ flange.location)
gap=(housing.matrix_world @ loc-flange.location).length if found else 1e9
test('mount collar on actual housing face',gap<.00005,f'gap={gap*1000:.4f}mm')
found,back=mesh_ray(housing,tip+axis*.00005,tip-axis*.10)
distance=(tip-back).length if found else -1
test('nozzle mounted externally not floating',found and .025<distance<.035,
     f'tip-to-shell={distance*1000:.3f}mm')
perp=Vector((-axis.y,axis.x,0))
for j,offset in enumerate((Vector((0,0,0)),perp*width,-perp*width,
                           Vector((0,0,width)),Vector((0,0,-width)))):
    blocked,_=mesh_ray(housing,tip+axis*.00005+offset,end(first,False)+offset)
    test('laser outgoing ray does not cross solid metal sample '+str(j),not blocked)
bezel=obj('laser_aperture_bezel')
test('visible lip ring centred at opening',(bezel.location-tip).length<.00005,
     f'offset={(bezel.location-tip).length*1000:.5f}mm')
# Targeted envelope causality checks. Widths are visual hypotheses only.
def width(a,b):
    o=next(o for o in bpy.data.objects if o.name.startswith('beam_') and o.name.endswith(a+'_to_'+b))
    return o['width_start_m'],o['width_end_m']
def flat(a,b):return abs(width(a,b)[0]-width(a,b)[1])<1e-9
test('L4 to BS downstream widths are collimated',all(flat(a,b) for a,b in
     (('L4','HWP'),('HWP','polarizer'),('polarizer','BS'))))
r_iris,r_l6=width('Iris2','L6');r6,r7=width('L6','L7');r7out,r_holder=width('L7','Holder')
test('Iris2 narrows then expands to L6',r_iris<.004 and r_iris<r_l6 and
     abs(r_l6-r6)<1e-9,f'{r_iris*1000:.2f}→{r_l6*1000:.2f} mm radii')
test('L6→L7 approximately constant wide radius',flat('L6','L7') and
     .008<=r6<=.012 and abs(r7-r7out)<1e-9,
     f'{r6*1000:.2f}→{r7*1000:.2f} mm radii')
test('L7→Holder focuses at fiber entrance',r7out>r_holder and r_holder<.003,
     f'{r7out*1000:.2f}→{r_holder*1000:.2f} mm radii')
for a,b in (('Iris2','L6'),('L6','L7'),('L7','Holder')):
    beam_ob=next(o for o in bpy.data.objects if o.name.startswith('beam_')
                 and o.name.endswith(a+'_to_'+b))
    radii=[p.radius*beam_ob.data.bevel_depth for p in beam_ob.data.splines[0].points]
    start,stop=width(a,b)
    test(a+'→'+b+' saved envelope has intended interpolated radii',
         len(radii)==17 and max(abs(r-((1-j/16)*start+j/16*stop))
                                for j,r in enumerate(radii))<1e-6)
red=bpy.data.materials['1064nm_schematic_red_not_visible_light']
types={n.bl_idname for n in red.node_tree.nodes}
clear=next(n for n in red.node_tree.nodes if n.bl_idname=='ShaderNodeBsdfTransparent')
em=next(n for n in red.node_tree.nodes if n.bl_idname=='ShaderNodeEmission')
mix=next(n for n in red.node_tree.nodes if n.bl_idname=='ShaderNodeMixShader')
color=clear.inputs['Color'].default_value
links={(l.from_node,l.to_node) for l in red.node_tree.links}
out=next(n for n in red.node_tree.nodes if n.bl_idname=='ShaderNodeOutputMaterial')
test('beam shader neutral transparent, moderate red display and no glossy rod',
     {'ShaderNodeBsdfTransparent','ShaderNodeEmission','ShaderNodeMixShader'}<=types and
     'ShaderNodeBsdfPrincipled' not in types and
     {(clear,mix),(em,mix),(mix,out)}<=links and
     max(abs(color[i]-1.0) for i in range(3))<1e-8 and
     .20<=mix.inputs[0].default_value<=.50 and
     .5<em.inputs['Strength'].default_value<=1.6 and
     em.inputs['Color'].default_value[0]>8*em.inputs['Color'].default_value[1])
for name in ('laser_camera_side_lower_edge','PD_front_lower_seam',
             'Oscilloscope_top_front_edge','M1_dark_rear_support','M2_dark_rear_support'):
    test('cosmetic outline exists '+name,obj(name) is not None)
log('NOTE: v5/v6 laser interface pass is retracted; the v10 nozzle position is schematic.')
log('NOTE: schematic red is not the visible colour of 1064 nm; radii/foci and exit position are modeling assumptions.')
log('NOTE: no Preview, screenshot or new PNG pixel reading was performed; geometry is not a visual pass.')
log(f'GEOMETRY {len(issues)} failed: {issues}')
(HERE/'verify_case2_v10_overview_results.txt').write_text('\n'.join(lines)+'\n',encoding='utf-8')
sys.exit(1 if issues else 0)
