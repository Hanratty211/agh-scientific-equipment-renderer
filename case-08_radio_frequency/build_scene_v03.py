"""08 fabricated vertical panel with dense thin horizontal stripes and tiny unit texture; no invented L-shaped circuits or black edge box. Run Blender --background --python build_scene_v03.py."""
import bpy
from pathlib import Path
from mathutils import Vector
R=Path(__file__).resolve().parent;bpy.ops.object.select_all(action='SELECT');bpy.ops.object.delete(use_global=False)
def mat(n,c,metal=0):
 m=bpy.data.materials.new(n);m.diffuse_color=(*c,1);m.use_nodes=True;p=next(v for v in m.node_tree.nodes if v.type=='BSDF_PRINCIPLED');p.inputs['Base Color'].default_value=(*c,1);p.inputs['Metallic'].default_value=metal;p.inputs['Roughness'].default_value=.48;return m
panel=mat('pale photograph face of manufactured metasurface',(.68,.69,.60));trace=mat('dark etched repeating stripes',(.24,.29,.27),.28);blue=mat('blue metal fixture',(.13,.32,.55),.25);cablemat=mat('dark insulated edge wire',(.04,.06,.08));screw=mat('fixture fastener silver',(.62,.64,.66),.64);back=mat('neutral stage',(.17,.19,.21))
def box(n,p,d,ma):
 bpy.ops.mesh.primitive_cube_add(size=1,location=p);o=bpy.context.object;o.name=n;o.dimensions=d;bpy.ops.object.transform_apply(location=False,rotation=False,scale=True);o.data.materials.append(ma);return o
def cyl(n,p,r,depth,ma,axis=(0,0,1)):
 bpy.ops.mesh.primitive_cylinder_add(vertices=24,radius=r,depth=depth,location=p);o=bpy.context.object;o.name=n;o.rotation_euler=Vector((0,0,1)).rotation_difference(Vector(axis)).to_euler();o.data.materials.append(ma)
def path(n,pts,r,ma):
 c=bpy.data.curves.new(n,'CURVE');c.dimensions='3D';c.bevel_depth=r;c.bevel_resolution=3;s=c.splines.new('POLY');s.points.add(len(pts)-1)
 for p,q in zip(s.points,pts):p.co=(*q,1)
 o=bpy.data.objects.new(n,c);bpy.context.collection.objects.link(o);o.data.materials.append(ma)
# X/Z is vertical photograph plane, with its broad face toward -Y.
box('vertical fabricated metasurface face',(0,.0,2.30),(3.62,.105,4.45),panel)
# Dense short horizontal rows with small isolated unit marks, not thick L-shaped circuitry.
# Repetition density is a readability proxy; exact meta-atom geometry/count remains unknown.
for k in range(22):
 z=.38+k*.177
 box(f'fine continuous horizontal band row {k}',(0,-.061,z),(3.43,.007,.014),trace)
 for j in range(16):
  x=-1.58+j*.210
  box(f'small horizontal isolated unit row{k} col{j}',(x,-.072,z+.073),(.115,.009,.012),trace)
for x in (-1.92,1.92):
 box(f'blue left-right vertical support {x}',(x,.18,2.22),(.23,.39,4.58),blue)
 for z in (.35,4.06):cyl(f'support fixing at x{x} z{z}',(x,-.035,z),.075,.025,screw,(0,1,0))
box('blue base foot',(0,.12,.18),(4.07,.52,.28),blue)
box('blue top bridge',(0,.12,4.55),(4.07,.40,.18),blue)
# Preserve only a thin visible edge line, terminating where the panel-side trace disappears.
# No separate black box, control-system function, or panel-side connector identity inferred.
path('thin unassigned edge line ending at visible blue support',[(1.84,-.08,1.26),(1.98,-.16,1.25),(2.16,-.26,1.09),(2.47,-.38,.90)],.025,cablemat)
box('neutral rear backdrop',(0,2.2,2.0),(10,.14,9),back)
for p,pow in [((-4,-6,7),680),((4,-3,6),430)]:
 bpy.ops.object.light_add(type='AREA',location=p);o=bpy.context.object;o.data.energy=pow;o.data.size=5;o.rotation_euler=(Vector((0,0,2))-o.location).to_track_quat('-Z','Y').to_euler()
bpy.ops.object.camera_add(location=(2,-7,4.2));cam=bpy.context.object;cam.name='08 v03 dense fine horizontal panel pattern';cam.rotation_euler=(Vector((0,0,2.20))-cam.location).to_track_quat('-Z','Y').to_euler();cam.data.type='ORTHO';cam.data.ortho_scale=6.15;bpy.context.scene.camera=cam
s=bpy.context.scene;s.render.engine='BLENDER_EEVEE';s.render.resolution_x=760;s.render.resolution_y=860;s.render.resolution_percentage=100;s.render.filepath=str(R/'overview_v03.png');s.render.image_settings.file_format='PNG';bpy.ops.wm.save_as_mainfile(filepath=str(R/'scene_v03.blend'));bpy.ops.render.render(write_still=True);print('CASE08_v03_SAVED')
