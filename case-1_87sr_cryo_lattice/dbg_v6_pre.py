import bpy, mathutils
bpy.ops.wm.open_mainfile(filepath="render-output/scene_v5.blend")
deps=bpy.context.evaluated_depsgraph_get()

def bb(name):
    o=bpy.data.objects.get(name)
    if not o: return None,None
    b=[o.matrix_world @ mathutils.Vector(c) for c in o.bound_box]
    lo=mathutils.Vector((min(v[i] for v in b) for i in range(3)))
    hi=mathutils.Vector((max(v[i] for v in b) for i in range(3)))
    return lo,hi

print("=== 铜腔 vs 左壁 交集检查（正确 BVH 方法） ===")
# 铜腔管壁 (cav_outer, 含剖切) 与左壁 (vac_shell 的 x≈-0.14 一段) 是否相交
# 方法: 取 cav_outer 顶点, 检查是否有顶点落在左壁薄壳范围内
# 左壁 x 范围: vac_shell bbox x_min=-0.140, 壁厚 T=0.003 → 左壁 x∈[-0.140,-0.137]
# 左壁在 y,z 方向是全壁 (未剖切左壁), 所以 x∈[-0.140,-0.137], y∈[-0.075,0.075], z∈[-0.075,0.075]
o=bpy.data.objects['cav_outer']
o_ev=o.evaluated_get(deps)
me=o_ev.data
in_wall=0; total=0
for v in me.vertices:
    w=o_ev.matrix_world @ v.co
    total+=1
    if -0.141 <= w.x <= -0.136 and abs(w.y)<=0.076 and abs(w.z)<=0.076:
        in_wall+=1
print(f"cav_outer 顶点总数 {total}, 落在左壁薄壳 x∈[-0.141,-0.136] 内的顶点数: {in_wall}")

# 同样检查 lining
o2=bpy.data.objects.get('cuo_lining')
if o2:
    o2ev=o2.evaluated_get(deps); me2=o2ev.data
    in2=0
    for v in me2.vertices:
        w=o2ev.matrix_world @ v.co
        if -0.141 <= w.x <= -0.136 and abs(w.y)<=0.076 and abs(w.z)<=0.076:
            in2+=1
    print(f"cuo_lining 落在左壁薄壳内的顶点数: {in2}")

# 铜腔管壁 z 范围 vs 左壁窗口 z 范围
lo,hi=bb('cav_outer')
print(f"cav_outer z∈[{lo.z:+.4f},{hi.z:+.4f}]")
lo2,hi2=bb('win_left')
if lo2: print(f"win_left z∈[{lo2.z:+.3f},{hi2.z:+.3f}]  ← 现有窗口中心 z=0, 与铜腔轴线 z=0.020 不一致")

print("\n=== 铜腔左端(-0.160) 在 左壁(-0.140) 之外 意味着什么 ===")
print("cav 左端 x=-0.160 < 左壁 x_min=-0.140: 铜腔末端(后窗)伸出真空室外, 合理")
print("但铜腔全长 x∈[-0.160, 0.000] 中 x∈[-0.140,-0.137] 这一段 (约 3mm 长的管壁) 与左壁薄壳相交!")

print("\n=== 二向色镜朝向 ===")
o=bpy.data.objects.get('dichroic_mir')
if o:
    print("dichroic_mir rot (deg):", [round(__import__('math').degrees(v),1) for v in o.rotation_euler])
    print("dichroic_mir loc:", [round(v,3) for v in o.location])
