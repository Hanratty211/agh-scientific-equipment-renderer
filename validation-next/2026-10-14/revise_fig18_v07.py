"""Fig18 v06 -> v07: replace only front face with continuous diagonal interlaced ribbons.
No new physical node geometry; depth, strand size and actual crossings illustrative.
"""
import bpy,sys,math
from pathlib import Path
root=Path(__file__).resolve().parent;sys.path.insert(0,str(root))
import render_core as r
from mathutils import Vector
r.M.clear()
for mat in bpy.data.materials:
 if mat.name.startswith('MAT_'):r.M[mat.name[4:]]=mat
sc=bpy.context.scene
if sc.get('revision_version')!='v06_fig18_broad_weave':raise RuntimeError('expected v06 parent')
out=root/'cases/18_mechanical_nature/v07_fig18_diagonal_weave'
if out.exists():raise RuntimeError('refuse overwrite')
plates={k:(tuple(bpy.data.objects[k].location),tuple(bpy.data.objects[k].rotation_euler),tuple(bpy.data.objects[k].scale)) for k in ('Fig18_upper_compression_plate','Fig18_lower_compression_plate')}
for j in range(15):
 for prefix in ('PIM_interlaced_front_','CIM_interlaced_cross_'):
  bpy.data.objects.remove(bpy.data.objects[prefix+str(j)],do_unlink=True)

def strand(name,pts,mat):
 cu=bpy.data.curves.new(name,'CURVE');cu.dimensions='3D';cu.resolution_u=32;cu.bevel_depth=.013;cu.bevel_resolution=4
 s=cu.splines.new('BEZIER');s.bezier_points.add(len(pts)-1)
 for q,point in zip(s.bezier_points,pts):q.co=point;q.handle_left_type='AUTO';q.handle_right_type='AUTO'
 ob=bpy.data.objects.new(name,cu);bpy.context.collection.objects.link(ob);cu.materials.append(r.M[mat]);r.tag(ob,'assumption')
 ob['evidence']='Fig18 left visible wavy interwoven face; individual trajectories illustrative'
 ob['unknown']='node bond, mechanical loading, material cross section, real Z/depth'
 return ob
# Parametric families run corner-to-corner at ±45° in front plane; neither is a
# horizontal-short-bar family. Boundary clipping yields continuous complete curves.
# Coordinate s=(x+z)/sqrt2, t=(z-x)/sqrt2 relative to square centre.
# Solve x=(s-t)/sqrt2, z=(s+t)/sqrt2. Start -1.9..1.9 & retain sample points inside face.
center_z=2.09;radius=.67;count=17
for family in (0,1):
 for j in range(count):
  lane=-.88+1.76*j/(count-1);coords=[]
  for k in range(281):
   u=-1.85+3.7*k/280
   # Warp the transverse diagonal coordinate with smooth phase staggering.
   transverse=lane+.045*math.sin(2*math.pi*2.8*u + j*.72)+.014*math.sin(2*math.pi*1.5*u+j*.43)
   if family==0:x=(u-transverse)/math.sqrt(2);z=center_z+(u+transverse)/math.sqrt(2)
   else:x=(u+transverse)/math.sqrt(2);z=center_z+(transverse-u)/math.sqrt(2)
   # Smooth shallow crossover ordering, not a claimed measured node architecture.
   y=.22+(.018 if family else -.018)+.011*math.sin(2*math.pi*2.8*u+j*.72)
   if abs(x)<=radius and abs(z-center_z)<=radius:coords.append((x,y,z))
  if len(coords)>4:strand(('CIM_diagonal_weave_' if family else 'PIM_diagonal_weave_')+str(j),coords,'soft' if family else 'blue')
assert all(tuple(bpy.data.objects[k].location)==v[0] and tuple(bpy.data.objects[k].rotation_euler)==v[1] and tuple(bpy.data.objects[k].scale)==v[2] for k,v in plates.items())
sc['revision_version']='v07_fig18_diagonal_weave';sc['visual_review']='PENDING_EXTERNAL';sc['source_location']='Supplementary Fig18 left visible weave; Fig18 middle compression plate assembly';sc['weave_limit']='illustrative 2 diagonal wavy families and representative depth offset, NOT true bonds/depth/material/force'
bpy.context.view_layer.update();out.mkdir(parents=True);bpy.ops.wm.save_as_mainfile(filepath=str(out/'scene.blend'));print('FIG18_V07_SAVED',str(out/'scene.blend'),flush=True)
