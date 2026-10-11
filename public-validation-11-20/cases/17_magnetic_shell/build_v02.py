"""R1: vertical Helmholtz housing stack in four-post frame, hemisphere on loading fixture."""
import sys,math
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from scene_parts_v02 import *
p=Path(__file__).resolve().parent;reset()
box('frame base',(0,0,.03),(3.15,2.45,.19),'black')
for x in (-1.33,1.33):
 for y in (-.96,.96):box('structural frame post',(x,y,1.44),(.11,.11,2.71),'silver')
box('frame top',(0,0,2.82),(3.17,2.45,.13),'black')
# Coil housings have a vertical common axis; not side-by-side open circles.
for z,label in ((.74,'lower'),(2.30,'upper')):
 flat_ring(label+' coil housing',(0,0,z),.99,.47,.24,'black')
 flat_ring(label+' copper winding',(0,0,z+.04),.81,.59,.09,'copper')
box('sample loading post',(0,0,1.09),(.19,.22,.52),'silver')
# True hemispherical mesh with equatorial rim (not a complete floating sphere).
verts=[(0,0,.29)];faces=[];n=32;rings=8
for i in range(1,rings+1):
 theta=(math.pi/2)*i/rings
 for j in range(n):
  phi=2*math.pi*j/n;verts.append((.29*math.sin(theta)*math.cos(phi),.29*math.sin(theta)*math.sin(phi),.29*math.cos(theta)))
for j in range(n):faces.append((0,1+j,1+(j+1)%n))
for i in range(rings-1):
 for j in range(n):
  a=1+i*n+j;b=1+i*n+(j+1)%n;faces.append((a,b,b+n,a+n))
mesh=bpy.data.meshes.new('hemisphere mesh');mesh.from_pydata(verts,[],faces);mesh.update();o=bpy.data.objects.new('hemispherical shell specimen',mesh);bpy.context.collection.objects.link(o);o.location=(0,0,1.38);o.data.materials.append(MAT['rubber'])
box('hemisphere loading fixture top',(0,0,1.37),(.67,.55,.10),'silver')
panel('left DC supply',(-3.0,.15,.55),(1.1,.72,.83),'black',True)
box('left positioning stage',(-1.97,-.3,.33),(.72,.6,.33),'silver')
panel('right red syringe pump',(3.1,.1,.78),(1.09,.81,1.05),'red',True)
cylinder('syringe actuator',(3.1,.1,1.42),.09,.63,'glass',rotation=(0,math.pi/2,0))
panel('front pressure sensor',(2.48,-.9,.29),(.45,.28,.43),'black',True)
polyline('observed pneumatic tube to fixture',[(2.49,.05,1.39),(1.58,.18,1.05),(.48,.11,1.37)],.023,'fluid')
polyline('visible sensor segment',[(.48,-.08,1.38),(1.26,-.44,.83),(2.28,-.9,.46)],.016,'fluid')
ortho_camera(p,look=(5.8,-10,6.7),at=(0,0,1.40),scale=9.2,width=1100,height=800)
