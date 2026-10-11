"""Fig.5(b) opposed array/reflector, probe, camera, lamp, amplifier, scope and computer."""
from pathlib import Path
import sys,math
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from scene_parts_v01 import *
p=Path(__file__).resolve().parent;reset()
box('apparatus platform',(-1,0,.02),(5.6,2.2,.16),'silver')
box('array support',(-1.55,0,.78),(.18,.65,1.38),'silver')
for x in (-2.1,-1.8,-1.5,-1.2,-.9):
 for y in (-.38,0,.38):
  cylinder('ultrasonic array element',(x,y,.82),.13,.24,'dark')
box('reflector standoff',(1.05,0,.72),(.17,.18,1.28),'silver')
cylinder('facing reflector',(1.05,0,1.42),.65,.11,'silver')
sphere('single levitated drop',(-.47,0,1.11),.085,'fluid')
box('microphone probe controller',(-2.85,-.8,.2),(.4,.4,.25),'dark')
tube('probe microphone',(-2.8,-.75,.41),(-.65,-.3,1.08),.025,'silver')
box('high-speed camera',(2,-.55,1.6),(.6,.58,.47),'blue');cylinder('camera lens',(1.65,-.55,1.6),.17,.25,'dark',rotation=(0,math.pi/2,0))
box('LED lamp',(.9,1,1.75),(.36,.4,.26),'white');tube('light stand',(.9,1,.4),(.9,1,1.6),.05,'silver')
for x,name in ((2.55,'amplifier'),(3.7,'oscilloscope')):
 box(name,(x,.4,.42),(.85,.85,.72),'dark');box(name+' panel',(x,-.04,.44),(.65,.02,.5),'screen')
box('computer',(4.55,-.7,.8),(.75,.1,.9),'dark');box('computer panel',(4.55,-.76,.8),(.64,.01,.73),'screen')
presentation(p,look=(8,-11,7.2),at=(.6,0,.9),scale=11.2,width=1020,height=750)
