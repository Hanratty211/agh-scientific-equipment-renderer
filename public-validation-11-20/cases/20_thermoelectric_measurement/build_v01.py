"""Extended Data Fig.1(a) two Cu blocks/Peltier/sample/grease/electrodes, visible leads only."""
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from scene_parts_v01 import *
p=Path(__file__).resolve().parent;reset()
box('insulated fixture base',(0,0,-.1),(7.6,3,.2),'white')
box('Peltier module',(0,0,.17),(3.1,1.45,.32),'white')
for x in (-1,1):
 box('copper thermal block',(x,0,.69),(.95,1.15,.72),'copper')
 box('grease interface patch',(x,0,1.08),(.67,.86,.047),'white')
box('bridged sample',(0,0,1.16),(2.62,.55,.10),'dark')
for x in (-.54,.54):
 box('sample electrode pad',(x,-.19,1.24),(.15,.16,.035),'gold')
 polyline('visible measurement lead',[(x,-.19,1.25),(x,-.88,1.45),(x*2.3,-1.1,.84)],.014,'copper')
for x in (-2.55,2.55):
 box('nanovoltmeter',(x,-.2,.42),(.88,.72,.67),'dark')
 box('meter face',(x,-.57,.5),(.62,.02,.27),'screen')
box('Peltier controller',(0,1.28,.37),(.95,.57,.6),'blue')
presentation(p,look=(6,-8,6.3),at=(0,0,.65),scale=8.4,width=1000,height=700)
