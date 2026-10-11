"""Fig.1 macro optical setup; no micro-scale sample inset, text, or hidden internals."""
from pathlib import Path
import sys,math
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from scene_parts_v01 import *
p=Path(__file__).resolve().parent;reset()
box('optical table',(0,0,-.15),(7.2,4.3,.3),'silver')
# Overall optical apparatus illustrative; optical focus/interaction is not a ray-trace.
for x in (-2.6,-1.1,.7,2.5):
 box('mount post',(x,0,.43),(.15,.15,.9),'silver')
 cylinder('upright collar',(x,0,.92),.21,.08,'dark')
for x in (-2.4,-.7,.8,2.25):
 cylinder('optic holder',(x,0,1.11),.34,.12,'dark',rotation=(0,math.pi/2,0))
 cylinder('optical face',(x,0,1.11),.25,.13,'glass',rotation=(0,math.pi/2,0))
box('illumination module',(-3.2,0,1.15),(.55,.55,.43),'blue')
box('sample stage',(1.65,.05,.35),(1.25,1.1,.22),'silver')
box('glass liquid cell',(1.65,.05,.6),(.55,.62,.28),'glass')
box('detector housing',(3.0,.0,1.15),(.46,.45,.5),'dark')
# Beam schematic shown only when supported by the figure; straight paths are optical, not structural supports.
polyline('visible optical axis',[(-2.92,0,1.11),(-.7,0,1.11),(.8,0,1.11),(1.65,0,1.11),(2.75,0,1.11)],.014,'red')
box('camera body',(1.7,-1.55,2.12),(.6,.48,.42),'dark');tube('camera view',(1.7,-1.55,1.9),(1.7,-.95,1.28),.11,'silver')
presentation(p,look=(7,-9,6.2),at=(0,0,.7),scale=9,width=960,height=690)
