import bpy, mathutils
bpy.ops.wm.open_mainfile(filepath="render-output/scene_v9.blend")
scene=bpy.context.scene
deps=bpy.context.evaluated_depsgraph_get()
CLK_HOLE_X=0.0; CLK_TOP_Z=0.075-0.0015
# clock_top_hole 中心 = (0, 0, CLK_TOP_Z). 用固定坐标查 cam_port_top 视锥
cam=bpy.data.objects['cam_port_top']; lens=cam.data.lens; SW=18.0
for tgt in ['dichroic_mir']:
    o=bpy.data.objects[tgt]; b=[o.matrix_world @ mathutils.Vector(c) for c in o.bound_box]
    lo=mathutils.Vector((min(v[i] for v in b) for i in range(3)))
    hi=mathutils.Vector((max(v[i] for v in b) for i in range(3)))
    c=(lo+hi)/2
    p=cam.matrix_world.inverted() @ c
    nx=(p.x/abs(p.z))*(lens/SW*0.5); ny=(p.y/abs(p.z))*(lens/(SW*9/16)*0.5)
    print(f"cam_port_top -> {tgt}: 中心 nx={nx:+.2f} ny={ny:+.2f} in_frame={abs(nx)<0.5 and abs(ny)<0.5}")
# 顶壁开孔中心(0,0,CLK_TOP_Z) 是否也在 cam_port_top 视锥
for pt,lab in [((CLK_HOLE_X,0,CLK_TOP_Z),"顶壁开孔中心"),
               ((CLK_HOLE_X,0,AXIS_Z:=0.020),"晶格轴上镜面中心 z")]:
    p=cam.matrix_world.inverted() @ mathutils.Vector(pt)
    if p.z>0: print(f"cam_port_top -> {lab}: BEHIND"); continue
    nx=(p.x/abs(p.z))*(lens/SW*0.5); ny=(p.y/abs(p.z))*(lens/(SW*9/16)*0.5)
    print(f"cam_port_top -> {lab}: nx={nx:+.2f} ny={ny:+.2f} in_frame={abs(nx)<0.5 and abs(ny)<0.5}")
# 铜腔全结构是否完整在 cam_cavo 视锥内(右端不岀框)
cam=bpy.data.objects['cam_cavo']; lens=cam.data.lens
for tgt in ['cav_outer','ap_ring','interrogation_vol','sapph_flange','sapph_window']:
    o=bpy.data.objects.get(tgt)
    if not o: print(f"cam_cavo -> {tgt}: 对象缺失"); continue
    b=[o.matrix_world @ mathutils.Vector(c) for c in o.bound_box]
    nx_list=[]
    for v in [b[i] for i in range(8)]:
        p=cam.matrix_world.inverted() @ v
        if p.z>0: nx_list.append('BEHIND'); continue
        nx_list.append(round((p.x/abs(p.z))*(lens/SW*0.5),2))
    nx_vals=[x for x in nx_list if isinstance(x,float)]
    if nx_vals:
        inall=all(abs(x)<0.5 for x in nx_vals)
        print(f"cam_cavo -> {tgt}: 8角nx范围=[{min(nx_vals)},{max(nx_vals)}] 全部入框={inall}")
    else:
        print(f"cam_cavo -> {tgt}: 全部 BEHIND CAMERA")
