"""One supplementary rear (+Y) three-quarter view of SAME saved scene_v05.
No hide/exclude, no save, no object edits. Independent Blender process only.
-- output.png report.json
"""
import bpy,sys,json,hashlib
from pathlib import Path
from mathutils import Vector
args=sys.argv[sys.argv.index('--')+1:];out=Path(args[0]);report=Path(args[1]);scene=bpy.context.scene
assert Path(bpy.data.filepath).name=='scene_v05.blend' and out.name=='detail_camera_data_rear_v05_reloaded_r2.png'
assert not out.exists() and not report.exists()
body=bpy.data.objects['high speed camera'];port=bpy.data.objects['camera representative DATA data socket'];plug=bpy.data.objects['camera representative DATA seated data plug'];boot=bpy.data.objects['camera representative DATA cable boot'];cable=bpy.data.objects['camera to laptop exterior DATA cable']
assert all(not obj.hide_render for obj in (body,port,plug,boot,cable))
assert cable.type=='CURVE' and len(cable.data.splines)==1
bpy.context.view_layer.update();deps=bpy.context.evaluated_depsgraph_get();deps.update()
original_camera=scene.camera;original_path=scene.render.filepath
# Camera rear is +Y, data port near x=+0.235 / y=+0.278 / z=2.59;
# oblique +X +Y avoids directly putting body in front of its rear jack.
focus=Vector((.24,.26,2.58));eye=Vector((1.65,2.0,3.10))
bpy.ops.object.camera_add(location=eye);cam=bpy.context.object;cam.name='TEMP_R2_CAMERA_REAR_DATA';cam.rotation_euler=(focus-eye).to_track_quat('-Z','Y').to_euler();cam.data.type='ORTHO';cam.data.ortho_scale=1.20
scene.camera=cam;scene.render.resolution_x=1080;scene.render.resolution_y=740;scene.render.resolution_percentage=100
scene.render.image_settings.file_format='PNG';scene.render.filepath=str(out)
assert all(not obj.hide_render for obj in (body,port,plug,boot,cable))
bpy.context.view_layer.update();deps.update();bpy.ops.render.render(write_still=True)
assert out.is_file() and out.stat().st_size>1000
scene.camera=original_camera;scene.render.filepath=original_path;bpy.data.objects.remove(cam,do_unlink=True)
report.write_text(json.dumps({'author':'AGH','scene':bpy.data.filepath,'scene_sha256':hashlib.sha256(Path(bpy.data.filepath).read_bytes()).hexdigest(),'image':str(out),'image_sha256':hashlib.sha256(out.read_bytes()).hexdigest(),'eye':list(eye),'focus':list(focus),'camera':'rear +Y, oblique +X','no_object_or_render_state_mutations':True,'source_spline':cable.name,'camera_port':port.name,'mated_plug':plug.name,'boot':boot.name,'pixel_status':'user to review'},indent=2)+'\n')
print('CAMERA_REAR',out,report)
