"""R2: external LEFT supply, framed top red drive, needle support, cylinder heater, angled IR."""
import sys,math
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from scene_parts_v03 import *
p=Path(__file__).resolve().parent;reset()
box('chamber floor',(0,0,.10),(3.3,2.24,.17),'ivory')
for x in (-1.64,1.64):box('clear Perspex side',(x,0,1.16),(.045,2.18,2.09),'resin')
box('Perspex rear wall',(0,1.07,1.16),(3.27,.043,2.09),'resin')
for x in (-1.64,1.64):box('front presentation frame',(x,-1.07,1.15),(.047,.047,2.1),'silver')
box('transparent chamber roof',(0,0,2.25),(3.31,2.20,.08),'resin')
# Show screw drive/carriage bracket rather than a plain cube.
box('drive upper red housing',(0,0,3.22),(.91,.69,.33),'red')
for x in (-.42,.42):box('drive guide rail',(x,0,2.73),(.08,.15,.80),'silver')
box('moving red carriage',(0,-.06,2.78),(.58,.41,.27),'red')
box('dispenser plunger',(0,0,2.55),(.14,.14,.30),'silver')
cylinder('syringe barrel',(0,0,2.18),.12,.65,'glass')
tube('visible PTFE feed',(0,0,1.87),(0,0,1.48),.035,'ivory')
# Needle support ACTUALLY ends on the shaft, not a detached parallel bar.
box('needle Perspex support',(0.31,0,1.44),(.62,.19,.105),'resin')
tube('vertical metal needle',(0,0,1.43),(0,0,.80),.026,'silver')
marker('needle support at shaft','needle Perspex support',(.023,0,1.44),.028)
cylinder('copper collector',(0,0,.34),.69,.075,'copper')
for s in (-1,1):
 o=box('upright PTFE Vee plate',(s*.42,0,.76),(.105,.81,.81),'ivory');o.rotation_euler[1]=s*.31
# Front heater source is a horizontal tube/housing.
cylinder('horizontal front heater',(0,-1.10,.35),.19,2.65,'black',rotation=(0,math.pi/2,0))
box('front heater base',(0,-1.10,.14),(2.76,.34,.14),'silver')
o=box('angled IR red source',(1.15,.33,1.25),(.32,.37,.53),'red');o.rotation_euler[1]=-.38
box('IR source lens',(1.02,.18,1.13),(.16,.14,.25),'ivory')
panel('external LEFT high voltage DC supply',(-3.09,0,.67),(1.10,.77,.91),'black',True)
marker('DC red output terminal','external LEFT high voltage DC supply',(-2.55,-.24,.85),.045,'red')
marker('DC green output terminal','external LEFT high voltage DC supply',(-2.55,-.24,.54),.045,'mint')
marker('chamber red boundary','clear Perspex side',(-1.64,-.51,1.16),.045,'red')
marker('chamber green boundary','clear Perspex side',(-1.64,-.51,.56),.045,'mint')
route('visible red DC lead',(-2.55,-.24,.85),(-1.64,-.51,1.16),'red',.019,[(-2.04,-.53,1.36)])
route('visible green DC lead',(-2.55,-.24,.54),(-1.64,-.51,.56),'mint',.019,[(-2.10,-.71,.45)])
ortho_camera(p,look=(4.8,-8.8,6.6),at=(-.34,0,1.51),scale=8.0,width=1090,height=850,version='v03')
