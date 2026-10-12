"""R1 physical geometry, additive. No commercial connector/CAD claim.
NURBS-free cubic Bezier has user-controlled end tangent and fillet smoothness.
"""
import bpy, math
from mathutils import Vector
from scene_parts_v03 import box,cylinder,flat_ring,tube,MAT

def bent_cable(name, anchors, radius=.015, mat='black', tension=.28):
 """One editable cubic Bezier spline; exact anchors and end tangent from adjacent spans.
 No POLY hard elbows. Caller supplies seat -> boot -> exterior waypoints -> boot -> seat.
 """
 points=[Vector(p) for p in anchors]
 curve=bpy.data.curves.new(name,'CURVE');curve.dimensions='3D';curve.resolution_u=24
 curve.bevel_depth=radius;curve.bevel_resolution=4
 sp=curve.splines.new('BEZIER');sp.bezier_points.add(len(points)-1)
 for i,(p,b) in enumerate(zip(points,sp.bezier_points)):
  b.co=p;b.handle_left_type='FREE';b.handle_right_type='FREE'
  if i==0:
   d=points[1]-p;b.handle_left=p-d*tension;b.handle_right=p+d*tension
  elif i==len(points)-1:
   d=p-points[i-1];b.handle_left=p-d*tension;b.handle_right=p+d*tension
  else:
   left=p-points[i-1];right=points[i+1]-p
   # derivative follows weighted, local neighbors, not distant fitting.
   b.handle_left=p-(left.normalized()+right.normalized()).normalized()*min(left.length,right.length)*tension if left.length>1e-6 and right.length>1e-6 else p-left*tension
   b.handle_right=p+(left.normalized()+right.normalized()).normalized()*min(left.length,right.length)*tension if left.length>1e-6 and right.length>1e-6 else p+right*tension
 obj=bpy.data.objects.new(name,curve);bpy.context.collection.objects.link(obj);obj.data.materials.append(MAT[mat]);return obj

def true_data_port(name,base,center,axis='left'):
 """Boolean cut through actual metal base wall; frame from four bars with an OPEN hole.
 Axis -X (left) or -Y (front); socket inner cavity black without opaque face plate.
 Return exact socket world centroid and cable boot end.
 """
 x,y,z=center
 if axis=='left':
  cutter=box(name+' Boolean cutter',(x+.033,y,z),(.105,.092,.051),'black');ext=(.008,.104,.061);inner=(.008,.077,.041)
 else:
  cutter=box(name+' Boolean cutter',(x,y+.006,z),(.104,.085,.061),'black');ext=(.104,.008,.061);inner=(.080,.008,.042)
 bpy.context.view_layer.update()
 # Apply the hole to the REAL base mesh. First apply previous non-geometric
 # weighted normals/bevel modifiers so the Boolean sees a single solid shell.
 bpy.ops.object.select_all(action='DESELECT');base.select_set(True)
 bpy.context.view_layer.objects.active=base
 for prior in list(base.modifiers):
  bpy.ops.object.modifier_apply(modifier=prior.name)
 mod=base.modifiers.new(name+' open side aperture','BOOLEAN');mod.operation='DIFFERENCE';mod.solver='EXACT';mod.object=cutter
 bpy.ops.object.modifier_apply(modifier=mod.name);bpy.data.objects.remove(cutter,do_unlink=True)
 if axis=='left':
  # Four open perimeter bars; visible black interior behind frame.
  sx=x-.023
  for side in (-1,1):box(name+' surround vertical',(sx,y+side*.044,z),(.008,.014,.058),'silver')
  for side in (-1,1):box(name+' surround horizontal',(sx,y,z+side*.025),(.008,.092,.008),'silver')
  socket=box(name+' data socket',(x+.031,y,z),(.008,.070,.033),'black')
  plug=box(name+' seated data plug',(x-.031,y,z),(.069,.063,.028),'dark')
  boot=box(name+' cable boot',(x-.094,y,z),(.059,.047,.031),'black')
  return {'socket':socket,'plug':plug,'axis':Vector((-1,0,0)),'seat':(x+.031,y,z),'boot_end':(x-.124,y,z),'base':base}
 sy=y-.023
 for side in (-1,1):box(name+' surround vertical',(x+side*.044,sy,z),(.014,.008,.058),'silver')
 for side in (-1,1):box(name+' surround horizontal',(x,sy,z+side*.025),(.092,.008,.008),'silver')
 socket=box(name+' data socket',(x,y+.031,z),(.070,.008,.033),'black')
 plug=box(name+' seated data plug',(x,y-.031,z),(.063,.069,.028),'dark')
 boot=box(name+' cable boot',(x,y-.094,z),(.047,.059,.031),'black')
 return {'socket':socket,'plug':plug,'axis':Vector((0,-1,0)),'seat':(x,y+.031,z),'boot_end':(x,y-.124,z),'base':base}

def syringe_axis_chain(name, barrel_center, barrel_length, outlet_end, axis_sign=1,barrel_radius=.073):
 """Action end of REAL barrel along X; fixed cylinder hub and nozzle overlap.
 Externally visible hose starts inside nozzle bore boundary. Never invent internal flow.
 Barrel (x,y,z), end_x=x+sign*length/2. outlet_end farther on same axis.
 """
 center=Vector(barrel_center);out=Vector(outlet_end);sign=axis_sign
 face=center+Vector((sign*barrel_length/2,0,0))
 if abs(out.y-face.y)>.002 or abs(out.z-face.z)>.002 or sign*(out.x-face.x)<.10:
  raise ValueError('Tip and outlet must share REAL barrel axis, outside action face')
 hub_end=face+Vector((sign*.075,0,0))
 tube(name+' barrel-end collar',face-Vector((sign*.018,0,0)),hub_end,max(.038,barrel_radius*.89),'silver')
 tip_start=hub_end-Vector((sign*.014,0,0))
 tube(name+' coax metal nozzle',tip_start,out,.035,'silver')
 # At true nozzle x face, bore is drawn as hollow ring along X, not a ball.
 face_ring=flat_ring(name+' open outlet seat',out,.037,.022,.015,'silver');face_ring.rotation_euler[1]=math.pi/2
 return {'barrel_face':tuple(face),'hub_end':tuple(hub_end),'outlet':tuple(out),'axis':tuple(Vector((sign,0,0))),'ring':face_ring}
