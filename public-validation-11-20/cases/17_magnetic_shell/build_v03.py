"""R2: open top support instead of opaque slab; visible pump/sensor tubing reaches interfaces."""
import sys,math
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from scene_parts_v03 import *
p=Path(__file__).resolve().parent;reset()
box('fixture base',(0,0,.03),(3.13,2.45,.18),'black')
for x in (-1.31,1.31):
 for y in (-.94,.94):box('mechanical frame post',(x,y,1.40),(.10,.10,2.69),'silver')
# Front/side thin rails keep the coil OPEN and legible, unlike v02 roof slab.
for y in (-.94,.94):box('thin top rail',(0,y,2.75),(2.85,.10,.09),'silver')
for z,label in ((.78,'lower'),(2.26,'upper')):
 flat_ring(label+' coil housing',(0,0,z),.98,.47,.21,'black')
 flat_ring(label+' copper winding',(0,0,z+.06),.82,.58,.07,'copper')
box('supported loading stage',(0,0,.38),(.61,.52,.58),'silver')
box('sample fixture top',(0,0,1.00),(.65,.54,.07),'silver')
# True upper hemisphere with underside equatorial rim.
verts=[(0,0,.29)];faces=[];n=32
for i in range(1,9):
 t=math.pi*i/16
 for j in range(n):
  phi=2*math.pi*j/n;verts.append((.29*math.sin(t)*math.cos(phi),.29*math.sin(t)*math.sin(phi),.29*math.cos(t)))
for j in range(n):faces.append((0,1+j,1+(j+1)%n))
for i in range(7):
 for j in range(n):
  a=1+i*n+j;b=1+i*n+(j+1)%n;faces.append((a,b,b+n,a+n))
me=bpy.data.meshes.new('hemisphere mesh');me.from_pydata(verts,[],faces);me.update();o=bpy.data.objects.new('hemispherical sample',me);bpy.context.collection.objects.link(o);o.location=(0,0,1.04);o.data.materials.append(MAT['rubber'])
panel('left compact DC supply',(-3.05,.0,.50),(1.06,.70,.77),'black',True)
box('left loading stage track',(-1.94,-.30,.21),(.67,.49,.35),'silver')
box('left stage bracket',(-1.75,-.30,.49),(.25,.41,.24),'silver')
panel('right red syringe pump',(3.02,.05,.82),(1.10,.81,1.01),'red',True)
cylinder('red pump syringe interface',(2.44,.05,1.42),.10,.18,'glass',rotation=(0,math.pi/2,0))
panel('front pressure sensor',(2.42,-.91,.34),(.44,.31,.41),'black',True)
marker('sample tube fitting','sample fixture top',(.315,-.03,1.00),.035,'blue')
marker('pump visible tube fitting','red pump syringe interface',(2.50,.05,1.42),.035,'blue')
marker('sensor tube fitting','front pressure sensor',(2.23,-.91,.42),.035,'blue')
route('sample to pump visible pneumatic segment',(.315,-.03,1.00),(2.50,.05,1.42),'fluid',.022,[(1.27,.27,1.10),(1.92,.24,1.45)])
route('sample to pressure sensor visible segment',(.315,-.03,1.00),(2.23,-.91,.42),'fluid',.015,[(1.31,-.51,.83)])
ortho_camera(p,look=(5.7,-10,6.8),at=(0,0,1.37),scale=9.3,width=1120,height=800,version='v03')
