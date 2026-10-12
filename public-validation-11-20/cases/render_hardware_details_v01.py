"""Render supplementary local camera views of unchanged saved-scene geometry.
Do not save .blend or alter original main camera/render flags in the saved file.
Blender --background scene.blend --python this.py -- output.png focus_x focus_y focus_z eye_x eye_y eye_z width height scale
"""
import bpy,sys
from mathutils import Vector
from pathlib import Path
args=sys.argv[sys.argv.index('--')+1:];out=Path(args[0]);focus=Vector(tuple(float(x) for x in args[1:4]));eye=Vector(tuple(float(x) for x in args[4:7]));width,height=int(args[7]),int(args[8]);scale=float(args[9])
s=bpy.context.scene
bpy.ops.object.camera_add(location=eye);cam=bpy.context.object;cam.name='TEMPORARY hard-detail camera (not saved)';cam.rotation_euler=(focus-eye).to_track_quat('-Z','Y').to_euler();cam.data.type='ORTHO';cam.data.ortho_scale=scale;s.camera=cam
s.render.resolution_x=width;s.render.resolution_y=height;s.render.resolution_percentage=100;s.render.filepath=str(out)
s.render.image_settings.file_format='PNG';bpy.ops.render.render(write_still=True)
print('DETAIL_RENDER',out,width,height,'focus',tuple(focus),'eye',tuple(eye))
