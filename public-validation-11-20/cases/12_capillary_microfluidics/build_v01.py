"""Fig.1(b) entire experiment; branch sealed during experiment, no hidden fluid loop."""
from pathlib import Path
import sys,math
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from scene_parts_v01 import *
p=Path(__file__).resolve().parent;reset()
box('bench',(0,0,-.13),(9.5,3,.26),'white')
for x in (-3.8,-2.5):
 box('syringe pump',(x,0,.25),(1,.75,.36),'blue')
 box('pump slide',(x,.0,.48),(.62,.22,.12),'silver')
 cylinder('syringe barrel',(x,-.1,.58),.09,.75,'glass',rotation=(0,math.pi/2,0))
 tube('syringe plunger',(x-.7,-.1,.58),(x-.25,-.1,.58),.05,'silver')
# Center transparent capillary zone with visually genuine aperture in raised sample carrier.
box('microfluidic mount',(-.5,0,.27),(1.65,1.1,.18),'silver')
tube('glass capillary',(-1.2,-.07,.52),(.3,-.07,.52),.09,'glass')
tube('inner visible line',(-1.1,-.07,.52),(.23,-.07,.52),.025,'fluid')
polyline('inlet one visible', [(-3.3,-.1,.58),(-2.7,-.9,.55),(-1.2,-.22,.52)],.025,'fluid')
polyline('inlet two visible',[(-2.0,-.1,.58),(-1.9,.83,.55),(-1.18,.11,.52)],.025,'fluid')
box('microscope base',(.8,-.85,.26),(1.25,.95,.22),'dark')
cylinder('inverted microscope column',(.9,-.85,.78),.14,1.05,'silver')
cylinder('objective',(.2,-.35,.75),.13,.44,'dark')
box('high speed camera',(.9,-.75,1.55),(.53,.45,.42),'blue')
polyline('visible waste segment',[(.28,-.07,.52),(1.25,.65,.53),(2.35,.75,.8)],.023,'fluid')
cylinder('waste vessel',(2.4,.75,.32),.28,.65,'glass')
box('computer',(3.65,0,.42),(.95,.22,.8),'dark');box('monitor face',(3.65,-.125,.45),(.8,.035,.62),'screen')
box('keyboard',(3.65,-.65,.12),(.85,.4,.05),'silver')
presentation(p,look=(8,-11,6.8),at=(0,0,.53),scale=11,width=1100,height=660)
