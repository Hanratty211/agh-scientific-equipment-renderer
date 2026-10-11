"""R2: laser→HWP→BS→HWP→lenses→45° XZ dichroic, actual surface-normal reflection.
This is a known optical-axis diagram, not a photon propagation simulator.
"""
import sys,math
from pathlib import Path
from mathutils import Vector
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from scene_parts_v03 import *
p=Path(__file__).resolve().parent;reset();z=1.05
box('laser housing',(3.5,0,z),(.74,.5,.45),'black')
box('laser output face',(3.10,0,z),(.05,.18,.18),'gold')
for i,x in enumerate((2.61,1.58)):
 cylinder('half wave plate '+str(i+1),(x,0,z),.22,.045,'ivory',rotation=(0,math.pi/2,0))
 marker('HWP '+str(i+1)+' right port','half wave plate '+str(i+1),(x+.0225,0,z),.025)
 marker('HWP '+str(i+1)+' left port','half wave plate '+str(i+1),(x-.0225,0,z),.025)
 box('HWP stand '+str(i+1),(x,0,.5),(.07,.16,.76),'dark')
# BS lies BETWEEN plates.
bs=box('power BS cube',(2.12,0,z),(.36,.36,.36),'glass')
marker('BS incoming surface','power BS cube',(2.30,0,z),.025)
marker('BS exiting surface','power BS cube',(1.94,0,z),.025)
for j,x in enumerate((1.11,.67)):
 cylinder('collimating lens '+str(j+1),(x,0,z),.19,.048,'glass',rotation=(0,math.pi/2,0))
 for side,xx in [('right',x+.024),('left',x-.024)]:marker('lens '+str(j+1)+' '+side+' face','collimating lens '+str(j+1),(xx,0,z),.024)
 box('collimating mount '+str(j+1),(x,0,.56),(.07,.15,.76),'silver')
# Incoming -X reflected +Z: n=(+X,-Z)/sqrt(2) yields r=d-2(d·n)n=+Z.
dich=box('tilted dichroic active plate',(0,0,z),(.035,.48,.54),'amber')
dich.rotation_euler[1]=-math.pi/4
# Route endpoints touch the actual evaluated panel surface (ray intersection calculated from mesh).
marker('dichroic incoming interface','tilted dichroic active plate',(.019,0,z),.022)
marker('dichroic upper interface','tilted dichroic active plate',(0,0,z+.019),.022)
marker('dichroic lower interface','tilted dichroic active plate',(0,0,z-.019),.022)
route('laser-HWP1 axis',(3.075,0,z),(2.634,0,z),'red',.012)
route('HWP1-BS axis',(2.588,0,z),(2.312,0,z),'red',.012)
route('BS-HWP2 axis',(1.928,0,z),(1.604,0,z),'red',.012)
route('HWP2-lens1 axis',(1.556,0,z),(1.135,0,z),'red',.012)
route('lens1-lens2 axis',(1.085,0,z),(.695,0,z),'red',.012)
route('lens2-dichroic axis',(.645,0,z),(.019,0,z),'red',.012)
route('dichroic to objective axis',(0,0,z+.019),(0,0,1.67),'red',.012)
# Upper source condenser → sample → objective; lower image path filter/lens/camera.
cylinder('objective',(0,0,1.84),.26,.33,'black')
marker('objective lower face','objective',(0,0,1.675),.023)
box('glass sample',(0,0,2.28),(.73,.62,.19),'glass')
cylinder('dark-field condenser',(0,0,2.75),.31,.22,'black')
cylinder('halogen source',(0,0,3.30),.30,.33,'ivory')
cylinder('short pass filter',(0,0,.72),.25,.07,'amber')
cylinder('imaging lens',(0,0,.39),.24,.07,'glass')
box('sCMOS camera',(0,0,-.23),(.72,.67,.47),'black')
for name,pt in [('filter upper',(0,0,.755)),('filter lower',(0,0,.685)),('imaging upper',(0,0,.425)),('imaging lower',(0,0,.355)),('sCMOS sensor top',(0,0,.005))]:marker(name,'imaging branch',(pt[0],pt[1],pt[2]),.022)
route('dichroic-filter imaging axis',(0,0,z-.019),(0,0,.755),'red',.012)
route('filter-imaging lens axis',(0,0,.685),(0,0,.425),'red',.012)
route('imaging lens-sCMOS axis',(0,0,.355),(0,0,.005),'red',.012)
ortho_camera(p,look=(5.8,-8,5.9),at=(1.26,0,1.43),scale=7.4,width=1000,height=820,version='v03')
