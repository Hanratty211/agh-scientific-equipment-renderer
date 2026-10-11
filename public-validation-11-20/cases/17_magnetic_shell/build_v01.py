"""Fig.1(a) whole experimental rig with paired coils, center shell, pump, sensor, supply."""
from pathlib import Path
import sys,math
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from scene_parts_v01 import *
p=Path(__file__).resolve().parent;reset()
box('experiment platform',(0,0,-.11),(9.6,3.6,.22),'white')
for x in (-1.05,1.05):
 ring('Helmholtz coil winding',(x,0,1.31),.82,.1,'copper',rotation=(0,math.pi/2,0))
 ring('Helmholtz coil frame',(x,0,1.31),.88,.045,'dark',rotation=(0,math.pi/2,0))
 box('coil pedestal',(x,0,.42),(.27,.5,.74),'silver')
sphere('center magnetic shell',(0,0,1.32),.24,'rubber')
box('shell sample fixture',(0,0,.46),(.42,.35,.4),'silver')
box('syringe pump',(-3.6,0,.41),(1.1,.8,.65),'blue')
cylinder('pressure actuator syringe',(-3.6,-.1,.82),.085,.85,'glass',rotation=(0,math.pi/2,0))
polyline('pneumatic tube visible',[(-3.05,-.1,.82),(-2.2,-.1,1.05),(-.4,-.07,1.28)],.026,'fluid')
box('pressure sensor',(2.35,.7,.42),(.53,.39,.48),'dark')
polyline('sensor tube visible',[(.32,.0,1.32),(1.5,.4,.88),(2.12,.7,.56)],.018,'fluid')
box('DC supply',(3.5,-.45,.5),(1.2,.84,.88),'dark');box('DC supply display',(3.5,-.89,.6),(.82,.025,.35),'screen')
# No coil current/wiring shape inferred beyond recognizable instrument/coil presence.
presentation(p,look=(7.5,-11,7.0),at=(0,0,.86),scale=11.6,width=1100,height=700)
