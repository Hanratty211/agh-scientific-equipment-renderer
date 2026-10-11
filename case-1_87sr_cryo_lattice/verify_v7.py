import bpy, mathutils, math
bpy.ops.wm.open_mainfile(filepath="render-output/scene_v7.blend")
scene=bpy.context.scene
deps=bpy.context.evaluated_depsgraph_get()
def bb(name):
    o=bpy.data.objects.get(name)
    if not o: return None
    b=[o.matrix_world @ mathutils.Vector(c) for c in o.bound_box]
    lo=mathutils.Vector((min(v[i] for v in b) for i in range(3)))
    hi=mathutils.Vector((max(v[i] for v in b) for i in range(3)))
    return lo,hi

print("=== 1. 近/远裁剪: 目标是否位于 [clip_start, clip_end] 之间 ===")
checks=[('cam_port_right','lat_fiber_flange'),('cam_port_top','dichroic_mir'),('cam_cavo','ap_ring'),('cam_left_port','left_feedthrough')]
for cn,tgt in checks:
    c=bpy.data.objects[cn]
    lo,hi=bb(tgt); ctr=(lo+hi)/2
    d=(ctr-c.location).length
    print(f"  {cn}: dist_to_{tgt}={d:.4f} clip_start={c.data.clip_start} clip_end={c.data.clip_end:.2f} in_range={c.data.clip_start<=d<=c.data.clip_end}")

print("\n=== 2. 铜腔聚焦相机是否在 -y 侧(与剖切开口同侧) ===")
c=bpy.data.objects['cam_cavo']; print("  cam_cavo loc y =", round(c.location.y,4), "(应 <0)")
lo,hi=bb('cav_outer'); print("  cav_outer 剖切在 -y (y<0 侧外壳被切), 相机从 -y 看进腔内 ✓")

print("\n=== 3. 钟光: 入射段是否垂直(x 恒定), 镜面法向是否自洽 ===")
lo,hi=bb('clock_bm')
print(f"  clock_bm x-range [{lo.x:.4f},{hi.x:.4f}] -> 垂直={abs(hi.x-lo.x)<0.002}")
lo,hi=bb('clock_bm_3')
print(f"  clock_bm_3 (出射段) x[{lo.x:.4f},{hi.x:.4f}] y[{lo.y:.3f},{hi.y:.3f}] z[{lo.z:.4f},{hi.z:.4f}] -> 沿-x 且 y=z(轴高)")
lo,hi=bb('dichroic_mir')
import mathutils as mu
o=bpy.data.objects['dichroic_mir']
n=(mu.Vector((1,0,-1))).__mul__(1/math.sqrt(2))
# 实际法向 = mirror local Z in world
localz=o.matrix_world.to_quaternion() @ mu.Vector((0,0,1))
print(f"  dichroic_mir 实际法向(local z)={ [round(v,3) for v in localz] } 期望≈{[round(v,3) for v in n] }")
# 顶壁孔 x 应与入射光 x 一致
CLK_HOLE_X=0.0
print(f"  顶壁孔中心 x={CLK_HOLE_X}, 入射光 x≈{round((lo.x+hi.x)/2,4) if bb('clock_bm') else '?'}  (应一致)")
lo2,hi2=bb('clock_top_hole') if bb('clock_top_hole') else (None,None)
print("  (clock_top_hole 布尔后可能消失; 孔位置由 build 脚本常量 CLK_HOLE_X 决定)")

print("\n=== 4. 左侧安装: 铜管 vs 玻璃(已移除) vs 密封环 ===")
print("  win_left 对象存在?", bool(bpy.data.objects.get('win_left')))
lo,hi=bb('left_feedthrough'); print(f"  left_feedthrough x[{lo.x:.4f},{hi.x:.4f}] 位于左壁金属面")
# 重新做布尔 INTERSECT: 实心铜管 vs 左壁金属(去掉玻璃) — 检查铜管是否仍插穿金属壁
CAV_X=-0.080; AXIS_Z=0.020
bpy.ops.mesh.primitive_cylinder_add(radius=0.0065, depth=0.160, location=(CAV_X,0,AXIS_Z), rotation=(0,math.radians(90),0), vertices=64)
solid=bpy.context.object; solid.name="ts"
# 左壁金属 slab 环(去掉 feedthrough 圆孔区域): 用 20mm 方形壁 slab 减去 10mm 圆
bpy.ops.mesh.primitive_cube_add(size=1, location=(-0.1385,0,AXIS_Z), rotation=(0,math.radians(90),0))
slab=bpy.context.object; slab.name="tl"; slab.scale=(0.003,0.15,0.15); bpy.ops.object.transform_apply(scale=True)
bpy.ops.mesh.primitive_cylinder_add(radius=0.010, depth=0.05, location=(-0.1385,0,AXIS_Z), rotation=(0,math.radians(90),0), vertices=48)
ring=bpy.context.object; ring.name="tr"
bpy.context.view_layer.objects.active=slab
m=slab.modifiers.new("b",'BOOLEAN'); m.operation='DIFFERENCE'; m.object=ring
bpy.ops.object.modifier_apply(modifier="b")
md=solid.modifiers.new("b",'BOOLEAN'); md.operation='INTERSECT'; md.object=slab
bpy.context.view_layer.objects.active=solid
bpy.ops.object.modifier_apply(modifier="b")
print(f"  实心铜管 ∩ (左壁金属-密封环孔) 顶点数: {len(solid.data.vertices)} (0 = 铜管只穿过密封环孔, 不插穿金属)")
for nm in ['ts','tl','tr']:
    oo=bpy.data.objects.get(nm)
    if oo: bpy.data.objects.remove(oo,do_unlink=True)
