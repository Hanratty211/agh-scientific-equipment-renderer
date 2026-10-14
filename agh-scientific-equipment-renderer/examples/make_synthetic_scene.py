"""Tiny synthetic saved Blender fixture. No scientific apparatus or old-case render.
blender --background --python examples/make_synthetic_scene.py -- /tmp/agh-v06/fixture.blend
"""
import bpy,sys,math
from mathutils import Vector
from pathlib import Path
out=Path(sys.argv[-1]);out.parent.mkdir(parents=True,exist_ok=True)
bpy.ops.object.select_all(action='SELECT');bpy.ops.object.delete(use_global=False)
def box(name,pos,size):
 bpy.ops.mesh.primitive_cube_add(size=1,location=pos);o=bpy.context.object;o.name=name;o.dimensions=size;bpy.ops.object.transform_apply(location=False,rotation=False,scale=True);return o
base=box('base_mesh',(0,0,.15),(2,2,.30))
plate=box('plate_mesh',(0,0,.38),(1.2,1.2,.16)) # bottom=.30 touches top of base
# Anchors are tiny true meshes centered on owner surfaces; not custom-property-only claims.
box('anchor_a',(-1,0,.15),(.02,.02,.02))
box('anchor_b',(.6,0,.38),(.02,.02,.02))
a=Vector((-1,0,.15));b=Vector((.6,0,.38))
c=bpy.data.curves.new('rod curve','CURVE');c.dimensions='3D';c.bevel_depth=.02;c.bevel_resolution=2;sp=c.splines.new('POLY');sp.points.add(1)
sp.points[0].co=(*a,1);sp.points[1].co=(*b,1);o=bpy.data.objects.new('rod_curve',c);bpy.context.collection.objects.link(o)
bpy.ops.object.camera_add(location=(3,-5,5));cam=bpy.context.object;cam.name='overview_camera';cam.rotation_euler=(Vector((0,0,.20))-cam.location).to_track_quat('-Z','Y').to_euler();cam.data.type='ORTHO';cam.data.ortho_scale=5.0;bpy.context.scene.camera=cam
scene=bpy.context.scene;scene.render.engine='BLENDER_EEVEE';scene.render.resolution_x=420;scene.render.resolution_y=300;scene.render.resolution_percentage=100;scene.render.film_transparent=False
bpy.ops.wm.save_as_mainfile(filepath=str(out));print('SYNTHETIC_SAVED',out)
