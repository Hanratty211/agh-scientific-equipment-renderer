"""R1: upper/lower left syringe pumps, two sample inlets, coaxial camera/objective; right sealed branch."""
import sys,math
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from scene_parts_v02 import *
p=Path(__file__).resolve().parent;reset()
# Explicit two feed pumps left upper/lower (diagram positioning is illustrative).
for label,loc in [('upper',(-3.2,0,2.0)),('lower',(-3.2,0,.55))]:
 x,y,z=loc;panel(label+' syringe pump',loc,(1.15,.72,.58),'ivory',True)
 cylinder(label+' syringe',(x+.16,y,z+.43),.09,.75,'glass',rotation=(0,math.pi/2,0))
 box(label+' plunger',(x-.31,y,z+.44),(.42,.11,.11),'silver')
 box(label+' visible exit fitting',(x+.68,y,z+.42),(.1,.12,.12),'blue')
# Tubular central capillary with two separate, visible inlet fittings on owner surface.
tube('horizontal capillary shell',(-.94,0,1.10),(1.07,0,1.10),.08,'glass')
tube('inner capillary channel',(-.88,0,1.10),(1.05,0,1.10),.021,'mint')
for label,pos in [('upper',(-.83,0,1.1)),('lower',(-.50,0,1.1))]:
 sphere(label+' inlet fitting',pos,.095,'blue')
polyline('upper visible feed',[(-2.48,0,2.42),(-1.98,0,2.42),(-1.35,0,1.56),(-.83,0,1.10)],.025,'fluid')
polyline('lower visible feed',[(-2.48,0,.97),(-1.87,0,.92),(-.98,0,.78),(-.50,0,1.10)],.024,'fluid')
# Aligned camera above / inverted microscope below the SAME sample (x=0).
box('high-speed digital camera',(0,0,2.55),(.68,.48,.54),'black')
cylinder('camera objective barrel',(0,0,2.12),.15,.38,'dark')
cylinder('microscope viewing objective',(0,0,.72),.14,.50,'black')
box('inverted microscope body',(0,0,.28),(1.22,1,.37),'silver')
# Outlet and waste are distinct from the capped temporary flushing needle/branch.
sphere('outlet fitting',(1.08,0,1.1),.09,'blue')
polyline('outlet to waste visible',[(1.08,0,1.1),(1.72,0,.8),(2.0,0,.6)],.025,'fluid')
cylinder('waste vessel',(2.04,0,.22),.25,.44,'glass')
polyline('sealable right flushing branch',[(1.24,0,1.07),(1.48,0,1.50),(1.77,0,1.50)],.019,'fluid')
box('sealed flush tip',(1.82,0,1.50),(.13,.13,.17),'red')
panel('computer monitor',(3.35,0,1.1),(1.15,.22,.82),'black',True)
polyline('visible camera computer lead',[(.37,0,2.58),(1.8,.55,2.72),(2.9,.3,1.4)],.013,'black')
ortho_camera(p,look=(5.8,-11,6.2),at=(0,0,1.35),scale=9.2,width=1120,height=690)
