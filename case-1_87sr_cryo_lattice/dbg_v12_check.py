import bpy, mathutils, math, bmesh
bpy.ops.wm.read_factory_settings(use_empty=True)
CAV_R_IN=0.005; CAV_R_OUT=0.0065; CAV_REAR_X=-0.160; AXIS_Z=0.020
SAP_TILT=math.radians(20)
SAPH_OUT=CAV_R_IN; FR_HOLE_R=CAV_R_IN+0.0008
SAP_SEAT_OUT=FR_HOLE_R; SAP_SEAT_IN=CAV_R_IN; SAP_SEAT_DEPTH=0.0008
def cyl(r,d,loc,rot=(0,math.radians(90),0),m=None,seg=48,hole=None):
    bpy.ops.mesh.primitive_cylinder_add(radius=r,depth=d,location=loc,rotation=rot,vertices=seg)
    o=bpy.context.object
    if hole:
        bpy.ops.mesh.primitive_cylinder_add(radius=hole,depth=d+0.002,location=loc,rotation=rot,vertices=seg)
        h=bpy.context.object
        md=o.modifiers.new('b','BOOLEAN'); md.operation='DIFFERENCE'; md.object=h
        bpy.context.view_layer.objects.active=o; bpy.ops.object.modifier_apply(modifier='b')
        bpy.data.objects.remove(h,do_unlink=True)
    return o
def inter(a,b):
    t1=bpy.data.objects.new('A',a.data.copy()); bpy.context.scene.collection.objects.link(t1); t1.matrix_world=a.matrix_world
    t2=bpy.data.objects.new('B',b.data.copy()); bpy.context.scene.collection.objects.link(t2); t2.matrix_world=b.matrix_world
    md=t1.modifiers.new('b','BOOLEAN'); md.operation='INTERSECT'; md.object=t2
    bpy.context.view_layer.objects.active=t1; bpy.ops.object.modifier_apply(modifier='b')
    bm=bmesh.new(); bm.from_mesh(t1.data); v=abs(bm.calc_volume()); bm.free()
    bpy.data.objects.remove(t2,do_unlink=True); bpy.data.objects.remove(t1,do_unlink=True)
    return v*1e9, len(t1.data.vertices) if False else None
# 简: 铜管末端用管壁环近似(内径5外6.5), 内衬末端=内径5
def tube_end():
    return cyl(CAV_R_OUT,0.004,(CAV_REAR_X,0,AXIS_Z),hole=CAV_R_IN)  # cav_outer 末端近似
def lining_end():
    return cyl(CAV_R_IN,0.004,(CAV_REAR_X,0,AXIS_Z))  # cuo_lining 末端近似
fl=cyl(CAV_R_OUT+0.001,0.004,(CAV_REAR_X,0,AXIS_Z))
# 通孔
bpy.ops.mesh.primitive_cylinder_add(radius=FR_HOLE_R,depth=0.006,location=(CAV_REAR_X,0,AXIS_Z),rotation=(0,math.radians(90),0),vertices=48)
fh=bpy.context.object
md=fl.modifiers.new('b','BOOLEAN'); md.operation='DIFFERENCE'; md.object=fh
bpy.context.view_layer.objects.active=fl; bpy.ops.object.modifier_apply(modifier='b')
bpy.data.objects.remove(fh,do_unlink=True)
seat=cyl(SAP_SEAT_OUT,SAP_SEAT_DEPTH,(CAV_REAR_X+0.0006,0,AXIS_Z),hole=SAP_SEAT_IN)
bpy.ops.mesh.primitive_cylinder_add(radius=SAPH_OUT,depth=0.0006,
    location=(CAV_REAR_X+0.0018,0,AXIS_Z),rotation=(0,math.radians(90)+SAP_TILT,0),vertices=48)
sap=bpy.context.object
pairs=[('镜盘∩铜管末端(cav)',sap,tube_end()),
       ('镜盘∩内衬末端(cuo)',sap,lining_end()),
       ('镜盘∩法兰铜环',sap,fl),
       ('镜盘∩承座环',sap,seat),
       ('承座环∩法兰',seat,fl)]
for lab,a,b in pairs:
    v,n=inter(a,b)
    print(f"  {lab}: {v:.3f} mm³")
# 覆盖: 镜盘投影半宽
print(f"镜盘投影半宽={SAPH_OUT*math.cos(SAP_TILT)*1000:.2f}mm; 承座环外径={SAP_SEAT_OUT*1000:.2f}mm, 内径={SAP_SEAT_IN*1000:.2f}mm")
print(f"覆盖逻辑: 镜盘关闭中央开口(投影4.70mm<5.8通孔, 中央区); 承座环外径5.8mm盖住镜盘缘与通孔间环缝")
