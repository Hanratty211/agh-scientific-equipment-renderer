"""R1 tilted glass, raised reservoir/U-shaped regulator/nozzle, two identifiable instruments."""
import sys,math
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from scene_parts_v02 import *
p=Path(__file__).resolve().parent;reset()
# Dry tilted pane; bottom support is a visible brace, not hidden return plumbing.
tube('glass lower stand',(-1.8,0,.15),(-1.8,0,.7),.055,'silver')
tube('glass upper stand',(.15,0,.15),(.15,0,1.48),.055,'silver')
obj=box('tilted glass TeRC plane',(-.83,0,1.05),(2.30,1.5,.052),'glass');obj.rotation_euler[1]=-.48
obj=box('thin functional film',(-.83,0,1.08),(2.14,1.34,.015),'ivory');obj.rotation_euler[1]=-.48
# Elevated reservoir and U-shaped visible regulator with terminal nozzle; no return loop.
cylinder('water reservoir',(-2.40,.15,2.65),.28,.66,'glass')
polyline('U-shaped flow regulator',[(-2.40,.15,2.29),(-2.42,.15,1.96),(-2.06,.15,1.78),(-1.76,.15,1.96),(-1.76,.15,2.37)],.035,'fluid')
tube('dropper nozzle',(-1.76,.15,2.34),(-1.76,.15,1.99),.034,'silver')
sphere('single falling droplet',(-1.76,.15,1.67),.077,'fluid')
for name,loc in [('resistance substituter',(1.25,.1,.51)),('oscilloscope',(3.0,.1,.65))]:
 panel(name,loc,(1.26,.75,.78 if 'resistance' in name else 1.10),'black',True)
polyline('visible glass electrical lead',[(.18,-.4,1.41),(.74,-.89,1.34),(1.08,-.30,.79)],.017,'gold')
ortho_camera(p,look=(5.2,-9,6),at=(0,0,1.37),scale=7.9,width=1070,height=800)
