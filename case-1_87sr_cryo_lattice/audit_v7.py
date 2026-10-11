import bpy, mathutils
bpy.ops.wm.open_mainfile(filepath="render-output/scene_v7.blend")
scene=bpy.context.scene
deps=bpy.context.evaluated_depsgraph_get()
SW=18.0
def bb(name):
    o=bpy.data.objects.get(name)
    if not o: return None
    b=[o.matrix_world @ mathutils.Vector(c) for c in o.bound_box]
    lo=mathutils.Vector((min(v[i] for v in b) for i in range(3)))
    hi=mathutils.Vector((max(v[i] for v in b) for i in range(3)))
    return lo,hi
def frustum(camo, ctr):
    cam=bpy.data.objects[camo]; lens=cam.data.lens
    m=cam.matrix_world.inverted(); p=m @ ctr
    if p.z>0: return "BEHIND",None
    nx=(p.x/abs(p.z))*(lens/SW*0.5); ny=(p.y/abs(p.z))*(lens/(SW*9/16)*0.5)
    return ("IN" if abs(nx)<0.5 and abs(ny)<0.5 else "OUT"), (round(nx,2),round(ny,2))
def occlude(camo, ctr):
    cam=bpy.data.objects[camo]
    d=(ctr-cam.location).normalized()
    hit,loc,nrm,idx,ob,_=scene.ray_cast(deps, cam.location, d)
    return ob.name if ob else None

for camo,tgt in [
    ('cam_cavo','interrogation_vol'),
    ('cam_cavo','ap_ring'),
    ('cam_cavo','sapph_window'),
    ('cam_port_right','lat_fiber_flange'),
    ('cam_port_top','dichroic_mir'),
    ('cam_port_top','clock_bm'),
    ('cam_left_port','left_feedthrough'),
]:
    r=bb(tgt)
    if not r: print(f"{camo} -> {tgt}: 对象缺失"); continue
    lo,hi=r; c=(lo+hi)/2
    st,nd=frustum(camo,c)
    first=occlude(camo,c)
    print(f"{camo:14s} -> {tgt:16s} frustum={st} ndc={nd}  ray_first_hit='{first}'  target_ctr={[round(v,3) for v in c]}")
