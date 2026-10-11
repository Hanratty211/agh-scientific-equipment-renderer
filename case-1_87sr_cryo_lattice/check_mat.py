import bpy
bpy.ops.wm.open_mainfile(filepath="render-output/scene_v16.blend")
m=bpy.data.materials.get("cool_win_cryo_glass")
if m:
    b=m.node_tree.nodes.get("Principled BSDF")
    print("cool_win_cryo_glass 输入:")
    for i in b.inputs:
        if i.name in ("Base Color","Roughness","Metallic","IOR","Transmission","Transmission Weight","Alpha"):
            try: print(f"  {i.name} = {i.default_value}")
            except: print(f"  {i.name} = {i.default_value[0]}...")
    # 实际用的名字
    print("所有可用输入名:", [i.name for i in b.inputs][:40])
else:
    print("材质缺失!")
# 确认 n/p 玻璃窗用的是 M_GLASS_CRYO
for wn in ["mot_opt_win_n","mot_opt_win_p"]:
    o=bpy.data.objects.get(wn)
    print(wn,"材质=",[s.material.name if s.material else None for s in o.material_slots])
# 共享 M_GLASS 未动
mg=bpy.data.materials.get("port_glass")
print("port_glass 仍在且未被改:", bool(mg))
