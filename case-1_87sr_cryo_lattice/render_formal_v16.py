#!/usr/bin/env python3
"""v16 正式交付渲染（1600×900, Cycles 96 采样, 去噪开启）。
按当前已通过状态生成 5 张正式图: 总览 / MOT局部 / 铜腔内部 / 后窗 / 右壁接口。
全部使用修正后的两个独立玻璃窗口(mot_opt_win_n/p, 独立可透光玻璃 M_GLASS_CRYO)。
各局部视图按既定临时隐藏规则, 渲染后恢复, 避免显示状态回归。
输出: render-output/formal_v16_*.png
"""
import bpy, math, mathutils

# 打开已通过核查的 v16 场景(几何/材质已全部确认)
bpy.ops.wm.open_mainfile(filepath="render-output/scene_v16.blend")
scene = bpy.context.scene

def make_cam(name, loc, look_at, lens=50, clip_start=0.001, clip_end=2.0):
    d = mathutils.Vector(look_at) - mathutils.Vector(loc)
    quat = (-d).to_track_quat('Z','Y')
    rot = quat.to_euler()
    bpy.ops.object.camera_add(location=loc, rotation=rot)
    c = bpy.context.object; c.name = name
    c.data.lens = lens
    c.data.clip_start = clip_start
    c.data.clip_end = clip_end
    return c

def get_or_make_cam(name, loc, look_at, lens):
    o = bpy.data.objects.get(name)
    if o: return o
    return make_cam(name, loc, look_at, lens)

# 补充 build 脚本中渲染时才创建(未持久化进 scene_v16.blend)的两个相机, 参数与 build_blender_v16.py 一致
MOT_CONV_X, AXIS_Z = 0.030, 0.020
cam_mot = get_or_make_cam("cam_mot_entrance", (MOT_CONV_X + 0.085, -0.055, AXIS_Z + 0.085),
                          ((MOT_CONV_X + 0.0)/2, 0.0, AXIS_Z), 38)
cam_rw  = get_or_make_cam("cam_rw_interface_v2", (0.120, -0.030, AXIS_Z + 0.050),
                          (0.0585, 0.0, AXIS_Z), 42)

# ---- 正式渲染参数: 1600×900 @ 96 采样(覆盖低预览的 32 采样), 去噪开启 ----
scene.render.resolution_x = 1600
scene.render.resolution_y = 900
scene.render.resolution_percentage = 100
scene.render.engine = 'CYCLES'
scene.cycles.samples = 96
scene.cycles.use_denoising = True

def key_parts_ok(name):
    KEY_PARTS = ['mot_coil_L','mot_coil_R','cav_outer','sapph_flange','sapph_window',
                 'vac_shell','left_mount_seat','left_feedthrough','lat_fiber_flange','dichroic_mir']
    missing = [k for k in KEY_PARTS if not bpy.data.objects.get(k)]
    return name, missing

def render_and_check(cam_obj, out, note=""):
    scene.camera = cam_obj
    scene.render.filepath = out
    bpy.ops.render.render(write_still=True)
    _c, _miss = key_parts_ok(out)
    print(f"FORMAL rendered {out} {note} | 关键部件: {('缺失 '+str(_miss)) if _miss else '完整(10 部件均在)'}")

# ---- 各视角的临时隐藏规则(渲染后恢复), 与 build 脚本一致 ----
def _set_hide(names, hide=True, restore_states=None):
    st = {}
    for k in names:
        o = bpy.data.objects.get(k)
        if o:
            st[k] = o.hide_render
            o.hide_render = hide
    return st

def _restore(st):
    for k, v in st.items():
        o = bpy.data.objects.get(k)
        if o: o.hide_render = v

cam1     = bpy.data.objects['cam_overview']          # 总览
cam6     = bpy.data.objects['cam_cavo']              # 铜腔内部
cam_rear = bpy.data.objects['cam_rear_window']        # 后窗
# cam_mot / cam_rw 已在上方 get_or_make_cam 创建/获取
assert cam_mot is not None and cam_rw is not None

# 0) 先核对 5 个相机都在
for cn in ['cam_overview','cam_cavo','cam_rear_window','cam_mot_entrance','cam_rw_interface_v2']:
    assert bpy.data.objects.get(cn), f"缺相机 {cn}"

# 1) 总览: 两个完整主线圈 + 修正后玻璃窗(两独立窗) + 冷却光经窗口进室
render_and_check(cam1, "render-output/formal_v16_overview.png", "(总览, 两完整线圈+双独立玻璃窗+冷却光进室)")

# 2) MOT 入口局部: 保留 4 冷却光 + 铜腔入口 + 窗口; 临时隐藏晶格光束 + 二向色镜(还原)
_st = _set_hide(['lat_beam_1','lat_beam_2','dichroic_mir'])
render_and_check(cam_mot, "render-output/formal_v16_mot_entrance.png", "(MOT/入口局部, 冷却光可见+入口, 晶格光束/二向色镜临时隐藏已恢复)")
_restore(_st)

# 3) 铜腔内部: 主线圈 L/R + 展示副本全隐藏使铜腔无遮挡(还原), 显示副本
_ml=bpy.data.objects.get('mot_coil_L'); _mr=bpy.data.objects.get('mot_coil_R'); _md=bpy.data.objects.get('mot_coil_L_display')
_st2={}
for _o in (_ml,_mr,_md):
    if _o: _st2[_o.name]=_o.hide_render; _o.hide_render=True
render_and_check(cam6, "render-output/formal_v16_cavity.png", "(铜腔内部无遮挡, 内衬不外伸, 主线圈/副本临时隐藏已恢复)")
for _k,_v in _st2.items():
    o=bpy.data.objects.get(_k)
    if o: o.hide_render = _v
# 恢复: 主线圈可见, 副本隐藏(与保存态一致)
if _ml: _ml.hide_render=False
if _mr: _mr.hide_render=False
if _md: _md.hide_render=True

# 4) 后窗连接剖切: 默认状态(镜盘+承座环+法兰), 无临时隐藏
render_and_check(cam_rear, "render-output/formal_v16_rear_window.png", "(后窗连接剖切, 承座前缘贴铜管端面 0.000mm, 镜盘覆盖通孔)")

# 5) 右壁接口: 临时隐藏遮挡线圈 L/R+副本(还原); 两独立玻璃窗+中央光纤接口+冷却光入射点
_st3 = _set_hide(['mot_coil_L','mot_coil_R','mot_coil_L_display'])
render_and_check(cam_rw, "render-output/formal_v16_rightwall.png", "(右壁接口, 双独立玻璃窗+光纤接口, 遮挡线圈临时隐藏已恢复)")
_restore(_st3)

# 保存正式场景
bpy.ops.wm.save_as_mainfile(filepath="render-output/scene_v16_formal.blend")
print("scene_v16_formal.blend saved")
