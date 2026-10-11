"""R3 limited v04: source camera LEFT, LED RIGHT, exposed angled probe and auditable visible leads.
No acoustic sound rods, waveform claims or inferred internal electric circuitry.
"""
import sys,math
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from scene_parts_v03 import *
p=Path(__file__).resolve().parent;reset()
box('apparatus base',(-1.48,0,.05),(4.0,2.57,.16),'ivory')
for x in (-2.27,-.68):box('array upright',(x,.12,1.43),(.11,.16,2.59),'silver')
box('top array support',(-1.48,0,2.67),(2.1,1.2,.14),'silver')
for x in (-1.96,-1.61,-1.26,-.91):
 for y in (-.34,0,.34):cylinder('downward transducer',(x,y,2.56),.12,.17,'black')
box('flat rectangular reflector',(-1.48,0,.70),(1.67,1.18,.094),'silver')
box('reflector post',(-1.48,0,.36),(.21,.24,.56),'silver')
sphere('single working-gap drop',(-1.48,0,1.52),.080,'fluid')
# CAMERA IS LEFT, its cylinder axis faces +X into working gap.
box('LEFT high speed camera',(-3.12,-.26,1.55),(.72,.57,.48),'black')
cylinder('LEFT inward camera lens',(-2.63,-.26,1.55),.16,.25,'silver',rotation=(0,math.pi/2,0))
marker('camera lead owner surface','LEFT high speed camera',(-3.12,.03,1.62),.025,'black')
# LED IS RIGHT, facing -X; no camera/LED reversal.
box('RIGHT LED housing',(.30,-.20,1.55),(.47,.41,.36),'ivory')
box('LED emitting face',(.055,-.20,1.55),(.022,.30,.27),'white')
# The probe is placed toward foreground, body outside the upper gap and stem enters at angle.
box('microphone exterior body',(-.10,-1.35,2.34),(.38,.29,.38),'black')
tube('visible angled microphone probe',(-.20,-1.32,2.19),(-1.27,-.35,1.66),.040,'silver')
marker('microphone cable surface','microphone exterior body',(.08,-1.35,2.42),.025,'black')
panel('amplifier electronics',(1.93,.48,.51),(1.03,.70,.78),'black',True)
panel('oscilloscope instrument',(3.22,.48,.55),(1.18,.73,.84),'blue',True)
box('scope controls',(3.63,.09,.42),(.12,.045,.28),'silver')
box('laptop base',(4.68,-.18,.17),(1.09,.80,.07),'silver')
box('laptop open screen',(4.68,.27,.80),(1.09,.085,1.08),'black')
box('laptop viewing panel',(4.68,.215,.80),(.91,.015,.89),'screen')
# Three source-visible segments only. QA surface markers are small/black, no gold hardware.
marker('amp microphone socket','amplifier electronics',(1.60,.12,.74),.025,'black')
marker('amp array socket','amplifier electronics',(1.60,.13,.45),.025,'black')
marker('array upper signal boundary','top array support',(-.58,0,2.745),.025,'black')
marker('laptop input socket','laptop open screen',(4.20,.22,.90),.025,'black')
route('microphone-to-amplifier visible wire',(.08,-1.35,2.42),(1.60,.12,.74),'black',.015,[(.77,-1.16,2.22),(1.48,-.52,1.16)])
route('array-to-amplifier visible wire',(-.58,0,2.745),(1.60,.13,.45),'black',.014,[(.65,.83,2.38),(1.70,.76,.96)])
route('camera-to-laptop visible wire',(-3.12,.03,1.62),(4.20,.22,.90),'black',.013,[(-2.7,.86,1.95),(.38,1.43,1.91),(3.4,1.09,1.31)])
ortho_camera(p,look=(4.5,-10,6.9),at=(.40,0,1.29),scale=10.9,width=1140,height=830,version='v04')
