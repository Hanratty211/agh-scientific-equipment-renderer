"""Run ONLY by Blender --background existing_final.blend --python this.py.
Never save .blend. Update dependency graph, render saved overview then optional
same-scene detail camera(s); restore saved camera for each detail. Content hash
and evaluated mesh extents are logged per independent process.
-- case_id output_suffix specs_json output_report_json
specs: [{"name":"pump_close","focus":[...],"eye":[...],"scale":1.3,"width":900,"height":680}]
"""
import bpy,sys,json,hashlib
from pathlib import Path
from mathutils import Vector
args=sys.argv[sys.argv.index('--')+1:];case=int(args[0]);suffix=args[1];specs=json.loads(Path(args[2]).read_text());out=Path(args[3]);scene=bpy.context.scene
assert bpy.data.filepath and Path(bpy.data.filepath).is_file()
original_cam=scene.camera;original_path=scene.render.filepath;original_w=scene.render.resolution_x;original_h=scene.render.resolution_y
scene.render.resolution_percentage=100;scene.render.image_settings.file_format='PNG'
scene.view_settings.view_transform='Standard'
bpy.context.view_layer.update();deps=bpy.context.evaluated_depsgraph_get();deps.update()
root=Path(bpy.data.filepath).parent
scene_hash=hashlib.sha256(Path(bpy.data.filepath).read_bytes()).hexdigest()
result={'case':case,'scene':bpy.data.filepath,'scene_sha256':scene_hash,'source':'reloaded saved .blend; dependency graph explicitly updated before overview and each detail','images':[],'evaluated_mesh_bounds':{},'main_camera':original_cam.name}
if case in (12,17):
 names=('upper syringe pump mounted syringe barrel','lower syringe pump mounted syringe barrel') if case==12 else ('right syringe pump mounted syringe barrel',)
 for name in names:
  obj=bpy.data.objects[name];ev=obj.evaluated_get(deps);me=ev.to_mesh()
  try:
   vertices=[ev.matrix_world@v.co for v in me.vertices]
   result['evaluated_mesh_bounds'][name]={key:[min(v[i] for v in vertices),max(v[i] for v in vertices)] for i,key in enumerate(('x','y','z'))}
  finally:ev.to_mesh_clear()
def record(path,label,camera):
 scene.render.filepath=str(path);bpy.context.view_layer.update();deps.update()
 bpy.ops.render.render(write_still=True)
 assert path.is_file() and path.stat().st_size>1000
 result['images'].append({'label':label,'path':str(path),'sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'camera':camera,'size':[scene.render.resolution_x,scene.render.resolution_y]})
scene.camera=original_cam;scene.render.resolution_x=original_w;scene.render.resolution_y=original_h
record(root/f'overview_{suffix}.png','overview',original_cam.name)
for spec in specs:
 eye=Vector(spec['eye']);focus=Vector(spec['focus'])
 bpy.ops.object.camera_add(location=eye);cam=bpy.context.object;cam.name='TEMP_R2_'+spec['name'];cam.data.type='ORTHO';cam.data.ortho_scale=float(spec['scale']);cam.rotation_euler=(focus-eye).to_track_quat('-Z','Y').to_euler()
 scene.camera=cam;scene.render.resolution_x=int(spec.get('width',900));scene.render.resolution_y=int(spec.get('height',680))
 record(root/f'detail_{spec["name"]}_{suffix}.png',spec['name'],cam.name)
 bpy.data.objects.remove(cam,do_unlink=True);scene.camera=original_cam
scene.render.filepath=original_path;scene.render.resolution_x=original_w;scene.render.resolution_y=original_h
assert scene.camera==original_cam
out.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
print('SAVED_R2',case,scene_hash,len(result['images']),out)
