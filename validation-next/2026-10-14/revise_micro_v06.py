"""04 v06 from v05: source-visible exterior fittings, smooth blue hoses, extended green balloons.
No claim of chip lumen, seal, backflow, real-scale green liquid, or functional pump.
"""
import sys,math
from pathlib import Path
import bpy
from mathutils import Vector
root=Path(__file__).resolve().parent;sys.path.insert(0,str(root))
import render_core as r
r.M.clear()
for m in bpy.data.materials:
 if m.name.startswith('MAT_'):r.M[m.name[4:]]=m

def smooth_tube(ob,anchors,resolution=7):
 """Bezier control points preserve exact two endpoints; intermediate handles are AUTO."""
 c=ob.data
 while c.splines:c.splines.remove(c.splines[0])
 sp=c.splines.new('BEZIER');sp.bezier_points.add(len(anchors)-1)
 for p,xyz in zip(sp.bezier_points,anchors):p.co=xyz;p.handle_left_type='AUTO';p.handle_right_type='AUTO'
 sp.resolution_u=resolution;c.resolution_u=20

def balloon(name,loc,i):
 """Editable ellipsoid mesh with narrowed neck oriented X; figure-shape only."""
 bpy.ops.mesh.primitive_uv_sphere_add(segments=24,ring_count=12,location=loc);o=bpy.context.object;o.name=name
 o.scale=(.30,.065,.095);o.data.materials.append(r.M['schematic_green']);r.tag(o,'source-visible')
 o['shape_note']='green Fig3C outlet balloon schematic, not sealed vessel/dimensions';return o
chip=bpy.data.objects['Transparent_microfluidic_chip'];chip['v06_note']='Solid chip exterior; five right and five left fittings touch sides. NO bore, no internal channel, no seal verified.'
for i,y in enumerate((-.69,-.87,-1.05,-1.23,-1.41)):
 x=.62+i*.63;start=(x,.07,.85);right=(-.395,y,.145);left=(-2.005,y,.145)
 # The hose starts at the true saved Syringe_hub_connector front y=.07, not the Pump_i_hub.
 blue=bpy.data.objects[f'Blue_inlet_exterior_{i}']
 smooth_tube(blue,[start,(x,-.30,.87),(x,-.75,.83),(x-.32,-1.12,.63),(-.15,y,.32),right])
 blue['v06_note']='External flexible route: world cap of syringe hub to externally visible fitting lip; image schematic layout, no internal flow claim.'
 # Exterior sleeve and contrasting lip help the five distinct chip boundary positions remain perceptible.
 sleeve=bpy.data.objects[f'Right_panel_fitting_{i}'];sleeve['visible_role']='exterior tube-hub sleeve, plain cylindrical mesh; solid chip wall behind'
 r.cyl(f'Right_fitting_visible_collar_{i}',(-.41,y,.145),.061,.025,'metal',axis='X',evidence='assumption')['physical_owner']=chip.name
 green=bpy.data.objects[f'Green_outlet_exterior_{i}']
 # The far endpoint lands inside the ellipsoid neck; five outlets, not five short end caps.
 smooth_tube(green,[left,(-2.35,y,.18),(-2.7,y,.23),(-3.0,y,.29),(-3.46,y,.32)])
 green['v06_note']='Five green Fig3C exterior balloon lines, topological seal not represented.'
 old=bpy.data.objects.get(f'Green_schematic_terminal_{i}')
 if old:bpy.data.objects.remove(old,do_unlink=True)
 balloon(f'Green_balloon_schematic_{i}',(-3.62,y,.32),i)
# Reference reads left-to-right balloon–chip–syringe; enlarge overview extent without dropping old rightmost pump.
for ob in list(bpy.data.objects):
 if ob.type=='CAMERA':bpy.data.objects.remove(ob,do_unlink=True)
r.camera((5.5,-7.8,5.6),(-.58,-.45,.47),10.3)
sc=bpy.context.scene;sc['revision_version']='v06';sc['visual_review']='external_human_review_pending';sc['basis']='Fig.3C p4, Fig3A pump shape only';sc['unknown']='No drilled chip port or invisible microchannels, fluid continuity, actual balloon seal or dimensions verified.'
bpy.context.view_layer.update();out=root/'cases/04_microfluidics/v06';out.mkdir(exist_ok=True)
bpy.ops.wm.save_as_mainfile(filepath=str(out/'scene.blend'));print('V06_SAVED',out/'scene.blend',flush=True)
