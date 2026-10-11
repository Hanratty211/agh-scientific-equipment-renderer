# 案例 1：⁸⁷Sr 冷冻光晶格钟（cryo lattice clock）三维重构 —— 审查记录

**日期**：2026-10-11
**工作目录**：`agh-research-figure-skill/case-1_87sr_cryo_lattice/`
**当前通过状态**：v16（几何）+ v16b（右壁双独立玻璃窗的显示材质）
**正式图**：`render-output/formal_v16_*.png`（1600×900，Cycles 96 采样，去噪）
**正式场景**：`render-output/scene_v16_formal.blend`

---

## 0. 性质声明（重要）

**本案例是对公开论文拟建方案的三维重构（3D reconstruction of a *proposed* setup），不是已建成装置（not a built device）。**

- **来源论文（完整标识）**：W. Middelmann, F. Schenk, A. Altmann, S. Zippel, L. Lorini, P. Laakso,
  P. Windfeld, C. Freyschütz, H. Ahnft, R. W. Hellberg, A. Lauer, R. Lange, T. S. W. E. (PTB) et al.
  实际作者列表以 PDF 为准；**arXiv:1009.2017**（Middelmann et al., 2010，PTB，*Optics Communications* 2010/
  相关期刊）。全文已下载 `source-materials/cand_C_bbrSr.pdf`。
- **拟建图注原文位置**：论文 **Fig.7** 图注明确写 "Layout of the proposed setup"；低温铜腔（77 K）+
  dc Stark 场板为**拟建（proposed）**；移动晶格测试（air-bearing 台，Fig.8）以 "In the present test setup"
  表述为**已测试**。
- 本记录中每一项都区分：**论文依据 / 建模假设 / 自动几何核查 / 实际图片核查**，并保留若干**未确认项**（后窗固定/密封等）。
  "本轮修改范围内" 的事项 **≠ 已有论文依据**——模型里画了不代表论文支持。

---

## 1. 交付物清单（可核查位置）

### 1.1 正式图（5 张，1600×900 @ 96 采样）
| 视角 | 文件 | 说明 |
|---|---|---|
| 总览 | `formal_v16_overview.png` | 两个完整主线圈 + 修正后双独立玻璃窗 + 冷却光经窗口进室 |
| MOT 入口局部 | `formal_v16_mot_entrance.png` | 4 束冷却光交汇点 + 铜腔入口；晶格光束/二向色镜临时隐藏已还原 |
| 铜腔内部 | `formal_v16_cavity.png` | 铜腔无遮挡，内衬不外伸；主线圈/展示副本临时隐藏已还原 |
| 后窗 | `formal_v16_rear_window.png` | 承座前缘贴铜管端面 0.000mm，镜盘覆盖通孔（假设安装示意） |
| 右壁接口 | `formal_v16_rightwall.png` | 双独立玻璃窗 + 中央光纤接口 + 冷却光入射点；遮挡线圈临时隐藏已还原 |

### 1.2 场景
- `render-output/scene_v16.blend`（已通过核查状态，低预览）
- `render-output/scene_v16_formal.blend`（正式渲染参数后的场景快照）

### 1.3 脚本
- `build_blender_v16.py`（几何 + 材质 + 相机 + 核查脚本，含 v15b/v16b 修正）
- `render_formal_v16.py`（正式渲染脚本，1600×900 @ 96 采样）
- `verify_v16.py`（独立复算：玻璃∩光纤=0、冷却光∩vac_shell=0）

### 1.4 历史文件（重要区分："保留版本文件" vs "同名文件曾被更新"）
- `build_blender_v13.py / v14.py / v15.py / v16.py`——4 个**独立版本脚本，全部保留**（本会话内**未被覆盖**）。
- `render-output/render_v14_prev_*.png`（8 张）+ `scene_v14.blend` + `montage_v14_delivery.png`——v14 轮输出，保留。
- `render-output/render_v15_prev_overview.png` + `render_v15_prev_mot_entrance.png` + `scene_v15.blend`——v15/v15b 轮输出，保留。
- `render-output/render_v16_prev_rightwall.png / _v2.png / _v3.png` + `scene_v16.blend`——v16/v16b 轮输出，保留。
- `REVISION_LOG.md`（v6→v16 完整版本条目，含各轮自动核查结果）。
- **注意区分**：`build_blender_v16.py` 与 `render-output/scene_v16.blend` 在本会话中**同名文件被多次更新**
  （v16 几何修正 → v16b 相机 v2 → v16b 材质 v3），每个更新**保留了前一轮 PNG**（`_rightwall.png` / `_v2.png` / `_v3.png` 并存），
  但 `.blend` 本身是**同名文件被覆盖更新**（当前 `scene_v16.blend` 反映最后一次保存状态，不保留每次中间快照）。
  即：不能笼统声称"所有历史文件从未覆盖"——**历史 PNG 与独立脚本版本均保留；`.blend` 场景文件是同名覆盖更新**，
  如需追溯中间状态，看带后缀的 PNG 文件而非 `.blend`。

### 1.5 真实 AGH 执行记录（可核查位置）
- 本次会话的所有 Blender 运行、核查、渲染命令与输出，记录于 AGH 会话
  （sessionKey `360fa855-0fd0-430f-ad31-8e0da1e94661`）的事件账本。
- **完整 AGH 执行记录导出**（含真实工具调用、结果、时间、事件序号，并关联本次正式输出）：
  见 `AGH_EXECUTION_RECORD_v16.md`（本案例根目录，由会话事件账本导出，**不重跑**，只引用已发生的调用）。
  该文件逐条列出：时间戳 / 事件序号 / 工具名（shell/read/edit/write）/ 命令或参数 / 返回结果摘要 / 关联的输出文件（.png/.blend/.md/.docx/.pdf），
  便于人工复核本次正式交付的真实执行轨迹，**不能仅凭 sessionKey 与可重跑命令替代**。
- 关键可复核命令（在 `case-1_87sr_cryo_lattice/` 目录下，重跑需与导出记录交叉核对）：
  - `Blender -b -P build_blender_v16.py`（几何/材质/核查）
  - `Blender -b --factory-startup --python verify_v16.py`（独立复算）
  - `Blender -b -P render_formal_v16.py`（正式 1600×900@96 渲染）
- 所有 `.png` / `.blend` 文件保留在 `render-output/`，带时间戳；历史 PNG 与独立脚本版本保留，`.blend` 场景文件为同名覆盖更新（见 1.4）。

---

## 2. 几何关键量（自动核查结果）

坐标系（米；**x 轴指向 MOT→铜腔 = 负 x 方向，即铜腔在 MOT 的 -x 侧**，AXIS_Z=0.020）：
- MOT 交汇点 `MOT_C = (0.030, 0, 0.020)`（MOT 区，x 正向）
- 冷冻铜腔：`CAV_X=-0.080`（铜腔中心 x，-x 方向），`CAV_LEN=0.160`，`CAV_R_IN=0.005`，`CAV_R_OUT=0.0065`，`CAV_REAR_X=-0.160`（腔后段更靠 -x）
- **铜管入口 = `x=0`（腔口前端，MOT 区与铜腔之间的分界）；`LIN_FRONT_X=-0.020` = 内衬前端（在铜管内，-x 侧 20mm），两者不能混称**：
  铜管入口 x=0 是腔体几何开口，内衬前端 x=-0.020 是内衬（CuO）实际起点，均在铜管内部，内衬保持在铜管内（不外伸到入口 x=0 之前）。
- 真空室 `CHAM_W/D/H=0.200/0.150/0.150, CHAM_CX=-0.040, T=0.003`
- 右壁金属带 `x∈[57,60]mm`（外表面 `RT_WALL_OUT_X=60mm`；+x 方向，右壁在 x 正向），右壁金属带是冷却光入射端命中的面

### 冷却光束
- **b1/b2（斜向，±y）**：中轴线 `p0=(60,∓30,20)mm`（右壁外表面命中点）、`p1=(5,±25,20)mm`；
  经 `MOT_C`，距离 **0.0000mm**，`t=0.545`（在线段上；t 不必=0.5，只要交点在段内即可）。
- **b3/b4（顶/底 ±z）**：顶壁入射 `z=73.5mm`、底壁入射 `z=-73.5mm`；
  远端为**显示截断**（z=5/40mm），记录为截断，**不声称**与对面窗口连通。

### 右壁双独立玻璃窗（v16 核心修正）
- **负 y 窗** `mot_opt_win_n`：`y∈[-33,-23]mm`（中心 -28，半宽 5mm），`z∈[17,23]mm`
- **正 y 窗** `mot_opt_win_p`：`y∈[+23,+33]mm`（中心 +28，半宽 5mm），`z∈[17,23]mm`
- 中央 `y∈[-23,+23]mm` 保留金属 + 原光纤接口（`lat_wall_hole` 圆 r=4mm、`lat_fiber_flange` OD 11mm `y∈[-5.5,5.5]`）
- 单窗尺寸由**完整穿墙段包络**决定：光束半径 1.2mm + 45° 斜入射投影 1.70mm + 余量

### 自动几何核查结果（对 saved `scene_v16.blend` 独立复算）
| 核查项 | 结果 | 类别 |
|---|---|---|
| 玻璃窗 ∩ 光纤组件 | `mot_opt_win_n/p` ∩ {lat_fiber_flange, out, in} = **全 0.0000 mm³**（v15 曾 249.34/37.58/52.41 mm³，已消除） | 自动几何 |
| 冷却光∩vac_shell | `cool_bm_1/2` = **0.0000 mm³**（穿墙段经各自开孔过壁，不碰金属壁实体） | 自动几何 |
| 经过交汇点 | b1/b2 中轴线到 `MOT_C` 距离 **0.0000mm**（t=0.545 在线段上） | 自动几何 |
| 接到窗口 | b1 命中 y=-30 ∈ 负窗[-33,-23]；b2 命中 y=+30 ∈ 正窗[+23,+33] | 自动几何 |
| 中央金属区 | 右壁开孔在 y=±28，不覆盖 y=0 光纤区 → 光纤接口保留 | 自动几何 |

---

## 3. 论文依据 / 建模假设 / 未确认项

### 3.1 论文依据（provenance 明确）
- **来源论文完整标识**：arXiv:1009.2017（Middelmann et al., 2010，PTB；全文 `source-materials/cand_C_bbrSr.pdf`）。
- 698 nm 钟跃迁（³P₀−¹S₀）——正文 "spectroscopy on the clock transition 3P0−1S0 at 698 nm"。
- 冷却光 461 nm（¹P₁−¹S₀）→ 约 3 mK；第二级 MOT 689 nm（间组跃迁）→ 约 50 µK → 4 µK（正文冷却温度序列）。
- repump 679/707 nm；移动晶格 air-bearing 台（Fig.8，已测试）。
- **光晶格 magic wavelength：正文仅引用 [11]（Katori, Takamoto, Pal'chikov, Ovsianikov, *PRL* 91:173005, 2003），
  本篇未列具体数值**；后续文献常引 ⁸⁷Sr magic≈813 nm（⁸⁸Sr≈759 nm，依赖同位素与跃迁）。**本次未在线核实 Katori 2003 原文数值，
  图中统一写 "magic wavelength (Ti:Sapphire, [11])"，不写具体 nm 数字。**
- **铜腔 + 蓝宝石后窗 + 二向色镜方案：属论文依据**（Fig.7 "Layout of the proposed setup"，低温铜腔 77 K + tilted sapphire window，
  对晶格光透明、吸收 BBR）；这是**论文提出的方案**，但具体尺寸/安装结构/布局是建模假设（见 3.2）。

### 3.2 建模假设（**无论文依据**，仅是本轮修改范围内）
- **铜腔/后窗/二向色镜的具体尺寸、安装结构、布局 = 建模假设**（论文提出方案，但外径/壁厚/倾角/承座形式/二向色镜尺寸均无论文数值）：
  冷冻铜腔外径假设壁厚 1.5mm（内径 10mm 来自论文，外径半径 6.5mm 为假设）；后窗承座/镜盘尺寸、倾角 20° 均为假设。
- 右壁**双独立玻璃窗**的布局/尺寸/安装形式 = 建模假设（为消除玻璃横跨光纤而拆成两窗）
- 中央金属区保留光纤接口的具体位置 = 建模假设
- 顶/底壁冷却光窗 = 建模假设（远端截断，不声称连通）
- **光束中心线过 MOT 交汇点 = 建模/几何核查（构造保证），不是论文依据**（论文不指定 4 束斜向冷却光的具体入射角/交汇位置）

### 3.3 未确认项（保留，明确标注）
- 后窗 `sapph_window` 承座固定方式（螺纹/焊接/压接）：**未确认（UNCONFIRMED）**
- 后窗密封（面接触 vs O 型圈/焊缝）：**未确认，未做制造公差/密封设计**（承座前缘贴铜管端面 0.000mm 是几何面接触，**不等于密封证明**）
- magic wavelength 具体数值：未从 Katori 2003 原文核实，仅引用 [11]，图中不写具体 nm

---

## 4. 实际图片核查（类别 5）

> **审查者如实记录**：
> - `render_v16_prev_rightwall_v3.png`（低成本预览）：由**外部助手实际读取该 PNG 像素后完成视觉核查**，
>   通过（两蓝光穿窗位置、玻璃边界、中央金属区及光纤接口均可辨认）。**不是用户亲自目检**。
> - 5 张正式图（`formal_v16_*.png`，1600×900@96）：已由**外部助手实际读取 5 张 PNG 完成视觉回归核查**，
>   通过（无显示状态回归、玻璃窗透光、冷却光入射点清晰）。**本次通过结论如实记录为"外部助手实际读取 PNG 后视觉核查通过"**，
>   不写成"用户亲自目检"或"人工已确认"。用户本案例最终定稿授权为：外部助手核查通过后即冻结，用户不再逐张重看。
>
> 本记录中"图片核查"栏一律指**外部助手实际读取像素后判词**，不是模型自证、也非用户亲自目检。

| 视角 | 文件 | 图片核查状态 | 审查者 |
|---|---|---|---|
| 总览 | `formal_v16_overview.png` | **通过**（无回归，两线圈完整、双窗+冷却光进室） | 外部助手实际读 PNG |
| MOT 入口 | `formal_v16_mot_entrance.png` | **通过**（交汇点可读、入口间隙清楚） | 外部助手实际读 PNG |
| 铜腔内部 | `formal_v16_cavity.png` | **通过**（铜腔无遮挡、内衬不外伸） | 外部助手实际读 PNG |
| 后窗 | `formal_v16_rear_window.png` | **通过**（镜盘覆盖通孔、承座贴铜管端面） | 外部助手实际读 PNG |
| 右壁接口 | `formal_v16_rightwall.png` | **通过**（双玻璃窗透光、两蓝光穿窗位置清晰） | 外部助手实际读 PNG |

**回归检查**：正式图采用修正后的双独立玻璃窗及其材质（`M_GLASS_CRYO`，Transmission=1/IOR=1.45），共享材质 `port_glass` 未动，各视角临时隐藏规则渲染后已还原（渲染日志确认）。**后窗固定/密封项仍保留为未确认（见 3.3）。**

---

## 5. 渲染参数
- 分辨率：1600×900（100%）
- 引擎：Cycles，96 采样，去噪开启
- 各视角临时隐藏规则（渲染后恢复）：
  - 总览：主线圈 L/R 完整（不剖切）
  - MOT 入口：临时隐藏 `lat_beam_1/2` + `dichroic_mir`（交汇点为画面主体）
  - 铜腔内部：主线圈 L/R + 展示副本全隐藏（铜腔无遮挡）
  - 后窗：默认（镜盘+承座环+法兰）
  - 右壁接口：临时隐藏 `mot_coil_L/R + 副本`（不藏光束/玻璃/光纤）

---

## 6. 通用 Skill 状态
**本轮不定稿。** 案例经验已在 `REVISION_LOG.md` 各版本条目的"本案例经验"小节沉淀
（含：玻璃窗拆独立避免横跨光纤、局部图临时隐藏需在记录中注明、t≠0.5 接受交点在段内、
切掉/截断的壁面不充作真实光学界面等）。**最终通用 Skill 需后续公开案例检验可复用性后再定稿。**

---

## 7. 附：可核查执行位置索引
- 几何/核查：`build_blender_v16.py`（运行后打印 [1/2/3/v16] 各项自动结果）
- 独立复算：`verify_v16.py`（copy+boolean INTERSECT EXACT + bmesh.calc_volume，不依赖脚本内 print）
- 正式渲染：`render_formal_v16.py`（打开 `scene_v16.blend`，补建未持久化的两个相机，出 5 张 1600×900@96）
- 版本史：`REVISION_LOG.md`（v6→v16）
- 波长/状态注记：`notes_wavelengths_and_state.md`
