"""10 v04 top-open phantom with top yellow strip and central patch; empty solid front face without unsupported raised marker. Run Blender --background --python build_scene_v04.py."""
import bpy
from pathlib import Path
from mathutils import Vector
R=Path(__file__).resolve().parent;bpy.ops.object.select_all(action='SELECT');bpy.ops.object.delete(use_global=False)
def mat(n,c,a=1):
 m=bpy.data.materials.new(n);m.diffuse_color=(*c,a);m.use_nodes=True;p=next(v for v in m.node_tree.nodes if v.type=='BSDF_PRINCIPLED');p.inputs['Base Color'].default_value=(*c,1);p.inputs['Roughness'].default_value=.65
 if a<1:p.inputs['Alpha'].default_value=a;m.surface_render_method='DITHERED'
 return m
white=mat('cream white commercial phantom surface',(.84,.83,.76));inner=mat('dark visible empty top recess',(.36,.40,.40));rim=mat('raised creamy rim around open top',(.89,.87,.80));yellow=mat('yellow strip on phantom side as visible color cue',(.77,.66,.20));patchmat=mat('dark visible sensing patch exterior',(.18,.22,.21));flex=mat('pale flexible patch lead',(.46,.53,.45));stage=mat('neutral backing',(.20,.21,.22))
def box(n,p,d,m):
 bpy.ops.mesh.primitive_cube_add(size=1,location=p);o=bpy.context.object;o.name=n;o.dimensions=d;bpy.ops.object.transform_apply(location=False,rotation=False,scale=True);o.data.materials.append(m);return o
# Hollow/open-topped visible silhouette, no extrapolation of actual phantom interior material.
box('thick phantom bottom plate',(0,0,.18),(4.65,3.25,.36),white)
for x in (-2.24,2.24):box(f'tall phantom wall at x{x}',(x,0,1.70),(.20,3.25,2.75),white)
for y in (-1.53,1.53):box(f'tall phantom wall at y{y}',(0,y,1.70),(4.3,.19,2.75),white)
box('visible recessed top opening dark interior',(0,0,.37),(4.17,2.82,.025),inner)
for x in (-2.22,2.22):box(f'top opening pale side lip x{x}',(x,0,3.09),(.22,3.27,.075),rim)
for y in (-1.53,1.53):box(f'top opening pale front back lip y{y}',(0,y,3.09),(4.25,.19,.075),rim)
# Strip traverses the visible OPEN TOP horizontally and touches the upper rim at both edges.
# Patch sits in the strip midpoint; no geometry on the phantom's front vertical face.
box('yellow strip spanning top visible opening',(0,-.07,3.155),(4.55,.43,.026),yellow)
box('small dark patch centered on top yellow strip',(0,-.07,3.195),(1.14,.38,.048),patchmat)
box('pale short top flex end at right edge of patch',(.66,-.07,3.18),(.29,.24,.022),flex)
# No sourced raised fixture/connector on the front wall. Leave it solid and unadorned.
# NO red box, white arrow, internal phantom target, or unsupported strip function.
box('neutral tabletop',(0,0,-.23),(10,9,.10),stage)
for p,pow in [((-4,-5,7),630),((4,2,5),380)]:
 bpy.ops.object.light_add(type='AREA',location=p);o=bpy.context.object;o.data.energy=pow;o.data.size=4;o.rotation_euler=(Vector((0,0,1.6))-o.location).to_track_quat('-Z','Y').to_euler()
bpy.ops.object.camera_add(location=(5,-7,5.5));cam=bpy.context.object;cam.name='10 v04 clean front and top mounted strip patch';cam.rotation_euler=(Vector((0,0,1.55))-cam.location).to_track_quat('-Z','Y').to_euler();cam.data.type='ORTHO';cam.data.ortho_scale=6.7;bpy.context.scene.camera=cam
s=bpy.context.scene;s.render.engine='BLENDER_EEVEE';s.render.resolution_x=860;s.render.resolution_y=690;s.render.resolution_percentage=100;s.render.filepath=str(R/'overview_v04.png');s.render.image_settings.file_format='PNG';bpy.ops.wm.save_as_mainfile(filepath=str(R/'scene_v04.blend'));bpy.ops.render.render(write_still=True);print('CASE10_v04_SAVED')
