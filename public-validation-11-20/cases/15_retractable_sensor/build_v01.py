"""Fig.1(c) main left exploded lid/rotor/stator; gaps intentional, no supports fabricated."""
from pathlib import Path
import sys,math
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from scene_parts_v01 import *
p=Path(__file__).resolve().parent;reset()
cylinder('stator exterior',(0,0,.1),1.0,.20,'white')
ring('stator rim',(0,0,.25),.93,.075,'dark')
ring('stator electrode outer',(0,0,.30),.72,.025,'gold')
ring('stator electrode inner',(0,0,.31),.48,.025,'gold')
cylinder('central spindle',(0,0,.38),.13,.45,'silver')
# Rotor lifted in explosion. Open center and actual modeled tracks are not filled disks.
ring('rotor shell',(0,0,1.28),.83,.13,'white')
ring('rotor electrode',(0,0,1.25),.61,.032,'gold')
ring('rotor hub',(0,0,1.23),.23,.08,'dark')
points=[]
for j in range(118):
 t=j/117*math.pi*7;rad=.21+j/117*.45;points.append((rad*math.cos(t),rad*math.sin(t),1.35))
polyline('coil spring illustrated',points,.024,'silver')
polyline('visible retractable cord',[(.8,0,1.23),(1.12,0,1.2),(1.52,-.05,1.17)],.035,'dark')
ring('lid edge',(0,0,2.27),1.0,.12,'white')
cylinder('lid cap',(0,0,2.33),.87,.1,'white')
# No human/inset electrodes/legend graphic from neighboring panels.
presentation(p,look=(5,-7,7),at=(.1,0,1.2),scale=4.5,width=780,height=980)
