"""R2: single-plane flat spiral ribbon; conformal grating stripe BANDS on translucent reel walls."""
import sys,math
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from scene_parts_v03 import *
p=Path(__file__).resolve().parent;reset()
# Separate display states deliberately no touching supports between layers.
flat_ring('stator translucent housing',(0,0,.28),1.04,.26,.19,'resin')
cylinder_open('stator side wall',(0,0,.45),1.01,.91,.25,'resin')
strip_band('stator alternating stripe band',.928,.38,.57,segment_count=48,stripe_ratio=.45,mat='gold')
flat_ring('stator thin electrode rim',(0,0,.59),.92,.81,.024,'gold')
flat_ring('central stator axle collar',(0,0,.66),.20,.09,.14,'dark')
flat_ring('rotor clear body',(0,0,1.43),.86,.19,.10,'resin')
cylinder_open('rotor transparent side wall',(0,0,1.55),.83,.75,.18,'resin')
strip_band('rotor alternating stripe band',.77,1.47,1.63,segment_count=40,stripe_ratio=.46,mat='gold')
cylinder('rotor reel hub',(0,0,1.60),.18,.23,'dark')
ribbon_spiral('flat spiral spring ribbon',(0,0,0),1.78,start=.20,end=.68,turns=3.8,width=.038,thickness=.012)
polyline('single retractable rope',[(.75,0,1.64),(1.12,0,1.64),(1.58,-.03,1.64)],.022,'black')
flat_ring('aperture lid thin resin',(0,0,2.54),1.03,.27,.11,'resin')
flat_ring('lid external retaining rim',(0,0,2.60),1.05,.91,.052,'ivory')
ortho_camera(p,look=(5.1,-7.5,7.3),at=(.12,0,1.37),scale=4.55,width=820,height=1070,version='v03')
