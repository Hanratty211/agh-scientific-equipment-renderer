import bpy, mathutils
bpy.ops.wm.open_mainfile(filepath="render-output/scene_v4.blend")
for k in ['sapph_window','ap_ring','cav_outer','interrogation_vol','dichroic_mir']:
    o=bpy.data.objects.get(k)
    if not o: print(k,'missing'); continue
    bb=[o.matrix_world @ mathutils.Vector(c) for c in o.bound_box]
    mn=mathutils.Vector((min(v[i] for v in bb) for i in range(3)))
    mx=mathutils.Vector((max(v[i] for v in bb) for i in range(3)))
    print(k,'bbox_min',[round(v,4) for v in mn],'bbox_max',[round(v,4) for v in mx])
