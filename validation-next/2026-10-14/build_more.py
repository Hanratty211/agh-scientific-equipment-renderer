"""Case-specific continuations; approximate geometry and external visibility only."""
import math
import bpy
import render_core as r
from mathutils import Vector

def sensor_power():
 # Fig.3a top window / PV, paired LiPo batteries, fPCB, optical PPG and base.
 r.box('PL_silicone_encapsulation',(0,0,.08),(3.9,2.15,.17),'red','source-visible')
 r.box('Flexible_printed_circuit',(0,0,.38),(3.55,1.90,.07),'copper','source-visible')
 r.box('BLE_SoC',(0,-.54,.50),(.75,.45,.13),'dark','source-visible')
 r.box('PPG_module',(0,.36,.53),(.72,.67,.14),'base','source-visible')
 for n,x in enumerate((-.31,.31)):
  r.cyl(f'Optical_LED_{n}',(x,.27,.63),.07,.04,'red','source-visible')
  r.cyl(f'PPG_detector_{n}',(x,.48,.63),.06,.03,'black','source-visible')
 for n,x in enumerate((-1.22,1.22)):
  r.box(f'LiPo_battery_{n}',(x,-.03,.88),(.64,.85,.18),'metal','source-visible')
 r.box('Photovoltaic_cell',(0,0,1.20),(1.35,.89,.06),'dark','source-visible')
 r.box('Upper_silicone_skin',(0,0,1.56),(3.91,2.17,.18),'soft','source-visible')
 # Real openings in a silicone top: ring-shaped bands and separate outside slabs, not black stickers.
 # Initial v01 uses an upper solid skin: opening is a known failure to repair in v02.
 r.camera((5,-7,5),(0,0,.68),6.8)

def electrolyzer():
 # Text-only Methods p9: pump -> membrane-free cell -> single-pass outlet.
 r.box('Peristaltic_pump_body',(-2.1,0,.61),(1.34,.90,1.20),'base','text-supported')
 r.box('Pump_control_face',(-2.1,-.47,.81),(.65,.02,.32),'screen','assumption')
 r.cyl('Pump_rotor',(-2.07,-.48,.42),.24,.12,'metal',axis='Y',evidence='assumption')
 for j in range(5):
  a=j*2*math.pi/5;r.cyl('Rotor_roller_'+str(j),(-2.07+math.cos(a)*.15,-.56,.42+math.sin(a)*.15),.043,.10,'dark',axis='Y')
 r.box('NOM_membrane_free_flow_cell',(1.3,.3,.53),(1.48,.68,1.01),'base','text-supported')
 for x in (.42,2.18):
  r.box(f'Cell_clamping_plate_{x}',(x,.3,.53),(.14,.79,1.06),'metal','assumption')
 for n,x in enumerate((.63,1.94)):
  r.open_port(f'Flowcell_visible_port_{n}',(x,-.10,.53),.08,'Y','NOM_membrane_free_flow_cell')
 r.cyl('External_single_pass_reservoir',(-3.50,-.80,.38),.37,.75,'glass',evidence='assumption')
 r.cyl('External_receiving_vessel',(3.50,-.80,.38),.38,.76,'glass',evidence='assumption')
 r.route('Single_pass_inlet_tube',[(-3.5,-.80,.8),(-3.05,-.8,.92),(-2.7,-.28,.43)],.038,'blue','text-supported')
 r.route('Single_pass_pump_to_cell',[(-1.6,-.48,.43),(-.80,-.52,.87),(.12,-.40,.88),(.63,-.12,.53)],.038,'blue','text-supported')
 r.route('Single_pass_cell_to_vessel',[(1.94,-.12,.53),(2.65,-.55,.94),(3.50,-.80,.82)],.038,'blue','text-supported')
 r.camera((7,-9,6),(0,-.25,.68),10)

def antenna():
 # Fig.1(a-d) cone/torus resonator + two slots cut in ground plate.
 r.box('Dielectric_substrate',(0,0,.17),(3.45,2.26,.16),'soft','source-visible')
 ground=r.box('Ground_plane',(0,0,.28),(3.48,2.27,.048),'copper','source-visible',bevel=0)
 # Elliptical slots are boolean subtractions applied to the real ground mesh.
 for j,x in enumerate((-.82,.82)):
  cutter=r.cyl(f'Elliptical_slot_cutter_{j}',(x,0,.28),.33,.30,'black',evidence='nonrender_QA')
  cutter.scale.x=1.60; cutter.scale.y=.58; bpy.context.view_layer.update()
  mod=ground.modifiers.new(f'Ground_open_slot_{j}','BOOLEAN');mod.operation='DIFFERENCE';mod.object=cutter
  bpy.context.view_layer.objects.active=ground;bpy.ops.object.modifier_apply(modifier=mod.name)
  bpy.data.objects.remove(cutter,do_unlink=True)
 r.box('Microstrip_feed_trace',(0,-.76,.36),(.12,.95,.042),'copper','source-visible',bevel=0)
 r.box('Feed_edge_connector',(0,-1.25,.38),(.24,.23,.17),'metal','assumption')
 # Tapered resonator with upper toroidal region.
 verts=[];faces=[];n=48
 for z,rad in ((.43,.60),(1.35,.18)):
  for i in range(n):
   a=2*math.pi*i/n;verts.append((rad*math.cos(a),rad*math.sin(a)+.16,z))
 for i in range(n):faces.append((i,(i+1)%n,n+(i+1)%n,n+i))
 faces.append(tuple(reversed(range(n))));faces.append(tuple(n+i for i in range(n)))
 me=bpy.data.meshes.new('DRA_conical_mesh');me.from_pydata(verts,[],faces);me.update();ob=bpy.data.objects.new('Dielectric_resonator_conical_radiator',me);bpy.context.collection.objects.link(ob);ob.data.materials.append(r.M['glass']);r.tag(ob,'source-visible')
 r.torus('DRA_toroidal_rim',(0,.16,1.28),.25,.085,'glass',evidence='source-visible')
 r.camera((5,-8,5),(0,0,.5),6.6)

def mechanical():
 # Text-only ZwickRoell Z100 name; representative chassis, not manufacturer's CAD.
 for n,z in (('lower',.14),('upper',3.82)):r.box('Z100_'+n+'_frame',(0,.35,z),(2.65,1.28,.23),'metal','text-supported')
 for n,x in enumerate((-1.02,1.02)):r.cyl(f'Z100_representative_column_{n}',(x,.35,2.0),.092,3.65,'metal',evidence='assumption')
 for name,z in (('lower',.78),('upper',3.02)):
  r.box(f'Z100_{name}_crosshead',(0,.35,z),(1.50,.94,.30),'base','assumption')
  r.box(f'{name}_jaw_working_face',(0,-.16,z+(.19 if name=='lower' else -.19)),(.48,.09,.27),'metal','assumption')
 # A simple connected lattice sample: cell struts exist as distinct meshes.
 for j in range(4):
  z=1.04+j*.43
  for x in (-.20,.20):r.segment(f'PIM_chain_vert_{j}_{x}',(x,.33,z),(x,.33,z+.42),.028,'soft','assumption')
  r.segment(f'PIM_chain_cross_{j}',(-.2,.33,z+.21),(.2,.33,z+.21),.035,'soft','assumption')
 r.box('Z100_control_panel',(1.44,-.21,2.14),(.58,.20,.90),'dark','assumption');r.box('Z100_panel_display',(1.44,-.33,2.33),(.38,.023,.29),'screen','assumption')
 r.camera((6,-9,5.7),(0,0,1.85),6.6)

def thermal():
 # Text-only AHP pp2/11: aluminum-plastic casing + self-supporting multi-layer copper-mesh wick.
 # Simple section leaves vapor volume UNKNOWN; it is not a factual duct.
 r.box('Aluminum_plastic_lower_casing',(0,0,.22),(4.60,1.50,.10),'metal','text-supported')
 r.box('Aluminum_plastic_back_wall',(0,.70,.48),(4.60,.10,.50),'metal','text-supported')
 r.box('Aluminum_plastic_front_lip',(0,-.70,.33),(4.60,.10,.20),'metal','assumption')
 r.box('Upper_casing_exposed_strip',(0,.43,.76),(4.60,.52,.09),'metal','assumption')
 for layer in range(3):
  z=.35+layer*.08
  for j in range(7):
   y=-.49+j*.15;r.segment(f'Copper_wick_warp_{layer}_{j}',(-2.18,y,z),(2.18,y,z),.016,'copper','text-supported')
  for j in range(19):
   x=-2.16+j*.24;r.segment(f'Copper_wick_weft_{layer}_{j}',(x,-.55,z+.018),(x,.55,z+.018),.016,'copper','text-supported')
 r.box('Heater_contact_end',(-2.30,0,.25),(.25,1.5,.22),'dark','assumption')
 r.box('Cooling_contact_end',(2.30,0,.25),(.25,1.5,.22),'base','assumption')
 r.camera((5,-9,5),(0,0,.31),7.5)
