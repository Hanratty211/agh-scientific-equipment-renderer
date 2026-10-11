"""06 transparent clamped specimen: two dark visible regions, upper clip points and separately routed visible leads; identities and actual junctions unknown. Run Blender --background --python build_scene_v02.py."""
import bpy
from pathlib import Path
from mathutils import Vector
R=Path(__file__).resolve().parent;bpy.ops.object.select_all(action='SELECT');bpy.ops.object.delete(use_global=False)
def mat(n,c,a=1,metal=0):
 m=bpy.data.materials.new(n);m.diffuse_color=(*c,a);m.use_nodes=True;p=next(v for v in m.node_tree.nodes if v.type=='BSDF_PRINCIPLED');p.inputs['Base Color'].default_value=(*c,1);p.inputs['Roughness'].default_value=.42;p.inputs['Metallic'].default_value=metal
 if a<1:p.inputs['Alpha'].default_value=a;m.surface_render_method='DITHERED'
 return m
dark=mat('black visible rectangular film or component identity unassigned',(.045,.062,.069));clear=mat('transparent carrier and clamp visual proxy',(.70,.81,.84),.28);pale=mat('offwhite structural edges',(.72,.72,.65));silver=mat('small contact metal visual proxy',(.53,.54,.53),1,.72);lead=mat('black leads',(.03,.04,.045));ground=mat('studio stage',(.21,.23,.23))
def box(n,p,d,m):
 bpy.ops.mesh.primitive_cube_add(size=1,location=p);o=bpy.context.object;o.name=n;o.dimensions=d;bpy.ops.object.transform_apply(location=False,rotation=False,scale=True);o.data.materials.append(m);return o
def cable(n,pts,r,ma):
 c=bpy.data.curves.new(n,'CURVE');c.dimensions='3D';c.bevel_depth=r;c.bevel_resolution=3;s=c.splines.new('POLY');s.points.add(len(pts)-1)
 for p,v in zip(s.points,pts):p.co=(*v,1)
 o=bpy.data.objects.new(n,c);bpy.context.collection.objects.link(o);o.data.materials.append(ma)
# Thin specimen is in XY image plane, with front visible Z face and transparent top retaining frame.
box('pale backplane of upright rectangular specimen',(0,0,.18),(2.65,4.25,.15),pale)
box('left dark visible main region',(-.64,-.34,.29),(1.12,2.81,.045),dark)
box('right dark visible main region',(.64,-.34,.29),(1.12,2.81,.045),dark)
box('vertical light boundary separating main regions',(0,-.34,.33),(.12,2.90,.014),pale)
# Cover and support are transparent frame parts, not an opaque plate over the dark faces.
for x in (-1.25,1.25):box(f'transparent carrier side rail x{x}',(x,0,.39),(.13,4.32,.14),clear)
box('transparent top cross-clamp',(0,1.84,.45),(2.80,.22,.19),clear)
box('transparent lower cross-clamp',(0,-1.86,.43),(2.80,.16,.14),clear)
for k,x in enumerate((-.73,.73)):
 box(f'upper clip metal foot {k}',(x,1.26,.37),(.33,.22,.12),silver)
 box(f'upper clip metal spring {k}',(x,1.56,.48),(.30,.64,.13),silver)
 box(f'identified visible lead-to-clip junction {k}',(x,1.73,.56),(.17,.14,.10),silver)
 cable(f'lead from visible upper clip to edge {k}',[(x,1.73,.56),(x,2.05,.65),(x*1.12,2.55,.72),(x*1.16,3.06,.62)],.035,lead)
# Wires end at the upper clip, not implied to traverse the hidden interior or electrodes.
box('neutral stage',(0,0,-.24),(9,11,.10),ground)
for pos,pow in [((-4,-4,7),600),((3,2,5),320)]:
 bpy.ops.object.light_add(type='AREA',location=pos);o=bpy.context.object;o.data.energy=pow;o.data.size=4;o.rotation_euler=(Vector((0,0,.3))-o.location).to_track_quat('-Z','Y').to_euler()
bpy.ops.object.camera_add(location=(2.0,-5.5,8));cam=bpy.context.object;cam.name='06 v02 clear clamp and clipped leads';cam.rotation_euler=(Vector((0,0,.34))-cam.location).to_track_quat('-Z','Y').to_euler();cam.data.type='ORTHO';cam.data.ortho_scale=6.4;bpy.context.scene.camera=cam
s=bpy.context.scene;s.render.engine='BLENDER_EEVEE';s.render.resolution_x=750;s.render.resolution_y=870;s.render.resolution_percentage=100;s.render.filepath=str(R/'overview_v02.png');s.render.image_settings.file_format='PNG';bpy.ops.wm.save_as_mainfile(filepath=str(R/'scene_v02.blend'));bpy.ops.render.render(write_still=True);print('CASE06_v02_SAVED')
