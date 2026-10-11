"""Fig.6(c) exploded ordered illustrative layers + separate assembled four-cell stack. No b/d cabinet/tubes."""
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from scene_parts_v01 import *
p=Path(__file__).resolve().parent;reset()
# Numbered series 1–11 + end 17 from caption; illustrative step spacing, not contact distance.
layers=[('end plate','silver'),('silicone gasket','rubber'),('bipolar self-breathing plate','blue'),('GDE','green'),('silicone gasket','rubber'),('cathode flow plate','silver'),('proton exchange membrane','white'),('anode','copper'),('silicone gasket','rubber'),('anode flow plate','silver'),('silicone gasket','rubber'),('anode current collector','gold'),('end plate','silver')]
for i,(name,mat) in enumerate(layers):
 y=-3.25+i*.39
 plate_with_hole(f'exploded {i+1} {name}',(-1.9,y,.56),(1.5,.06,1.5),.28 if 'gasket' not in name else .35,mat)
# Assembled four-cell packet shown alongside, repeating visual units rather than false single cell.
for k in range(4):
 for j,(name,mat) in enumerate((('bipolar plate','blue'),('GDE','green'),('membrane','white'),('anode','copper'),('flow plate','silver'))):
  y=-1.45+k*.72+j*.11
  plate_with_hole(f'assembled cell{k+1} {name}',(2.2,y,.56),(1.42,.065,1.42),.25,mat)
plate_with_hole('assembled rear end plate',(2.2,-1.66,.56),(1.6,.14,1.6),.22,'silver')
plate_with_hole('assembled front end plate',(2.2,1.68,.56),(1.6,.14,1.6),.22,'silver')
presentation(p,look=(7,-9,8),at=(0,0,.55),scale=10.4,width=1280,height=700)
