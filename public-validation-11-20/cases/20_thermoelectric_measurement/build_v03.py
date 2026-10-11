"""R2: compact thin vertical Peltier between/under Cu blocks, sample/grease inner contacts, edge pads."""
import sys,math
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from scene_parts_v03 import *
p=Path(__file__).resolve().parent;reset()
# Small upright Peltier plate under/through bridge region, not horizontal wide pad.
box('thin vertical Peltier module',(0,0,.51),(.15,.95,.92),'ivory')
for x in (-.88,.88):
 box('copper thermal block',(x,0,.70),(.72,.99,.75),'copper')
 # Precisely at each source-facing INNER edge of sample end; sample runs from -.55 to +.55.
 box('grease inner contact',((-.57 if x<0 else .57),0,1.13),(.046,.40,.085),'ivory')
 marker('Cu grease face '+('left' if x<0 else 'right'),'copper thermal block',((-.52 if x<0 else .52),0,1.13),.027,'gold')
box('narrow bridging thermoelectric sample',(0,0,1.13),(1.10,.37,.082),'black')
for y in (-.18,.18):
 for x in (-.39,-.17,.17,.39):
  box('sample edge electrode',(x,y,1.18),(.10,.07,.019),'gold')
  polyline('visible edge lead',[(x,y,1.19),(x+(.22 if x>0 else -.22),y+(.24 if y>0 else -.24),1.31)],.010,'copper')
# V1/V2/heat-gradient figure symbols are not physical meter housings or rods.
ortho_camera(p,look=(4.5,-7.4,5.3),at=(0,0,.78),scale=4.25,width=1020,height=720,version='v03')
