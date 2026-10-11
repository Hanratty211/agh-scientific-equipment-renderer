"""R3 v04 case-local optical contrast only; exploded lid/rotor/spring/stator are NOT touching.
The dark ribbon and stripe counts are schematic, not measured manufacture.
"""
import sys,math
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from scene_parts_v03 import *
p=Path(__file__).resolve().parent;reset()
MAT['case resin']=material('smoked transparent resin',(.26,.43,.48),alpha=.34,metal=.10)
MAT['case edge']=material('satin gray metal',(.28,.37,.43),metal=.52)
MAT['spring black']=material('spring blue black',(.095,.11,.14),metal=.48)
MAT['stripe dark']=material('reel stripe graphite',(.15,.18,.22),metal=.38)
# Stator body/rim: tinted transparent wall and visible attached dark/gold stripes.
flat_ring('stator base cup',(0,0,.24),1.04,.27,.16,'case resin')
cylinder_open('stator cylindrical cup wall',(0,0,.43),1.01,.915,.27,'case resin')
flat_ring('stator outer metal lip',(0,0,.57),1.05,.99,.032,'case edge')
strip_band('stator fine gold stripe',.93,.37,.57,segment_count=48,stripe_ratio=.28,mat='gold')
strip_band('stator alternate dark stripe',.928,.37,.57,segment_count=48,stripe_ratio=.29,mat='stripe dark')
flat_ring('stator electrode inner rim',(0,0,.59),.92,.80,.020,'gold')
flat_ring('stator axle collar',(0,0,.68),.19,.085,.12,'case edge')
# Distinct rotor platter, wall and hub; tighter contrast than v03 luminous white.
flat_ring('rotor translucent platter',(0,0,1.40),.86,.18,.085,'case resin')
cylinder_open('rotor shallow outer cup',(0,0,1.54),.84,.75,.22,'case resin')
flat_ring('rotor fine rim',(0,0,1.66),.83,.78,.027,'case edge')
strip_band('rotor fine gold stripe',.772,1.46,1.63,segment_count=40,stripe_ratio=.25,mat='gold')
strip_band('rotor alternate dark stripe',.773,1.46,1.63,segment_count=40,stripe_ratio=.27,mat='stripe dark')
cylinder('rotor central hub',(0,0,1.59),.20,.24,'case edge')
# Single planar black flat ribbon spring set clear ABOVE rotor hub in exploded display.
ribbon_spiral('flat dark spiral spring',(0,0,0),1.87,start=.21,end=.68,turns=3.8,width=.042,thickness=.012,material='spring black')
polyline('retractable rope',[(.74,0,1.63),(1.10,0,1.62),(1.57,-.02,1.62)],.026,'spring black')
flat_ring('lid true center aperture',(0,0,2.63),1.03,.27,.10,'case resin')
flat_ring('lid reinforced lip',(0,0,2.69),1.055,.925,.041,'case edge')
# Same light field/background, but case-local metallic/tint contrast avoids washed-out resin.
ortho_camera(p,look=(5.0,-7.3,7.2),at=(.08,0,1.45),scale=4.6,width=820,height=1070,version='v04')
