"""Fig.2(g) tilted TeRC/glass droplet experiment and adjacent readout; no time-series hardware."""
from pathlib import Path
import sys,math
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from scene_parts_v01 import *
p=Path(__file__).resolve().parent;reset()
box('test table',(0,0,-.12),(7.2,3.2,.24),'white')
box('tilted glass support',(-.8,0,.62),(2.3,1.75,.09),'silver')
obj=box('transparent TeRC glass',(-.8,0,.82),(2.15,1.58,.05),'glass');obj.rotation_euler[1]=-.25
obj=box('thin film on glass',(-.8,0,.86),(1.95,1.34,.012),'white');obj.rotation_euler[1]=-.25
box('drop dispenser stand',(-2.3,.38,1.05),(.12,.12,2),'silver')
tube('drop dispenser',(-1.63,.38,2.02),(-1.63,.38,1.55),.085,'glass')
sphere('one visible incoming droplet',(-1.62,.38,1.22),.065,'fluid')
box('electrical readout',(2.1,.05,.38),(1.2,.76,.66),'dark')
box('readout face',(2.1,-.34,.48),(.85,.02,.39),'screen')
# Exposed segment only; electrode termination/hidden topology unknown.
polyline('visible lead to readout',[(.21,-.2,.78),(.82,-.75,.57),(1.6,-.45,.43)],.016,'copper')
presentation(p,look=(5.7,-8.3,6.4),at=(0,0,.75),scale=8.6,width=990,height=690)
