"""Only Fig.1(b) Vee-shield setup. Visible source devices and PTFE path; no spooling (d)."""
from pathlib import Path
import sys,math
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from scene_parts_v01 import *
p=Path(__file__).resolve().parent;reset()
box('working table',(0,0,-.08),(8.5,3.8,.17),'white')
# Perspex chamber: translucent walls are thin transparent slabs, not a white block.
for x in (-.9,2.6):pane_frame('chamber end',(x,0,1.0),(.055,2.45,1.95))
for y in (-1.2,1.2):pane_frame('chamber door',(0.85,y,1.0),(3.45,.05,1.95))
box('syringe dispenser controller',(-3.25,0,.37),(1.02,.72,.65),'blue')
box('dispense drive',(-2.72,.2,1.2),(.25,.4,.73),'silver')
cylinder('syringe barrel',(-2.65,0,1.75),.11,.8,'glass')
tube('syringe plunger',(-2.65,0,2.02),(-2.65,0,2.6),.055,'silver')
polyline('visible PTFE tube',[(-2.65,0,1.32),(-2.05,0,1.13),(-.8,0,1.7),(.25,0,1.5)],.035,'fluid')
box('needle Perspex support',(.3,.45,1.22),(.65,.18,.14),'glass');tube('metal needle',(.3,0,1.3),(.3,0,.72),.029,'silver')
# Grounded circular collector and separate PTFE V: no impossible solid plug.
cylinder('collector disk',(.4,0,.34),.67,.065,'silver')
tube('collector support',(.4,0,.09),(.4,0,.32),.055,'silver')
polyline('PTFE Vee-shield edge',[(.05,-.5,.46),(.45,0,.3),(.82,-.5,.46)],.08,'white')
box('infrared heat source',(1.15,.75,1.7),(.7,.38,.25),'dark')
box('storage heater',(1.9,.35,.24),(.73,.52,.45),'dark')
box('high voltage supply',(3.65,-.2,.42),(.95,.83,.78),'blue')
presentation(p,look=(7,-11,7),at=(.25,0,1),scale=10.8,width=1100,height=720)
