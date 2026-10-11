import bpy, mathutils, math, bmesh
bpy.ops.wm.read_factory_settings(use_empty=True)
# 复刻 v11 后窗几何, 验证槽半径/深度是否消除 镜盘∩法兰铜环 实体相交
CAV_R_OUT=0.0065; CAV_R_IN=0.005; CAV_REAR_X=-0.160; AXIS_Z=0.020
SAP_TILT=math.radians(20); FR_HOLE_R=CAV_R_IN+0.0004
SAPH_R = FR_HOLE_R/math.cos(SAP_TILT)
SAP_CLEAR=0.0004; SAP_GROOVE_R=SAPH_R+SAP_CLEAR
SAP_GROOVE_DEPTH=0.0006/math.cos(SAP_TILT)+0.0003
def cyl(r,d,loc,rot=(0,math.radians(90),0)):
    bpy.ops.mesh.primitive_cylinder_add(radius=r,depth=d,location=loc,rotation=rot,vertices=48)
    o=bpy.context.object; return o
def cut(t,c):
    m=t.modifiers.new('b','BOOLEAN'); m.operation='DIFFERENCE'; m.object=c
    bpy.context.view_layer.objects.active=t; bpy.ops.object.modifier_apply(modifier='b')
    bpy.data.objects.remove(c,do_unlink=True)
fl = cyl(CAV_R_OUT+0.001,0.004,(CAV_REAR_X,0,AXIS_Z))
cut(fl, cyl(FR_HOLE_R,0.006,(CAV_REAR_X,0,AXIS_Z)))
cut(fl, cyl(SAP_GROOVE_R,SAP_GROOVE_DEPTH,(CAV_REAR_X+0.002,0,AXIS_Z)))
# 镜盘: 半径 SAPH_R, 厚 0.6mm, 倾斜, 向腔内偏移 0.8mm
bpy.ops.mesh.primitive_cylinder_add(radius=SAPH_R,depth=0.0006,
    location=(CAV_REAR_X+0.0008,0,AXIS_Z),rotation=(0,math.radians(90)+SAP_TILT,0),vertices=48)
sw=bpy.context.object
# 交集
t1=bpy.data.objects.new('a',sw.data.copy()); bpy.context.scene.collection.objects.link(t1); t1.matrix_world=sw.matrix_world
t2=bpy.data.objects.new('b',fl.data.copy()); bpy.context.scene.collection.objects.link(t2); t2.matrix_world=fl.matrix_world
md=t1.modifiers.new('b','BOOLEAN'); md.operation='INTERSECT'; md.object=t2
bpy.context.view_layer.objects.active=t1; bpy.ops.object.modifier_apply(modifier='b')
bm=bmesh.new(); bm.from_mesh(t1.data); vol=abs(bm.calc_volume()); bm.free()
print(f"镜盘∩法兰铜环 = {len(t1.data.vertices)} 顶点 {vol*1e9:.3f} mm³ (0=不穿模)")
# 投影覆盖
print(f"镜盘投影半宽={SAPH_R*math.cos(SAP_TILT)*1000:.2f}mm vs 通孔半径={FR_HOLE_R*1000:.2f}mm -> {'覆盖' if SAPH_R*math.cos(SAP_TILT)>=FR_HOLE_R else '不足'}")
print(f"槽半径={SAP_GROOVE_R*1000:.2f}mm 槽深={SAP_GROOVE_DEPTH*1000:.2f}mm; 镜盘外缘={SAPH_R*1000:.2f}mm 落入槽内")
