import bpy, mathutils
bpy.ops.wm.open_mainfile(filepath="render-output/scene_v5.blend")
def bb(name):
    o=bpy.data.objects.get(name)
    bb=[o.matrix_world @ mathutils.Vector(c) for c in o.bound_box]
    lo=mathutils.Vector((min(v[i] for v in bb) for i in range(3)))
    hi=mathutils.Vector((max(v[i] for v in bb) for i in range(3)))
    return lo,hi

print("=== 铜腔左端是否穿过 vac_shell 左壁 ===")
lo,hi=bb('vac_shell')
print("vac_shell x range: [%+.3f, %+.3f]" % (lo.x,hi.x))
lo2,hi2=bb('cav_outer')
print("cav_outer x range: [%+.3f, %+.3f]" % (lo2.x,hi2.x))
print("cav left end (%.3f) < shell left wall (%.3f)? %s" % (lo2.x, lo.x, lo2.x < lo.x))

print("\n=== 冷却光束 +-z 对是否穿顶/底壁 ===")
lo,hi=bb('vac_shell')
print("vac_shell z range: [%+.3f, %+.3f]" % (lo.z,hi.z))
for k in ['cool_bm_3','cool_bm_4']:
    lo2,hi2=bb(k)
    top = hi2.z > hi.z - 0.003
    bot = lo2.z < lo.z + 0.003
    print("%s: z in [%+.3f,%+.3f]  穿顶壁=%s 穿底壁=%s" % (k,lo2.z,hi2.z,top,bot))

print("\n=== 开孔与光纤/光轴对齐 ===")
lo,hi=bb('lat_fiber_flange')
print("lat_fiber_flange z center = %.4f (光轴 AXIS_Z=0.020, 应一致才算对齐)" % ((lo.z+hi.z)/2))
lo2,hi2=bb('clock_bm')
print("clock_bm 起点应位于顶部窗口开孔中心上方, 其 z range [%+.3f,%+.3f]" % (lo2.z,hi2.z))
