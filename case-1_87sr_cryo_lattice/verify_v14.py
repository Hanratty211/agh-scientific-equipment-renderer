import bpy, bmesh, mathutils
bpy.ops.wm.open_mainfile(filepath="render-output/scene_v14.blend")
scene=bpy.context.scene
def inter_mm3(oA,oB):
    tA=bpy.data.objects.new('tA', oA.data.copy()); scene.collection.objects.link(tA); tA.matrix_world=oA.matrix_world
    tB=bpy.data.objects.new('tB', oB.data.copy()); scene.collection.objects.link(tB); tB.matrix_world=oB.matrix_world
    md=tA.modifiers.new('b','BOOLEAN'); md.operation='INTERSECT'; md.object=tB; md.solver='EXACT'
    bpy.context.view_layer.objects.active=tA; bpy.ops.object.modifier_apply(modifier='b')
    bm=bmesh.new(); bm.from_mesh(tA.data); v=bm.calc_volume(); bm.free()
    bpy.data.objects.remove(tB,do_unlink=True); bpy.data.objects.remove(tA,do_unlink=True)
    return abs(v)*1e9
def axisdist(name, P):
    o=bpy.data.objects.get(name); p0=o.get('beam_p0'); p1=o.get('beam_p1')
    A=list(p0); B=list(p1)
    u=[B[i]-A[i] for i in range(3)]; w=[P[i]-A[i] for i in range(3)]
    uu=sum(x*x for x in u); uuw=sum(u[i]*w[i] for i in range(3)); t=uuw/uu
    cl=[A[i]+t*u[i] for i in range(3)]
    return sum((P[i]-cl[i])**2 for i in range(3))**0.5, t
MOT_C=(0.030,0.0,0.020)
print("=== 5 类证据核查 (对 saved scene_v14.blend 独立复算) ===")
print("[1] 交汇: 每束实际线段到 MOT_C")
for b in ['cool_bm_1','cool_bm_2','cool_bm_3','cool_bm_4']:
    d,t=axisdist(b,MOT_C); print(f"   {b}: 距离={d*1000:.4f}mm t={t:.3f} ({'包含' if 0<=t<=1 and d<5e-4 else '未包含'})")
print("[3] 实体相交: 光束∩{vac_shell,cav_outer,cuo_lining,mot_coil_L,mot_coil_R}")
for b in ['cool_bm_1','cool_bm_2','cool_bm_3','cool_bm_4']:
    o=bpy.data.objects[b]
    vols={t:inter_mm3(o,bpy.data.objects[t]) for t in ['vac_shell','cav_outer','cuo_lining','mot_coil_L','mot_coil_R']}
    print(f"   {b}: "+", ".join(f"{k}={v:.3f}" for k,v in vols.items()))
print("[4] 安装接触: 后窗 承座前缘 vs 铜管端面 间隙 + 镜盘覆盖")
seat=bpy.data.objects['sapph_seat_ring']
sx=[seat.matrix_world @ mathutils.Vector(v.co) for v in seat.data.vertices]
front=max(v.x for v in sx)
print(f"   承座前缘 x={front*1000:.3f}mm 铜管端面 x={-0.160*1000:.1f}mm 间隙={(front+0.160)*1000:.3f}mm")
disc=bpy.data.objects['sapph_window']
dv=disc.matrix_world.inverted() @ mathutils.Vector((disc.matrix_world @ mathutils.Vector((disc.data.vertices[0].co)) ).to_tuple())
proj=disc.data.vertices[0].co
import math
R=0.0054; tilt=math.radians(20)
print(f"   镜盘投影半宽={R*math.cos(tilt)*1000:.2f}mm vs 通孔 5.00mm (>=才关闭开口)")
print("   承座∩cav_outer=%.3f 承座∩cuo_lining=%.3f 镜盘∩cav_outer=%.3f (全应0)"%(inter_mm3(seat,bpy.data.objects['cav_outer']),inter_mm3(seat,bpy.data.objects['cuo_lining']),inter_mm3(disc,bpy.data.objects['cav_outer'])))
print("[5] 实际图片: 8 张 v14 预览 + 蒙太奇, PNG 像素清晰度待人工核查(agent 无法自证)")
import os
for f in ['render_v14_prev_overview','render_v14_prev_cavity','render_v14_prev_rear_window','render_v14_prev_mot_entrance','render_v14_prev_top_hole','render_v14_prev_top_mirror','render_v14_prev_right','render_v14_prev_left_conn']:
    p=f"render-output/{f}.png"; print(f"   {f}.png {'存在' if os.path.exists(p) else '缺失'}")
