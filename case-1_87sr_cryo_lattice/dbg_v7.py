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
print("=== 1. camera clip settings ===")
for n in ['cam_port_right','cam_port_top','cam_cavo']:
    c=bpy.data.objects[n]
    tgt='lat_fiber_flange' if n=='cam_port_right' else ('ap_ring' if n=='cam_cavo' else None)
    if n=='cam_port_top':
        ctr=mathutils.Vector((0.010,0.0,0.075+0.030))  # clock hole top
    else:
        lo,hi=bb(tgt); ctr=(lo+hi)/2
    dist=(ctr-c.location).length
    print(f"{n}: clip_start={c.data.clip_start:.4f} target_depth={dist:.4f} -> CLIPPED={c.data.clip_start>dist}")
print("\n=== 3. clock light ACTUAL ===")
CLK_HOLE_X=0.010; CAV_X=-0.080
p0=mathutils.Vector((0.010,0,0.075+0.030)); p1=mathutils.Vector((CAV_X+0.005,0,0.020))
t=(0.075-p0.z)/(p1.z-p0.z); xcross=p0.x+(p1.x-p0.x)*t
print(f"beam crosses top wall(z=0.075) at x={xcross:.4f}; hole center x={CLK_HOLE_X}; offset={abs(xcross-CLK_HOLE_X)*1000:.1f}mm")
print("\n=== 4. left wall/glass/copper ===")
for k in ['cav_outer','win_left','sapph_window']:
    lo,hi=bb(k); print(f"{k:14s} x[{lo.x:+.4f},{hi.x:+.4f}] y[{lo.y:+.4f},{hi.y:+.4f}] z[{lo.z:+.4f},{hi.z:+.4f}]")
cav=bpy.data.objects['cav_outer'].evaluated_get(deps)
lo,hi=bb('win_left')
cnt=sum(1 for v in cav.data.vertices if lo.x<=(w:=cav.matrix_world @ v.co).x<=hi.x and lo.y<=w.y<=hi.y and lo.z<=w.z<=hi.z)
print(f"cav_outer vertices inside win_left glass slab: {cnt}")
