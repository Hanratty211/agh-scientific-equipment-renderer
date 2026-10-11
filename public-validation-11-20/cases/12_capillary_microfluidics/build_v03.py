"""R2: feed fittings, waste terminal INTO open vessel; computer laptop, capped flush branch separate."""
import sys,math
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from scene_parts_v03 import *
p=Path(__file__).resolve().parent;reset()
for label,loc in [('upper',(-3.0,0,2.02)),('lower',(-3.0,0,.57))]:
 x,y,z=loc;panel(label+' pump',loc,(1.10,.70,.51),'ivory',True)
 cylinder(label+' syringe',(x+.16,0,z+.40),.085,.66,'glass',rotation=(0,math.pi/2,0))
 marker(label+' pump exit',label+' syringe',(x+.51,0,z+.40),.035,'blue')
tube('horizontal clear capillary',(-.90,0,1.10),(1.05,0,1.10),.082,'glass')
tube('capillary visible inner line',(-.86,0,1.10),(1.03,0,1.10),.022,'mint')
for label,point in [('upper',(-.78,0,1.10)),('lower',(-.43,0,1.10))]:
 sphere(label+' inlet fitting',point,.085,'blue');marker(label+' inlet contact',label+' inlet fitting',point,.025,'gold')
route('upper pump to capillary',(-2.49,0,2.42),(-.78,0,1.10),'fluid',.023,[(-1.75,0,2.28),(-1.20,0,1.37)])
route('lower pump to capillary',(-2.49,0,.97),(-.43,0,1.10),'fluid',.023,[(-1.74,0,.74),(-.74,0,.76)])
box('high speed camera',(0,0,2.55),(.68,.53,.50),'black');cylinder('top camera objective',(0,0,2.14),.16,.35,'dark')
cylinder('inverted microscope objective',(0,0,.73),.14,.52,'dark');box('inverted microscope',(0,0,.30),(1.2,1,.35),'silver')
# Vessel real open mouth through vertical axis, not a solid bowl; the outlet descends into that mouth.
flat_ring('waste vessel rim',(2.10,0,.46),.30,.24,.05,'glass')
cylinder('waste vessel bottom',(2.10,0,.08),.27,.09,'glass')
flat_ring('waste vessel side wall',(2.10,0,.27),.29,.255,.35,'glass')
marker('capillary outlet face','horizontal clear capillary',(1.05,0,1.10),.03)
marker('waste mouth boundary','waste vessel rim',(2.10,-.255,.46),.03)
route('capillary outlet to waste',(1.05,0,1.10),(2.10,-.255,.46),'fluid',.023,[(1.57,0,.86),(2.10,-.20,.55)])
route('flush needle sealed branch',(1.22,0,1.06),(1.74,0,1.55),'fluid',.019,[(1.48,0,1.54)])
box('sealed branch cap',(1.78,0,1.55),(.12,.15,.16),'red')
box('laptop base',(3.50,-.24,.23),(1.18,.95,.075),'silver')
box('laptop open screen',(3.50,.22,.89),(1.17,.10,1.15),'black')
box('laptop screen glass',(3.50,.155,.89),(.98,.015,.95),'screen')
route('camera to laptop visible lead',(.37,0,2.57),(3.05,.19,1.25),'black',.013,[(1.81,.4,2.43)])
ortho_camera(p,look=(5.7,-11,6.1),at=(0,0,1.32),scale=9.0,width=1140,height=720,version='v03')
