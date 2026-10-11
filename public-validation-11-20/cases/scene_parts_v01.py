"""AGH-authored lightweight Blender shapes for public batch 11–20.
Presentation geometry only; no hidden wiring/physics inferred. World units illustrative.
"""
import bpy,math
from mathutils import Vector

def material(name,color,alpha=1,metal=0):
 m=bpy.data.materials.new(name);m.diffuse_color=(*color,alpha);m.use_nodes=True
 bs=next(n for n in m.node_tree.nodes if n.type=='BSDF_PRINCIPLED');bs.inputs['Base Color'].default_value=(*color,1);bs.inputs['Metallic'].default_value=metal;bs.inputs['Roughness'].default_value=.33 if metal else .6
 if alpha<1:
  bs.inputs['Alpha'].default_value=alpha
  try:m.surface_render_method='DITHERED'
  except AttributeError:pass
 return m
MAT={
 'silver':material('brushed aluminum',(.42,.49,.55),metal=.55),
 'white':material('ceramic white',(.84,.88,.89)),
 'dark':material('dark polymer',(.055,.09,.12)),
 'copper':material('copper',(0.72,.34,.13),metal=.7),
 'gold':material('electrode gold',(.76,.55,.19),metal=.7),
 'blue':material('instrument blue',(.13,.34,.62)),
 'red':material('alignment red',(.78,.16,.11)),
 'glass':material('translucent pane',(.54,.83,.91),alpha=.32),
 'fluid':material('fluid tube',(.32,.64,.81),alpha=.78),
 'green':material('PCB green',(.19,.43,.35)),
 'rubber':material('silicone',(.24,.28,.34)),
 'screen':material('screen dark blue',(.08,.17,.25)),
}
def finish(obj,name,mat):
 obj.name=name;obj.data.materials.append(MAT[mat])
 if obj.type=='MESH':
  bevel=obj.modifiers.new('soft edges','BEVEL');bevel.width=.018;bevel.segments=2
  obj.modifiers.new('weighted normals','WEIGHTED_NORMAL')
 return obj

def box(name,loc,size,mat='silver'):
 bpy.ops.mesh.primitive_cube_add(size=1,location=loc);o=bpy.context.object;o.dimensions=size
 bpy.ops.object.transform_apply(location=False,rotation=False,scale=True)
 return finish(o,name,mat)
def cylinder(name,loc,r,depth,mat='silver',vertices=48,rotation=None):
 bpy.ops.mesh.primitive_cylinder_add(vertices=vertices,radius=r,depth=depth,location=loc,rotation=rotation or (0,0,0))
 return finish(bpy.context.object,name,mat)
def sphere(name,loc,r,mat='glass'):
 bpy.ops.mesh.primitive_uv_sphere_add(segments=24,ring_count=12,radius=r,location=loc)
 return finish(bpy.context.object,name,mat)
def polyline(name,points,r=.018,mat='fluid'):
 curve=bpy.data.curves.new(name,'CURVE');curve.dimensions='3D';curve.resolution_u=16;curve.bevel_depth=r;curve.bevel_resolution=3
 spline=curve.splines.new('POLY');spline.points.add(len(points)-1)
 for p,v in zip(spline.points,points):p.co=(*v,1)
 o=bpy.data.objects.new(name,curve);bpy.context.collection.objects.link(o);o.data.materials.append(MAT[mat]);return o

def ring(name,loc,major=.55,minor=.04,mat='copper',rotation=None):
 bpy.ops.mesh.primitive_torus_add(major_radius=major,minor_radius=minor,major_segments=64,minor_segments=12,location=loc,rotation=rotation or (0,0,0))
 return finish(bpy.context.object,name,mat)
def tube(name,a,b,r=.024,mat='silver'):
 va,vb=Vector(a),Vector(b);mid=(va+vb)/2;axis=vb-va
 if axis.length<1e-6:return sphere(name,a,r,mat)
 obj=cylinder(name,mid,r,axis.length,mat);obj.rotation_euler=axis.to_track_quat('Z','Y').to_euler();return obj

def pane_frame(name,center,size,mat='glass'):
 x,y,z=size;box(name+' pane',center,size,mat)
 for xx in (-x/2,x/2):box(name+' side', (center[0]+xx,center[1],center[2]),(.045,y,z),'silver')
 for zz in (-z/2,z/2):box(name+' rail',(center[0],center[1],center[2]+zz),(x+.04,y,.045),'silver')

def open_frame(name,center,w,h,depth=.09,mat='silver'):
 x,y,z=center
 for dx in (-w/2,w/2):box(name+' post',(x+dx,y,z),(depth,depth,h),mat)
 for dz in (-h/2,h/2):box(name+' rail',(x,y,z+dz),(w+depth,depth,depth),mat)

def plate_with_hole(name,loc,size,hole_r,mat='silver'):
 x,y,z=size;outer=bpy.data.meshes.new(name+' mesh');v=[];f=[];n=48
 # Annular square plate: ring outer square perimeter and circular real inner aperture.
 for level in (-z/2,z/2):
  for j in range(n):
   t=2*math.pi*j/n;co=math.cos(t);si=math.sin(t);k=max(abs(co),abs(si))
   v.append((x/2*co/k,y/2*si/k,level));v.append((hole_r*co,hole_r*si,level))
 for j in range(n):
  a=2*j;b=2*((j+1)%n)
  f.extend(((a,b,b+1,a+1),(2*n+a+1,2*n+b+1,2*n+b,2*n+a),(a,a+1,2*n+a+1,2*n+a),(a+1,b+1,2*n+b+1,2*n+a+1),(b,a,2*n+a,2*n+b)))
 outer.from_pydata(v,[],f);outer.update();o=bpy.data.objects.new(name,outer);bpy.context.collection.objects.link(o);o.location=loc;o.data.materials.append(MAT[mat]);return o

def reset():
 bpy.ops.object.select_all(action='SELECT');bpy.ops.object.delete(use_global=False)

def presentation(path,look=(8,-11,8),at=(0,0,.8),scale=8.5,width=960,height=700,samples=16):
 world=bpy.context.scene.world;world.color=(.8,.8,.8);world.use_nodes=True;world.node_tree.nodes['Background'].inputs['Color'].default_value=(.84,.88,.93,1)
 world.node_tree.nodes['Background'].inputs['Strength'].default_value=.8
 bpy.ops.object.camera_add(location=look);cam=bpy.context.object;cam.name='overview_camera';cam.rotation_euler=(Vector(at)-cam.location).to_track_quat('-Z','Y').to_euler();cam.data.type='ORTHO';cam.data.ortho_scale=scale
 scene=bpy.context.scene;scene.camera=cam
 for i,loc in enumerate(((2,-4,10),(-5,-1,7))):
  bpy.ops.object.light_add(type='AREA',location=loc);light=bpy.context.object;light.name='softbox';light.data.energy=900 if i==0 else 500;light.data.shape='DISK';light.data.size=7
 scene.render.engine='BLENDER_EEVEE';scene.render.resolution_x=width;scene.render.resolution_y=height;scene.render.resolution_percentage=100
 scene.render.image_settings.file_format='PNG';scene.render.film_transparent=False
 scene.render.filepath=str(path/'overview_v01.png');scene.render.image_settings.color_mode='RGBA';scene.render.film_transparent=False
 scene.render.engine='BLENDER_EEVEE';scene.render.use_file_extension=True
 scene.render.resolution_percentage=100;scene.render.image_settings.color_depth='8'
 scene.view_settings.view_transform='AgX'
 bpy.ops.wm.save_as_mainfile(filepath=str(path/'scene_v01.blend'))
 bpy.ops.render.render(write_still=True)
