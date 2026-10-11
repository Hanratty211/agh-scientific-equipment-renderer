"""R3 v04: use actual film.matrix_world local coords for cable anchors, hide QA anchors in render.
Two readout sockets and one continuous regulator stay visible; no inferred closed fluid circuit.
"""
import sys,math
from pathlib import Path
from mathutils import Vector
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from scene_parts_v03 import *
p=Path(__file__).resolve().parent;reset()
MAT['glass pale edge']=material('transparent glass blue edge',(.28,.63,.74),alpha=.34)
MAT['thin visible film']=material('restrained translucent coating',(.52,.72,.77),alpha=.21)
tube('low glass brace',(-1.80,0,.13),(-1.80,0,.72),.054,'silver')
tube('high glass brace',(.15,0,.13),(.15,0,1.47),.054,'silver')
glass=box('tilted transparent glass',(-.83,0,1.07),(2.27,1.49,.047),'glass pale edge');glass.rotation_euler[1]=-.48
film=box('TeRC transparent coating',(-.83,0,1.10),(2.11,1.34,.010),'thin visible film');film.rotation_euler[1]=-.48
# Object mesh dimensions were baked by box(); both anchors derived from film local edge points.
# Blender matrix_world is re-evaluated after rotation; their world x/z follow source tilt.
bpy.context.view_layer.update()
local_points={'left':Vector((-1.00,-.55,0.005)),'right':Vector((1.00,-.55,0.005))}
anchors={}
for side,local in local_points.items():
 pt=film.matrix_world@local;anchors[side]=tuple(pt)
 qa=marker('QA glass '+side+' contact','TeRC transparent coating',pt,.006,'black')
 # Tiny black tip on real film surface; audit v0.6 requires marker render enabled.
 # Not a fictional gold electrode package; pixel visibility is explicitly unverified.
# Narrow edge border, not an opaque slab filling the glass.
for sign in (-1,1):
 a=film.matrix_world@Vector((-1.055,sign*.67,0));b=film.matrix_world@Vector((1.055,sign*.67,0))
 tube('visible thin film edge',a,b,.012,'glass pale edge')
cylinder('raised clear reservoir',(-2.50,.10,2.70),.27,.66,'glass')
polyline('continuous U regulator',[(-2.50,.10,2.37),(-2.53,.10,2.05),(-2.19,.10,1.82),(-1.86,.10,2.02),(-1.86,.10,2.30),(-1.58,.10,2.32),(-1.58,.10,2.03)],.032,'fluid')
tube('downward nozzle',(-1.58,.10,2.03),(-1.58,.10,1.79),.038,'silver')
sphere('one falling drop',(-1.58,.10,1.59),.075,'fluid')
panel('resistance substituter',(1.32,.10,.53),(1.24,.75,.79),'ivory',True)
for k in range(3):cylinder('resistance selector knob',(1.03+k*.27,-.33,.38),.052,.04,'black',rotation=(math.pi/2,0,0))
panel('oscilloscope',(3.0,.10,.63),(1.33,.76,1.04),'black',True)
box('scope side controls',(3.42,-.30,.39),(.13,.035,.18),'silver')
for label,obj,pos in [('resistor','resistance substituter',(1.00,-.29,.77)),('scope','oscilloscope',(2.58,-.29,.92))]:
 qa=marker('QA '+label+' terminal',obj,pos,.006,'black')
route('visible signal to resistance socket',anchors['left'],(1.00,-.29,.77),'gold',.014,[(-.65,-.75,1.22),(.45,-.60,.93)])
route('visible signal to scope socket',anchors['right'],(2.58,-.29,.92),'gold',.014,[(.85,-.76,1.03),(1.88,-.66,.91)])
ortho_camera(p,look=(5.1,-9,6.4),at=(.16,0,1.35),scale=8.0,width=1100,height=800,version='v04')
