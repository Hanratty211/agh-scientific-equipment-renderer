import bpy
bpy.ops.wm.open_mainfile(filepath="render-output/scene_v16.blend")
print("cameras in scene_v16.blend:")
for o in bpy.data.objects:
    if o.type=='CAMERA':
        print("  ", o.name, [round(v,4) for v in o.location], "lens=",o.data.lens)
