"""R1 opposed vertical array/reflector gap, source-listed camera LED probe, instruments."""
import sys,math
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from scene_parts_v02 import *
p=Path(__file__).resolve().parent;reset()
box('working platform',(-1.5,0,.04),(4.0,2.5,.15),'ivory')
for x in (-2.35,-.65):box('array load frame post',(x,0,1.42),(.11,.12,2.65),'silver')
box('array holder',(-1.5,0,2.72),(2.05,1.13,.14),'silver')
# Small simplified array: the exact paper transducer count/orientation not claimed.
for x in (-2.03,-1.68,-1.33,-.98):
 for y in (-.37,0,.37):cylinder('downward ultrasound transducer',(x,y,2.59),.12,.18,'black')
cylinder('horizontal reflector',(-1.5,0,.64),.75,.10,'silver')
box('reflector pedestal',(-1.5,0,.30),(.22,.23,.46),'silver')
sphere('levitated droplet',(-1.5,0,1.49),.087,'fluid')
# Camera side-on from the right; LED opposite from the left; microphone enters gap obliquely.
box('side high-speed camera',(.48,-.3,1.52),(.71,.58,.47),'black')
cylinder('camera lens',(.03,-.3,1.52),.14,.3,'silver',rotation=(0,math.pi/2,0))
box('opposed LED light',(-3.31,-.17,1.57),(.41,.37,.34),'ivory')
tube('angled microphone probe',(-.4,-1.05,2.24),(-1.33,-.26,1.65),.024,'silver')
box('probe stand',(-.25,-1.05,.49),(.13,.13,.83),'silver')
for label,loc in [('amplifier',(2.0,.43,.50)),('oscilloscope',(3.28,.43,.52)),('computer',(4.63,.43,.96))]:
 panel(label,loc,(1.08,.67,.75 if label!='computer' else 1.18),'black',True)
polyline('source-visible amp lead',[(-.56,.05,2.72),(.65,.7,2.6),(1.51,.7,.76)],.012,'black')
polyline('source-visible scope lead',[(-.17,-.3,1.53),(1.9,-.5,1.75),(2.8,.1,.72)],.012,'black')
ortho_camera(p,look=(5.5,-10,6.5),at=(.48,0,1.28),scale=10.8,width=1120,height=800)
