"""R1 distinct thin resin lid with aperture; rotor/grating bands/stator, exploded presentation only."""
import sys,math
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from scene_parts_v02 import *
p=Path(__file__).resolve().parent;reset()
flat_ring('stator transparent tray',(0,0,.25),1.05,.28,.24,'resin')
flat_ring('stator wall lip',(0,0,.42),1.02,.79,.09,'resin')
flat_ring('stator electrode band',(0,0,.48),.79,.72,.09,'gold')
# Visible cylindrical grating as alternating vertical conductor strips on stator and rotor walls.
for j in range(42):
 t=j*2*math.pi/42
 tube('stator vertical electrode strip',(.77*math.cos(t),.77*math.sin(t),.47),(.77*math.cos(t),.77*math.sin(t),.70),.016,'gold' if j%2 else 'black')
ring('stator central spindle collar',(0,0,.65),.20,.05,'dark')
# Rotor floats intentionally above tray, with distinct clear housing and central hub.
flat_ring('rotor transparent disk',(0,0,1.42),.85,.20,.10,'resin')
flat_ring('rotor electrode ring',(0,0,1.50),.73,.63,.035,'gold')
for j in range(36):
 t=j*2*math.pi/36
 tube('rotor vertical electrode strip',(.68*math.cos(t),.68*math.sin(t),1.43),(.68*math.cos(t),.68*math.sin(t),1.61),.014,'gold' if j%2 else 'black')
cylinder('rotor hub',(0,0,1.60),.19,.25,'dark')
pts=[]
for j in range(160):
 t=j/159*8*math.pi;r=.16+.53*j/159;pts.append((r*math.cos(t),r*math.sin(t),1.8))
polyline('flat spiral spring',pts,.018,'copper')
polyline('retractable rope',[(.71,0,1.65),(1.04,0,1.64),(1.60,-.02,1.63)],.026,'black')
flat_ring('lid with genuine center aperture',(0,0,2.55),1.04,.25,.14,'resin')
flat_ring('lid outer rim',(0,0,2.63),1.06,.89,.07,'ivory')
ortho_camera(p,look=(5.3,-7.6,7),at=(.18,0,1.37),scale=4.65,width=780,height=1050)
