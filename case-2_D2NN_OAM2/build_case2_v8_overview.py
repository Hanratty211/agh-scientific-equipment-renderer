#!/usr/bin/env python3
"""Low-cost wordless Fig.2(a) schematic reconstruction, v8 optical-axis/BS/plano-convex refinement of v5; NOT a measured CAD layout.
Run: /Applications/Blender.app/Contents/MacOS/Blender -b --factory-startup -P build_case2_v8_overview.py
R10 cyan tracing coordinates are NOT imported: device placement is a fresh visual blocking
pass from the original reference, paper p3/4/8/9, and saved uncertainty notes.
"""
import bpy, math, os
from mathutils import Vector
from pathlib import Path
BASE=Path(__file__).resolve().parent
OUT=BASE/'render-output'; OUT.mkdir(exist_ok=True)
bpy.ops.wm.read_factory_settings(use_empty=True)
sc=bpy.context.scene
sc.render.engine='CYCLES'; sc.cycles.samples=24
sc.render.resolution_x=1280; sc.render.resolution_y=720; sc.render.resolution_percentage=100
sc.render.image_settings.file_format='PNG';sc.render.film_transparent=False
sc.view_settings.view_transform='AgX';sc.view_settings.look='AgX - Medium High Contrast'
sc.view_settings.exposure=-0.68
sc.world=bpy.data.worlds.new('warm_light_gray_world');sc.world.use_nodes=True
bg=sc.world.node_tree.nodes.get('Background');bg.inputs['Color'].default_value=(.48,.52,.56,1);bg.inputs['Strength'].default_value=.63

def material(name,color,metal=0,rough=.45, emission=0):
    mat=bpy.data.materials.new(name);mat.diffuse_color=(*color,1);mat.use_nodes=True
    bs=mat.node_tree.nodes.get('Principled BSDF')
    bs.inputs['Base Color'].default_value=(*color,1)
    bs.inputs['Metallic'].default_value=metal;bs.inputs['Roughness'].default_value=rough
    bs.inputs['Emission Color'].default_value=(*color,1)
    bs.inputs['Emission Strength'].default_value=emission
    return mat
METAL=material('housing_graphite',(.13,.18,.23),.45,.38)
BLACK=material('optical_black',(.035,.05,.065),.30,.36)
SILVER=material('anodized_silver',(.43,.49,.55),.55,.32)
SHELL=material('instrument_deep_blue_shell',(.115,.16,.205),.38,.38)
TOP=material('instrument_brushed_top',(.29,.35,.41),.60,.34)
PANEL=material('instrument_front_steel',(.22,.28,.35),.48,.35)
MIRROR=material('mirror_coating_polished',(.72,.79,.84),.92,.11)
HWP_MAT=material('HWP_tinted_plate_visual',(.69,.51,.23),.08,.20)
POL_MAT=material('polarizer_dark_blue_visual',(.14,.28,.37),.14,.19)
GLASS=material('lens_transmissive_ior147',(.73,.89,.94),0,.09)
gbs=GLASS.node_tree.nodes.get('Principled BSDF')
gbs.inputs['Transmission Weight'].default_value=.94
gbs.inputs['IOR'].default_value=1.47
gbs.inputs['Coat Weight'].default_value=.12
RIM=material('lens_edge_blue_silver',(.23,.35,.42),.68,.26)
for mat,t in ((HWP_MAT,.72),(POL_MAT,.52)):
    node=mat.node_tree.nodes.get('Principled BSDF')
    node.inputs['Transmission Weight'].default_value=t
    node.inputs['IOR'].default_value=1.47
WAVE=material('scope_waveform_illustrative_not_data',(.12,.91,.47),0,.27,.35)
RED=material('1064nm_schematic_red_not_visible_light',(.72,.002,.002),0,.52,.015)
FIBER=[material('delay_fiber_a_copper',(.42,.095,.013),.15,.42),material('delay_fiber_b_bronze',(.62,.17,.018),.12,.40),material('delay_fiber_c_amber',(.76,.24,.026),.11,.39)]
CABLE=material('signal_cable_dark',(.07,.12,.20))
SCREEN=material('scope_screen',(.04,.12,.14),0,.2,.15)
GROUND=material('ground_matte',(.40,.44,.48),0,.92)

def box(name,loc,dims,mat,normal=None):
    bpy.ops.mesh.primitive_cube_add(size=1, location=loc);o=bpy.context.object;o.name=name
    o.dimensions=dims
    if normal is not None:o.rotation_euler=Vector(normal).to_track_quat('Z','Y').to_euler()
    bpy.ops.object.transform_apply(location=False,rotation=False,scale=True)
    o.data.materials.append(mat);return o

def cyl(name,loc,r,depth,axis,mat):
    bpy.ops.mesh.primitive_cylinder_add(vertices=32,radius=r,depth=depth,location=loc)
    o=bpy.context.object;o.name=name;o.rotation_euler=Vector(axis).to_track_quat('Z','Y').to_euler()
    o.data.materials.append(mat);return o

def softened(points,steps=8):
    """Endpoint-preserving Catmull-Rom sampler for flexible cables only."""
    pts=[Vector(p) for p in points]
    out=[]
    for j in range(len(pts)-1):
        a=pts[max(j-1,0)];b=pts[j];c=pts[j+1];d=pts[min(j+2,len(pts)-1)]
        for k in range(steps):
            t=k/steps
            out.append(.5*(2*b+(-a+c)*t+(2*a-5*b+4*c-d)*t*t+
                             (-a+3*b-3*c+d)*t*t*t))
    return out+[pts[-1]]

def tube(name,coords,r,mat,smooth=False,radii=None):
    pts=softened(coords) if smooth else list(map(Vector,coords))
    cu=bpy.data.curves.new(name,'CURVE');cu.dimensions='3D';cu.resolution_u=16
    sp=cu.splines.new('POLY');sp.points.add(len(pts)-1)
    for j,(p,v) in enumerate(zip(sp.points,pts)):
        p.co=(*v,1)
        if radii is not None:p.radius=radii[j]
    cu.bevel_depth=r;cu.bevel_resolution=4;cu.use_fill_caps=True
    ob=bpy.data.objects.new(name,cu);sc.collection.objects.link(ob);ob.data.materials.append(mat)
    return ob

def beam(name,a,b,wa,wb):
    """A continuous tapered schematic envelope between actual surface endpoints."""
    if (Vector(a)-Vector(b)).length<1e-8:return None
    count=17
    points=[];radii=[]
    for j in range(count):
        t=j/(count-1)
        points.append(Vector(a).lerp(Vector(b),t))
        radii.append(((1-t)*wa+t*wb)/.004)
    o=tube('beam_'+name,points,.004,RED,radii=radii)
    o['width_start_m']=wa;o['width_end_m']=wb
    return o

def reflect_normal(incoming,outgoing):
    i=Vector(incoming).normalized();o=Vector(outgoing).normalized()
    n=(i-o).normalized();assert n.length>.1
    test=(i-2*i.dot(n)*n).normalized()
    assert (test-o).length<1e-5,(tuple(test),tuple(o))
    return n

# Approximate optical contact points in the reference's two-dimensional arrangement.
# These are a fresh visual blocking pass, NOT R10's off-centre trace coordinates.
# Pixel y controls depth on the table, NOT world height. All apparatus centres z=0.17m.
PIX={'laser':(877,548),'L1':(570,530),'L2':(445,506),'M1':(135,460),
     'M2':(371,429),'DMD':(108,309),'L3':(476,392),'Iris1':(566,411),
     'L4':(692,432),'HWP':(806,453),'polarizer':(890,467),'BS':(985,480),
     'SLM':(1042,480),'M3':(1036,327),'L5':(973,321),'Iris2':(856,295),
     'L6':(744,268),'L7':(575,239),'Holder':(440,228),'BC':(187,187),
     'PD':(473,158),'Oscilloscope':(675,123)}
def point(px,py,z=.17):return Vector(((px-574)*.00185,(420-py)*.00210,z))
P={key:point(*xy) for key,xy in PIX.items()}
# Left-facing exterior outlet is a schematic position, derived from the actual shell.
laser_body=box('laser_housing',P['laser']+Vector((.055,-.047,-.006)),(.22,.125,.082),SHELL)
LASER_AXIS=(P['M1']-P['laser']).normalized()
bpy.context.view_layer.update()
im=laser_body.matrix_world.inverted()
hit,local,n,idx=laser_body.ray_cast(im @ P['laser'],
        (im.to_3x3() @ LASER_AXIS).normalized(),distance=1)
if not hit:raise RuntimeError('laser reference ray missed housing exterior')
LASER_HOUSING_FACE=laser_body.matrix_world @ local
LASER_BASE=LASER_HOUSING_FACE-LASER_AXIS*.001
LASER_TIP=LASER_BASE+LASER_AXIS*.030

def align_on_axis(start,end,names):
    """Project intermediate centres onto the real outlet/target-defined axis."""
    origin=P[start] if isinstance(start,str) else Vector(start)
    u=(P[end]-origin).normalized()
    for name in names:
        old=P[name].copy();P[name]=origin+u*(old-origin).dot(u)
        print('AXIS_SHIFT',name,f'{(P[name]-old).length*1000:.3f} mm')
# Do not connect separate visual estimates into a refracting zigzag.
align_on_axis(LASER_TIP,'M1',('L1','L2'))
align_on_axis('DMD','BS',('L3','Iris1','L4','HWP','polarizer'))
align_on_axis('M3','Holder',('L5','Iris2','L6','L7'))
# A schematic thin-plate BS cannot bend the forward transmitted chief ray.
u=(P['BS']-P['DMD']).normalized();old_slm=P['SLM'].copy()
P['SLM']=P['BS']+u*(old_slm-P['BS']).dot(u)
print('AXIS_SHIFT SLM',f'{(P["SLM"]-old_slm).length*1000:.3f} mm')
def dir_to(a,b):return (P[b]-P[a]).normalized()
def plano_convex_lens(name,center,axis,rad,edge_depth=.003,sag=.0045):
    """Planar incident side, curved outgoing side; shape orientation is illustrative."""
    N=48;verts=[];faces=[]
    verts.append((0,0,-edge_depth/2));front0=0
    levels=(.25,.50,.75,1.)
    for side in (-1,1):
        for u in levels:
            z=-edge_depth/2 if side==-1 else edge_depth/2+sag*(1-u*u)
            for k in range(N):
                a=2*math.pi*k/N;verts.append((rad*u*math.cos(a),rad*u*math.sin(a),z))
    back0=len(verts);verts.append((0,0,edge_depth/2+sag))
    for k in range(N):faces.append((front0,1+(k+1)%N,1+k))
    for layer in range(3):
        for k in range(N):
            a=1+layer*N+k;b=1+layer*N+(k+1)%N
            c=a+N;d=b+N;faces.append((a,b,d,c))
    base=1+4*N
    for k in range(N):
        a=1+3*N+k;b=1+3*N+(k+1)%N
        c=base+3*N+k;d=base+3*N+(k+1)%N
        faces.append((a,c,d,b))
    for layer in range(3):
        for k in range(N):
            a=base+layer*N+k;b=base+layer*N+(k+1)%N
            faces.append((a,b,b+N,a+N))
    last=base+3*N
    for k in range(N):faces.append((back0,last+k,last+(k+1)%N))
    mesh=bpy.data.meshes.new(name+'_plano_convex_mesh');mesh.from_pydata(verts,[],faces);mesh.update()
    if mesh.validate(verbose=True):raise RuntimeError(f'{name}: invalid plano-convex topology')
    ob=bpy.data.objects.new(name,mesh);sc.collection.objects.link(ob)
    ob.location=center;ob.rotation_euler=Vector(axis).to_track_quat('Z','Y').to_euler()
    ob.data.materials.append(GLASS)
    for poly in mesh.polygons:poly.use_smooth=True
    # dark-coated outer rim makes transmitted faces legible.
    bpy.ops.mesh.primitive_torus_add(major_segments=48,minor_segments=10,
                                    location=center,major_radius=rad,minor_radius=.0022)
    rim=bpy.context.object;rim.name=name+'_edge_rim'
    rim.rotation_euler=ob.rotation_euler;rim.data.materials.append(RIM)
    return ob,center-Vector(axis).normalized()*edge_depth/2,center+Vector(axis).normalized()*(edge_depth/2+sag)

def port(name,axis,depth=.010,rad=.029):
    center=P[name]
    if name.startswith('L'):
        optic,i,o=plano_convex_lens(name,center,axis,rad)
    else:
        i=center-Vector(axis).normalized()*depth/2
        o=center+Vector(axis).normalized()*depth/2
        optic=cyl(name,center,rad,depth,axis,GLASS)
    optic['entry']=tuple(i);optic['exit']=tuple(o)
    return i,o

def face(name,point_hit,normal,dims,mat):
    """Thin box actual front -Z face at named optical hit; no bbox extrema."""
    norm=Vector(normal).normalized(); thickness=dims[2]
    body=box(name,Vector(point_hit)+norm*thickness/2,dims,mat,normal=norm)
    body['optical_hit']=tuple(point_hit);body['optical_normal']=tuple(norm)
    return body

def bs_thin_plate(hit,normal):
    """Schematic zero-thickness active plate; housing is an open frame."""
    n=Vector(normal).normalized();mesh=bpy.data.meshes.new('BS_active_quad_mesh')
    hx=.0275;hy=.0325
    mesh.from_pydata([(-hx,-hy,0),(hx,-hy,0),(hx,hy,0),(-hx,hy,0)],[],[(0,1,2,3)])
    mesh.update()
    if mesh.validate(verbose=True):raise RuntimeError('invalid BS active quad')
    o=bpy.data.objects.new('BS',mesh);sc.collection.objects.link(o)
    o.location=hit;o.rotation_euler=n.to_track_quat('Z','Y').to_euler()
    o.data.materials.append(GLASS)
    o['optical_hit']=tuple(hit);o['optical_normal']=tuple(n)
    o['representation']='zero-thickness schematic plate; not a measured prism'
    q=n.to_track_quat('Z','Y')
    for side in (-1,1):
        box(f'BS_open_frame_side_{side}',hit+q @ Vector((side*.034,0,.001)),
            (.009,.082,.005),RIM,normal=n)
        box(f'BS_open_frame_end_{side}',hit+q @ Vector((0,side*.039,.001)),
            (.059,.008,.005),RIM,normal=n)
    return o

def hollow_laser_nozzle(base,tip,axis,outer=.008,bore=.0045):
    """Open-ended annular mesh: emitted ray starts at the visible open lip."""
    N=48;verts=[];faces=[];length=(tip-base).length
    for radius,z in ((outer,-length/2),(outer,length/2),
                     (bore,-length/2),(bore,length/2)):
        verts.extend((radius*math.cos(2*math.pi*k/N),
                      radius*math.sin(2*math.pi*k/N),z) for k in range(N))
    for k in range(N):
        j=(k+1)%N
        faces.extend(((k,j,N+j,N+k),
                      (N+k,N+j,3*N+j,3*N+k),
                      (3*N+k,3*N+j,2*N+j,2*N+k),
                      (2*N+k,2*N+j,j,k)))
    mesh=bpy.data.meshes.new('laser_nozzle_open_annulus')
    mesh.from_pydata(verts,[],faces);mesh.update()
    if mesh.validate(verbose=True):raise RuntimeError('invalid laser outlet annulus')
    ob=bpy.data.objects.new('laser_exit',mesh);sc.collection.objects.link(ob)
    ob.location=(base+tip)/2
    ob.rotation_euler=Vector(axis).to_track_quat('Z','Y').to_euler()
    mesh.materials.append(BLACK)
    ob['outlet_model']='hollow external nozzle, illustrative position'
    ob['aperture_center']=tuple(tip);ob['bore_radius_m']=bore
    return ob

# Form factors: modest visual cues, not measured manufacturer details.
box('laser_top_rail',P['laser']+Vector((.055,-.047,.037)),(.16,.05,.009),BLACK)
# Cosmetic top and front panels; do not intersect the left-going optical axis.
box('laser_top_sheet',P['laser']+Vector((.055,-.048,.036)),(.190,.105,.003),TOP)
box('laser_camera_side',P['laser']+Vector((.055,-.110,-.007)),(.195,.003,.064),PANEL)
box('laser_camera_side_inset',P['laser']+Vector((.055,-.112,-.004)),(.155,.001,.035),SHELL)
nozzle=hollow_laser_nozzle(LASER_BASE,LASER_TIP,LASER_AXIS)
# Registration flange touches and slightly overlaps the REAL housing exit face.
for name,position,major,minor in (
    ('laser_mount_collar',LASER_HOUSING_FACE,.0085,.001),
    ('laser_aperture_bezel',LASER_TIP,.008,.0015)):
    bpy.ops.mesh.primitive_torus_add(major_segments=48,minor_segments=12,
        location=position,major_radius=major,minor_radius=minor)
    ring=bpy.context.object;ring.name=name
    ring.rotation_euler=LASER_AXIS.to_track_quat('Z','Y').to_euler()
    ring.data.materials.append(RIM)
for j in range(4):
    box(f'laser_vent_{j}',P['laser']+Vector((.010+j*.027,-.047,.043)),
        (.012,.048,.0014),METAL)
for name,pre,post in [('L1','laser','L2'),('L2','L1','M1'),('L3','DMD','Iris1'),
                      ('L4','Iris1','HWP'),('L5','M3','Iris2'),('L6','Iris2','L7'),
                      ('L7','L6','Holder')]:
    # Transmission direction follows the local incoming/outgoing segment bisector.
    axis=(dir_to(pre,name)+dir_to(name,post)).normalized()
    if axis.length<.1:axis=dir_to(pre,name)
    port(name,axis,rad=.032 if name in ('L1','L2','L3','L4') else .027)
# Iris apertures: actual annular geometry, not solid disks.
for name,pre,post in [('Iris1','L3','L4'),('Iris2','L5','L6')]:
    axis=(dir_to(pre,name)+dir_to(name,post)).normalized()
    bpy.ops.mesh.primitive_torus_add(major_segments=48,minor_segments=12,
                                   location=P[name],major_radius=.023,minor_radius=.006)
    o=bpy.context.object;o.name=name;o.rotation_euler=axis.to_track_quat('Z','Y').to_euler()
    o.data.materials.append(BLACK)
    o['clear_radius']=.017
# Other transmissive plates on incident free-space path.
for name,pre,post in [('HWP','L4','polarizer'),('polarizer','HWP','BS')]:
    axis=(dir_to(pre,name)+dir_to(name,post)).normalized()
    port(name,axis,depth=.006,rad=.026)
    plate=bpy.data.objects[name];plate.data.materials.clear()
    plate.data.materials.append(HWP_MAT if name=='HWP' else POL_MAT)
    bpy.ops.mesh.primitive_torus_add(major_segments=40,minor_segments=10,
            location=P[name],major_radius=.027,minor_radius=.002)
    trim=bpy.context.object;trim.name=name+'_distinct_frame'
    trim.rotation_euler=axis.to_track_quat('Z','Y').to_euler()
    trim.data.materials.append(SILVER if name=='HWP' else BLACK)

# Reflecting M1/M2/M3: actual final mesh face orientation follows the adjacent rays.
for name,pre,post in [('M1','L2','M2'),('M2','M1','DMD'),('M3','BS','L5')]:
    n=reflect_normal(P[name]-P[pre],P[post]-P[name])
    face(name,P[name],n,(.077,.070,.004),MIRROR)
# DMD micromirror array: outgoing +1 diffraction not ordinary specular reflection.
# Paper gives 12-degree DMD incidence; reference macro-plane normal chosen 12°
# from reverse incident ray in table plane. Micromirror tilt/blaze is not resolved.
i=dir_to('M2','DMD')
angle=math.radians(12); dn=Vector((i.x*math.cos(angle)-i.y*math.sin(angle),
                                   i.x*math.sin(angle)+i.y*math.cos(angle),0))
face('DMD',P['DMD'],dn,(.105,.080,.006),BLACK)
box('DMD_chassis',P['DMD']+dn*.022+Vector((0,0,-.012)),(.135,.10,.025),METAL,normal=dn)
# Outline trim stays away from central optical action point.
for objname,center,norm in [('DMD',P['DMD'],dn)]:
    q=norm.to_track_quat('Z','Y')
    for side in (-1,1):
        off=q @ Vector((side*.053,0,0))
        box(f'{objname}_edge_{side}',center+off,(.005,.084,.005),RIM,normal=norm)
# BS schematic: passes forward toward SLM; deflects returned beam to M3.
# No claim BS separates zero order. Paper: blazed grating on SLM spatially
# separates zero order and target field; dichroic prism+M3 reflect output.
bsn=reflect_normal(P['BS']-P['SLM'],P['M3']-P['BS'])
bs_thin_plate(P['BS'],bsn)
slmn=dir_to('BS','SLM')
face('SLM',P['SLM'],slmn,(.094,.097,.008),BLACK)
box('SLM_chassis',P['SLM']+slmn*.029+Vector((0,0,-.017)),(.123,.122,.033),METAL,normal=slmn)
for side in (-1,1):
    off=slmn.to_track_quat('Z','Y') @ Vector((side*.049,0,0))
    box(f'SLM_edge_{side}',P['SLM']+off,(.005,.10,.006),RIM,normal=slmn)
# Holder and detection bodies
box('Holder',P['Holder'],(.065,.070,.045),BLACK)
box('BC_3x1',P['BC'],(.065,.045,.035),SILVER)
cyl('PD_optical_input',P['PD'],.021,.048,dir_to('BC','PD'),BLACK)
box('PD_housing',P['PD']+Vector((.018,.018,-.006)),(.095,.065,.045),SHELL)
box('PD_front_panel',P['PD']+Vector((.019,-.015,-.005)),(.078,.003,.032),PANEL)
box('PD_top_sheet',P['PD']+Vector((.018,.018,.018)),(.089,.060,.003),TOP)
bpy.ops.mesh.primitive_torus_add(major_segments=32,minor_segments=10,
    location=P['PD']+dir_to('PD','BC')*.023,major_radius=.024,minor_radius=.002)
ring=bpy.context.object;ring.name='PD_input_ring'
ring.rotation_euler=dir_to('PD','BC').to_track_quat('Z','Y').to_euler()
ring.data.materials.append(RIM)
box('PD_output_port',P['PD']+Vector((.053,.014,.008)),(.013,.021,.013),BLACK)
box('Oscilloscope',P['Oscilloscope'],(.22,.115,.125),SHELL)
box('Oscilloscope_top_sheet',P['Oscilloscope']+Vector((0,0,.064)),(.215,.110,.004),TOP)
box('Oscilloscope_front_panel',P['Oscilloscope']+Vector((0,-.059,0)),(.214,.004,.115),PANEL)
box('Oscilloscope_bezel',P['Oscilloscope']+Vector((-.020,-.063,.014)),(.147,.006,.087),BLACK)
box('Oscilloscope_display',P['Oscilloscope']+Vector((-.020,-.068,.014)),(.128,.004,.068),SCREEN)
# Illustrative waveform is not a measured trace from the paper.
wpts=[]
for k in range(32):
    x=-.076+k*.0036
    z=.015+.006*math.sin(k*.54)+(.018 if k in (8,9,20,21) else 0)
    wpts.append(P['Oscilloscope']+Vector((x,-.071,z)))
tube('Oscilloscope_screen_waveform_illustrative',wpts,.0010,WAVE,smooth=True)
for j in range(3):
    cyl(f'Oscilloscope_front_knob_{j}',P['Oscilloscope']+Vector((.076,-.069,.045-j*.032)),
        .008,.006,(0,-1,0),BLACK)
# Surface points are literal mesh-surface centres for mirrors/DMD/BS/SLM.
def surface_toward(name,other):
    """Actual mesh face toward other world point, no bounding-box extreme."""
    ob=bpy.data.objects[name];c=ob.matrix_world.translation
    direction=(Vector(other)-c).normalized();outside=c+direction*.30
    im=ob.matrix_world.inverted()
    local=(im.to_3x3() @ (-direction)).normalized()
    hit,p,n,face=ob.ray_cast(im @ outside,local,distance=1e3)
    if not hit:raise RuntimeError(f'{name}: interface ray missed real mesh')
    return ob.matrix_world @ p

def inport(name):
    ob=bpy.data.objects.get(name)
    if ob and 'entry' in ob:return Vector(ob['entry'])
    if name=='Holder':return surface_toward(name,P['L7'])
    return P[name]
def outport(name):
    ob=bpy.data.objects.get(name)
    if ob and 'exit' in ob:return Vector(ob['exit'])
    if name=='laser':return LASER_TIP.copy()
    return P[name]



# @PARTS@
# Continuous source→DMD→SLM→BS-return→M3→fiber focal holder schematic.
# Beam segments end at mesh surfaces. Glass segments are explicitly present through
# transmissive optics; reflective SLM path returns to BS (not through SLM chassis).
path=('laser','L1','L2','M1','M2','DMD','L3','Iris1','L4','HWP',
      'polarizer','BS','SLM','BS','M3','L5','Iris2','L6','L7','Holder')
# Schematic radii (metres), NOT measured beam waists/focal lengths. Adjacent
# segments share radii exactly at each optic; they are topologically continuous.
WIDTH={'laser':.0020,'L1':.0045,'L2':.0090,'M1':.0090,'M2':.0092,
       'DMD':.0110,'L3':.0100,'Iris1':.0035,'L4':.0080,
       'HWP':.0080,'polarizer':.0080,'BS':.0080,'SLM':.0080,
       'M3':.0080,'L5':.0080,'Iris2':.0034,'L6':.0080,'L7':.0070,'Holder':.0016}
for k,(a,b) in enumerate(zip(path,path[1:])):
    src=outport(a);dst=inport(b)
    beam(f'{k:02d}_{a}_to_{b}',src,dst,WIDTH[a],WIDTH[b])
    ob=bpy.data.objects.get(b)
    if ob and 'entry' in ob and 'exit' in ob:
        beam(f'{k:02d}_inside_{b}',inport(b),outport(b),WIDTH[b],WIDTH[b])
# SLM return overlaps its incoming segment by necessity in this economical schematic.
# This is a reflection; BS redirects the return toward M3, not an invented zero-order port.

# Three continuous, bevelled curves from three Holder ports to three BC ports.
# Coil diameters/turns are visual shorthand; they are NOT physical 2/4/6 m drawings.
for j,(label,turns) in enumerate((('2m',2),('4m',3),('6m',4))):
    dz=(j-1)*.008
    def fp(x,y):return point(x,y,.17+dz)
    start=surface_toward('Holder',point(397,213+(j-1)*10))
    finish=surface_toward('BC_3x1',point(249,184+(j-1)*12))
    cc=fp(320+(j-1)*18,200+(j-1)*18)
    base_radius=.025+j*.004
    pts=[start,fp(397,213+(j-1)*10),cc+Vector((base_radius,0,0))]
    for k in range(1,turns*48+1):
        t=k/(turns*48);a=2*math.pi*k/48
        # Evolving radius, drift and height keep successive coils distinguishable.
        radius=base_radius+.024*t
        pts.append(cc+Vector((radius*math.cos(a)-.015*t,
                              radius*.72*math.sin(a)+.008*t,.003*t)))
    pts.extend((fp(249,184+(j-1)*12),finish))
    fiber=tube(f'MMF_delay_{label}_visual_turns',pts,.0033,FIBER[j],smooth=True)
    fiber['upstream']='Holder';fiber['downstream']='BC_3x1'
    fiber['length_label']=label;fiber['loop_dimensions']='illustrative not measured'
# Single continuous output MMF (BC→PD); dark electrical cable (PD→oscilloscope).
optic_fiber=tube('MMF_BC_to_PD',[surface_toward('BC_3x1',point(131,141)),point(131,141),point(174,111),
                                  point(336,123),point(405,144),surface_toward('PD_optical_input',point(405,144))],
                                  .0032,FIBER[1],smooth=True)
optic_fiber['upstream']='BC_3x1';optic_fiber['downstream']='PD_optical_input'
signal=tube('PD_to_oscilloscope_electrical',[
                 surface_toward('PD_output_port',P['Oscilloscope']),
                 point(530,182,.184),point(600,201,.19),point(685,168,.19),
                 surface_toward('Oscilloscope',point(685,168,.19))],
                 .0022,CABLE,smooth=True)
signal['kind']='electrical_signal_not_optical'

# Shallow gray table, every optical part and fiber above its ACTUAL top face.
box('ground_table',(0,.03,-.030),(2.80,2.50,.030),GROUND)
for name,kind,loc,power,size in [('key','AREA',(-.45,-.35,1.25),145,2.7),
                                  ('fill','AREA',(.70,.65,1.12),85,2.6)]:
    lamp=bpy.data.lights.new(name,kind);lamp.energy=power;lamp.shape='DISK';lamp.size=size
    obj=bpy.data.objects.new(name,lamp);sc.collection.objects.link(obj);obj.location=loc
    obj.rotation_euler=(Vector((0,.05,.10))-obj.location).to_track_quat('-Z','Y').to_euler()
camdata=bpy.data.cameras.new('overview_camera');cam=bpy.data.objects.new('overview_camera',camdata)
sc.collection.objects.link(cam);cam.location=(.08,-1.48,1.38)
cam.rotation_euler=(Vector((0,.18,.17))-cam.location).to_track_quat('-Z','Y').to_euler()
camdata.type='ORTHO';camdata.ortho_scale=1.98;camdata.clip_start=.01;camdata.clip_end=8
sc.camera=cam
# Auxiliary close oblique view looks from outside the nozzle, above and toward
# its shell. It is an independent camera/render, not a different optical layout.
auxdata=bpy.data.cameras.new('laser_outlet_oblique_camera')
aux=bpy.data.objects.new('laser_outlet_oblique_camera',auxdata)
sc.collection.objects.link(aux)
aux.location=LASER_TIP+LASER_AXIS*.18+Vector((.03,-.16,.14))
aux.rotation_euler=(LASER_TIP-LASER_AXIS*.055+Vector((0,0,.007))-aux.location).to_track_quat('-Z','Y').to_euler()
auxdata.type='ORTHO';auxdata.ortho_scale=.37;auxdata.clip_start=.001;auxdata.clip_end=5
# The .blend is saved with overview camera, world, and no 3D words or labels.
# Re-runs replace only v8 outputs, without accumulating .blend1 backups.
bpy.context.preferences.filepaths.save_version=0
bpy.context.view_layer.update()
blend=OUT/'scene_case2_v8_overview.blend'
bpy.ops.wm.save_as_mainfile(filepath=str(blend))
sc.render.filepath=str(OUT/'case2_v8_overview_wordless.png')
bpy.ops.render.render(write_still=True)
print('WROTE_OVERVIEW',blend,sc.render.filepath,'parts',len(sc.objects))
sc.camera=aux
sc.render.resolution_x=960;sc.render.resolution_y=640
sc.render.filepath=str(OUT/'case2_v8_laser_outlet_oblique.png')
bpy.ops.render.render(write_still=True)
print('WROTE_OUTLET',sc.render.filepath)
# Saved .blend stays on overview camera at 1280x720; auxiliary camera is editable.
sc.camera=cam
sc.render.resolution_x=1280;sc.render.resolution_y=720

