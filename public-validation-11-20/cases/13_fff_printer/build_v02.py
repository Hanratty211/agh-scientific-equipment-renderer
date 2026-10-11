"""R1 near-frontal printer/photo silhouette, mounted bed/head, two left/front displays, laptop."""
import sys,math
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from scene_parts_v02 import *
p=Path(__file__).resolve().parent;reset()
# Printer shell/frame: enclosing front rectangle, dark inner bay and mounted gantry.
box('printer lower housing',(-.95,0,.28),(3.45,2.05,.54),'black')
box('printer rear dark bay',(-.95,.8,1.5),(3.33,.17,2.12),'black')
for x in (-2.6,.7):
 for y in (-.95,.93):box('silver vertical rail',(x,y,1.54),(.09,.10,2.62),'silver')
 box('anchored foot',(x,-.95,.12),(.31,.31,.2),'black')
for y in (-.95,.93):box('roof rail',(-.95,y,2.88),(3.4,.12,.12),'silver')
box('gantry crossbar',(-1.0,0,2.22),(3.18,.12,.16),'silver')
box('head carriage',(-1.2,-.22,2.09),(.63,.42,.34),'red')
box('extruder body',(-1.2,-.26,1.85),(.40,.38,.36),'black')
tube('nozzle',(-1.2,-.26,1.72),(-1.2,-.26,1.49),.036,'copper')
polyline('looped head cable',[(-1.25,-.15,2.30),(-1.8,-.1,2.65),(-.55,.2,2.82),(.12,.4,2.55)],.036,'black')
box('heated build bed',(-.95,-.23,.94),(2.5,1.5,.14),'black')
for x in (-2.0,.1):box('bed mount leg',(x,-.23,.64),(.14,.14,.5),'silver')
# Source left emission display + front light sensor/display; no floating model cube.
panel('left emission display',(-3.45,-.1,2.19),(.88,.20,.88),'black',True)
panel('front sensor display',(1.22,-1.0,.86),(.70,.24,.78),'ivory',True)
box('visible front sensor',(1.12,-1.16,1.36),(.24,.19,.23),'silver')
box('laptop keyboard',(3.06,-.9,.32),(1.9,1.12,.085),'silver')
box('laptop screen',(3.06,-.26,1.10),(1.9,.095,1.44),'black')
box('laptop active panel',(3.06,-.34,1.12),(1.66,.016,1.2),'screen')
ortho_camera(p,look=(3.8,-12,4.5),at=(-.13,0,1.42),scale=8.2,width=1130,height=690)
