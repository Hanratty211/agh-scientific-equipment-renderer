"""07 Fig.4b dual-membrane PSA RFB complete PHOTOGRAPH-LEVEL test apparatus, not Fig4a. Pumps/vessels/outer hose paths are visible layout proxies; endpoints hidden in photo stop at occlusion. Run Blender --background --python build_scene_v03.py."""
import bpy
from pathlib import Path
from mathutils import Vector
R=Path(__file__).resolve().parent;bpy.ops.object.select_all(action='SELECT');bpy.ops.object.delete(use_global=False)
def mat(n,c,m=0,a=1):
 q=bpy.data.materials.new(n);q.diffuse_color=(*c,a);q.use_nodes=True;p=next(v for v in q.node_tree.nodes if v.type=='BSDF_PRINCIPLED');p.inputs['Base Color'].default_value=(*c,1);p.inputs['Metallic'].default_value=m;p.inputs['Roughness'].default_value=.43
 if a<1:p.inputs['Alpha'].default_value=a;q.surface_render_method='DITHERED'
 return q
black=mat('dark end plate',(.12,.13,.14));metal=mat('metal frame',(.59,.61,.61),.63);grey=mat('visible center block',(.36,.41,.42));tube=mat('pale visible tube',(.70,.76,.74),0,.79);amber=mat('warm vessel content visual cue',(.55,.39,.14),0,.68);pump=mat('dark pump housings',(.20,.22,.23));clear=mat('translucent container exterior',(.78,.84,.81),0,.46);blue=mat('laboratory mounting rail',(.27,.39,.50));bg=mat('neutral laboratory stage',(.21,.22,.24))
def box(n,p,d,ma):
 bpy.ops.mesh.primitive_cube_add(size=1,location=p);o=bpy.context.object;o.name=n;o.dimensions=d;bpy.ops.object.transform_apply(location=False,rotation=False,scale=True);o.data.materials.append(ma);return o
def cyl(n,p,r,h,ma,axis=(0,0,1)):
 bpy.ops.mesh.primitive_cylinder_add(vertices=32,radius=r,depth=h,location=p);o=bpy.context.object;o.name=n;o.rotation_euler=Vector((0,0,1)).rotation_difference(Vector(axis)).to_euler();o.data.materials.append(ma);return o
def pipe(n,pts,r,ma):
 c=bpy.data.curves.new(n,'CURVE');c.dimensions='3D';c.bevel_depth=r;c.bevel_resolution=4;s=c.splines.new('BEZIER');s.bezier_points.add(len(pts)-1)
 for v,p in zip(s.bezier_points,pts):v.co=p;v.handle_left_type='AUTO';v.handle_right_type='AUTO'
 o=bpy.data.objects.new(n,c);bpy.context.collection.objects.link(o);o.data.materials.append(ma)
# One compact raised cell centered between ancillary test hardware (no exposed fictitious membrane colours).
box('central dual-membrane stack exterior',(0,0,1.82),(.95,1.50,1.31),grey)
for x in (-.57,.57):box(f'central stack compression plate {x}',(x,0,1.82),(.19,1.65,1.53),black)
box('thin externally visible center-frame spacer',(0,-.84,1.82),(.12,.035,1.36),metal)
for y in (-.56,.56):
 for z in (1.22,2.42):cyl(f'tie rod at y{y} z{z}',(0,y,z),.06,1.41,metal,(1,0,0))
for i,(x,y,z) in enumerate([(-.71,-.35,1.76),(-.71,.39,1.94),(.71,-.35,1.78),(.71,.39,1.98)]):
 cyl(f'visible external cell fitting {i}',(x,y,z),.105,.26,metal,(1,0,0))
# Vertical adjustable lab lift supporting THIS stack; exact bench mechanism unknown.
box('stack riser top support',(0,0,.93),(1.62,1.70,.14),metal)
box('vertical lift central column',(0,0,.57),(.23,.26,.65),metal)
box('lift bottom platform',(0,0,.18),(1.8,1.68,.27),blue)
for x in (-.66,.66):box(f'lift visible side screw guide {x}',(x,.40,.56),(.10,.11,.54),metal)
# Separate apparatus on either side; deliberately do NOT label pump model, port identity or vessel fluid.
for side in (-1,1):
 x=side*2.60
 box(f'{side} pump base',(x,-.72,.22),(1.30,1.06,.29),pump)
 box(f'{side} visible rectangular pump',(x,-.72,.72),(.90,.73,.76),pump)
 cyl(f'{side} pump head',(x,-1.13,.76),.30,.16,metal,(0,1,0))
 box(f'{side} container platform',(x,.69,.16),(.94,.91,.24),blue)
 cyl(f'{side} vessel outer sidewalls',(x,.68,1.00),.30,1.42,clear)
 cyl(f'{side} vessel tinted lower volume',(x,.68,.76),.263,.82,amber if side<0 else tube)
 cyl(f'{side} vessel top lid',(x,.68,1.75),.33,.13,metal)
 cyl(f'{side} visible vessel top tube stop',(x,.68,1.85),.08,.11,metal)
 # Separate cropped external visible stretches, never a self-closed hose ring.
 pipe(f'{side} pump-to-cell externally visible hose',[(x,-1.20,.78),(x-side*.22,-1.45,1.05),(side*1.39,-1.10,1.49),(side*.83,-.35,1.77)],.050,tube)
 pipe(f'{side} vessel-to-cell externally visible hose',[(x,.68,1.86),(x-side*.21,1.05,2.22),(side*1.43,.92,2.30),(side*.83,.39,1.96)],.044,tube)
 # Photograph may obscure passage across pump/vessel: no hidden return path or container connection drawn.
box('bench support surface',(0,0,-.12),(8.45,3.40,.16),bg)
for xyz,power in [((-5,-6,7),850),((5,3,6),500)]:
 bpy.ops.object.light_add(type='AREA',location=xyz);o=bpy.context.object;o.data.energy=power;o.data.size=5;o.rotation_euler=(Vector((0,0,1.25))-o.location).to_track_quat('-Z','Y').to_euler()
bpy.ops.object.camera_add(location=(4,-9,6.2));cam=bpy.context.object;cam.name='07 v03 complete Fig4b photo-level test arrangement';cam.rotation_euler=(Vector((0,0,1.12))-cam.location).to_track_quat('-Z','Y').to_euler();cam.data.type='ORTHO';cam.data.ortho_scale=9.2;bpy.context.scene.camera=cam
s=bpy.context.scene;s.render.engine='BLENDER_EEVEE';s.render.resolution_x=1000;s.render.resolution_y=730;s.render.resolution_percentage=100;s.render.filepath=str(R/'overview_v03.png');s.render.image_settings.file_format='PNG';bpy.ops.wm.save_as_mainfile(filepath=str(R/'scene_v03.blend'));bpy.ops.render.render(write_still=True);print('CASE07_v03_SAVED')
