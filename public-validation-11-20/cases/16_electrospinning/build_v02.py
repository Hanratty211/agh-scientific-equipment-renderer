"""R1 Fig1b tall red top drive, clear chamber and paired Vee shield; no motorized spool."""
import sys,math
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from scene_parts_v02 import *
p=Path(__file__).resolve().parent;reset()
box('chamber bottom',(0,0,.08),(3.35,2.25,.17),'ivory')
# Clear pane walls with front side omitted as a PRESENTATION cut, not a physical opening.
for x in (-1.65,1.65):box('Perspex chamber side',(x,0,1.20),(.045,2.2,2.15),'resin')
box('Perspex chamber back',(0,1.08,1.20),(3.33,.044,2.15),'resin')
for x in (-1.61,1.61):box('front chamber frame',(x,-1.09,1.23),(.045,.04,2.2),'silver')
box('clear chamber roof',(0,0,2.28),(3.42,2.24,.09),'resin')
# Dispenser DRIVE physically mounted above roof.
box('top dispenser drive',(0,0,2.90),(.65,.58,.94),'red')
box('screw-driven slide',(0,-.09,2.42),(.20,.27,.48),'silver')
cylinder('syringe barrel',(0,0,2.06),.12,.68,'glass')
tube('PTFE vertical feed',(0,0,1.78),(0,0,1.31),.039,'ivory')
box('Perspex needle support',(.26,.0,1.46),(.55,.17,.10),'resin')
tube('metal needle',(0,0,1.31),(0,0,.82),.026,'silver')
# Copper circular collector supports two facing angled shield plates.
cylinder('circular copper collector',(0,0,.36),.67,.08,'copper')
for sign in (-1,1):
 v=box('upright angled PTFE Vee shield',(sign*.43,0,.78),(.10,.86,.83),'ivory')
 v.rotation_euler[1]=sign*.30
box('front lower heater support',(0,-1.05,.30),(2.8,.3,.33),'black')
box('side infrared heat source',(1.16,.30,1.19),(.34,.35,.44),'black')
panel('black high-voltage DC supply',(3.04,-.1,.62),(1.0,.71,.86),'black',True)
# Lead termination limited to source-visible chamber boundary; no inferred hidden electrode route.
polyline('red source lead',[(2.55,-.36,.78),(1.99,-.6,1.12),(1.63,-.6,1.18)],.018,'red')
polyline('green source lead',[(2.55,-.30,.55),(1.96,-.4,.42),(1.63,-.4,.42)],.018,'mint')
ortho_camera(p,look=(5.4,-8.6,6.4),at=(.45,0,1.44),scale=7.1,width=1050,height=850)
