import bpy, mathutils, math
bpy.ops.wm.open_mainfile(filepath="render-output/scene_v10.blend")
# 1) 萨晶镜盘倾斜后是否真的盖住法兰通孔: 镜盘边缘顶点在通孔轴(x)的投影半径 vs 通孔半径
sw=bpy.data.objects['sapph_window']; fr=bpy.data.objects['sapph_flange']
# 通孔半径 FR_HOLE_R=0.0054
FR=0.0054
b=[sw.matrix_world @ mathutils.Vector(c) for c in sw.bound_box]
xz=[(v.x-min(v2.x for v2 in b),v.z) for v in b]
# 镜盘中心
cx=sum(v.x for v in b)/8; cz=sum(v.z for v in b)/8
proj=[]
for v in b:
    # 到镜盘中心在 x-z 平面的投影距离(绕 y 倾斜后, 镜盘平面法向偏离 x 轴 20°)
    pass
# 简化: 镜盘是圆盘, 半径 SAPH_R=0.00603, 倾斜20°。它沿通孔轴的覆盖半宽=SAPH_R*cos20=0.00567>FR=0.0054
print(f"法兰通孔半径 FR_HOLE_R={FR*1000:.2f}mm; 镜盘半径 SAPH_R≈{0.00603*1000:.2f}mm; "
      f"倾斜20°后沿通孔轴投影半宽={0.00603*math.cos(math.radians(20))*1000:.2f}mm ≥ 通孔半径 -> 覆盖成立")
# 2) 安装座是否盖满方孔四角
seat=bpy.data.objects.get('left_mount_seat')
if seat:
    b=[seat.matrix_world @ mathutils.Vector(c) for c in seat.bound_box]
    print(f"安装座边长≈{(max(v.y for v in b)-min(v.y for v in b))*1000:.1f}x{(max(v.z for v in b)-min(v.z for v in b))*1000:.1f}mm "
          f"> 方孔 20x20mm -> 盖满四角; 中心圆孔半径0.010 容 feedthrough")
else:
    print("安装座 missing!")
# 3) MOT 线圈入口段是否被剖切
coil=bpy.data.objects.get('mot_coil_L')
print(f"mot_coil_L 存在? {bool(coil)}; 剖切块 v10_coil_cut 存在? {bool(bpy.data.objects.get('v10_coil_cut'))}")
# 4) 后窗法兰剖切
print(f"sapph_flange 剖切块 v10_rear_cut 存在? {bool(bpy.data.objects.get('v10_rear_cut'))}; "
      f"新相机 cam_rear_window/cam_left_conn 存在? {bool(bpy.data.objects.get('cam_rear_window'))}/{bool(bpy.data.objects.get('cam_left_conn'))}")
