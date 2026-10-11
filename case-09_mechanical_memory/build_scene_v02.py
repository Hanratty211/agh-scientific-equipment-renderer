"""09 single modified-TCO static cell: pentagonal transparent plates, hinged diagonals and coil segments fixed at BOTH junctions. Run Blender --background --python build_scene_v02.py."""
import bpy,math
from pathlib import Path
from mathutils import Vector
R=Path(__file__).resolve().parent;bpy.ops.object.select_all(action='SELECT');bpy.ops.object.delete(use_global=False)
def mat(n,c,m=0,a=1):
 q=bpy.data.materials.new(n);q.diffuse_color=(*c,a);q.use_nodes=True;p=next(v for v in q.node_tree.nodes if v.type=='BSDF_PRINCIPLED');p.inputs['Base Color'].default_value=(*c,1);p.inputs['Metallic'].default_value=m;p.inputs['Roughness'].default_value=.39
 if a<1:p.inputs['Alpha'].default_value=a;q.surface_render_method='DITHERED'
 return q
acrylic=mat('transparent acrylic appearance of plate',(.69,.83,.81),0,.46);rim=mat('clear pale plate edge',(.45,.52,.52));rodmat=mat('stainless steel visible shaft proxy',(.56,.58,.60),.69);coilmat=mat('metallic coil on diagonal rods',(.66,.59,.43),.72);joint=mat('dark 3D printed universal-joint proxy',(.14,.16,.18));bg=mat('plain stage',(.19,.20,.21))
def seg(n,a,b,r,ma):
 a=Vector(a);b=Vector(b);d=b-a;bpy.ops.mesh.primitive_cylinder_add(vertices=18,radius=r,depth=d.length,location=(a+b)/2);o=bpy.context.object;o.name=n;o.rotation_euler=Vector((0,0,1)).rotation_difference(d.normalized()).to_euler();o.data.materials.append(ma)
def ball(n,p,r,ma):
 bpy.ops.mesh.primitive_uv_sphere_add(segments=12,ring_count=8,radius=r,location=p);o=bpy.context.object;o.name=n;o.data.materials.append(ma)
def meshplate(n,r,z,ang):
 N=5;xy=[(r*math.cos(ang+2*math.pi*i/N),r*math.sin(ang+2*math.pi*i/N)) for i in range(N)];v=[(x,y,z+h) for h in (-.045,.045) for x,y in xy];f=[tuple(range(N-1,-1,-1)),tuple(range(N,2*N))]
 for i in range(N):j=(i+1)%N;f.append((i,j,N+j,N+i))
 me=bpy.data.meshes.new(n);me.from_pydata(v,[],f);me.update();o=bpy.data.objects.new(n,me);bpy.context.collection.objects.link(o);o.data.materials.append(acrylic)
 for i in range(N):seg(n+' rim '+str(i),(*xy[i],z+.048),(*xy[(i+1)%N],z+.048),.019,rim)
 return [Vector((x,y,z)) for x,y in xy]
low=meshplate('lower transparent pentagonal polygon',1.19,.19,.05);high=meshplate('upper transparent pentagonal polygon',1.19,2.30,.42)
for i in range(5):
 # Each diagonal attaches precisely between a lower and adjacent upper polygon vertex.
 a=low[i];b=high[(i+1)%5];axis=(b-a).normalized();length=(b-a).length
 ball(f'lower polygon pivot {i}',a,.10,joint);ball(f'upper polygon pivot {i}',b,.10,joint)
 seg(f'continuous diagonal rod {i}',a,b,.037,rodmat)
 # Coil sits axially ON this same rod and touches lower/upper sleeve collars at exactly s=.35/.65.
 t0=.33;t1=.68;start=a+(b-a)*t0;end=a+(b-a)*t1
 seg(f'lower fixed sleeve {i}',a+(b-a)*.12,start,.057,rodmat)
 seg(f'upper fixed sleeve {i}',end,a+(b-a)*.88,.057,rodmat)
 side=axis.cross(Vector((0,0,1))).normalized();cross=axis.cross(side).normalized();rad=.081;turns=6
 c=bpy.data.curves.new(f'spring {i} curve','CURVE');c.dimensions='3D';c.bevel_depth=.014;c.bevel_resolution=3;sp=c.splines.new('POLY');steps=120;sp.points.add(steps)
 for j in range(steps+1):
  t=j/steps;rise=math.sin(math.pi*t)**.5;v=start+(end-start)*t+rad*rise*(side*math.cos(2*math.pi*turns*t)+cross*math.sin(2*math.pi*turns*t));sp.points[j].co=(*v,1)
 ob=bpy.data.objects.new(f'coil physically terminated at both sleeves {i}',c);bpy.context.collection.objects.link(ob);ob.data.materials.append(coilmat)
 # Assert relative ends mathematically: zero radial offset at both sleeve tips.
 assert (Vector(sp.points[0].co[:3])-start).length<1e-5 and (Vector(sp.points[-1].co[:3])-end).length<1e-5
bpy.ops.mesh.primitive_cube_add(size=1,location=(0,0,-.26));o=bpy.context.object;o.name='neutral stage';o.dimensions=(9,9,.12);bpy.ops.object.transform_apply(location=False,rotation=False,scale=True);o.data.materials.append(bg)
for p,pow in [((-4,-5,7),720),((4,2,5),440)]:
 bpy.ops.object.light_add(type='AREA',location=p);o=bpy.context.object;o.data.energy=pow;o.data.size=4;o.rotation_euler=(Vector((0,0,1))-o.location).to_track_quat('-Z','Y').to_euler()
bpy.ops.object.camera_add(location=(4,-6,4.2));cam=bpy.context.object;cam.name='09 v02 connected TCO coil sleeves';cam.rotation_euler=(Vector((0,0,1.16))-cam.location).to_track_quat('-Z','Y').to_euler();cam.data.type='ORTHO';cam.data.ortho_scale=4.6;bpy.context.scene.camera=cam
s=bpy.context.scene;s.render.engine='BLENDER_EEVEE';s.render.resolution_x=760;s.render.resolution_y=800;s.render.resolution_percentage=100;s.render.filepath=str(R/'overview_v02.png');s.render.image_settings.file_format='PNG';bpy.ops.wm.save_as_mainfile(filepath=str(R/'scene_v02.blend'));bpy.ops.render.render(write_still=True);print('CASE09_v02_SAVED')
