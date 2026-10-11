"""R2: varied 1–17 vertical-face layers; no invented ports. 15/16 caption remain ambiguous.
Open windows are four-bar XZ shells through plate-normal Y; endplates are solid with real bolt holes.
"""
import sys,math
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from scene_parts_v03 import *
p=Path(__file__).resolve().parent;reset()
# Build solid endplates as rectangular plate with four actual through-Y fastener holes.
def endplate(name,x,y,z,w,h,depth):
 o=box(name,(x,y,z),(w,depth,h),'silver')
 for dx in (-.63,.63):
  for dz in (-.48,.48):
   cutter=cylinder(name+' bolt cutter',(x+dx,y,z+dz),.054,depth+.30,'white',vertices=24,rotation=(math.pi/2,0,0))
   mod=o.modifiers.new('through-Y bolt aperture','BOOLEAN');mod.operation='DIFFERENCE';mod.object=cutter
   bpy.context.view_layer.objects.active=o;bpy.ops.object.modifier_apply(modifier=mod.name);bpy.data.objects.remove(cutter,do_unlink=True)
 return o
items={1:('endplate','silver',.17),2:('gasket','rubber',.036),3:('bipolar frame','blue',.13),4:('thin GDE','green',.018),5:('gasket','rubber',.036),6:('cathode patterned flow','silver',.11),7:('thin proton membrane','ivory',.015),8:('thin anode','copper',.020),9:('gasket','rubber',.036),10:('anode patterned flow','silver',.11),11:('gasket','rubber',.036),12:('framed cell A','blue',.17),13:('framed cell B','blue',.17),14:('framed cell C','blue',.17),15:('unresolved layer','ivory',.025),16:('caption conflict layer','gold',.031),17:('endplate','silver',.17)}
for n,(label,mat,dep) in items.items():
 y=-3.63+(n-1)*.455;prefix=f'position {n:02d} {label}'
 if n in (1,17):endplate(prefix,-2.1,y,.66,1.65,1.30,dep)
 elif n in (2,5,9,11):vertical_window(prefix,(-2.1,y,.66),(1.51,1.19),(1.13,.80),dep,mat)
 elif n in (4,7,8,15,16):
  box(prefix,(-2.1,y,.66),(1.43,dep,1.06),mat)
 else:
  vertical_window(prefix,(-2.1,y,.66),(1.50,1.17),(.97,.72),dep,mat)
  if n in (3,6,10,12,13,14):
   for k in range(4):box(prefix+' visible flow rib',(-2.1-.34+k*.22,y,.66),(.036,dep+.006,.68),'copper' if n in (6,10) else 'ivory')
# Four clearly framed assembled cells, not one packet; pair endplates & tie rods.
for cell in range(4):
 y=-1.18+cell*.77
 for j,(label,mat,dep) in enumerate((('frame','blue',.12),('gasket','rubber',.035),('GDE','green',.020),('membrane','ivory',.016),('flow','silver',.08))):
  pos=(2.1,y+j*.09,.66)
  if label in ('GDE','membrane'):box(f'assembled cell {cell+1} {label}',pos,(1.41,dep,1.07),mat)
  else:vertical_window(f'assembled cell {cell+1} {label}',pos,(1.52,1.20),(.96,.70),dep,mat)
for y,label in ((-1.43,'rear'),(1.56,'front')):endplate('assembled '+label+' endplate',2.1,y,.66,1.75,1.38,.20)
for x in (1.39,2.81):
 for z in (.13,1.19):
  tube('assembled long tie rod',(x,-1.59,z),(x,1.77,z),.03,'silver')
  cylinder('tie rod nut',(x,1.80,z),.075,.11,'dark',rotation=(math.pi/2,0,0))
ortho_camera(p,look=(5.4,-11,7),at=(0,0,.68),scale=11.4,width=1380,height=800,version='v03')
