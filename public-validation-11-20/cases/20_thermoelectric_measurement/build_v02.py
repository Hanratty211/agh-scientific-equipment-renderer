"""R1 Fig. Extended Data 1(a) compact Cu-block/Peltier/sample fixture only; no V1/V2 meter boxes."""
import sys,math
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from scene_parts_v02 import *
p=Path(__file__).resolve().parent;reset()
box('Peltier module fixture',(0,0,.23),(2.65,1.22,.45),'ivory')
for x in (-.91,.91):
 box('copper heat block',(x,0,.73),(.76,1.04,.61),'copper')
 # Real narrow grease surfaces at inner Cu-block-facing sample ends.
 box('thermal grease inner face',(x/abs(x)*.50,0,1.055),(.11,.65,.061),'ivory')
# Narrow strip bridges between facing blocks, not a broad slab laid over two blocks.
box('bridging thermoelectric sample',(0,0,1.10),(1.25,.33,.079),'black')
for y in (-.155,.155):
 for x in (-.37,.37):
  box('sample-edge electrode pad',(x,y,1.165),(.14,.074,.018),'gold')
  polyline('sample edge measurement lead',[(x,y,1.17),(x+(.35 if x>0 else -.35),y+(-.32 if y<0 else .32),1.36),(x+(.6 if x>0 else -.6),y+(-.46 if y<0 else .46),1.16)],.013,'copper')
# Only fixture geometry, annotated reference V1/V2 and field arrows are not hardware.
ortho_camera(p,look=(4.5,-7.5,5.2),at=(0,0,.75),scale=4.45,width=1020,height=720)
