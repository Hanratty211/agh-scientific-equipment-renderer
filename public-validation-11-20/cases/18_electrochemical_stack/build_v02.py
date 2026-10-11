"""R1 Fig.6(c) 1–17 visual positions, 12–14 grouped cells, four-cell assembled repeat.
Caption conflicts for 15/16 explicitly UNKNOWN in notes; visual layer colors are not identities.
"""
import sys,math
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from scene_parts_v02 import *
p=Path(__file__).resolve().parent;reset()
# Left vertical XZ sheets ordered along depth Y; actual rectangular windows THROUGH Y.
items=[
 (1,'endplate','silver',.16), (2,'gasket','rubber',.045),(3,'self-breathing bipolar plate','blue',.11),
 (4,'GDE','green',.032),(5,'gasket','rubber',.044),(6,'cathode flow plate','silver',.12),
 (7,'proton exchange membrane','ivory',.025),(8,'anode','copper',.035),(9,'gasket','rubber',.045),
 (10,'anode flow plate','silver',.12),(11,'gasket','rubber',.043),
 (12,'grouped cell unit A','blue',.15),(13,'grouped cell unit B','blue',.15),(14,'grouped cell unit C','blue',.15),
 (15,'unresolved identity','ivory',.040),(16,'caption-conflicted gasket or collector','gold',.06),(17,'endplate','silver',.17)]
for n,name,mat,depth in items:
 y=-3.68+(n-1)*.45
 outer=(1.53,1.20) if n not in (1,17) else (1.75,1.36)
 inner=(.96,.70) if n not in (1,17) else (.74,.56)
 # Each visible ring/frame has four bars; thin membranes/electrodes preserve thinner profiles.
 vertical_window(f'position {n:02d} {name}',(-2.15,y,.63),outer,inner,depth,mat)
 if n in (3,6,10,12,13,14):
  for dz in (-.17,0,.17):box(f'pattern channel p{n}',(-2.15,y,.63+dz),(.78,depth+.005,.018),'copper' if n in (6,10) else 'ivory')
# Right: four assembled repeating cell packs, narrow color-coded layers; thick endplates.
for k in range(4):
 for j,(name,mat,depth) in enumerate((('flow','silver',.12),('electrode','green',.045),('membrane','ivory',.029),('anode','copper',.045),('separator','rubber',.052))):
  y=-1.13+k*.67+j*.105
  vertical_window(f'assembled cell {k+1} {name}',(2.15,y,.63),(1.45,1.20),(.86,.63),depth,mat)
for y,label in ((-1.49,'rear'),(1.49,'front')):
 vertical_window(f'assembled {label} endplate',(2.15,y,.63),(1.78,1.45),(.68,.52),.20,'silver')
for x in (1.37,2.93):
 for z in (.03,1.25):
  tube('visible assembled tie rod',(x,-1.68,z),(x,1.7,z),.034,'silver')
  cylinder('tie rod front nut',(x,1.74,z),.075,.11,'dark',rotation=(math.pi/2,0,0))
ortho_camera(p,look=(5.5,-11,6.7),at=(.1,0,.63),scale=11.5,width=1350,height=760)
