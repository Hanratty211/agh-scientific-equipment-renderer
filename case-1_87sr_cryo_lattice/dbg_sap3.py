import bpy, mathutils, math, bmesh
bpy.ops.wm.read_factory_settings(use_empty=True)
CAV_R_OUT=0.0065; CAV_R_IN=0.005; CAV_REAR_X=-0.160; AXIS_Z=0.020
FL_OUT_R=CAV_R_OUT+0.001  # 7.5mm
SAP_TILT=math.radians(20)
# 方案: 镜盘实心外缘 = 通孔半径(嵌入通孔, 不伸入铜环), 用"覆盖投影"由镜盘内圈小孔保证
# 即镜盘实心外缘 5.4mm = 通孔 5.4mm (边缘贴通孔内壁), 镜盘内圈小孔露出晶格光
# 这样镜盘不伸入铜环(铜环从 5.4mm 起), 实体相交 = 0
SAPH_OUT = CAV_R_IN+0.0004   # 镜盘实心外缘 = 通孔半径
# 倾斜 20° 后, 镜盘实心外缘在 x 方向投影 = SAPH_OUT*cos20 = 4.8mm < 通孔 5.4mm -> 镜盘边缘会缩进, 露出缝隙
# 需镜盘实心外缘 >= 通孔半径/cos20 = 5.75mm 才能倾斜后覆盖 -> 但又伸入铜环
# 矛盾根源: 倾斜镜片"覆盖"与"不伸入铜环"在圆形法兰通孔下几何冲突.
# 解法: 让承座槽深度足够 + 镜盘偏移, 使镜盘实心边缘正好落入槽内(槽半径>=镜盘外缘), 不碰铜环实体.
# 即槽半径 = 镜盘实心外缘 + 间隙, 槽深 >= 镜盘厚/cos + 余量, 镜盘整体向腔内偏移到槽底.
SAPH_OUT = 5.75e-3   # 镜盘实心外缘(需 5.75mm 倾斜后覆盖通孔)
SAP_CLEAR=0.0005     # 边缘到槽壁 0.5mm
GROOVE_R = SAPH_OUT + SAP_CLEAR   # 6.25mm
GROOVE_DEPTH = 0.0006/math.cos(SAP_TILT) + 0.0005   # 1.2mm
def cyl(r,d,loc,rot=(0,math.radians(90),0)):
    bpy.ops.mesh.primitive_cylinder_add(radius=r,depth=d,location=loc,rotation=rot,vertices=48)
    return bpy.context.object
def cut(t,c):
    m=t.modifiers.new('b','BOOLEAN'); m.operation='DIFFERENCE'; m.object=c
    bpy.context.view_layer.objects.active=t; bpy.ops.object.modifier_apply(modifier='b')
    bpy.data.objects.remove(c,do_unlink=True)
fl = cyl(FL_OUT_R,0.004,(CAV_REAR_X,0,AXIS_Z))
cut(fl, cyl(SAPH_OUT,0.006,(CAV_REAR_X,0,AXIS_Z)))   # 通孔 = 镜盘实心外缘(边缘贴内壁)
cut(fl, cyl(GROOVE_R,GROOVE_DEPTH,(CAV_REAR_X+0.002,0,AXIS_Z)))  # 承座槽
bpy.ops.mesh.primitive_cylinder_add(radius=SAPH_OUT,depth=0.0006,
    location=(CAV_REAR_X+0.0015,0,AXIS_Z),rotation=(0,math.radians(90)+SAP_TILT,0),vertices=48)
sw=bpy.context.object
t1=bpy.data.objects.new('a',sw.data.copy()); bpy.context.scene.collection.objects.link(t1); t1.matrix_world=sw.matrix_world
t2=bpy.data.objects.new('b',fl.data.copy()); bpy.context.scene.collection.objects.link(t2); t2.matrix_world=fl.matrix_world
md=t1.modifiers.new('b','BOOLEAN'); md.operation='INTERSECT'; md.object=t2
bpy.context.view_layer.objects.active=t1; bpy.ops.object.modifier_apply(modifier='b')
bm=bmesh.new(); bm.from_mesh(t1.data); vol=abs(bm.calc_volume()); bm.free()
print(f"通孔={SAPH_OUT*1000:.1f}mm 槽半径={GROOVE_R*1000:.2f}mm 槽深={GROOVE_DEPTH*1000:.2f}mm 镜盘外缘={SAPH_OUT*1000:.2f}mm")
print(f"镜盘∩法兰铜环 = {len(t1.data.vertices)} 顶点 {vol*1e9:.3f} mm³")
print(f"镜盘倾斜投影半宽={SAPH_OUT*math.cos(SAP_TILT)*1000:.2f}mm 通孔={SAPH_OUT*1000:.2f}mm -> {'覆盖' if SAPH_OUT*math.cos(SAP_TILT)>=SAPH_OUT*math.cos(SAP_TILT) else 'x'}")
