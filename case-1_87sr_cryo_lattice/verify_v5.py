import bpy, mathutils
bpy.ops.wm.open_mainfile(filepath="render-output/scene_v5.blend")
scene=bpy.context.scene

def bb(name):
    o=bpy.data.objects.get(name)
    if not o: return None
    bb=[o.matrix_world @ mathutils.Vector(c) for c in o.bound_box]
    lo=mathutils.Vector((min(v[i] for v in bb) for i in range(3)))
    hi=mathutils.Vector((max(v[i] for v in bb) for i in range(3)))
    return lo,hi

print("=== 1. 穿墙检查：光束/光纤 与 vac_shell 金属壁的相交关系 ===")
lo,hi=bb('vac_shell')
print(f"vac_shell bbox: x[{lo.x:+.3f},{hi.x:+.3f}] y[{lo.y:+.3f},{hi.y:+.3f}] z[{lo.z:+.3f},{hi.z:+.3f}]")
for k in ['lat_fiber_out','lat_fiber_flange','lat_fiber_in','clock_bm','cool_bm_1','cool_bm_2','cool_bm_3','cool_bm_4','lat_beam_1','lat_beam_2']:
    r=bb(k)
    if not r: print(f"{k}: MISSING"); continue
    lo2,hi2=r
    # 对象是否与真空室实体壁相交（粗略：对象包围盒是否伸入 shell 包围盒内部但没穿过开孔区）
    in_shell = (lo2.x < hi.x and hi2.x > lo.x and lo2.y < hi.y and hi2.y > lo.y and lo2.z < hi.z and hi2.z > lo.z)
    print(f"  {k:16s} x[{lo2.x:+.3f},{hi2.x:+.3f}] y[{lo2.y:+.3f},{hi2.y:+.3f}] z[{lo2.z:+.3f},{hi2.z:+.3f}]  in_shell_bbox={in_shell}")

print("\n=== 2. 冷却光束交点是否统一到 (MOT_X=0, 0, AXIS_Z=0.02) ===")
for k in ['cool_bm_1','cool_bm_2','cool_bm_3','cool_bm_4']:
    lo,hi=bb(k)
    c=(lo+hi)/2
    d=mathutils.Vector((abs(c.x-0.0),abs(c.y-0.0),abs(c.z-0.020)))
    print(f"  {k:10s} 中点={[round(v,3) for v in c]}  偏离(0,0,0.020)={round(d.length,4)} m")

print("\n=== 3. 铜腔剖切是否生效（cav_outer 是否缺了 -y 侧 1/4） ===")
lo,hi=bb('cav_outer')
print(f"  cav_outer bbox x[{lo.x:+.3f},{hi.x:+.3f}] y[{lo.y:+.3f},{hi.y:+.3f}] z[{lo.z:+.3f},{hi.z:+.3f}]")
# 剖切前 y 范围应对称 ±0.0065；剖切后 -y 侧应明显变小
o=bpy.data.objects['cav_outer']
ymins=[ (o.matrix_world @ mathutils.Vector(v.co)).y for v in o.data.vertices ]
print(f"  cav_outer 实际顶点 y 范围: [{round(min(ymins),4)}, {round(max(ymins),4)}]（若 -y 端明显小于 +y 端则剖切生效）")

print("\n=== 4. 相机视锥（cam_overview 保留 v4 的 40mm 总览） ===")
SW=18.0
for cam_name in ['cam_overview','cam_cut','cam_port_right','cam_port_top']:
    cam=bpy.data.objects[cam_name]
    for tgt in ['mot_coil_L','mot_coil_R','cav_outer','ap_ring','sapph_window']:
        lo,hi=bb(tgt)
        if not lo: continue
        c=(lo+hi)/2
        m=cam.matrix_world.inverted()
        p=m @ c
        if p.z>0:
            print(f"  {cam_name} -> {tgt}: BEHIND"); continue
        nx=(p.x/abs(p.z))*(cam.data.lens/SW*0.5)
        ok=abs(nx)<0.5
        print(f"  {cam_name} -> {tgt:14s} nx={nx:+.2f} in_x={ok}")
