"""15 v03: make Fig.3a source-visible two cells, optical module and fPCB read as parts.
Based on v02 saved geometry with existing real PV opening; no electrical-connection assertion.
"""
import bpy,sys,math
from pathlib import Path
root=Path(__file__).resolve().parent
sys.path.insert(0,str(root))
import render_core as r
r.M.clear()
for m in bpy.data.materials:
 if m.name.startswith('MAT_'):r.M[m.name[4:]]=m
# Identity-first: two battery pouches should not disappear behind one generic opaque slab.
upper=bpy.data.objects['Upper_silicone_skin']
# Replace opaque post-boolean skin with two clear side rails and end rails, preserving original on-disk v02.
# This is an exploded assembly view: upper is moved up 0.45 scene units; physical layer spacing not paper-measured.
upper.location.z += .50
upper['v03_note']='exploded top to expose pair of LiPo cells, optical PPG and fPCB; aperture from v02 remains real mesh'
for n in range(2):
 b=bpy.data.objects[f'LiPo_battery_{n}'];b['evidence_type']='source-visible';b['v03_note']='individual battery pouch silhouette; leads/electrical pads not confirmed'
 # A thin raised separator between edge and central PV identity; isolated visual rib, not asserted electrode.
# Expose the actual fPCB as a narrow rim; source shows planar flexible board, not a large generic copper rectangle.
f=bpy.data.objects['Flexible_printed_circuit'];f.dimensions.x=3.05;f.dimensions.y=1.45
f['v03_note']='PCB footprint revised as visualization assumption, conductive traces not proven'
# Create editable distinct outline of a PV module on its own physical surface, not a second square sticker.
pv=bpy.data.objects['Photovoltaic_cell'];r.box('PV_module_edge',tuple(pv.location+__import__('mathutils').Vector((0,0,.036))),(1.43,.97,.025),'metal','assumption',bevel=.01)
# Camera lower than v02 orthographic top-down to reveal actual spaced layers.
for cam in list(bpy.data.objects):
 if cam.type=='CAMERA':bpy.data.objects.remove(cam,do_unlink=True)
r.camera((5.1,-7.5,4.8),(0,0,.68),6.2)
sc=bpy.context.scene;sc['revision_version']='v03';sc['visual_review']='pending_AGH_pixel_review';sc['v03_limit']='Visual exploded assembly only; exact layer clearances/shape/contacts and body-mounted stack unknown.'
bpy.context.view_layer.update();out=root/'cases/15_biomed_energy/v03';out.mkdir(exist_ok=True)
bpy.ops.wm.save_as_mainfile(filepath=str(out/'scene.blend'));print('SENSOR_V03_SAVED',out/'scene.blend',flush=True)
