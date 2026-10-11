#!/usr/bin/env python3
"""Three cropped material-only renders of the SAME frozen v10 scene and camera.
Internal crop renderer invoked by compare_case2_v10_beam_material.py.
Only writes three temporary cropped tiles. No .blend/overview is overwritten.
Weights below are illustrative display proposals, NOT optical measurements or
an assertion that 1064 nm appears visibly red.
"""
import bpy, os
from pathlib import Path
from bpy_extras.object_utils import world_to_camera_view

BASE=Path(__file__).resolve().parent
SOURCE=BASE/'render-output'/'scene_case2_v10_overview.blend'
TILE_DIR=Path(os.environ['CASE2_COMPARE_TILE_DIR'])
assert TILE_DIR.is_dir(), 'temporary output directory is required' 
bpy.ops.wm.open_mainfile(filepath=str(SOURCE))
scene=bpy.context.scene
cam=scene.camera
assert cam is not None and cam.name=='overview_camera'
material=bpy.data.materials['1064nm_schematic_red_not_visible_light']
nodes=material.node_tree.nodes
clear=next(n for n in nodes if n.bl_idname=='ShaderNodeBsdfTransparent')
emission=next(n for n in nodes if n.bl_idname=='ShaderNodeEmission')
mix=next(n for n in nodes if n.bl_idname=='ShaderNodeMixShader')
assert all(c>0.999 for c in clear.inputs['Color'].default_value[:3])
# Iris2→L6→L7→Holder includes two real saved-scene lens meshes; both are
# present in EVERY crop. Compute a fixed camera border from their positions.
parts=('Iris2','L6','L7','Holder')
projected={name:world_to_camera_view(scene,cam,bpy.data.objects[name].location)
           for name in parts}
assert all(0<p.x<1 and 0<p.y<1 for p in projected.values())
x0=max(0,min(p.x for p in projected.values())-.057)
x1=min(1,max(p.x for p in projected.values())+.057)
y0=max(0,min(p.y for p in projected.values())-.105)
y1=min(1,max(p.y for p in projected.values())+.105)
assert x1-x0>.45 and y1-y0>.30
scene.render.use_border=True
scene.render.use_crop_to_border=True
scene.render.border_min_x=x0;scene.render.border_max_x=x1
scene.render.border_min_y=y0;scene.render.border_max_y=y1
scene.render.resolution_percentage=150  # enlarge the SAME optics/camera for thin-ray comparison
scene.cycles.samples=20
scene.render.image_settings.file_format='PNG'
scene.render.image_settings.color_mode='RGB'
# Strength compensates modestly for varying weights; no blown-out bloom/glare.
# Transparent BSDF stays neutral white in all three, so it does not filter
# underlying devices to dark red. At 1.0 the candidate is intentionally opaque.
variants=((.6,.90),(.8,.70),(1.0,.56))
for index,(weight,strength) in enumerate(variants):
    mix.inputs[0].default_value=weight
    clear.inputs['Color'].default_value=(1,1,1,1)
    emission.inputs['Color'].default_value=(1.0,.002,.001,1)
    emission.inputs['Strength'].default_value=strength
    file=TILE_DIR/f'crop_{index}.png'
    scene.render.filepath=str(file)
    bpy.ops.render.render(write_still=True)
    assert file.exists() and file.stat().st_size>1000
    print('CROP',index,'weight',weight,'emission',strength,
          'camera',cam.name,'border',tuple(round(x,4) for x in (x0,x1,y0,y1)),flush=True)
print('TILES_COMPLETE',TILE_DIR,flush=True)
