"""04 v04 photo-level board: smaller visible gold center package relative to board; right connector bank remains a density PROXY. Run Blender --background --python build_scene_v04.py."""
import bpy,math
from mathutils import Vector
from pathlib import Path
R=Path(__file__).resolve().parent;bpy.ops.object.select_all(action='SELECT');bpy.ops.object.delete(use_global=False)
def mat(n,c,met=0):
 m=bpy.data.materials.new(n);m.diffuse_color=(*c,1);m.use_nodes=True;p=next(q for q in m.node_tree.nodes if q.type=='BSDF_PRINCIPLED');p.inputs['Base Color'].default_value=(*c,1);p.inputs['Metallic'].default_value=met;p.inputs['Roughness'].default_value=.48;return m
board=mat('main PCB green soldermask',(.045,.25,.11));sub=mat('small under-board pale electronics',(.62,.65,.58));ceramic=mat('pale central ceramic die carrier',(.75,.71,.48));gold=mat('gold finish around central carrier and coax plugs',(.65,.45,.13),.75);chip=mat('exposed central microelectronic die dark green',(.20,.26,.11),.35);black=mat('black connector jacket',(.035,.04,.04));metal=mat('silver shell of mating coax plugs',(.55,.58,.56),.72);bg=mat('studio stage',(.22,.23,.22))
def box(n,p,d,m):
 bpy.ops.mesh.primitive_cube_add(size=1,location=p);o=bpy.context.object;o.name=n;o.dimensions=d;bpy.ops.object.transform_apply(location=False,rotation=False,scale=True);o.data.materials.append(m);return o
def cyl(n,p,r,h,m,axis=(0,0,1)):
 bpy.ops.mesh.primitive_cylinder_add(vertices=28,radius=r,depth=h,location=p);o=bpy.context.object;o.name=n;o.rotation_euler=Vector((0,0,1)).rotation_difference(Vector(axis)).to_euler();o.data.materials.append(m);return o
def cable(n,points,r,m):
 c=bpy.data.curves.new(n,'CURVE');c.dimensions='3D';c.bevel_depth=r;c.bevel_resolution=3;s=c.splines.new('BEZIER');s.bezier_points.add(len(points)-1)
 for q,v in zip(s.bezier_points,points):q.co=v;q.handle_left_type='AUTO';q.handle_right_type='AUTO'
 o=bpy.data.objects.new(n,c);bpy.context.collection.objects.link(o);o.data.materials.append(m)
box('dominant rectangular green PCB',(0,0,.38),(5.2,2.48,.11),board)
# A smaller exposed board protrudes from underneath near the near edge; exact identities remain unknown.
box('lower attached pale daughter PCB',(.11,-.84,.16),(1.63,1.36,.10),sub)
for i in range(6):box(f'daughter board visible small part {i}',(-.52+i*.20,-1.31,.23),(.095,.13,.045),black)
# Restore a SMALL photo-proportioned gold package relative to the full 5.2-unit board width;
# schematic width ratio 0.78/5.2=.15, not a physical measurement from a calibrated photo.
box('central small square package outer gold mount',(-.73,.36,.465),(.78,.73,.075),gold)
box('central pale package border',(-.73,.36,.507),(.61,.56,.012),ceramic)
box('central dark inset of visible package',(-.73,.36,.518),(.34,.31,.013),chip)
for i in range(12):
 x=-1.035+i*.055;box(f'fine bond edge surrogate {i}',(x,.765,.515),(.032,.055,.006),gold)
# Two ordered rows of fine pads run lengthwise adjacent to chip, not indiscriminate board edge stripes.
for row,y in enumerate((-.45,-.18)):
 for i in range(20):box(f'visible small PCB pad row {row} index {i}',(-1.7+i*.18,y,.446),(.075,.040,.007),gold)
box('small black surface connector at main-board left',(-2.36,.11,.54),(.42,.57,.22),black)
box('terminal dark header near main-board back',(-.02,1.04,.52),(.64,.21,.17),black)
# Dense photo-level right connector bank. Count 5 is ONLY a sampling of visually repeated parts;
# do not equate proxy sockets to a measured number of ports, cables or signal channels.
for i,y in enumerate((-.92,-.60,-.28,.04,.36)):
 cyl(f'gold visible board-edge socket proxy {i}',(2.57,y,.48),.108,.30,gold,(1,0,0))
 cyl(f'mating metal ring attached to socket {i}',(2.78,y,.48),.113,.15,metal,(1,0,0))
 cyl(f'dark jacket at visible interface {i}',(2.97,y,.48),.11,.25,black,(1,0,0))
 cable(f'continuous external cable proxy {i}',[(3.04,y,.48),(3.48,y+.01,.53),(4.03,y+.10*(i-2),.46)],.053,black)
# Connector shell begins flush with PCB edge at x=2.6 and cables start inside strain relief.
box('neutral surface',(0,0,-.20),(12,8,.10),bg)
for p,power in [((-4,-5,7),650),((4,3,6),400)]:
 bpy.ops.object.light_add(type='AREA',location=p);o=bpy.context.object;o.data.energy=power;o.data.size=5;o.rotation_euler=(Vector((0,0,.3))-o.location).to_track_quat('-Z','Y').to_euler()
bpy.ops.object.camera_add(location=(2,-6,7));cam=bpy.context.object;cam.name='04 v04 smaller gold package on mainboard';cam.rotation_euler=(Vector((.5,0,.36))-cam.location).to_track_quat('-Z','Y').to_euler();cam.data.type='ORTHO';cam.data.ortho_scale=7.5;bpy.context.scene.camera=cam
s=bpy.context.scene;s.render.engine='BLENDER_EEVEE';s.render.resolution_x=880;s.render.resolution_y=590;s.render.resolution_percentage=100;s.render.filepath=str(R/'overview_v04.png');s.render.image_settings.file_format='PNG';bpy.ops.wm.save_as_mainfile(filepath=str(R/'scene_v04.blend'));bpy.ops.render.render(write_still=True);print('CASE04_v04_SAVED')
