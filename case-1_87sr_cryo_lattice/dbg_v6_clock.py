import bpy, mathutils
bpy.ops.wm.open_mainfile(filepath="render-output/scene_v6.blend")
scene=bpy.context.scene
deps=bpy.context.evaluated_depsgraph_get()
def bb(name):
    o=bpy.data.objects.get(name)
    if not o: return None
    b=[o.matrix_world @ mathutils.Vector(c) for c in o.bound_box]
    lo=mathutils.Vector((min(v[i] for v in b) for i in range(3)))
    hi=mathutils.Vector((max(v[i] for v in b) for i in range(3)))
    return lo,hi
for k in ['clock_bm','clock_bm_3','dichroic_mir']:
    r=bb(k)
    if r:
        lo,hi=r
        print(f"{k:14s} x[{lo.x:+.4f},{hi.x:+.4f}] y[{lo.y:+.4f},{hi.y:+.4f}] z[{lo.z:+.4f},{hi.z:+.4f}]")
# 铜腔入口 CAV_X+0.005 = -0.075 (CAV_X=-0.080)
print("\nCLK_HOLE_X=0.010, CLK_TOP_Z =", 0.0+0.075-0.0015, "≈ 顶壁中心")
print("CLK_IRRIG_X = CAV_X+0.005 =", -0.080+0.005)
# clock_bm 从 (0.010, 0, CLK_TOP_Z+0.030) 到 (CLK_IRRIG_X=-0.075, 0, AXIS_Z=0.02)
# 中点 x = (0.010-0.075)/2 = -0.0325  ✓ 与实测一致
print("clock_bm 中点 x 应为 (0.010 + (-0.075))/2 =", (0.010-0.075)/2, "(斜线入射段，x 从 +0.010 斜降到 -0.075，合理)")
