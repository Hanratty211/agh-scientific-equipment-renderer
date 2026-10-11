"""R2: source-visible rectangular reflector, angled microphone body and amp lead, laptop."""
import sys,math
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from scene_parts_v03 import *
p=Path(__file__).resolve().parent;reset()
box('apparatus base',(-1.55,0,.04),(4.05,2.54,.16),'ivory')
for x in (-2.38,-.72):box('upper array upright',(x,.1,1.42),(.11,.16,2.59),'silver')
box('ultrasonic top holder',(-1.55,0,2.67),(2.08,1.18,.14),'silver')
# Deliberate simplified transducer grid; count not asserted from paper.
for x in (-2.00,-1.63,-1.26,-.89):
 for y in (-.34,0,.34):cylinder('down-facing transducer',(x,y,2.57),.12,.17,'black')
box('flat rectangular reflector',(-1.55,0,.70),(1.62,1.16,.095),'silver')
box('reflector support',(-1.55,0,.36),(.20,.25,.57),'silver')
sphere('working-gap droplet',(-1.55,0,1.52),.078,'fluid')
box('side imaging camera',(.51,-.34,1.54),(.65,.56,.46),'black')
cylinder('side imaging lens',(.08,-.34,1.54),.16,.27,'silver',rotation=(0,math.pi/2,0))
box('opposite LED light',(-3.36,-.20,1.55),(.39,.34,.32),'ivory')
# Body outside and real angled probe terminates at the gap.
box('microphone rear body',(-.21,-1.16,2.43),(.31,.23,.34),'black')
tube('angled microphone stem',(-.32,-1.12,2.24),(-1.31,-.23,1.68),.025,'silver')
polyline('microphone to amplifier visible lead',[(-.1,-1.16,2.48),(.60,-1.16,2.52),(1.65,-.25,.82)],.014,'black')
panel('amplifier electronics',(2.08,.42,.48),(1.06,.68,.72),'black',True)
panel('oscilloscope instrument',(3.36,.42,.54),(1.12,.70,.82),'blue',True)
box('oscilloscope dials',(3.75,.02,.39),(.12,.035,.27),'silver')
box('laptop keyboard',(4.65,-.19,.16),(1.03,.75,.065),'silver')
box('laptop open screen',(4.65,.29,.77),(1.03,.08,1.09),'black')
box('laptop panel',(4.65,.23,.79),(.86,.02,.87),'screen')
polyline('array amplifier lead',[(-.50,.06,2.70),(.64,.88,2.45),(1.67,.31,.71)],.012,'black')
ortho_camera(p,look=(5.3,-10,6.5),at=(.52,0,1.27),scale=10.8,width=1120,height=800,version='v03')
