"""R2: mounted emissions display, front-center sensor unit, open frame void and routed head loop."""
import sys,math
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from scene_parts_v03 import *
p=Path(__file__).resolve().parent;reset()
box('printer lower shell',(-.95,0,.30),(3.42,2.10,.49),'black')
for x in (-2.61,.71):
 for y in (-.98,.98):box('printer upright',(x,y,1.62),(.10,.12,2.53),'silver')
 box('printer frame foot',(x,-.98,.08),(.32,.30,.15),'black')
for y in (-.98,.98):box('upper cross rail',(-.95,y,2.88),(3.41,.12,.10),'silver')
# Rear OPEN structural perimeter instead of broad opaque dark wall.
frame_on_face('open printer rear outline',(-.95,.96,1.71),(3.18,.10,2.08),'dark')
box('anchored gantry beam',(-.95,0,2.22),(3.20,.14,.13),'silver')
box('red extruder carriage',(-1.13,-.25,2.10),(.60,.50,.34),'red')
box('dark extruder body',(-1.13,-.28,1.88),(.40,.39,.37),'black')
tube('head nozzle',(-1.13,-.28,1.72),(-1.13,-.28,1.49),.035,'copper')
# U-loop with actual two anchors on frame and head (not a lone diagonal).
polyline('looped head cable',[(.34,.55,2.73),(.16,.39,3.12),(-.88,-.14,3.12),(-1.20,-.20,2.29)],.033,'black')
box('heated print bed',(-.95,-.22,.96),(2.53,1.61,.13),'black')
for x in (-2.04,.14):box('bed support',(x,-.22,.68),(.14,.17,.50),'silver')
# Source's upper-left black emission readout attached to a visible frame bracket.
tube('emission display bracket',(-2.58,-.90,2.50),(-3.13,-.90,2.50),.045,'silver')
panel('attached emissions display',(-3.49,-.90,2.37),(.79,.16,.77),'black',True)
# Lower FRONT CENTER rather than right floating box.
box('front sensor support',(0,-1.21,.40),(.16,.18,.59),'silver')
panel('front-center sensor display',(0,-1.28,.87),(.72,.23,.69),'ivory',True)
box('front probe',(0,-1.39,1.28),(.17,.14,.19),'silver')
box('laptop keyboard',(3.04,-.80,.30),(1.84,1.02,.08),'silver')
box('laptop open screen',(3.04,-.21,1.02),(1.84,.08,1.34),'black')
box('laptop display pixels',(3.04,-.26,1.04),(1.61,.014,1.10),'screen')
ortho_camera(p,look=(4.4,-11.5,4.5),at=(-.06,0,1.35),scale=8.4,width=1130,height=700,version='v03')
