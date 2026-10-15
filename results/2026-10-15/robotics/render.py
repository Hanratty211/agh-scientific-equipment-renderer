"""Independent saved-scene reload; all geometry and materials unchanged.
Usage: blender -b INPUT.blend --python render_views.py -- OUTPUT_DIR [WIDTH]
"""
import bpy, sys, json, hashlib, time
from pathlib import Path
from mathutils import Vector
a=sys.argv[sys.argv.index('--')+1:]; out=Path(a[0]).resolve();out.mkdir(parents=True,exist_ok=True)
width=int(a[1]) if len(a)>1 else 1800
scene=bpy.context.scene; cam=scene.camera; source=Path(bpy.data.filepath)
before=hashlib.sha256(source.read_bytes()).hexdigest()
bpy.context.view_layer.update();bpy.context.evaluated_depsgraph_get().update()
original=(cam.matrix_world.copy(),cam.data.ortho_scale,scene.render.resolution_x,scene.render.resolution_y,scene.render.resolution_percentage)
state={o.name:{'hide_render':o.hide_render,'materials':[m.name for m in o.data.materials if m] if hasattr(o.data,'materials') else []} for o in scene.objects}
reports=[]
def render(name,loc=None,target=None,ortho=None):
 if loc is not None:
  cam.location=loc;cam.rotation_euler=(Vector(target)-cam.location).to_track_quat('-Z','Y').to_euler();cam.data.ortho_scale=ortho
 scene.render.resolution_x=width;scene.render.resolution_y=round(width*640/900);scene.render.resolution_percentage=100
 scene.render.filepath=str(out/(name+'.png'));t=time.monotonic();bpy.ops.render.render(write_still=True)
 reports.append({'view':name,'png_sha256':hashlib.sha256((out/(name+'.png')).read_bytes()).hexdigest(),'camera_location':list(cam.location),'camera_rotation':list(cam.rotation_euler),'ortho_scale':cam.data.ortho_scale,'seconds':time.monotonic()-t,'width':scene.render.resolution_x,'height':scene.render.resolution_y,'geometry_modified':False,'visibility_modified':False,'pixel_review':'PENDING'})
try:
 render('overview')
 render('front',(0,-8,1.6),(0,0,1.6),5.4)
 render('upper_grip',(1.8,-4,2.9),(0,0,2.48),1.45)
 render('lower_grip',(1.8,-4,1.15),(0,0,.73),1.45)
finally:
 cam.matrix_world=original[0];cam.data.ortho_scale=original[1]
 scene.render.resolution_x,scene.render.resolution_y,scene.render.resolution_percentage=original[2:]
 assert before==hashlib.sha256(source.read_bytes()).hexdigest()
 assert state=={o.name:{'hide_render':o.hide_render,'materials':[m.name for m in o.data.materials if m] if hasattr(o.data,'materials') else []} for o in scene.objects}
 (out/'render_report.json').write_text(json.dumps({'scene':str(source),'scene_sha256':before,'blender':bpy.app.version_string,'engine':scene.render.engine,'saved_scene_unchanged':True,'views':reports},indent=2))
