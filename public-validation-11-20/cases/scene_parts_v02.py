"""AGH R1 v02 geometry helpers; no original renderer code or generic physics claims.
Geometry is illustrative world units; no-text PNG, saved Blender. v01 stays immutable.
"""
import bpy,math
from mathutils import Vector
from scene_parts_v01 import material,finish,box,cylinder,sphere,ring,tube,polyline,reset,MAT
MAT['resin']=material('clear resin',(.84,.94,.94),.26)
MAT['ivory']=material('warm ivory',(.92,.89,.76))
MAT['black']=material('black instrument',(.022,.028,.04))
MAT['amber']=material('amber',(.96,.53,.09))
MAT['mint']=material('teal',(.12,.65,.53))

def ortho_camera(path,look,at,scale,width,height,version='v02'):
 scene=bpy.context.scene;world=scene.world;world.use_nodes=True
 bg=next(n for n in world.node_tree.nodes if n.type=='BACKGROUND');bg.inputs['Color'].default_value=(1,1,1,1);bg.inputs['Strength'].default_value=.8
 bpy.ops.object.camera_add(location=look);cam=bpy.context.object;cam.name='overview_camera_v02';cam.rotation_euler=(Vector(at)-cam.location).to_track_quat('-Z','Y').to_euler();cam.data.type='ORTHO';cam.data.ortho_scale=scale;scene.camera=cam
 for name,loc,power in [('key',(1,-4,9),850),('fill',(-5,2,7),550)]:
  bpy.ops.object.light_add(type='AREA',location=loc);o=bpy.context.object;o.name=name;o.data.energy=power;o.data.shape='DISK';o.data.size=6
 scene.render.engine='BLENDER_EEVEE';scene.render.resolution_x=width;scene.render.resolution_y=height;scene.render.resolution_percentage=100
 scene.render.image_settings.file_format='PNG';scene.render.image_settings.color_mode='RGBA';scene.render.film_transparent=False
 scene.render.filepath=str(path/f'overview_{version}.png');scene.view_settings.view_transform='Standard'
 bpy.ops.wm.save_as_mainfile(filepath=str(path/f'scene_{version}.blend'));bpy.ops.render.render(write_still=True)

def panel(name,center,size,color='black',screen=True):
 x,y,z=center;w,depth,h=size
 box(name,center,size,color)
 if screen:box(name+' glass',(x,y-depth/2-.008,z+.02),(w*.74,.022,h*.55),'screen')
 for k in range(3):cylinder(name+f' knob{k}',(x-w*.28+k*w*.27,y-depth/2-.035,z-h*.36),.036,.025,'silver',rotation=(math.pi/2,0,0))

def flat_ring(name,center,r_outer,r_inner,thickness,mat='silver',segments=64):
 # Closed annular solid, with genuine center aperture along local Z.
 verts=[];faces=[]
 for level in (-thickness/2,thickness/2):
  for j in range(segments):
   t=2*math.pi*j/segments
   for rad in (r_outer,r_inner):verts.append((rad*math.cos(t),rad*math.sin(t),level))
 for j in range(segments):
  a=2*j;b=2*((j+1)%segments)
  faces.extend(((a,b,b+1,a+1),(2*segments+a+1,2*segments+b+1,2*segments+b,2*segments+a),(a,2*segments+a,2*segments+b,b),(a+1,b+1,2*segments+b+1,2*segments+a+1)))
 mesh=bpy.data.meshes.new(name+' mesh');mesh.from_pydata(verts,[],faces);mesh.update();o=bpy.data.objects.new(name,mesh);bpy.context.collection.objects.link(o);o.location=center;o.data.materials.append(MAT[mat]);return o

def vertical_window(name,center,outer,inner,thickness,mat='silver'):
 # Rectangular frame assembled from four real bars in XZ; true opening through Y,
 # NOT the prior v01 xy hole in a thin-Y plate. parent empty is presentation only.
 x,y,z=center;w,h=outer;wi,hi=inner;wi=min(wi,w-.05);hi=min(hi,h-.05)
 group=bpy.data.objects.new(name,None);bpy.context.collection.objects.link(group)
 for label,c,size in (
  ('left',(x-(w+wi)/4,y,z),((w-wi)/2,thickness,h)),
  ('right',(x+(w+wi)/4,y,z),((w-wi)/2,thickness,h)),
  ('bottom',(x,y,z-(h+hi)/4),(wi,thickness,(h-hi)/2)),
  ('top',(x,y,z+(h+hi)/4),(wi,thickness,(h-hi)/2))):
  o=box(name+' '+label,c,size,mat);o.parent=group
 return group

def rectangular_layer(name,center,size,mat='silver',window=None):
 w,depth,h=size
 if window:return vertical_window(name,center,(w,h),window,depth,mat)
 return box(name,center,size,mat)

def cupped_disk(name,center,r,thickness,mat='silver'):
 base=cylinder(name+' cup body',center,r,thickness,mat)
 flat_ring(name+' lip',(center[0],center[1],center[2]+thickness/2),r*.96,r*.65,.035,mat)
 return base
