"""R1: orthogonal source optical apparatus. Approximate free-space axes only, no ray tracing."""
import sys,math
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from scene_parts_v02 import *
p=Path(__file__).resolve().parent;reset()
# Horizontal optical train from right, vertical imaging/trapping line at x=0.
box('laser housing',(3.25,0,.95),(.82,.44,.46),'black')
box('laser aperture',(2.81,0,.95),(.06,.13,.13),'gold')
for i,x in enumerate((2.2,1.75)):
 cylinder('half wave plate '+str(i+1),(x,0,.95),.21,.055,'ivory',rotation=(0,math.pi/2,0))
 box('half wave holder '+str(i+1),(x,0,.52),(.075,.13,.6),'dark')
box('power-control BS frame',(1.3,0,.95),(.38,.37,.44),'silver')
bs=box('power-control BS optical face',(1.3,0,.95),(.024,.33,.36),'glass');bs.rotation_euler[2]=math.pi/4
for j,x in enumerate((.86,.50)):
 cylinder('collimating lens '+str(j+1),(x,0,.95),.18,.07,'glass',rotation=(0,math.pi/2,0))
 box('collimating mount '+str(j+1),(x,0,.53),(.06,.12,.65),'silver')
box('tilted dichroic holder',(0,0,.92),(.46,.18,.51),'black')
dich=box('tilted dichroic active face',(0,0,.95),(.38,.022,.4),'amber');dich.rotation_euler[2]=math.pi/4
# Polarized illumination reaches tilted optical surface; turn occurs at that face, not a remote center.
polyline('laser to BS axis',[(2.78,0,.95),(1.48,0,.95)],.012,'red')
polyline('BS to dichroic axis',[(1.1,0,.95),(.22,0,.95)],.012,'red')
polyline('dichroic to objective axis',[(0,0,1.12),(0,0,1.68)],.012,'red')
# Above: objective/sample + dark-field condenser + halogen source.
cylinder('objective body',(0,0,1.82),.27,.34,'black')
cylinder('objective front glass',(0,0,2.04),.19,.055,'glass')
box('sample and upper glass cell',(0,0,2.32),(.7,.60,.23),'glass')
cylinder('dark field condenser',(0,0,2.83),.32,.25,'black')
cylinder('halogen lamp',(0,0,3.43),.32,.38,'ivory')
# Bottom imaging branch below the tilted dichroic.
cylinder('short-pass filter',(0,0,.62),.26,.06,'amber')
cylinder('imaging lens',(0,0,.34),.25,.07,'glass')
box('sCMOS camera',(0,0,-.17),(.77,.65,.51),'black')
# Identity intentionally named; no extra arbitrary side camera or nanoparticle inset.
ortho_camera(p,look=(5.4,-8,5.8),at=(1.1,0,1.48),scale=7.9,width=950,height=800)
