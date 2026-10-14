#!/usr/bin/env python3
"""
blender_core.py — 科研装置三维渲染可复用助手（v0.5 试用；最早抽取于 v0.1）
============================================================
用途：Blender 几何/材质/相机/布尔/核查基础助手。
通用可复用的 Blender 几何助手，不含任何论文场景的物件名、路径或空间坐标；
用户需根据当前来源设置尺寸与端口，不可把函数参数误认为已验证的器件实例。

设计原则（详见 ../references/physical_equipment_and_interfaces.md 与当前任务证据）：
  P2  光束端点记录为对象自定义属性（核查用中轴线，非顶点云）
  P5  独立材质 + Principled 透射输入名兼容（Blender 4.x/5.x）
  P8  独立复算（copy + 布尔 INTERSECT EXACT + bmesh.calc_volume）
  P9  局部视角隐藏规则渲染后还原
  P10 近裁剪面可调（mm 尺度场景 clip_start=0.001）

本文件为可导入模块：
    import blender_core as bc
    bc.setup_scene(samples=chosen_samples, resolution=chosen_size)
    wall = bc.box("wall", ...)
    ...

在 headless Blender 中运行调用方脚本：
    /Applications/Blender.app/Contents/MacOS/Blender -b -P your_build.py
"""
import bpy
import bmesh
import math
import mathutils

# ---------- 场景 ----------
def setup_scene(samples=None, resolution=None, engine='CYCLES',
                 denoise=True, background=None):
    """新建空场景；调用方必须指定采样/尺寸，底色可按任务指定。
    None 不能悄悄落到昂贵的 Blender 出厂采样或旧案例默认值。"""
    if samples is None or resolution is None:
        raise ValueError('setup_scene requires explicit samples and resolution for this task')
    bpy.ops.wm.read_factory_settings(use_empty=True)
    scene = bpy.context.scene
    scene.render.resolution_x, scene.render.resolution_y = resolution
    scene.render.resolution_percentage = 100
    scene.render.engine = engine
    scene.cycles.samples = samples
    scene.cycles.use_denoising = denoise
    world = bpy.data.worlds[0] if bpy.data.worlds else bpy.data.worlds.new("W")
    world.use_nodes = True
    if background is not None:
        world.node_tree.nodes["Background"].inputs[0].default_value = tuple(background) + (1.0,)
    return scene

# ---------- 材质 ----------
def mat(name, base, rough=0.5, metal=0.0, emis=None, es=0.0):
    """基础 Principled 材质（不透射）。base 为 RGB 三元组。"""
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    b = m.node_tree.nodes.get("Principled BSDF")
    b.inputs["Base Color"].default_value = base + (1.0,)
    b.inputs["Roughness"].default_value = rough
    b.inputs["Metallic"].default_value = metal
    if emis:
        b.inputs["Emission Color"].default_value = emis + (1.0,)
        b.inputs["Emission Strength"].default_value = es
    return m


def glass_mat(name, base, rough, ior, transmission=1.0):
    """理想化透射玻璃材质助手；颜色/粗糙度/IOR 由当前任务显式提供。
    `transmission=1.0` 仅是选用本助手时的理想透明预设，非论文量测值，
    更不保证最终 PNG 中玻璃可读；需真实读图。兼容 Principled 输入名差异。
    """
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    b = m.node_tree.nodes.get("Principled BSDF")
    b.inputs["Base Color"].default_value = tuple(base) + (1.0,)
    b.inputs["Roughness"].default_value = rough
    b.inputs["Metallic"].default_value = 0.0
    tw = b.inputs.get("Transmission Weight")
    if tw is not None:
        tw.default_value = transmission
    else:
        tr = b.inputs.get("Transmission")
        if tr is not None:
            tr.default_value = transmission
    io_ = b.inputs.get("IOR")
    if io_ is not None:
        io_.default_value = ior
    return m

# ---------- 几何助手 ----------
def box(name, sx, sy, sz, loc, rot=(0, 0, 0), m=None):
    """
    立方体（以 1 为单位尺寸再缩放）。Blender 5.x 陷阱：transform_apply(scale=True)
    会连带烘焙 loc/rot，故显式 location=False, rotation=False, scale=True。
    """
    bpy.ops.mesh.primitive_cube_add(size=1, location=loc, rotation=rot)
    o = bpy.context.object
    o.name = name
    o.scale = (sx, sy, sz)
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    if m:
        o.data.materials.append(m)
    return o


def cyl(name, r, depth, loc, rot=(0, 0, 0), m=None, seg=48):
    bpy.ops.mesh.primitive_cylinder_add(radius=r, depth=depth, location=loc,
                                        rotation=rot, vertices=seg)
    o = bpy.context.object
    o.name = name
    if m:
        o.data.materials.append(m)
    return o


def torus(name, R, r, loc, rot=(0, 0, 0), m=None, s1=96, s2=20):
    bpy.ops.mesh.primitive_torus_add(major_radius=R, minor_radius=r,
                                     location=loc, rotation=rot,
                                     major_segments=s1, minor_segments=s2)
    o = bpy.context.object
    o.name = name
    if m:
        o.data.materials.append(m)
    return o


def sphere(name, r, loc, segments=24, rings=12, m=None):
    bpy.ops.mesh.primitive_uv_sphere_add(radius=r, location=loc,
                                         segments=segments, ring_count=rings)
    o = bpy.context.object
    o.name = name
    if m:
        o.data.materials.append(m)
    return o

# ---------- 光束 ----------
def beam(name, p0, p1, r=0.0012, m=None, seg=16, record_ends=True):
    """
    圆柱光束，输入 p0→p1 为创建时世界坐标。beam_p0/beam_p1 始终存【对象局部坐标】，
    由当前 matrix_world 恢复世界轴（中轴线，非 bounding box 对角线）。
    """
    v = mathutils.Vector(p1) - mathutils.Vector(p0)
    mid = (mathutils.Vector(p0) + mathutils.Vector(p1)) / 2
    rot = v.to_track_quat('Z', 'Y').to_euler()
    o = cyl(name, r, v.length, tuple(mid), tuple(rot), m, seg=seg)
    if record_ends:
        # 切忌把世界输入原样存入端点属性：读取时还要乘 matrix_world。
        inv = o.matrix_world.inverted()
        o['beam_p0'] = tuple(inv @ mathutils.Vector(p0))
        o['beam_p1'] = tuple(inv @ mathutils.Vector(p1))
    return o


def beam_via_point(name, p0, p1, m=None, r=0.0012):
    """
    P2/P3：建光束并记录端点；入射端须真接壁面命中点（沿真实传播方向延长），不得提前截断。
    交汇是否在线段上由 beam_crosses_point() 用端点中轴线核查（0≤t≤1，不要求对称）。
    """
    return beam(name, p0, p1, r=r, m=m)

# ---------- 布尔 ----------
def boolean_cut(target, cutter, op='DIFFERENCE'):
    """对 target 做布尔（applied），删除 cutter。开孔/剖切用。"""
    md = target.modifiers.new("bool", 'BOOLEAN')
    md.operation = op
    md.object = cutter
    bpy.context.view_layer.objects.active = target
    bpy.ops.object.modifier_apply(modifier="bool")
    bpy.data.objects.remove(cutter, do_unlink=True)


def solid_inter_mm3(oA, oB, solver='EXACT'):
    """
    P8：实体相交体积（mm³），在【世界空间】下计算。

    实现：copy 两对象的 mesh 与变换 → 对副本做布尔 INTERSECT（EXACT）→
    bmesh.calc_volume 得本地(m³)体积 → 乘以 A 的世界变换行列式（含缩放）归一到世界体积。

    输入条件（必须满足，否则数值不可靠）：
      - oA/oB 为同一场景、有已烘焙或正常变换的实体 mesh 对象；
      - 对象【未】挂未应用的修改器（若挂，先 apply 或用 evaluated 网格）；
      - 对象被移动/缩放/旋转后，调用本函数前应刷新 depsgraph
        （bpy.context.view_layer.update()）使 matrix_world 生效，
        否则 |det(matrix_world)| 取的是旧值，世界体积归一会出错；
      - 本助手几何（box/cyl/torus）在创建时已 transform_apply(scale=True)，
        其世界缩放=1，行列式≈1；但对象后续被整体缩放/移动后仍正确（本函数按 A 的世界变换缩放体积）。

    反例校验：两个重合单位立方体（size=1）各自 scale=2（世界 2×2×2），应得 8 m³ 重叠；
    若漏掉世界缩放只会得 1 m³。本函数按 A 的 det(matrix_world) 归一，返回 8e9 mm³（即 8 m³）。
    """
    scene = bpy.context.scene
    tA = bpy.data.objects.new('_tA', oA.data.copy())
    scene.collection.objects.link(tA)
    tA.matrix_world = oA.matrix_world.copy()
    tB = bpy.data.objects.new('_tB', oB.data.copy())
    scene.collection.objects.link(tB)
    tB.matrix_world = oB.matrix_world.copy()
    md = tA.modifiers.new('_b', 'BOOLEAN')
    md.operation = 'INTERSECT'
    md.object = tB
    md.solver = solver
    bpy.context.view_layer.objects.active = tA
    bpy.ops.object.modifier_apply(modifier='_b')
    bm = bmesh.new()
    bm.from_mesh(tA.data)
    vol_local = bm.calc_volume()          # 本地(m³)，随 mesh 数据（已含被应用的缩放）
    bm.free()
    # 世界体积 = 本地体积 × |det(世界变换)|（布尔后 tA 仍保留 oA 的 matrix_world）
    det = tA.matrix_world.determinant()
    vol_world = abs(vol_local) * abs(det)
    bpy.data.objects.remove(tB, do_unlink=True)
    bpy.data.objects.remove(tA, do_unlink=True)
    return vol_world * 1e9  # m³ -> mm³

# ---------- 相机 ----------
def make_cam(name, loc, look_at, lens=None, clip_start=None, clip_end=None):
    """相机位置/焦距/裁剪随任务配置；None 使用 Blender 本机参数。
    mm 尺度的近裁剪需由调用方显式设定，非所有装置通用默认值。
    to_track_quat 需大写 'Z','Y'。
    """
    d = mathutils.Vector(look_at) - mathutils.Vector(loc)
    quat = (-d).to_track_quat('Z', 'Y')
    rot = quat.to_euler()
    bpy.ops.object.camera_add(location=loc, rotation=rot)
    c = bpy.context.object
    c.name = name
    if lens is not None:
        c.data.lens = lens
    if clip_start is not None:
        c.data.clip_start = clip_start
    if clip_end is not None:
        c.data.clip_end = clip_end
    return c


def get_or_make_cam(name, loc, look_at, lens=None, clip_start=None, clip_end=None):
    """已存在则取，不存在则建（用于正式渲染脚本补建 build 时未持久化的相机）。"""
    o = bpy.data.objects.get(name)
    if o:
        return o
    return make_cam(name, loc, look_at, lens, clip_start, clip_end)


def clip_check(cam_name, tgt_name, require_some_in_front=True):
    """
    P10：目标 bounding box 全 8 角 → 先变换到【世界坐标】(o.matrix_world)，
    再变换到【相机坐标系】(cam.matrix_world.inverted())，取有符号轴向深度 d=-p.z（相机前方为正）。

    返回 (message, in_range_bool)。
    规则（修复版；保留 require_some_in_front 形参供旧调用，完整判定不受其放宽）：
      - 相机后方角点(p.z>=0)单独计数；若目标全部 8 角都在相机后方（behind==8），
        则【不能】判"完整通过"——返回 in_range=False 并注明"全部在相机后方"。
      - 只有 8 角均在前方，且全部满足 [clip_start, clip_end] 才判完整入裁剪范围；
        混合前后角点不得因跳过后方角点而误判完整通过。仅检轴向裁剪，不检横纵视锥。
    必须把世界变换计入，否则对象离相机 11m 会被误报成 1m。
    """
    o = bpy.data.objects.get(tgt_name)
    if not o:
        return f"  {cam_name} -> {tgt_name}: 对象缺失", False
    cam = bpy.data.objects[cam_name]
    # 关键：bound_box 是本地坐标，先乘 o.matrix_world 到世界，再转相机系
    world_corners = [o.matrix_world @ mathutils.Vector(c) for c in o.bound_box]
    cam_inv = cam.matrix_world.inverted()
    cam_corners = [cam_inv @ c for c in world_corners]
    mn, mx, behind, infront, ok = 1e9, -1e9, 0, 0, True
    for p in cam_corners:
        if p.z >= 0:      # 相机后方
            behind += 1
            continue
        infront += 1
        d = -p.z          # 有符号轴向深度（前方为正）
        mn, mx = min(mn, d), max(mx, d)
        if not (cam.data.clip_start <= d <= cam.data.clip_end):
            ok = False
    if infront == 0:      # 全在后方：绝不判完整通过
        return (f"  {cam_name} -> {tgt_name}: 全部 8 角在相机后方(behind=8)，无法完整入框 "
                f"behind_cam={behind}角点 in_range=False"), False
    msg = (f"  {cam_name} -> {tgt_name}: 有符号轴向深度=[{mn:.4f},{mx:.4f}]m "
           f"clip=[{cam.data.clip_start:.3f},{cam.data.clip_end:.1f}] in_range={ok and behind == 0} "
           f"front={infront}/8角 behind_cam={behind}角点")
    # 有任一后方角点都不能称为完整位于裁剪范围内；仅检查轴向，不检查画面边界。
    return msg, (ok and behind == 0)

# ---------- 渲染（局部视角独立隐藏规则 + 还原） ----------
class LocalRenderRule:
    """
    P9：局部视角临时隐藏遮挡件（记录原 hide_render，渲染后逐件还原），
    待核查对象（光束/玻璃/接口）绝不隐藏。
    hidden_names：要临时隐藏的部件名列表。
    must_keep：绝不能隐藏的部件名列表（渲染前校验）。
    """

    def __init__(self, hidden_names=(), must_keep=()):
        self.hidden_names = list(hidden_names)
        self.must_keep = list(must_keep)

    def apply(self):
        st = {}
        for k in self.hidden_names:
            o = bpy.data.objects.get(k)
            if o:
                st[k] = o.hide_render
                o.hide_render = True
        return st

    def verify(self):
        """渲染前校验：must_keep 中每个对象 必须 存在 且 未被隐藏(参与渲染)。
        返回 dict: name -> (exists, will_render)。若任一 must_keep 缺失或将被隐藏，render() 拒绝渲染。"""
        rep = {}
        for k in self.must_keep:
            o = bpy.data.objects.get(k)
            exists = o is not None
            will = (not o.hide_render) if exists else False
            rep[k] = (exists, will)
        return rep

    def restore(self, st):
        for k, v in st.items():
            o = bpy.data.objects.get(k)
            if o:
                o.hide_render = v

    def render(self, cam, out, extra_note=""):
        # 渲染前校验：must_keep 必须存在且参与渲染，否则拒绝（不渲染出不完整图）
        rep = self.verify()
        bad = {k: v for k, v in rep.items() if not (v[0] and v[1])}
        if bad:
            print(f"  [render 拒绝] {out}: must_keep 不满足(缺失或被隐藏) = {bad}")
            return False, rep
        st = self.apply()
        try:
            scene = bpy.context.scene
            scene.camera = cam
            scene.render.filepath = out
            bpy.ops.render.render(write_still=True)
        finally:
            self.restore(st)   # 异常也恢复显示状态
        print(f"rendered {out} (待核查对象 must_keep={rep}, 临时隐藏已恢复) {extra_note}")
        return True, rep

# ---------- 关键件完整性核查（轴向裁剪 ≠ 画幅投影） ----------
def key_parts_ok(view_name, KEY_PARTS, cam_name=None):
    """分层返回 exists / renders / in_clip_range；后者仅为 bbox 8 角
    的相机轴向 near/far 检查，不判断画幅水平/垂直投影或互遮挡。
    未指定相机或对象缺失时 in_clip_range=None。旧消费者依赖
    report[name]['in_frame'] 的代码须更新，不能把旧键再当作入框通过。
    返回 (view_name, report)，不承诺视觉可辨或真实连接。
    """
    report = {}
    for k in KEY_PARTS:
        o = bpy.data.objects.get(k)
        exists = o is not None
        renders = (not o.hide_render) if exists else False
        in_clip_range = None
        if exists and cam_name:
            _msg, in_clip_range = clip_check(cam_name, k)
        report[k] = {'exists': exists, 'renders': renders,
                     'in_clip_range': in_clip_range}
    return view_name, report

# ---------- 光路交汇核查（中轴线，非顶点云） ----------
def pt_to_line_dist(P, A, B):
    """点 P 到线段 AB 的最短距离 + 参数 t。返回 (dist, t)。"""
    u = [B[i] - A[i] for i in range(3)]
    w = [P[i] - A[i] for i in range(3)]
    uu = sum(x * x for x in u)
    uuw = sum(u[i] * w[i] for i in range(3))
    t = uuw / uu if uu else 0.0
    cl = [A[i] + t * u[i] for i in range(3)]
    return sum((P[i] - cl[i]) ** 2 for i in range(3)) ** 0.5, t


def beam_axis_world(beam_obj):
    """返回当前世界轴端点或 None；beam_p0/p1 必须是对象局部坐标。

    不把包围盒对角线当轴，也不按任意长度差臆断端点过期。比较属性端点
    与当前【局部网格】两端截面中心；不符即失败关闭（旧版世界坐标属性也会拒绝）。
    当前对象及父级的 matrix_world 只对一致的局部端点乘一次。
    仅针对 beam() 生成的直圆柱且网格未被重塑的轴；其他模型请显式定义接口。
    """
    p0 = beam_obj.get('beam_p0')
    p1 = beam_obj.get('beam_p1')
    if p0 is None or p1 is None or beam_obj.type != 'MESH':
        return None
    try:
        a, b = mathutils.Vector(p0), mathutils.Vector(p1)
        if (b - a).length < 1e-10:
            return None
        verts = beam_obj.data.vertices
        if not verts:
            return None
        zs = [v.co.z for v in verts]
        zlo, zhi = min(zs), max(zs)
        lo = [v.co for v in verts if abs(v.co.z - zlo) < 1e-6]
        hi = [v.co for v in verts if abs(v.co.z - zhi) < 1e-6]
        if not lo or not hi:
            return None
        center_lo = sum(lo, mathutils.Vector()) / len(lo)
        center_hi = sum(hi, mathutils.Vector()) / len(hi)
        if (a - center_lo).length > 1e-5 or (b - center_hi).length > 1e-5:
            return None
        M = beam_obj.matrix_world
        return tuple(M @ a), tuple(M @ b)
    except (TypeError, ValueError, OverflowError):
        return None


def beam_crosses_point(beam_obj, point, tol=5e-4):
    """
    P2：当前世界轴是否经过世界坐标 point。返回 (dist,t,passed,axis_known)。
    属性缺失或不符当前局部网格时 axis_known=False/passed=False；
    0≤t≤1 且 dist<tol 判通过。平移/旋转/父级变换由局部端点随 matrix_world
    正确更新；轴仍已知，但旧交点不再通过。
    """
    ends = beam_axis_world(beam_obj)
    if ends is None:
        return None, None, False, False
    p0, p1 = ends  # 已是世界坐标，绝不再乘 matrix_world
    d, t = pt_to_line_dist(tuple(point), p0, p1)
    passed = (0.0 <= t <= 1.0) and (d < tol)
    return d, t, passed, True
