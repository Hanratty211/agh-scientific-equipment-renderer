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
SW=18.0

print("=== 局部图视角: cam_cavo -> ap_ring 是否还被二向色镜挡 ===")
cam=bpy.data.objects['cam_cavo']
lo,hi=bb('ap_ring'); c=(lo+hi)/2
d=(c-cam.matrix_world.translation).normalized()
hit,loc,nrm,idx,ob,_=scene.ray_cast(deps, cam.matrix_world.translation, d)
print(f"  cam_cavo -> ap_ring: 先命中 '{ob.name if ob else None}'  目标中心={[round(v,3) for v in c]}")

print("\n=== cam_cavo 视锥: ap_ring/interrogation_vol/sapph_window/cav_outer ===")
lens=cam.data.lens
for tgt in ['ap_ring','interrogation_vol','sapph_window','cav_outer']:
    r=bb(tgt)
    if not r: print(f"  {tgt}: 对象缺失"); continue
    lo,hi=r; c=(lo+hi)/2
    m=cam.matrix_world.inverted(); p=m @ c
    if p.z>0: print(f"  cam_cavo -> {tgt}: BEHIND CAMERA"); continue
    nx=(p.x/abs(p.z))*(lens/SW*0.5)
    print(f"  cam_cavo -> {tgt:18s} nx={nx:+.2f} in_x={abs(nx)<0.5}")

print("\n=== cam_cavo 下无关线圈 ===")
for tgt in ['mot_coil_L','mot_coil_R']:
    r=bb(tgt)
    if not r: continue
    lo,hi=r; c=(lo+hi)/2
    m=cam.matrix_world.inverted(); p=m @ c
    if p.z>0:
        print(f"  cam_cavo -> {tgt}: BEHIND CAMERA (不入画)")
    else:
        nx=(p.x/abs(p.z))*(lens/SW*0.5)
        print(f"  cam_cavo -> {tgt}: nx={nx:+.2f} in_x={abs(nx)<0.5}")
