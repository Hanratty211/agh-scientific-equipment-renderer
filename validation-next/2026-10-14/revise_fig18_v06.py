"""Rebuild only Fig18 face from saved v05; keep machine frame and compression plates untouched.
Source: Supplementary Fig18 left ~20x20 mm visible face; waveform, depth and links are
illustrative assumptions. Smooth Bézier geometry with no abrupt depth flips or loose knots.
"""
import bpy,sys,math
from pathlib import Path
root=Path(__file__).resolve().parent;sys.path.insert(0,str(root))
import render_core as r
r.M.clear()
for m in bpy.data.materials:
 if m.name.startswith('MAT_'):r.M[m.name[4:]]=m
if bpy.context.scene.get('revision_version')!='v05_fig18_dense_weave':raise RuntimeError('wrong source revision')
for j in range(13):
 for prefix in ('PIM_dense_wavy_','CIM_dense_wavy_'):
  ob=bpy.data.objects.get(prefix+str(j))
  if ob:bpy.data.objects.remove(ob,do_unlink=True)

def path(name,points,depth,mat):
 cu=bpy.data.curves.new(name,'CURVE');cu.dimensions='3D';cu.resolution_u=32;cu.bevel_depth=depth;cu.bevel_resolution=3
 spline=cu.splines.new('BEZIER');spline.bezier_points.add(len(points)-1)
 for p,xyz in zip(spline.bezier_points,points):p.co=xyz;p.handle_left_type='AUTO';p.handle_right_type='AUTO'
 ob=bpy.data.objects.new(name,cu);bpy.context.collection.objects.link(ob);cu.materials.append(r.M[mat]);r.tag(ob,'assumption')
 ob['basis']='Fig18 left visually dense wavy interwoven face; form representative only';ob['unknown']='crossing bond, physical strand section, depth and mechanics not resolved'
 return ob
# Retain the Fig18 face bounds x[-.67,.67], z[1.42,2.76]. More strands and thicker
# smooth continuous extrusions, with diagonal drift to break orthogonal graph-paper appearance.
count=15;x0,x1=-.67,.67;z0,z1=1.42,2.76;yc=.22
for j in range(count):
 x_center=x0+j*(x1-x0)/(count-1);pts=[]
 for k in range(97):
  t=k/96;z=z0+(z1-z0)*t
  # Taper drift at endpoints to preserve square outline; alternating phase/direction.
  drift=(.026 if j%2 else -.026)*math.sin(math.pi*t)
  x=x_center+drift+.023*math.sin(2*math.pi*(3.5*t)+j*.63)*math.sin(math.pi*t)
  # Smooth periodic y through each crossover; no pointwise abrupt y sign flips.
  y=yc-.033+.011*math.sin(2*math.pi*(3.5*t)+j*.63)
  pts.append((x,y,z))
 path(f'PIM_interlaced_front_{j}',pts,.016,'blue')
for j in range(count):
 z_center=z0+j*(z1-z0)/(count-1);pts=[]
 for k in range(97):
  t=k/96;x=x0+(x1-x0)*t
  drift=(.026 if j%2 else -.026)*math.sin(math.pi*t)
  z=z_center+drift+.023*math.sin(2*math.pi*3.5*t+(j+1)*.63)*math.sin(math.pi*t)
  y=yc+.033-.011*math.sin(2*math.pi*3.5*t+(j+1)*.63)
  pts.append((x,y,z))
 path(f'CIM_interlaced_cross_{j}',pts,.016,'soft')
sc=bpy.context.scene;sc['revision_version']='v06_fig18_broad_weave';sc['visual_review']='external_pixel_review_pending';sc['source_location']='Supplementary Fig18 left interwoven 20x20 mm visible front face + middle compression plates only';sc['weave_limit']='two smoothly offset visible strand families; no claim of actual cross-joints, sample thickness, stiffness, material cross-section or full 3D architecture'
out=root/'cases/18_mechanical_nature/v06_fig18_broad_weave'
if out.exists():raise RuntimeError('refusing overwrite '+str(out))
bpy.context.view_layer.update();out.mkdir(parents=True);bpy.ops.wm.save_as_mainfile(filepath=str(out/'scene.blend'));print('FIG18_V06_SAVED',str(out/'scene.blend'),flush=True)
