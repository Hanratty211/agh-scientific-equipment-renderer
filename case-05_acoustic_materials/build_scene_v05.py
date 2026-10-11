"""05 v05 one material/lighting revision, no geometry or overview camera changes: low-cost Cycles transmitted glass, not EEVEE alpha dithering. Run Blender --background --python build_scene_v05.py."""
import bpy,math
from pathlib import Path
from mathutils import Vector
R=Path(__file__).resolve().parent;bpy.ops.object.select_all(action='SELECT');bpy.ops.object.delete(use_global=False)
def mat(n,c,rough=.42,trans=0):
 m=bpy.data.materials.new(n);m.diffuse_color=(*c,1);m.use_nodes=True;p=next(x for x in m.node_tree.nodes if x.type=='BSDF_PRINCIPLED');p.inputs['Base Color'].default_value=(*c,1);p.inputs['Roughness'].default_value=rough;p.inputs['Alpha'].default_value=1;p.inputs['Transmission Weight'].default_value=trans
 if trans:p.inputs['IOR'].default_value=1.45
 return m
# Cycles true transmissive shader: no alpha blending/dither grain on plate faces.
solid=mat('clear lower plate transmitted proxy',(.91,.97,.98),.06,.96);upper=mat('clear upper plate transmitted proxy',(.93,.98,.99),.045,.97)
spacer=mat('silver spacer rods',(.39,.48,.53),.31);ground=mat('charcoal stage backdrop',(.11,.15,.19),.75)
edge=mat('translucent darker rim visual contrast',(.35,.53,.58),.08,.52)
def cub(n,p,d,m):
 bpy.ops.mesh.primitive_cube_add(size=1,location=p);o=bpy.context.object;o.name=n;o.dimensions=d;bpy.ops.object.transform_apply(location=False,rotation=False,scale=True);o.data.materials.append(m);return o
def cyl(n,p,r,h,m):
 bpy.ops.mesh.primitive_cylinder_add(vertices=32,radius=r,depth=h,location=p);o=bpy.context.object;o.name=n;o.data.materials.append(m);return o
# Boolean difference is applied to monolithic solids, leaving actual voids in the plate meshes.
def bore_plate(name,z,material,face):
 o=cub(name,(0,0,z),(5.5,5.0,.20),material)
 # face = 1 means holes open on upper face, -1 lower face; blind depth .12 < plate thickness .20.
 for i in range(10):
  for j in range(10):
   x=(i-4.5)*.44;y=(j-4.5)*.43
   if x*x+y*y<.25**2:continue
   cutter=cyl('temporary blind cavity cutter',(x,y,z+face*(.10-.06)),.133,.12,material)
   mod=o.modifiers.new('actual blind cylindrical cavity','BOOLEAN');mod.operation='DIFFERENCE';mod.solver='EXACT';mod.object=cutter
   bpy.context.view_layer.objects.active=o;bpy.ops.object.modifier_apply(modifier=mod.name);bpy.data.objects.remove(cutter,do_unlink=True)
 # central entrance passes THROUGH plate, independent from nearby blind holes.
 cutter=cyl('temporary center entrance cutter',(0,0,z),.27,.5,material);mod=o.modifiers.new('actual central through opening','BOOLEAN');mod.operation='DIFFERENCE';mod.solver='EXACT';mod.object=cutter;bpy.context.view_layer.objects.active=o;bpy.ops.object.modifier_apply(modifier=mod.name);bpy.data.objects.remove(cutter,do_unlink=True)
 return o
bore_plate('lower transparent slab with real upward blind holes',.20,solid,1);bore_plate('upper transparent slab with real downward blind holes',.89,upper,-1)
# Thin dark-tinted edge strips preserve transparent slab thickness and make the spaced cavity readable.
for z in (.20,.89):
 for x in (-2.75,2.75):cub(f'tinted thickness edge x{x} z{z}',(x,0,z),(.021,5.00,.20),edge)
 for y in (-2.50,2.50):cub(f'tinted thickness edge y{y} z{z}',(0,y,z),(5.48,.021,.20),edge)
for x in (-2.48,2.48):
 for y in (-2.19,2.19):
  cyl(f'corner spacer column x{x} y{y}',(x,y,.545),.12,.43,spacer)
  cyl(f'spacer top retainer x{x} y{y}',(x,y,1.04),.145,.025,spacer)
cub('neutral stage',(0,0,-.30),(12,11,.10),ground)
for pos,pow in [((-5,-5,7),650),((4,1,5),300),((1,4,4),340)]:
 bpy.ops.object.light_add(type='AREA',location=pos);o=bpy.context.object;o.data.energy=pow;o.data.size=5;o.rotation_euler=(Vector((0,0,.4))-o.location).to_track_quat('-Z','Y').to_euler()
bpy.ops.object.camera_add(location=(7,-8,8));cam=bpy.context.object;cam.name='05 v05 unchanged whole plate overview camera';cam.rotation_euler=(Vector((0,0,.52))-cam.location).to_track_quat('-Z','Y').to_euler();cam.data.type='ORTHO';cam.data.ortho_scale=11.6;bpy.context.scene.camera=cam
s=bpy.context.scene;s.render.engine='CYCLES';s.cycles.samples=48;s.cycles.use_denoising=True;s.cycles.max_bounces=6;s.cycles.transparent_max_bounces=8
s.render.resolution_x=900;s.render.resolution_y=660;s.render.resolution_percentage=100;s.render.filepath=str(R/'overview_v05.png');s.render.image_settings.file_format='PNG';bpy.ops.wm.save_as_mainfile(filepath=str(R/'scene_v05.blend'));bpy.ops.render.render(write_still=True);print('CASE05_v05_SAVED')
