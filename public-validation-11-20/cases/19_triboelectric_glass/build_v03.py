"""R2: continuous downturned U regulator, transparent film, two socket-terminated leads."""
import sys,math
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from scene_parts_v03 import *
p=Path(__file__).resolve().parent;reset()
tube('glass low brace',(-1.80,0,.13),(-1.80,0,.72),.054,'silver')
tube('glass high brace',(.15,0,.13),(.15,0,1.47),.054,'silver')
obj=box('tilted transparent TeRC glass',(-.83,0,1.07),(2.27,1.49,.047),'glass');obj.rotation_euler[1]=-.48
obj=box('transparent thin film',(-.83,0,1.10),(2.11,1.34,.010),'resin');obj.rotation_euler[1]=-.48
for label,point in [('left',(-1.76,-.47,.66)),('right',(.08,-.47,1.54))]:
 marker('glass '+label+' electrode socket','transparent thin film',point,.05,'gold')
cylinder('raised fluid reservoir',(-2.50,.10,2.70),.27,.66,'glass')
# One continuous U path ending in a downward nozzle directly aligned to one visible falling drop.
polyline('continuous U regulator',[(-2.50,.10,2.37),(-2.53,.10,2.05),(-2.19,.10,1.82),(-1.86,.10,2.02),(-1.86,.10,2.30),(-1.58,.10,2.32),(-1.58,.10,2.03)],.032,'fluid')
tube('downward terminal nozzle',(-1.58,.10,2.03),(-1.58,.10,1.79),.038,'silver')
sphere('falling drop',(-1.58,.10,1.59),.075,'fluid')
panel('resistance substituter',(1.32,.10,.53),(1.24,.75,.79),'ivory',True)
for k in range(3):cylinder('resistance step knob',(1.03+k*.27,-.33,.38),.052,.04,'black',rotation=(math.pi/2,0,0))
panel('oscilloscope',(3.0,.10,.63),(1.33,.76,1.04),'black',True)
box('scope channel control',(3.42,-.30,.39),(.13,.035,.18),'silver')
marker('resistance instrument side socket','resistance substituter',(1.00,-.29,.77),.045,'gold')
marker('scope instrument side socket','oscilloscope',(2.58,-.29,.92),.045,'gold')
route('visible signal to resistance socket',(-1.76,-.47,.66),(1.00,-.29,.77),'gold',.014,[(-.65,-.75,1.32),(.45,-.60,.93)])
route('visible signal to scope socket',(.08,-.47,1.54),(2.58,-.29,.92),'gold',.014,[(.90,-.76,.54),(1.88,-.66,.69)])
ortho_camera(p,look=(5.1,-9,6.4),at=(.16,0,1.35),scale=8.0,width=1100,height=800,version='v03')
