"""Small editable-Blender assembly primitives; explicit source/assumption tagging.

This is a batch-specific scaffold, not a replacement for the installed Skill's audit.
Case coordinates are illustrative, not paper dimensions. A separate Blender process
reloads each saved scene before rendering. No text objects are added to scene.
"""
import bpy, math
from mathutils import Vector

BG=(0.88,0.92,0.96,1)

def material(name,color,metal=0.0,rough=0.55,alpha=1):
 m=bpy.data.materials.get(name) or bpy.data.materials.new(name);m.diffuse_color=(*color[:3],alpha)
 m.use_nodes=True; p=m.node_tree.nodes.get('Principled BSDF');p.inputs['Base Color'].default_value=(*color[:3],1);p.inputs['Metallic'].default_value=metal;p.inputs['Roughness'].default_value=rough
 if alpha<1:
  p.inputs['Alpha'].default_value=alpha
  if hasattr(m,'surface_render_method'):m.surface_render_method='DITHERED'
 return m

M={}
def setup():
 bpy.ops.object.select_all(action='SELECT');bpy.ops.object.delete(use_global=False)
 bpy.context.scene.render.engine='BLENDER_EEVEE';bpy.context.scene.render.resolution_x=900;bpy.context.scene.render.resolution_y=640;bpy.context.scene.render.resolution_percentage=100
 bpy.context.scene.render.image_settings.file_format='PNG';bpy.context.scene.render.film_transparent=False
 bpy.context.scene.render.engine='BLENDER_EEVEE';bpy.context.scene.render.resolution_x=900
 if hasattr(bpy.context.scene,'eevee'):bpy.context.scene.eevee.taa_render_samples=16
 bpy.context.scene.world.color=(0.35,0.38,0.43)
 colors={'base':((0.22,0.30,0.36),0.12),'metal':((0.43,0.52,0.59),0.7),'dark':((0.09,0.14,0.20),0.1),'screen':((0.10,0.45,0.52),0.0),'blue':((0.16,0.48,0.78),0.1),'red':((0.75,0.25,0.20),0.1),'copper':((0.60,0.34,0.18),0.55),'soft':((0.85,0.60,0.37),0.0),'white':((0.79,0.85,0.86),0.05),'glass':((0.46,0.72,0.78),0.05),'black':((0.03,0.04,0.06),0.1),'yellow':((0.85,0.72,0.29),0.0)}
 for k,(c,metal) in colors.items():M[k]=material('MAT_'+k,c,metal,alpha=0.30 if k=='glass' else 1)
 box('Backdrop', (0,0,-0.26),(15,10,0.08),'white','assumption')
 camera((9,-12,8),(0,0,0.8));light((1,-5,8),1100);light((-6,3,6),650)

def tag(obj,evidence='assumption',owner=''):
 obj['evidence_type']=evidence;obj['owner']=owner or obj.name;return obj

def box(name,loc,scale,mat='base',evidence='assumption',bevel=0.04):
 bpy.ops.mesh.primitive_cube_add(size=1,location=loc);o=bpy.context.object;o.name=name;o.dimensions=scale;bpy.ops.object.transform_apply(location=False,rotation=False,scale=True)
 o.data.materials.append(M[mat]);tag(o,evidence)
 if bevel:
  mod=o.modifiers.new('Editable edge fillet','BEVEL');mod.width=bevel;mod.segments=2
  o.modifiers.new('Weighted normals','WEIGHTED_NORMAL')
 return o

def cyl(name,loc,radius,depth,mat='metal',axis='Z',evidence='assumption',vertices=24):
 bpy.ops.mesh.primitive_cylinder_add(vertices=vertices,radius=radius,depth=depth,location=loc);o=bpy.context.object;o.name=name
 if axis=='X':o.rotation_euler[1]=math.pi/2
 if axis=='Y':o.rotation_euler[0]=math.pi/2
 o.data.materials.append(M[mat]);return tag(o,evidence)

def torus(name,loc,major,minor,mat='metal',axis='Z',evidence='assumption'):
 bpy.ops.mesh.primitive_torus_add(major_radius=major,minor_radius=minor,major_segments=32,minor_segments=8,location=loc);o=bpy.context.object;o.name=name
 if axis=='Y':o.rotation_euler[0]=math.pi/2
 if axis=='X':o.rotation_euler[1]=math.pi/2
 o.data.materials.append(M[mat]);return tag(o,evidence)

def route(name,pts,r=.035,mat='black',evidence='assumption'):
 cu=bpy.data.curves.new(name,'CURVE');cu.dimensions='3D';cu.resolution_u=18;cu.bevel_depth=r;cu.bevel_resolution=3
 spline=cu.splines.new('POLY');spline.points.add(len(pts)-1)
 for p,xyz in zip(spline.points,pts):p.co=(*xyz,1)
 ob=bpy.data.objects.new(name,cu);bpy.context.collection.objects.link(ob);cu.materials.append(M[mat]);return tag(ob,evidence)

def segment(name,a,b,r=.04,mat='metal',evidence='assumption'):
 a=Vector(a);b=Vector(b);m=(a+b)*.5;o=cyl(name,m,r,(b-a).length,mat,evidence=evidence);o.rotation_euler=(b-a).to_track_quat('Z','Y').to_euler();return o

def open_port(name,loc,r=.1,axis='Y',owner=''):
 # Annular mesh has actual empty center; attached to visible panel by the caller.
 o=torus(name,loc,r,.025,'metal',axis,evidence='source-visible');o['physical_owner']=owner;return o

def camera(pos,target=(0,0,0),orth=12):
 bpy.ops.object.camera_add(location=pos);c=bpy.context.object;c.name='Overview_Camera';c.rotation_euler=(Vector(target)-c.location).to_track_quat('-Z','Y').to_euler();c.data.type='ORTHO';c.data.ortho_scale=orth;bpy.context.scene.camera=c;return c

def light(loc,power):
 bpy.ops.object.light_add(type='AREA',location=loc);o=bpy.context.object;o.data.energy=power;o.data.shape='DISK';o.data.size=8

def laptop(x,y,z,screen=True):
 box('Laptop_Base',(x,y,z),(.95,.68,.10),'metal');box('Laptop_Keyboard',(x,y-.06,z+.07),(.70,.35,.012),'dark',bevel=0)
 cyl('Laptop_Hinge',(x,y+.31,z+.10),.025,.85,'dark',axis='X')
 if screen:
  s=box('Laptop_Display',(x,y+.36,z+.51),(.95,.065,.76),'dark');s.rotation_euler[0]=-.13
  display=box('Laptop_Screen',(x,y+.315,z+.51),(.80,.01,.59),'screen',bevel=.02);display.rotation_euler[0]=-.13
 open_port('Laptop_Data_Port',(x+.49,y-.04,z),.05,'X','Laptop_Base')

def pump(x,y,z,idx=0):
 box(f'Pump_{idx}_frame',(x,y,z),(.84,.72,.43),'base');box(f'Pump_{idx}_display',(x,y-.365,z+.04),(.25,.016,.14),'screen',bevel=.01)
 cyl(f'Pump_{idx}_barrel',(x,y,z+.30),.10,.57,'glass',axis='Y',evidence='source-visible');cyl(f'Pump_{idx}_piston',(x,y+.38,z+.30),.035,.33,'metal',axis='Y')
 cyl(f'Pump_{idx}_hub',(x,y-.38,z+.30),.062,.12,'metal',axis='Y');open_port(f'Pump_{idx}_nozzle',(x,y-.44,z+.30),.050,'Y',f'Pump_{idx}_barrel')
