"""AGH R2 v03: additive geometric helpers; all dimensions illustrative world units.
Do not infer internal plumbing/physics from readable illustration geometry.
"""
import bpy,math
from mathutils import Vector
from scene_parts_v02 import *

def marker(name,owner,point,size=.045,mat='gold'):
 """Real small mesh centered on a known *owner surface*; not an empty/center proxy.
 Name and coordinate provenance must be audited independently against the saved scene.
 """
 return box(name,point,(size,size,size),mat)

def route(name,a,b,mat='fluid',r=.018,via=()):
 return polyline(name,[a,*via,b],r,mat)

def cylinder_open(name,center,outer,inner,height,mat='resin',n=64):
 return flat_ring(name,center,outer,inner,height,mat,n)

def ribbon_spiral(name,center,z,start=.19,end=.72,turns=3.8,width=.032,thickness=.014,material='copper',steps=150):
 """Flat planar spiral ribbon mesh; sides give a thin rectangular section, not a rising wire helix."""
 verts=[];faces=[]
 for j in range(steps+1):
  t=j/steps*turns*2*math.pi;r=start+(end-start)*j/steps
  for h in (-thickness/2,thickness/2):
   for delta in (-width/2,width/2):verts.append(((r+delta)*math.cos(t),(r+delta)*math.sin(t),h))
 for j in range(steps):
  a=4*j;b=4*(j+1)
  faces.extend(((a,a+1,b+1,b),(a+2,b+2,b+3,a+3),(a,b,b+2,a+2),(a+1,a+3,b+3,b+1)))
 mesh=bpy.data.meshes.new(name+' ribbon mesh');mesh.from_pydata(verts,[],faces);mesh.update()
 obj=bpy.data.objects.new(name,mesh);bpy.context.collection.objects.link(obj);obj.location=(center[0],center[1],z);obj.data.materials.append(MAT[material]);return obj

def strip_band(name,r,z0,z1,segment_count=32,stripe_ratio=.46,mat='gold'):
 for j in range(segment_count):
  t=2*math.pi*j/segment_count
  o=box(name+' '+str(j),(r*math.cos(t),r*math.sin(t),(z0+z1)/2),(.020,2*math.pi*r/segment_count*stripe_ratio,z1-z0),mat)
  o.rotation_euler[2]=t

def frame_on_face(name,center,size,mat='silver'):
 """External bracket pair, with void rather than a solid back wall."""
 x,y,z=center;w,depth,h=size
 for dx in (-w/2,w/2):box(name+' post',(x+dx,y,z),(.08,depth,h),mat)
 box(name+' lower',(x,y,z-h/2),(w,depth,.08),mat)
 box(name+' top',(x,y,z+h/2),(w,depth,.08),mat)
