"""Batch physical device DETAILS, task-configured not a generic knobbed panel.
Evidence about commercial port type belongs in PHYSICAL_HARDWARE_SOURCE_AND_SCOPE.md;
these low-poly bodies are representative and never exact commercial CAD.
Coordinates illustrative Blender world units; only exterior visible interfaces modeled.
"""
import bpy,math
from mathutils import Vector
from scene_parts_v03 import box,cylinder,flat_ring,tube,polyline,material,MAT

def bind_existing_materials():
 """After bpy.ops.wm.open_mainfile, imported module globals point at removed datablocks.
 Rebind MAT to loaded scene materials by their stable material names, never silently
 create a second typeface/color that changes frozen whole-scene materials.
 """
 names={'silver':'brushed aluminum','white':'ceramic white','dark':'dark polymer',
  'copper':'copper','gold':'electrode gold','blue':'instrument blue','red':'alignment red',
  'glass':'translucent pane','fluid':'fluid tube','green':'PCB green','rubber':'silicone',
  'screen':'screen dark blue','resin':'clear resin','ivory':'warm ivory',
  'black':'black instrument','amber':'amber','mint':'teal'}
 for key,display in names.items():
  m=bpy.data.materials.get(display)
  if m:MAT[key]=m
  else:MAT[key]=material(display,(.3,.3,.3))

def metal_foot(name,x,y,z,depth=.08):
 return box(name,(x,y,z),(.17,.19,depth),'dark')

def laptop(name,center,width=1.17,depth=.92,angle=math.radians(108),port=False):
 """Clamshell: continuous base/hinge/lid; lid rotates about actual hinge at rear edge.
 Screen face toward negative y; a rearward lean >90° measured from base forward vector.
 Outputs world surface points for a representative DATA socket, if needed.
 """
 x,y,z=center;front=y-depth/2;hinge=y+depth/2-.065
 base=box(name+' base',(x,y,z),(width,depth,.072),'silver')
 for xx in (-width*.40,width*.40):
  for yy in (front+.12,hinge-.12):metal_foot(name+' foot',x+xx,yy,z-.062,.043)
 # Model connected barrels (hinge pin shares axis with both base and screen root).
 cylinder(name+' full hinge axle',(x,hinge,z+.055),.055,width*.84,'dark',rotation=(0,math.pi/2,0))
 for xx in (-width*.34,0,width*.34):
  cylinder(name+' hinge barrel',(x+xx,hinge,z+.055),.069,width*.12,'silver',rotation=(0,math.pi/2,0))
 # `angle` is opening >90 degrees; tilt back relative to vertical by angle-90.
 tilt=angle-math.pi/2;h=depth*.94
 side=Vector((0,math.sin(tilt),math.cos(tilt)))
 bottom=Vector((x,hinge,z+.065));mid=bottom+side*(h/2)
 lid=box(name+' lid',tuple(mid),(width,.073,h),'black');lid.rotation_euler[0]=-tilt
 # Inset face follows the lid tilt as a separate editable mesh in world space.
 bpy.context.view_layer.update()
 inset=mid+lid.matrix_world.to_3x3()@Vector((0,-.042,.042))
 display=box(name+' display inset',tuple(inset),(width*.88,.010,h*.78),'screen')
 display.rotation_euler[0]=-tilt
 box(name+' touchpad',(x,front+depth*.19,z+.043),(width*.32,depth*.16,.006),'dark')
 for row in range(3):
  for col in range(11):box(name+' key',(x+(col-5)*width*.070,front+depth*(.39+.075*row),z+.043),(width*.057,depth*.046,.005),'black')
 box(name+' left rim',(x-width*.48,y,z+.007),(.020,depth,.041),'dark')
 if port:
  # Socket is in outer LEFT side wall of base, not in screen. Small rectangular void.
  sx=x-width/2-.006;sy=y+.06;sz=z+.004
  socket=box(name+' representative DATA receptacle',(sx,sy,sz),(.006,.079,.030),'black')
  collar=box(name+' DATA port surround',(sx-.004,sy,sz),(.012,.090,.045),'silver')
  return {'base':base,'screen':lid,'hinge':(x,hinge,z+.055),'socket_center':(sx-.013,sy,sz),'socket_axis':(-1,0,0),'front':front,'port_owner':socket,'housing':base}
 return {'base':base,'screen':lid,'hinge':(x,hinge,z+.055),'front':front}

def chassis(name,center,size,color='black',screen=False,handle=False):
 x,y,z=center;w,d,h=size;body=box(name,center,size,color)
 for xx in (x-w*.38,x+w*.38):
  for yy in (y-d*.39,y+d*.39):metal_foot(name+' foot',xx,yy,z-h/2-.036)
 box(name+' front bezel',(x,y-d/2-.009,z),(w*.91,.018,h*.83),'dark')
 if screen:box(name+' screen',(x-w*.16,y-d/2-.025,z+h*.13),(w*.45,.018,h*.40),'screen')
 if handle:
  for xx in (x-w*.31,x+w*.31):box(name+' handle leg',(xx,y,z+h*.57),(.047,.07,.18),'silver')
  box(name+' carry grip',(x,y,z+h*.67),(w*.69,.079,.06),'silver')
 for i in range(4):box(name+' side vent',(x+w/2+.002,y-d*.20+i*d*.13,z+h*.06),(.006,.030,h*.25),'dark')
 return body

def analog_input(name,point,r=.065):
 """Representative analog BNC-form input facing camera (-Y). True open inner annulus.
 Plug inserts axially, never terminated at screen. No actual electrical claims.
 """
 x,y,z=point
 outer=flat_ring(name+' BNC input ring',(x,y,z),r,r*.52,.025,'silver');outer.rotation_euler[0]=math.pi/2
 dark=flat_ring(name+' socket dielectric',(x,y-.017,z),r*.48,r*.15,.012,'dark');dark.rotation_euler[0]=math.pi/2
 pin=cylinder(name+' analog input center contact',(x,y-.027,z),r*.095,.018,'gold',rotation=(math.pi/2,0,0))
 # mating cylindrical collar occupies negative Y face, coax extends outward
 plug=cylinder(name+' coax mating shell',(x,y-.065,z),r*.43,.075,'silver',rotation=(math.pi/2,0,0))
 for dx in (-r*.33,r*.33):box(name+' bayonet lug',(x+dx,y-.060,z),(.019,.012,.018),'silver')
 boot=cylinder(name+' plug strain relief',(x,y-.136,z),r*.27,.072,'black',rotation=(math.pi/2,0,0))
 return {'input_ring':outer,'plug':plug,'axis':(0,-1,0),'cable_start':(x,y-.172,z),'input_center':(x,y,z),'body_gap_world':.0}

def signal_scope(name,center,size,signal_point,color='black'):
 """Oscilloscope-style body: wide screen, grouped channel controls, recessed analog input.
 Signal channel selection representative unless source specifies it.
 """
 x,y,z=center;w,d,h=size;body=chassis(name,center,size,color,screen=False,handle=True)
 front=y-d/2-.025
 box(name+' display rim',(x-w*.19,front-.004,z+h*.13),(w*.47,.018,h*.52),'silver')
 box(name+' raster screen',(x-w*.19,front-.018,z+h*.13),(w*.42,.008,h*.46),'screen')
 for i in range(3):
  for j in range(2):cylinder(name+' channel knob',(x+w*(.17+.145*j),front-.032,z+h*(.24-.24*i)),.039,.035,'silver',rotation=(math.pi/2,0,0))
 connector=analog_input(name+' ANALOG INPUT',signal_point,r=.055)
 return {'body':body,'signal':connector}

def resistance_substituter(name,center,size):
 x,y,z=center;w,d,h=size;body=chassis(name,center,size,'ivory',False,False)
 front=y-d/2-.018
 for k in range(5):cylinder(name+' resistance selector',(x-w*.35+k*w*.175,front-.022,z+.02),.043,.033,'black',rotation=(math.pi/2,0,0))
 for xx in (x-w*.25,x+w*.25):
  ring=flat_ring(name+' resistance terminal',(xx,front-.005,z-h*.30),.048,.023,.017,'gold');ring.rotation_euler[0]=math.pi/2
 return body

def hv_supply(name,center,size):
 x,y,z=center;w,d,h=size;body=chassis(name,center,size,'black',screen=True,handle=True);front=y-d/2-.018
 box(name+' interlock cover',(x+w*.26,front-.018,z-h*.15),(w*.31,.033,h*.34),'red')
 for k,zoff in enumerate((.14,-.16)):
  # guarded / insulated HV and return termination, no ordinary LV banana label
  cylinder(name+(' guarded positive HV boundary' if k==0 else ' insulated return boundary'),(x+w*.25,front-.046,z+zoff),.060,.067,'red' if k==0 else 'green',rotation=(math.pi/2,0,0))
 return body

def dc_supply(name,center,size):
 x,y,z=center;w,d,h=size;body=chassis(name,center,size,'black',screen=True,handle=False);front=y-d/2-.020
 for k,xx in enumerate((x+w*.18,x+w*.37)):
  ring=flat_ring(name+(' positive terminal' if k==0 else ' negative terminal'),(xx,front-.003,z-h*.23),.045,.026,.024,'red' if k==0 else 'dark');ring.rotation_euler[0]=math.pi/2
 return body

def syringe_drive(name,center,size,color='red'):
 x,y,z=center;w,d,h=size;body=chassis(name,center,size,color,screen=True)
 for s in (-1,1):box(name+' syringe rail',(x+s*w*.37,y-d*.16,z+h*.60),(.048,d*.27,h*.58),'silver')
 cylinder(name+' plunger drive',(x+w*.16,y-d*.16,z+h*.52),.058,w*.58,'silver',rotation=(0,math.pi/2,0))
 cylinder(name+' mounted syringe barrel',(x-w*.17,y-d*.26,z+h*.50),.073,w*.45,'glass',rotation=(0,math.pi/2,0))
 return body

def camera_body(name,center,size,front_axis='z'):
 x,y,z=center;w,d,h=size;body=chassis(name,center,size,'black',screen=False)
 box(name+' finned cooler',(x,y+d/2+.014,z),(w*.75,.04,h*.42),'silver')
 if front_axis=='x':cylinder(name+' inward lens',(x+w*.62,y,z),.15,w*.36,'silver',rotation=(0,math.pi/2,0))
 else:cylinder(name+' C-mount collar',(x,y,z-h*.53),w*.24,.10,'silver')
 return body

def representative_data_seat(name,point,axis='left'):
 """Unknown camera/laptop DATA socket type: recessed block and seated dark plug;
 visually distinct from analog BNC and power terminals, NOT named USB/RJ45.
 """
 x,y,z=point
 if axis=='left':
  box(name+' data socket',(x,y,z),(.012,.085,.046),'black')
  box(name+' seated data plug',(x-.050,y,z),(.085,.067,.034),'dark')
  box(name+' cable boot',(x-.105,y,z),(.050,.050,.037),'black')
  return (x-.130,y,z)
 box(name+' data socket',(x,y,z),(.090,.012,.052),'black')
 box(name+' seated data plug',(x,y-.051,z),(.071,.086,.039),'dark')
 box(name+' cable boot',(x,y-.103,z),(.055,.054,.038),'black')
 return (x,y-.130,z)
