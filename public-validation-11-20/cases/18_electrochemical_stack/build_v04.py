"""R3 v04: visibly framed 12–14 modules with distinguishable patterned inner panels.
15 unresolved, 16 conflicting publisher caption; visual coding is not material identification.
"""
import sys,math
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from scene_parts_v03 import *
p=Path(__file__).resolve().parent;reset()
def endplate(name,x,y,z,w,h,depth):
 o=box(name,(x,y,z),(w,depth,h),'silver')
 for dx in (-.63,.63):
  for dz in (-.48,.48):
   cutter=cylinder(name+' cutter',(x+dx,y,z+dz),.052,depth+.31,'white',vertices=24,rotation=(math.pi/2,0,0))
   mod=o.modifiers.new('through-Y fastener aperture','BOOLEAN');mod.operation='DIFFERENCE';mod.object=cutter
   bpy.context.view_layer.objects.active=o;bpy.ops.object.modifier_apply(modifier=mod.name);bpy.data.objects.remove(cutter,do_unlink=True)
 return o
items={1:('endplate','silver',.17),2:('gasket','rubber',.036),3:('bipolar frame','blue',.13),4:('thin GDE','green',.018),5:('gasket','rubber',.036),6:('cathode patterned flow','silver',.11),7:('thin proton membrane','ivory',.015),8:('thin anode','copper',.020),9:('gasket','rubber',.036),10:('anode patterned flow','silver',.11),11:('gasket','rubber',.036),12:('framed cell A','blue',.17),13:('framed cell B','blue',.17),14:('framed cell C','blue',.17),15:('unresolved layer','ivory',.025),16:('caption conflict layer','gold',.031),17:('endplate','silver',.17)}
for n,(label,mat,dep) in items.items():
 y=-3.63+(n-1)*.455;prefix=f'position {n:02d} {label}'
 if n in (1,17):endplate(prefix,-2.10,y,.66,1.65,1.30,dep)
 elif n in (2,5,9,11):vertical_window(prefix,(-2.10,y,.66),(1.51,1.19),(1.13,.80),dep,mat)
 elif n in (4,7,8,15,16):box(prefix,(-2.10,y,.66),(1.43,dep,1.06),mat)
 else:
  vertical_window(prefix,(-2.10,y,.66),(1.50,1.17),(.97,.72),dep,mat)
  if n in (3,6,10):
   for k in range(4):box(prefix+' flow rib',(-2.44+k*.22,y,.66),(.036,dep+.006,.68),'copper' if n in (6,10) else 'ivory')
  if n in (12,13,14):
   # Framed cell subassembly with contrasting INNER layer and an actual patterned flow-field;
   # a display of repeated modules, not declared electrode material identity.
   box(prefix+' inner panel',(-2.10,y-.027,.66),(.88,.024,.61),'copper' if n%2 else 'green')
   for k in range(5):box(prefix+' interior field line',(-2.46+k*.18,y-.061,.66),(.026,.024,.55),'black')
   for x in (-2.75,-1.45):
    for z in (.18,1.14):cylinder(prefix+' perimeter fastener',(x,y,z),.043,.026,'silver',rotation=(math.pi/2,0,0))
# Assembled four-cell repetition, each with frame + patterned panel and thin gasket/film.
for cell in range(4):
 y=-1.18+cell*.77;stem=f'assembled cell {cell+1}'
 vertical_window(stem+' frame',(2.10,y,.66),(1.52,1.20),(.96,.70),.12,'blue')
 box(stem+' contrasting inner field panel',(2.10,y-.035,.66),(.87,.027,.62),'copper' if cell%2 else 'green')
 for k in range(4):box(stem+' flow field line',(1.78+k*.22,y-.073,.66),(.035,.022,.54),'silver')
 vertical_window(stem+' thin gasket',(2.10,y+.105,.66),(1.50,1.18),(1.10,.77),.034,'rubber')
 box(stem+' membrane',(2.10,y+.16,.66),(1.41,.016,1.06),'ivory')
for y,label in ((-1.43,'rear'),(1.56,'front')):endplate('assembled '+label+' endplate',2.10,y,.66,1.75,1.38,.20)
for x in (1.39,2.81):
 for z in (.13,1.19):
  tube('assembled long tie rod',(x,-1.59,z),(x,1.77,z),.030,'silver')
  cylinder('front tie rod nut',(x,1.80,z),.075,.11,'dark',rotation=(math.pi/2,0,0))
ortho_camera(p,look=(5.4,-11,7.0),at=(0,0,.68),scale=11.4,width=1380,height=800,version='v04')
