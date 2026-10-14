"""Non-destructive v02 targeted repairs to v01 scenes; v01 files remain untouched.
Use Blender -b cases/ID/v01/scene.blend --python revise_cases.py -- ID
This is geometry repair, not a claim of physical functioning or pixel acceptance.
"""
import sys,json,math
from pathlib import Path
import bpy
from mathutils import Vector
ROOT=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT))
import render_core as r


def move(name,xyz):
 ob=bpy.data.objects.get(name)
 if ob:ob.location=xyz
 return ob

def remove(name):
 o=bpy.data.objects.get(name)
 if o:bpy.data.objects.remove(o,do_unlink=True)

def reclass(ob,note):
 ob['revision_reason']=note;ob['evidence_type']='assumption';return ob

def glass_fix():
 r.M.clear()
 for obj in bpy.data.materials:
  if obj.name.startswith('MAT_'):r.M[obj.name.removeprefix('MAT_')]=obj


def microfluidics():
 glass_fix()
 # Fix five routes individually. Endpoints here meet the *actual top surface* of the same chip,
 # whose interior channels are not visible/verified. Do not misdescribe floating torus as a drilled port.
 for i in range(5):
  x=.62+i*.63;dst=(-1.62+i*.20,-.65,.205)
  remove(f'External_fluid_tube_{i}');remove(f'Chip_inlet_{i}');remove(f'Chip_outlet_{i}')
  # exterior nozzle/hub is a continuous tube at the visible syringe working end
  r.cyl(f'Fluid_luer_sleeve_{i}',(x,.13,.85),.052,.12,'metal',axis='Y',evidence='assumption')
  rr=r.route(f'External_fluid_tube_{i}',[(x,.07,.85),(x,-.15,.87),(x-.18,-.43,.90),(-1.6+i*.20,-.43,.59),dst],.024,'blue','text-supported')
  rr['visible_terminus']='chip exterior upper wall; ingress/opening NOT VERIFIED'
  # We do not claim a perforation in the solid chip; endpoint appears supported without a floating annulus.
  reclass(rr,'v01 floating annular port removed; path to outside wall only; internal fluid topology remains unknown')
 sc=bpy.context.scene;sc['v02_limitation']='Five tubes end on exterior chip face; no proof of internal channel openings, sealing, or usable flow.'
 r.camera((5.6,-7.4,8.2),(.05,-.20,.47),8.5)


def sensor_power():
 glass_fix();old=bpy.data.objects.get('Upper_silicone_skin')
 if not old:raise RuntimeError('missing upper skin')
 # A real modeled opening, not a black decal; two mesh bars bound the PV aperture.
 mod=old.modifiers.new('PV_window_boolean','BOOLEAN');mod.operation='DIFFERENCE'
 bpy.ops.mesh.primitive_cube_add(size=1,location=(0,0,1.56));cut=bpy.context.object;cut.name='Temporary_PV_window_cutter';cut.dimensions=(1.53,1.02,.5)
 bpy.ops.object.transform_apply(location=False,rotation=False,scale=True);bpy.context.view_layer.update();mod.object=cut
 bpy.context.view_layer.objects.active=old;bpy.ops.object.modifier_apply(modifier=mod.name);bpy.data.objects.remove(cut,do_unlink=True)
 old['revision_reason']='v01 solid silicone blocked paper Fig3a PV cell; v02 editable opening mesh'
 # second window is separately justified by schematic but its exact shape unknown
 sc=bpy.context.scene;sc['v02_limitation']='PV visible through mesh cut; neither sealed encapsulation nor internal electric connectivity checked.'
 r.camera((4.4,-6.5,6.0),(0,0,.65),6.5)

FIX={'04_microfluidics':microfluidics,'15_biomed_energy':sensor_power}
if __name__=='__main__':
 args=sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else []
 if len(args)!=1 or args[0] not in FIX:raise SystemExit('usage: blender -b v01/scene.blend --python revise_cases.py -- 04_microfluidics|15_biomed_energy')
 case=args[0];FIX[case]();bpy.context.view_layer.update()
 out=ROOT/'cases'/case/'v02';out.mkdir(exist_ok=True)
 bpy.context.scene['revision_version']='v02';bpy.context.scene['visual_review']='pending';bpy.context.scene['revision_target']=case
 bpy.ops.wm.save_as_mainfile(filepath=str(out/'scene.blend'))
 print('V02_SAVED',case,str(out/'scene.blend'),flush=True)
