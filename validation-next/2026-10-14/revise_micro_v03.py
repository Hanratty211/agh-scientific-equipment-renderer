"""Targeted 04 v03: repair v02 visual regression, add only Fig.3C left reservoirs.
Base v01 saved scene is used because v02 route revision was rejected after pixel review.
Outputs separate v03; does not overwrite v01/v02.
"""
import bpy,math,sys
from pathlib import Path
root=Path(__file__).resolve().parent
sys.path.insert(0,str(root))
import render_core as r
r.M.clear()
for m in bpy.data.materials:
 if m.name.startswith('MAT_'):r.M[m.name[4:]]=m
# A saved v01 blend omits unused material presets; restore only the new reservoir material.
if 'soft' not in r.M:
 mat=bpy.data.materials.new('MAT_soft_reservoir');mat.diffuse_color=(0.33,0.71,0.31,1);mat.use_nodes=True
 bsdf=mat.node_tree.nodes.get('Principled BSDF')
 if bsdf:bsdf.inputs['Base Color'].default_value=(0.33,0.71,0.31,1)
 r.M['soft']=mat

def remove(n):
 o=bpy.data.objects.get(n)
 if o:bpy.data.objects.remove(o,do_unlink=True)

# Source Fig3C: left outlet side has five green balloon reservoirs; exact internal seal unknown.
for i in range(5):
 x=.62+i*.63
 for prefix in ('External_fluid_tube_','Chip_inlet_','Chip_outlet_'):remove(prefix+str(i))
 y=-.73+i*.20
 # source-right connector axis aligns to physical chip edge y=-.56? This is still representative;
 # on 2D schematic right edge maps to +X side of real chip.
 chip_side=(-.42,y,.19)
 sleeve=r.cyl(f'Chip_exterior_Luer_{i}',(-.37,y,.19),.046,.19,'metal',axis='X',evidence='assumption')
 cable=r.route(f'External_syringe_to_chip_{i}',[(x,.13,.85),(x,-.22,.85),(x-.25,-.46,.73),(-.23,y,.23),chip_side],.025,'blue','source-visible')
 cable['unknown']='tube exterior contact only; no drilled channel demonstrated'
 # Fig.3C green balloon outlet on opposite (negative X) chip side, not a sixth pump.
 left=(-2.12,y,.20)
 r.cyl(f'Outlet_exterior_sleeve_{i}',(-2.05,y,.20),.045,.18,'metal',axis='X',evidence='assumption')
 r.route(f'Green_balloon_neck_{i}',[left,(-2.42,y,.20),(-2.69,y,.21)],.028,'blue','source-visible')
 r.cyl(f'Green_balloon_reservoir_{i}',(-2.98,y,.22),.09,.62,'soft',axis='X',evidence='source-visible')
# A note in scene expressly prevents port PASS claim.
bpy.context.scene['revision_version']='v03';bpy.context.scene['v03_limit']='Visual external Luer sleeves only; chip no real through bore. Ports and five flow routes NOT VALIDATED.'
r.camera((5,-7.8,7),(-.20,-.18,.47),8.8)
bpy.context.view_layer.update()
out=root/'cases/04_microfluidics/v03';out.mkdir(exist_ok=True)
bpy.ops.wm.save_as_mainfile(filepath=str(out/'scene.blend'))
print('V03_SAVED',out/'scene.blend')
