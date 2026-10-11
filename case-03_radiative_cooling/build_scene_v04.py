"""03 v04 photo-level: one cross-post fine wire, little white disk, annular cylinder top, stronger reflective metal lighting. Mount unknown. Run Blender --background --python build_scene_v04.py."""
import bpy,math
from pathlib import Path
from mathutils import Vector
R=Path(__file__).resolve().parent;bpy.ops.object.select_all(action='SELECT');bpy.ops.object.delete(use_global=False)
def mat(n,c,m=0,a=1):
 q=bpy.data.materials.new(n);q.diffuse_color=(*c,a);q.use_nodes=True;p=next(v for v in q.node_tree.nodes if v.type=='BSDF_PRINCIPLED');p.inputs['Base Color'].default_value=(*c,1);p.inputs['Metallic'].default_value=m;p.inputs['Roughness'].default_value=.07 if m else .62
 if a<1:p.inputs['Alpha'].default_value=a;q.surface_render_method='DITHERED'
 return q
alu=mat('bright reflective tray aluminium visual proxy',(.89,.92,.93),.98);dark=mat('dark reflective cylinder rim',(.26,.33,.38),.73);blue=mat('blue cylinder external appearance',(.16,.34,.52),.62);foil=mat('clear cover visual proxy identity unknown',(.71,.83,.87),.25,.45);wiremat=mat('fine transverse wire',(.78,.82,.79),.68);black=mat('dark visible center region identity unknown',(.025,.055,.09));white=mat('white small circular plate visible above transverse wires',(.92,.91,.87),.12);ground=mat('background',(.19,.20,.21))
def box(n,p,d,m):
 bpy.ops.mesh.primitive_cube_add(size=1,location=p);o=bpy.context.object;o.name=n;o.dimensions=d;bpy.ops.object.transform_apply(location=False,rotation=False,scale=True);o.data.materials.append(m);return o
def cyl(n,p,r,h,m,N=48):
 bpy.ops.mesh.primitive_cylinder_add(vertices=N,radius=r,depth=h,location=p);o=bpy.context.object;o.name=n;o.data.materials.append(m);return o
def annulus(n,p,ro,ri,h,m,N=64):
 verts=[];faces=[]
 for z,r in [(-h/2,ro),(-h/2,ri),(h/2,ro),(h/2,ri)]:
  for i in range(N):t=2*math.pi*i/N;verts.append((p[0]+r*math.cos(t),p[1]+r*math.sin(t),p[2]+z))
 for i in range(N):
  j=(i+1)%N
  # Four annular surfaces: outside, inside, lower face, upper face.
  faces.extend([(i,j,2*N+j,2*N+i),(N+j,N+i,3*N+i,3*N+j),(i,N+i,N+j,j),(2*N+j,3*N+j,3*N+i,2*N+i)])
 mesh=bpy.data.meshes.new(n);mesh.from_pydata(verts,[],faces);mesh.update();o=bpy.data.objects.new(n,mesh);bpy.context.collection.objects.link(o);o.data.materials.append(m);return o
def line(n,pts,rad,m):
 c=bpy.data.curves.new(n,'CURVE');c.dimensions='3D';c.bevel_depth=rad;c.bevel_resolution=3;s=c.splines.new('POLY');s.points.add(len(pts)-1)
 for v,p in zip(s.points,pts):v.co=(*p,1)
 o=bpy.data.objects.new(n,c);bpy.context.collection.objects.link(o);o.data.materials.append(m)
box('reflective lower tray broad foot',(0,0,.075),(3.45,2.55,.15),alu);box('second stepped reflective tray level',(.0,.06,.164),(3.15,2.30,.032),alu);box('rear raised reflective movable surface',(.24,.55,.23),(2.72,1.0,.06),alu)
box('translucent film canopy low over base',(0,-.15,.26),(2.8,1.8,.012),foil)
# Broad annular top ring encloses a clearly visible circular area. No segmented cap or convex nub.
cyl('blue central vertical cylindrical outside',(0,.02,.77),.55,.99,blue)
annulus('wide annular cylinder top surrounding visible circular region',(0,.02,1.285),.62,.34,.063,alu)
cyl('dark circular region visibly recessed within annular top',(0,.02,1.246),.335,.009,black)
for j,(x,y) in enumerate([(-1.36,.65),(1.40,.62)]):
 annulus(f'tall hollow metallic support tube {j}',(x,y,1.52),.088,.052,2.70,alu,36)
 cyl(f'dark visible opening of tall support {j}',(x,y,2.90),.050,.005,black)
 cyl(f'foot of tall support {j}',(x,y,.23),.16,.07,dark)
# ONE photo-supported transverse wire; white small plate is independently visible above it.
line('single cross-post fine wire',[(-1.36,.65,2.92),(-.64,.62,2.83),(0,.57,2.79),(.68,.63,2.84),(1.40,.62,2.92)],.010,wiremat)
cyl('small white circular plate above the single transverse wire',(0,.53,2.88),.27,.048,white)
line('thin wire from cylinder ring to left frame edge',[(0,.0,1.27),(-.52,-.20,1.31),(-1.6,-.88,.44)],.009,wiremat)
box('small edge mounted black terminal',(-1.47,-1.01,.32),(.70,.19,.16),black)
box('neutral stage',(0,0,-.24),(10,9,.09),ground)
for xyz,power in [((-4,-5,7),1100),((3,3,6),670),((0,5,4),510)]:
 bpy.ops.object.light_add(type='AREA',location=xyz);o=bpy.context.object;o.data.energy=power;o.data.size=4;o.rotation_euler=(Vector((0,0,1))-o.location).to_track_quat('-Z','Y').to_euler()
bpy.ops.object.camera_add(location=(5,-7,5.0));cam=bpy.context.object;cam.name='03 v04 one line and reflective metal overview' ;cam.rotation_euler=(Vector((0,0,1.32))-cam.location).to_track_quat('-Z','Y').to_euler();cam.data.type='ORTHO';cam.data.ortho_scale=5.35;bpy.context.scene.camera=cam
s=bpy.context.scene;s.render.engine='BLENDER_EEVEE';s.render.resolution_x=820;s.render.resolution_y=720;s.render.resolution_percentage=100;s.render.filepath=str(R/'overview_v04.png');s.render.image_settings.file_format='PNG';bpy.ops.wm.save_as_mainfile(filepath=str(R/'scene_v04.blend'));bpy.ops.render.render(write_still=True);print('CASE03_v04_SAVED')
