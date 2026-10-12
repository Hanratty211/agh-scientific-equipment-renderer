"""Codex R4: ONLY case18 exploded DISPLAY geometry / camera; panels 12–14 face outward.
Layer identities/order preserved, no new internal channels or operational gaps claimed.
Overview includes assembled stack; detail uses SAME saved meshes with second camera only.
"""
import sys, math
from pathlib import Path
from mathutils import Vector
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from scene_parts_v03 import *
p=Path(__file__).resolve().parent;reset()
# Increase illustrated display spacing around positions 11–17; NOT assembly distances.
def layer_y(n):
 return -4.00+(n-1)*.50 + max(0,n-11)*.37

def exploded_x(n):
 # A gentle DISPLAY stair toward the right for successive layers exposes each real
 # negative-Y module face to the overview; order remains monotonically along Y.
 return -2.10 + max(0,n-9)*1.78

def endplate(name,x,y,z,w,h,depth):
 o=box(name,(x,y,z),(w,depth,h),'silver')
 for dx in (-.63,.63):
  for dz in (-.48,.48):
   cutter=cylinder(name+' cutter',(x+dx,y,z+dz),.052,depth+.31,'white',vertices=24,rotation=(math.pi/2,0,0))
   mod=o.modifiers.new('through-Y fastener aperture','BOOLEAN');mod.operation='DIFFERENCE';mod.object=cutter
   bpy.context.view_layer.objects.active=o;bpy.ops.object.modifier_apply(modifier=mod.name);bpy.data.objects.remove(cutter,do_unlink=True)
 return o
items={1:('endplate','silver',.17),2:('gasket','rubber',.036),3:('bipolar frame','blue',.13),4:('thin GDE','green',.018),5:('gasket','rubber',.036),6:('cathode patterned flow','silver',.11),7:('thin proton membrane','ivory',.015),8:('thin anode','copper',.020),9:('gasket','rubber',.036),10:('anode patterned flow','silver',.11),11:('gasket','rubber',.036),12:('framed cell A','blue',.17),13:('framed cell B','blue',.17),14:('framed cell C','blue',.17),15:('unresolved layer','ivory',.025),16:('caption conflict layer','gold',.031),17:('endplate','silver',.17)}
for n,(label,mat,dep) in items.items():
 y=layer_y(n);prefix=f'position {n:02d} {label}';x=exploded_x(n)
 if n in (1,17):endplate(prefix,x,y,.66,1.65,1.30,dep)
 elif n in (2,5,9,11):vertical_window(prefix,(x,y,.66),(1.51,1.19),(1.13,.80),dep,mat)
 elif n in (4,7,8,15,16):box(prefix,(x,y,.66),(1.43,dep,1.06),mat)
 else:
  vertical_window(prefix,(x,y,.66),(1.50,1.17),(.97,.72),dep,mat)
  if n in (3,6,10):
   for k in range(4):box(prefix+' flow rib',(x-.34+k*.22,y,.66),(.036,dep+.006,.68),'copper' if n in (6,10) else 'ivory')
  if n in (12,13,14):
   # LOOK direction of overview is from negative Y. Place inner panel/field lines
   # toward negative Y, ahead of its OWN four-bar frame and away from preceding layer.
   # Deep display spacing exposes all three inner faces: no seals/contact implied.
   box(prefix+' inner panel',(x,y-.095,.66),(.88,.025,.61),'copper' if n%2 else 'green')
   for k in range(5):box(prefix+' interior field line',(x-.36+k*.18,y-.118,.66),(.027,.026,.55),'black')
   for xx in (x-.65,x+.65):
    for zz in (.18,1.14):cylinder(prefix+' perimeter fastener',(xx,y-.092,zz),.043,.024,'silver',rotation=(math.pi/2,0,0))
# The assembled four-cell arrangement is the same v04 scene geometry; only the exploded
# Y positions changed. Its endplate, fastener and cell pattern remain illustrative.
for cell in range(4):
 y=-1.18+cell*.77;stem=f'assembled cell {cell+1}'
 vertical_window(stem+' frame',(2.10,y,.66),(1.52,1.20),(.96,.70),.12,'blue')
 box(stem+' contrasting inner field panel',(2.10,y-.035,.66),(.87,.027,.62),'copper' if cell%2 else 'green')
 for k in range(4):box(stem+' flow field line',(1.78+k*.22,y-.073,.66),(.035,.022,.54),'silver')
 vertical_window(stem+' thin gasket',(2.10,y+.105,.66),(1.50,1.18),(1.10,.77),.034,'rubber')
 box(stem+' membrane',(2.10,y+.16,.66),(1.41,.016,1.06),'ivory')
for y,label in ((-1.43,'rear'),(1.56,'front')):endplate('assembled '+label+' endplate',2.10,y,.66,1.75,1.38,.20)
for x in (1.39,2.81):
 for z in (.13,1.19):
  tube('assembled long tie rod',(x,-1.59,z),(x,1.77,z),.030,'silver')
  cylinder('front tie rod nut',(x,1.80,z),.075,.11,'dark',rotation=(math.pi/2,0,0))
# Overview from NEGATIVE Y, with shallow X parallax. X stair is display, not assembly offset.
ortho_camera(p,look=(4.8,-38,7.0),at=(4.15,.0,.66),scale=21.0,width=1840,height=920,version='v05')
# Supplementary view of the SAME geometry: camera-only detail, no duplicate model.
scene=bpy.context.scene;overview=scene.camera
bpy.ops.object.camera_add(location=(4.8,-34,5.2));detail=bpy.context.object;detail.name='repeated_cell_detail_camera_v05'
detail.rotation_euler=(Vector((exploded_x(13),layer_y(13),.66))-detail.location).to_track_quat('-Z','Y').to_euler();detail.data.type='ORTHO';detail.data.ortho_scale=6.7
scene.camera=detail;scene.render.resolution_x=1100;scene.render.resolution_y=660
scene.render.filepath=str(p/'repeated_cell_detail_v05.png')
bpy.ops.wm.save_as_mainfile(filepath=str(p/'scene_v05.blend'))
bpy.ops.render.render(write_still=True)
scene.camera=overview;scene.render.resolution_x=1840;scene.render.resolution_y=920
scene.render.filepath=str(p/'overview_v05.png')
bpy.ops.wm.save_as_mainfile(filepath=str(p/'scene_v05.blend'))
