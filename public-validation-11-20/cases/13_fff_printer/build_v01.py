"""Fig.1(a) visible printer and laptop, not panel b or hidden wiring."""
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from scene_parts_v01 import *
p=Path(__file__).resolve().parent;reset()
box('workbench',(0,0,-.1),(8.6,3.4,.2),'white')
box('printer plinth',(-1.2,.0,.18),(3.5,2.8,.36),'dark')
for x in (-2.85,.45):
 for y in (-1.2,1.2):box('printer vertical extrusion',(x,y,1.62),(.11,.11,2.6),'silver')
for x in (-2.85,.45):box('top x-rail',(x,0,2.95),(.13,2.52,.13),'silver')
for y in (-1.2,1.2):box('top y-rail',(-1.2,y,2.95),(3.4,.13,.13),'silver')
box('gantry crossbar',(-1.15,0,2.1),(3.3,.1,.15),'silver')
box('extruder carriage',(-1.3,-.12,1.9),(.52,.5,.43),'blue')
tube('hot end',(-1.3,-.1,1.75),(-1.3,-.1,1.35),.095,'silver')
box('heated bed',(-1.3,-.12,.96),(2.65,2.04,.11),'silver')
box('visible model sample',(-1.2,-.08,1.05),(.42,.35,.12),'white')
box('display module',(.13,-1.3,.48),(.72,.13,.5),'dark');box('display glass',(.13,-1.38,.48),(.59,.03,.33),'screen')
box('visible sensor',(-.3,-1.27,1.4),(.21,.18,.24),'blue')
box('laptop base',(2.65,-.22,.14),(2.1,1.2,.08),'silver')
box('laptop screen',(2.65,.4,.85),(2.12,.08,1.4),'dark');box('laptop panel',(2.65,.35,.87),(1.9,.02,1.2),'screen')
presentation(p,look=(8,-10,6.8),at=(0,0,1.05),scale=9.8,width=1120,height=660)
