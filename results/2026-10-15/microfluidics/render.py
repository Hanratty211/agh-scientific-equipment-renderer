"""Render four views of the saved v11 schematic without changing the saved scene.
Based on the original AI-assisted multi-view renderer.
"""
import bpy,sys,json,hashlib,time
from pathlib import Path
from mathutils import Vector
args=sys.argv[sys.argv.index('--')+1:];out=Path(args[0]).resolve();out.mkdir(parents=True,exist_ok=True)
width=int(args[1]) if len(args)>1 else 1800
scene=bpy.context.scene;cam=scene.camera;source=Path(bpy.data.filepath)
before=hashlib.sha256(source.read_bytes()).hexdigest()
bpy.context.view_layer.update();bpy.context.evaluated_depsgraph_get().update()
original=(cam.matrix_world.copy(),cam.data.ortho_scale,scene.render.resolution_x,scene.render.resolution_y,scene.render.resolution_percentage)
state={o.name:{'hide_render':o.hide_render,'materials':[m.name for m in o.data.materials if m] if hasattr(o.data,'materials') else []} for o in scene.objects}
scene.render.engine='CYCLES';scene.cycles.device='CPU';scene.cycles.samples=32;scene.cycles.use_denoising=True
reports=[]
def render(name,loc=None,target=None,ortho=None):
 if loc is not None:
  cam.location=loc;cam.rotation_euler=(Vector(target)-cam.location).to_track_quat('-Z','Y').to_euler();cam.data.ortho_scale=ortho
 scene.render.resolution_x=width;scene.render.resolution_y=round(width*(850/1800 if name=='overview' else 640/900));scene.render.resolution_percentage=100
 f=out/(name+'.png');assert not f.exists(),f
 scene.render.filepath=str(f);t=time.monotonic();bpy.ops.render.render(write_still=True)
 reports.append({'view':name,'png_sha256':hashlib.sha256(f.read_bytes()).hexdigest(),'camera_location':list(cam.location),'camera_rotation':list(cam.rotation_euler),'ortho_scale':cam.data.ortho_scale,'seconds':time.monotonic()-t,'width':scene.render.resolution_x,'height':scene.render.resolution_y,'geometry_modified':False,'visibility_modified':False,'pixel_review':'PENDING'})
try:
 render('overview')
 render('top',(0,-.1,12),(0,-.1,0),8.6)
 render('chip_detail',(-.3,-3.6,3.8),(-1.25,-1.1,.15),2.4)
 render('syringe_detail',(2.0,-3.0,3.4),(1.9,.4,.70),4.6)
finally:
 cam.matrix_world=original[0];cam.data.ortho_scale=original[1]
 scene.render.resolution_x,scene.render.resolution_y,scene.render.resolution_percentage=original[2:]
 assert before==hashlib.sha256(source.read_bytes()).hexdigest()
 assert state=={o.name:{'hide_render':o.hide_render,'materials':[m.name for m in o.data.materials if m] if hasattr(o.data,'materials') else []} for o in scene.objects}
 (out/'render_report.json').write_text(json.dumps({'scene':str(source),'scene_sha256':before,'blender':bpy.app.version_string,'engine':scene.render.engine,'saved_scene_unchanged':True,'views':reports},indent=2))
