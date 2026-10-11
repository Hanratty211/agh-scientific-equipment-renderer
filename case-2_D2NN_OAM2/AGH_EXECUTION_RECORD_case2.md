# AGH 执行记录 —— Case-2（D2NN OAM-STM Fig.2(a)）+ Skill v0.2 修订
**会话 sessionKey**：360fa855-0fd0-430f-ad31-8e0da1e94661　**日期**：2026-10-11　**模型**：agnes-3.0-flash
**性质**：关键项摘录（非 ledger 行号转储、非回放日志）；E# 为摘要编号关联真实 AGH 工具调用。

## A · Skill v0.2 修订（外部核查 7 项修复）
- E1 `clip_check`：目标 bbox 先 `o.matrix_world`→世界，再 `cam.matrix_world.inverted()`→相机系；8 角全在相机后方→`in_range=False`，不报通过；返回 `(msg, in_range_bool)`。
- E2 `solid_inter_mm3`：按 `abs(oA.matrix_world.determinant())` 归一世界体积；文档化 depsgraph 刷新前提。反例 T1（重合 scale=2 立方体）= 8 m³ PASS。
- E3 `beam_axis_world` + `beam_crosses_point` 4-tuple：端点属性过期/缺失→`axis_known=False`，不回退包围盒对角线。反例 T3（光束平移 5m 不再误报经过原交点）PASS。
- E4 `LocalRenderRule.verify()`：must_keep 缺失/被隐藏→**拒绝渲染**；`try/finally` 异常也还原；`key_parts_ok` 分层报告 exists/renders/in_frame，不混"可见"。
- E5 `SKILL.md`：补 YAML frontmatter（name/description，含触发词 + "v0.1 草案不宣称通用已验证"）；case-1 五视角/9-10 件/1600×900@96 降级为"案例配置示例"；已实现/拟建由当前来源定。
- E6 注册到 AGH 可发现位置：`ln -s <skill> /Users/wht/Desktop/黑客松/agnes-harness/.agh/skills/agh-scientific-equipment-renderer`；加载证据 = 软链可读到 frontmatter。
- E7 `behavior_tests.py` 三反例（真实 Blender）：T1/T2/T3 全 PASS，结果保留 `behavior_results.txt`。
- E8 `check_structure.py` 升级：frontmatter 校验 + 引用文件存在 + 退出码 + 反例行为验证（不靠字符串黑名单）；exit_code=0。
- E9 `pitfalls_and_fixes.md` P2/P6 更正 + `PROVENANCE.md` v0.2 修订记录（E1–E10 标注摘要编号关联本会话事件）。

## B · Case-2 建模（D2NN OAM-STM Fig.2(a)）
- E10 复制 `source_paper.pdf` + `reference_Fig2a.png`（md5 46d7b56d571c0a8557b4c6a3cb541b8d）。
- E11 pymupdf 抽第 4 页 Fig.2(a) 图注 + 第 3 页 Materials & methods + 第 9 页详细方法（正文 dichroic prism、4f 系统、2/4/6 m MMF、DMD–SLM 0.7 m）。
- E12 `evidence_base.md`：光路顺序 + 相对布局 + 命名差异（BS vs dichroic、Hologram/Phase 判示意）+ 部件清单 + 建模假设/不确定项。
- E13 `build_case2.py`：用**修正后** `blender_core`（不带 case-1 对象名/坐标）建 24 关键件 + 10 段示意光束 + 3 相机。
- E14 `Blender -b -P build_case2.py`：3 预览 PNG + `scene_case2.blend`；`key_parts_ok` 3 视角 24 件无异常；`LocalRenderRule` 局部 must_keep 全过并还原。
- E15 `verify_case2.py` **独立核查**（载入 .blend，不渲染）发现**缺陷**：初版光路段端点用"部件中心±固定偏移"，导致 8/10 段端点距目标入射面 54–95 mm（漂浮）；其中 2 面 45° 倾斜镜入射面因 bbox 扩大实际在 loc.x−0.0293（而非 −0.0015）。
- E16 **修正** `build_case2.py` 光路段端点贴**相邻部件实际表面**（按各件 x 半厚/镜面 bbox 偏移重算），重跑后独立核查 **10/10 段间隙=0.0 mm**（不漂浮不穿透）；MMF 并排 y=−0.02/0/0.02 正确；相机 in_frame 全 OK（`clip_check` 修复版世界坐标）。
- E17 标签层 `label_layer.md`（独立可编辑，3D 无字，含命名差异标注）+ `REVISION_LOG_case2.md`。
- **E18 照明/可见性修复（像素核查触发）**：factory empty 场景无灯光，初版 3 预览全部渲成**纯黑**（PIL 测 mean_lum≈0.0003，非白底）。补 3 盏 Sun/area 灯 + 地面参考平面 + 局部视角地面临时隐藏/降曝 + 总览相机拉远（lens 24），重出 3 预览（现中央带物体信号 0.40–1.00，非黑）。
- **E19 诚实记录——read 工具缓存现象（未确认）**：本轮多次用 `read` 回读 `case2_preview_*.png`，返回的**字节大小与磁盘当前文件不符**（如磁盘 overview 981,904 B 而 read 报 1,827,508 B）；几何/亮度统计（PIL/numpy，按磁盘文件计算）与 read 返回内容不一致。按 P6，记为**当时遇到的未确认现象**，**不**据此作像素级判定；视觉对应关系仍须外部助手读**磁盘正确版本** PNG 核实。

## C · Case-2 R4/R5（外部读图核查 → 折叠布局重建 + 核查方法修正）
- **E20 外部读图核查（审查者：外部助手实际读磁盘 PNG，MD5 与记录一致）**：判定照明修复成立但 Fig.2(a) **复刻未通过**，列 6 项确定问题（折叠光路缺失/镜未实际转向/MMF 短柱未连续连 BC/PD–示波器无信号连接/Iris 无真孔/总览器件小地面大）。→ `REVISION_LOG_case2.md` R4。
- **E21 撤回“10/10 段贴面”结论 + 独立复算**：`verify_case2.py` 旧 `nearest_x_face` 用 **bbox 极值** 非真实作用面 → 无效。改用 **射线/真实表面求交** `verify_case2_r4.py`：`beam_seg_L2_M1` 端点距 M1 真实镜面 **27.18 mm**（与外部复算值一致）；其余段 4–50 mm 漂浮。结果保留 `verify_case2_r4_results.txt`。**不改阈值让它通过**。
- **E22 重读参考图 → 折叠布局草图 + 完整连接表** `folded_layout_v2.md`：M1/M2/M3 三次 90° 转向；Holder→3×MMF 盘绕→BC→输出 MMF→PD→示波器；各件真实作用面/入射出射方向；**更正 DMD–SLM 0.7 m = 扣除 4f 后净距**（非含 4f 总间距）。
- **E23 重建 v2 场景** `build_case2_v2.py`（可重跑，修正后 blender_core，无 case-1 对象名）：折叠光路 + 45° 镜由路径定方向 + **Iris 布尔开真孔** + **3×MMF 连续曲线盘绕**（Holder→BC）+ **BC→MMF→PD 光路** + **PD→示波器电信号线（深蓝，可区分）** + 红色示意光束（注 1064 nm 示意配色）+ 浅灰背景柔光。出 `scene_case2_v2.blend` + 2 预览（无字总览/光纤局部）。
- **E24 可编辑 SVG 标签层** `_gen_svg.py` → `render-output/case2_v2_label_layer.svg`（26 标签，`data-target` 映射 3D 对象名）+ 系统 Python PIL 叠加 `case2_v2_overview_labeled.png`（带标签预览；3D 渲染本身无字）。
- **E25 诚实核查（本轮预览仍待外部读图）**：3 张 v2 PNG 已生成，亮度/过曝/中央带信号统计见下；**视觉对应（折叠是否正确表达、盘绕/电信号线是否可辨）尚未由读图者核实**，按 P6 交还外部；不沿用“几何全通过”结论。

## D · Case-2 R6（v3 忠实复刻参考图重建 + 逐项核查）
- **E26 参考图像素分析锁定布局** `layout_v3.md`：1152×692 px，主光轴 z=0、下方探测段 z=−0.15；M1/M2/M3 按入/出射线段求法向（不预设 90°）；**DMD 12° 入射角**（微镜衍射非镜面反射）；SLM 共光路不折返；BS 分出零级到 M3；**消除 L6 无依据转弯**；透镜/光圈法向与局部光轴一致。
- **E27 v3 真正可渲染光纤** `build_case2_v3.py` `coiled_fiber`：三条 `mmf_delay_*` = **bezier 曲线 + bevel_depth 0.004 管状截面**（盘绕 turns=4/3/2 视觉示意），Holder→BC 连续；saved scene 核查三条均 **CURVE + bevel>0（可渲染）**，**修复 R5 “0 面 mesh 不可渲染”**。
- **E28 v3 镜面法向修正**：`mirror_from_paths` 按入/出射线段求法向并记 `mirror_normal` 属性；M3 初版法向错（+x 反射为 +y），改 `force_normal=(0.707,0.707,0)` 使 +x 反射为 **−y**（saved scene 复验通过）。
- **E29 v3 标签交付修复** `_gen_svg_v3.py`：SVG 锚点=对象**世界几何位置**（光纤用曲线首控制点世界坐标，**非对象默认原点**）；**SVG 命名空间修复**（`ET.parse().getroot()` 子元素带 `{http://...svg}` 前缀，v2 裸标签匹配=0 是 bug）；系统 Python PIL **真正渲染合成**带标签 PNG，带标签 vs 无字**像素差异 25,328 px（1.759%）**（v2=0）。
- **E30 v3 浅灰 World 背景修复**：`build_case2_v3.py` **实际创建并保存** `scene.world`（BG 0.78 灰 strength 0.6），**修复 R5 “world=None 图片上方黑”**；地面缩小 2.8×2.0 m 浅灰让装置占主画面；总览 mean 0.798 过曝 0；局部不加曝（曝光 0.0）器件不变白块；保存前恢复总览相机。
- **E31 v3 核查** `verify_case2_v3.py`（真实表面射线，**非 bbox**，不用部件数量/非黑统计）：**MMF 可渲染 ✓ / Iris 真孔（14,210 mm³ < 实心 17,000）✓ / 电信号线 ✓ / M3 反射 −y ✓ / 相机入框 ✓**；**光束端点贴合未全过**（laser→L1、dmd→L3 各 8 mm 漂浮；多段射线未命中斜面——端点落在倾斜镜侧面，按段出射方向射线才准；**不宣称“端点全贴合”**），结果保留 `verify_case2_v3_results.txt`。
- **E32 视觉对应仍交还外部**：v3 折叠方向/DMD 12°/SLM 共光路/盘绕/电信号线**视觉可辨否**未由读图者核实；M1 出射角（斜向 DMD）为建模假设；盘绕/透镜/角度=视觉示意非实测。按 P6 不作像素判定。

### v3 文件哈希（md5 12 位）
| 文件 | md5 |
|------|-----|
| case2_v3_overview_wordless.png | c5c105eea869 |
| case2_v3_overview_labeled.png | 53b230bffc15 |
| case2_v3_link_fiber.png | d397be6c8348 |
| case2_v3_m1_slm_bs.png | 0a2919addfef |
| case2_v3_label_layer.svg | b0d5d1b6014f |
| scene_case2_v3.blend | 0e2b07e01b29 |

> 保留 v1（scene_case2.blend）/ v2（scene_case2_v2.blend）不删。Skill 保持 v0.2 草案，**不定稿**，等 v3 经外部读图确认后再细化。

## E · Case-2 R7（外部读 v3 核查 + 布局理解校正；本轮两个限定任务，不批量生成新 3D）
**外部判读（读 v3 四张 PNG + 复算 saved scene）**：背景/光纤可渲染/标签合成 **三项确认修复**；整体复刻未通过。
**本轮先做 A（参考图识别与布局校正）+ B（修复核查方法），先确认布局理解正确再重建 3D。**
- **E33 撤回 v3 多项结论（R7 记入 REVISION_LOG）**：
  - `layout_v3.md` 器件识别/空间布局错误（"最左激光源""下方探测支路"不符合原图；原图激光右下/DMD 左/SLM 右/光纤左上）；根因=仅靠颜色区域统计推器件身份，未结合可读标签+连续光路逐件识别。
  - 屏幕坐标上下≠世界 z：v3 把参考图下方像素区映射 z=−0.15，地面 z=−0.02 遮住整条探测支路；**撤回"装置在总览完整呈现"**。
  - **撤回"M3 真实反射方向验证通过"**：v3 仅用 mirror_normal 属性自证；外部从真实镜面复算 +x→+y（非属性算的 −y）。
  - **撤回"laser→L1 8mm 漂浮"**：实际前表面≈0mm；旧 ray_to_target 推进 1mm 进镜片量到后表面误判。
  - **撤回现有 in_frame 结果**：v3 用 visible_get 代替相机投影；外部复算 M1 在 cam_m1_slm_bs 左侧画外。
- **E34 A 参考图识别与布局校正**：`annotate_reference.py` → `reference_Fig2a_annotated.png`（独立标注副本，器件/转向点/关键作用点，绿=实/蓝=推/橙=未确认/红点=转向）+ `reference_Fig2a_annotated.md`（标注数据+完整 I/O 路径+SLM/BS 分出重判+DMD 12° 对应+未确认项）。依据=官方图注（L1~L7 plano-convex/M1~M3 mirrors/HWP/BS/MMF/BC 3×1/PD InGaAs）+ 正文光路 + 外部 R7 判读；**不写虚构像素分析结论**，无法识别列未确认。
- **E35 A 二维布局草图**：`draw_2d_layout.py` → `layout_v4_2d.png`（保留原图相对位置/折叠方向/连接）+ `layout_v4_2d.md`（连接表）。**SLM 重判为透射式相调制（不称"反射式共光路"）**；**DMD 12° 入射角对应明确入射线与参考法向（不靠旋转欧拉角声称满足，保留建模假设）**。
- **E36 B 修复核查方法 + 最小反例**：`verify_case2_v4.py` → `verify_case2_v4_results.txt`（保留）。修正 4 缺陷：不推进射线起点/真实镜面法向从几何取（非属性）/相机真投影（非 visible_get）/地面遮挡检查。**反例全部验证通过**：
  - 反例1 lens 前表面端点=接触 0.00mm（旧推进法误报 8mm 已修）
  - 反例2 M1/M2/M3 几何法向与属性**不一致**（M3 +x 经真实镜面反射=+y 非 −y）→ v3 属性自证假通过被揭
  - 反例3 M1 @ cam_m1_slm_bs=画外（与外部复算一致；v3 visible_get 误判）
  - 反例4 L5/L6/L7/Holder/BC/MMF/PD/Scope 8 件位于不透明地面 z=0 以下→总览被遮挡（证实外部指出）
  结果**分开报告接触/间隙/穿入/未命中/先碰其他**，不用部件数量或非黑统计证明复刻通过。

### 本轮交付（4 项，先确认布局理解正确）
1. 参考图标注副本 `reference_Fig2a_annotated.{png,md}`；
2. 二维布局草图+连接表 `layout_v4_2d.{png,md}`；
3. 修正后核查脚本+反例结果 `verify_case2_v4.{py,txt}`；
4. 更正记录 `REVISION_LOG_case2.md` R7 + 本 AGH 执行记录 E33–E36。

> **保留 v3（scene_case2_v3.blend 等不删）；不出正式图；Skill 保持 v0.2 草案。**
> 下一步：外部确认布局理解（标注副本/二维草图）正确后，再据此重建三维场景（不先批量生成）。

## F · Case-2 R9（第一段识别 + 核查脚本修正；未进入三维重建）
**外部判读（读 `reference_Fig2a_annotated.png` / `layout_v4_2d.png`）**：本轮布局未通过；**保留文件，更正记录，不进入三维重建**。
- **E37 撤回 R8/E34 撤回项中的错误**：原图**确有** Pulse laser/L1/L2/DMD/SLM 文字标签（本轮从 PDF 文本层实抽到）。
- **E38 A 第一段识别（改从 PDF 文本层取标签坐标）**：`annotate_seg1.py` → `reference_Fig2a_seg1_annotated.png`
  （编号 1–6 黄圆 + 红指引线，**不遮挡原标签**；STHeiti 中文字体；洋红线描摹该段红色光路）
  + `reference_Fig2a_seg1_table.md`（六行表：编号/原标签/文本层拼写/参考PNG像素/连接上下游）。
  来源方法：`pymupdf get_text("dict")` 抽第 4 页标签 → `page.get_image_rects(17)`=Rect(64.27,95.39)–(532.28,370.10) 映射到 PNG 像素（sx=2.4615, sy=2.5190）。
  **实抽第一段坐标**：Pulse laser(516,432)→L2(256,366)→L1(331,379)→M2(213,311)→M1(71,331)→DMD(81,196)。
  → 实际顺序：**激光右中，向左经 L2/L1 到 M2/M1 折叠入 DMD（左上）**；撤回 R7 “激光右下/DMD 左”粗略判读。
  文本层拼写差异：L1 抽为 `Ll`、M1 抽为 `Ml`；未确认：M1/M2 反射角、红色光路转折点为描摹近似。
- **E39 B 核查脚本修正**：`verify_case2_v5.py` → `verify_case2_v5_results.txt`（保留，**13/13 断言 PASS，exit_code=0**）。
  修正 R8 七项：单位统一（0.5mm=0.0005m）/10mm 不判接触/地面高度从 mesh 顶点取/入框查全角点+横纵+轴向裁剪/
  五分类（接触·间隙·穿入·未命中·先碰其他对象）/法向取 abs 不误判同面/可失败断言+实际结果。
- **E40 case-2 v3 实测（分开报告，不证明通过）**：ground_top_z=-0.0200，8 件待显示器件在面下（总览遮挡）；
  光束五分类多条“先碰其他对象=自身/相邻光束”（**自命中未排除**，端点贴合仍须修）；镜面几何法向 vs 属性 |dot|=0.000（v3 属性自证无效）。

### 本轮交付（仅 4 项，不画整套布局、不生成三维图）
1. 第一段标注副本 `reference_Fig2a_seg1_annotated.png`；
2. 六行对应表 `reference_Fig2a_seg1_table.md`；
3. 修正后核查脚本+结果 `verify_case2_v5.{py,txt}`；
4. 更正记录 `REVISION_LOG_case2.md` R8/R9 + 本 AGH 记录 E37–E40。

> **待外部确认第一段（Pulse laser→L1→L2→M1→M2→DMD）识别正确后，再继续 DMD→SLM 与探测支路；Skill 保持草案。**

## 图像核查方法声明（P6 红线）
- 本轮 3 张预览 PNG 与参考图的**视觉对应**（部件相对位置/光路连接/折叠成束）**尚未由读 PNG 的模型或人完成核实**；
  几何核查（关键件存在/入框/光束贴合）已自动通过，**不能顶替实际图片核查**。
- 视觉审查可由模型读图或人读 PNG，均须分别如实记录审查者；几何统计不作像素判词。
- 若读 PNG 与磁盘 md5 不符 → 记为**当时遇到的未确认现象**，交还正确文件供外部审查。

## 本轮文件哈希（md5，可复算）
| 文件 | md5 |
|------|-----|
| reference_Fig2a.png | 46d7b56d571c0a8557b4c6a3cb541b8d |
| case2_v2_overview_wordless.png | 8ca34fcf1a99…（R5） |
| case2_v2_overview_labeled.png | 9d3f0d7250f0…（R5） |
| case2_v2_link_fiber.png | decbe3f62332…（R5） |
| case2_v2_label_layer.svg | （可编辑，26 标签） |
| scene_case2_v2.blend | （R5 折叠布局 + 3×MMF 盘绕 + 电信号线 + Iris 真孔） |
| verify_case2_r4_results.txt | （射线复算，L2→M1 = 27.18 mm） |
| folded_layout_v2.md | （折叠布局草图 + 完整连接表） |

> 注：R3 的 `case2_preview_*`（旧直线布局）已被 R5 `case2_v2_*`（折叠布局）取代；旧文件保留未删。R5 预览亮度/过曝统计：
> overview mean=0.678 过曝=0.411 中央带信号=0.961；link_fiber mean=0.084 过曝=0.060 中央带信号=0.213。
> overview 过曝 0.411 偏高（地面反射 + soft_area 200 W），仍待外部读图判断是否需再降曝/收地面。

## G · R10 第一段裁剪校正与核查反例（2026-10-11，同一会话；摘要非原始 ledger 行号）
- E41 `functions.computer_use`：Preview 原图 `reference_Fig2a.png` 精确窗口截图，实际看到右下 Pulse laser、L1/L2、左下 M1、M2、左上 DMD 以及从右下向左、折返到 DMD 的红色路线；不是颜色分区推断。`functions.shell` 使用 pymupdf 第4页文字层得 Pulse laser/L2/DMD 标签框，按用户给的 clip=(64,95,352,268)×4 映射；三处在 Preview 图中文字处独立核对。R9 整张 Fig.2 图片边界误映射本张 a 裁剪图，R9 位置/路径/“激光右中”撤回，保留旧文件。
- E42 `functions.write/edit/shell`：新建并运行 `annotate_seg1_r10.py`，得到 `reference_Fig2a_seg1_r10.png` 与六行 `reference_Fig2a_seg1_r10.md`。`functions.computer_use` 再次实际查看新副本，六个引线指向器件、青色描摹遵循第一段原红线，编号未挡原标签；黄色作用点只表示目视近似。原图/旧副本未改。
- E43 `functions.write/edit/shell`：新建运行 `verify_case2_r10.py`（Blender headless）。首轮真实失败：地面测试将浮点 `location.z==.1` 精确比较，top≈.155 正确但断言失败；改为浮点容差后重跑，真实进程 exit=0，`verify_case2_r10_results.txt` 保留 16 条 PASS。非均匀缩放逆转置与变换边叉积 abs dot≈0.99999996；正交法向 abs dot=0；10mm 不会当接触；laser→L1 saved scene 只读接触距离≈2.9e−9m。其他 v3 异常仅记录，非场景通过。
- E44 本轮只交第一段标注、六行表、反例脚本及实际结果，并追加此更正记录。没有新 .blend，没有后续支路，Skill 仍是 v0.2 草案。

## H · R11 低成本三维总览（2026-10-11，摘要，关联本会话工具事件）
- 约 06:45–06:50 UTC，`functions.read` 读取历史证据与脚本，`functions.shell` 用 pymupdf 读 PDF p.8 的 DMD 入射 12°、p.9 的 blazed grating/空间分离与 dichroic prism/M3。此前 `functions.computer_use capture` 曾成功展示 Fig.2(a) 原图；新 PNG 的 `computer_use list_windows/capture` **失败**（见下）。
- `functions.write/edit` 新建并迭代 `build_case2_v4_overview.py`；`functions.shell` 执行 `/Applications/Blender.app/Contents/MacOS/Blender -b --factory-startup -P build_case2_v4_overview.py`：首次 AgX look 枚举错误失败；修正后最终真实进程 **exit=0**，输出 `.blend` 137616 B 与 PNG 915779 B（1200×750、Cycles 24 samples）。保存前 scene.world/overview camera 有效。旧 v1/v2/v3 保留。
- `functions.write/edit/shell` 独立核查 `verify_case2_v4_overview.py`：首轮 SLM 返程误用物体中心向量失败（dot=.99481），改用真实作用面点后最终 **exit=0，GEOMETRY 0 failed**；6 个光学命中点在网格面、镜面法向与反射方向、SLM 返回 BS、3 根有厚度盘绕光纤/输出纤/电缆、地面上方与入框角点等结构性检查见保留结果。**未做可读性/遮挡视觉判定**。
- `functions.shell` 启 Preview 窗口；`functions.computer_use list_windows/capture(app='预览')` 多次返回 `Computer Use windows discovery failed`。**本轮未实际读取新 PNG 像素，未完成并排视觉核查；不报告“复刻通过”**。仅提交低成本待审草案与文件版本哈希：脚本 sha256 `6dbcb7287f66d34f…`；saved blend `a06305b91d54ce87…`；PNG `334479eece2a81dd…`；核查结果 `0e7afb151983d3ec…`（`functions.shell` 2026-10-11T06:50:55Z）。
- `CASE2_V4_OVERVIEW_DRAFT_REPORT.md` 记已知简化差异和未确认项；不将几何/文件哈希/亮度替代视觉审查。Skill 不晋级。

## I · R12 v5 低成本预览（2026-10-11，sessionKey 360fa855-0fd0-430f-ad31-8e0da1e94661）
- `functions.read`（本会话）：读取 v4 构建脚本、v4 saved-scene 核查脚本、v4 报告。`functions.computer_use list_windows` → `Computer Use windows discovery failed`；稍后 `list_apps` → `Computer Use apps discovery failed`。旧参考图在历史会话已有记录；**未看到新的 v5 PNG**。
- `functions.shell` 复制 v4 源码与验证脚本为 v5 专用文件；`functions.edit` 分批改光束、镜片、材质、器件、柔性曲线及相机。Blender 5.1.2 内查询 Principled 输入证实 `Transmission Weight`/`IOR` socket 存在。
- `functions.shell` 首次运行 v5 构建出 `Bus error: 10`（exit 138），读取保存的 .blend 低样本渲染同样 SIGBUS（exit 134）；v4 .blend 同命令可渲染；删 v5 曲线仍失败、删 mesh 成功、删 7 片凸透镜成功。随后 `mesh.validate(verbose=True)` 指出 invalid vertex/重复面。`functions.edit` 修正背面索引和外缘环，并把 mesh.validate 纳入构建 fail-fast；这些失败版本**没有交付**。
- 最终 `functions.shell`：`/Applications/Blender.app/Contents/MacOS/Blender -b --factory-startup -P build_case2_v5_overview.py` 产出 `WROTE … scene_case2_v5_overview.blend … case2_v5_overview_wordless.png parts 89`，进程 exit=0。`Blender -b --factory-startup --python verify_case2_v5_overview.py` → **196 PASS、GEOMETRY 0 failed、exit=0**，结果留存 `verify_case2_v5_overview_results.txt`。自动备份的无效 `.blend1` 已删，v4 hash 不变。
- `functions.shell`（2026-10-11T07:10:09Z）：v5 脚本 SHA-256 `3fa69e011f5a55c629910086b1fda820148371ea20a713b9377856663395ee4f`；核查脚本 `8d58f1ce4740e658e9e99cfeb7b111ffae194092e40743fdeb0fc604ca76a126`；.blend `cdc05b06a96046334e3efbd56591a48262cb9601e8006f14b3e850e7945ddf39`（213683 B）；PNG `eff78f943fd03928c676df6fd2895c6b36574715171c9c2a67d695e0124a6663`（913278 B，1200×750）；核查结果 `d7dc5aec917b104394a8c57091723a1d4c74c9ca37865167eea756330dca24fd`。v4 三文件哈希仍为 `6dbcb728…`、`a06305b9…`、`334479ee…`。
- **视觉审查未完成**：文件大小、哈希、PIL 尺寸/均值、几何验证不是图像观察，未报告外形/遮挡/相似度通过。外部请直接读 v5 正确 PNG 版本后反馈；Skill 草案，未晋级。
- **I 节最终重跑订正（2026-10-11T07:11:51Z，`functions.edit/shell`）**：构建脚本加入 `bpy.context.preferences.filepaths.save_version=0` 避免每次重跑产生 `.blend1`；重建 `WROTE … parts 89`，复核 `GEOMETRY 0 failed`，exit 均 0，目录无 `.blend1`。此段为**最终版本**：脚本 SHA-256 `e88c8b37643bf73daa17d4596b854120d7d9e9ccd4e7bdf7809291b58effdddc`；.blend `5e57f74d0162a1f175090a09b7fdc300feeda304b28ee8c35bf12936afee8620`（213716 B）；PNG `b1ccd71909c97608d438ad8889b76b617b39e065c5f195b8daf42200fa3c2dfe`（913278 B）。上段的 v5 制品哈希是中间版本，**不得用于最终视觉审查**；核查结果 hash 不变 `d7dc5aec…`。

## J · R13 v6（2026-10-11；AGH 工具事件摘要，sessionKey 360fa855-0fd0-430f-ad31-8e0da1e94661）
- 先前两个“继续”请求因文件权限被拒时，`functions.read` 返回 E_FS_DENIED，未动项目。此次 `functions.read` 成功读取 v5 两脚本；`functions.shell` pymupdf 从 `source_paper.pdf` p.4/8/9 核实 Fig.2 图注 plano-convex、扩束准直描述和 SLM/BS 路由。权限变化仅据成功返回确认。
- `functions.shell` 复制 v5 文件为 `build_case2_v6_overview.py`、`verify_case2_v6_overview.py`；`functions.edit` 分批修改公共轴/平凸镜/BS 单四边形真实作用面/开放外框、材质和相机；脚本构建日志的 `AXIS_SHIFT` 逐器件给出 4–38 mm 的位置协调量。
- `functions.shell`：`/Applications/Blender.app/Contents/MacOS/Blender -b --factory-startup -P build_case2_v6_overview.py` → `WROTE … scene_case2_v6_overview.blend … case2_v6_overview_wordless.png parts 94`，exit 0。`Blender -b --factory-startup --python verify_case2_v6_overview.py` → **247 PASS / 0 FAIL，exit 0**（保留核查结果文件）；真实 BS 四边形法向反射 dot≈1、双向 ray-cast 命中同一点、开放框架抽样无碰撞；公共轴最大误差 <0.0002 mm。
- `functions.write` 新建 `crop_case2_v6.py`，`functions.shell` 执行，源 PNG sha256 `a93fe93d81ab4b89…`，两裁图 bounds (384,390,1008,608) / (816,292,1200,578)；PIL `ImageChops.difference(source.crop(bounds),crop).getbbox() is None` 双图均 True。注意这仅核查裁图真实性，**不代表图像好看/符合论文**。
- `functions.computer_use list_windows` 成功发现 Preview 既有参考/v4 窗口；但 `capture(mode='vision', pid=26225,window_id=11919/11625)` 均报 `Computer Use capture failed`，`capture(app='screen')` 报 full-desktop capture disabled。**本轮未在 AGH 中实际读到 v6 PNG**；图片视觉判定留给外部读最终文件，不把 hash/PIL/几何 PASS 当图像观察。
- `functions.shell` 2026-10-11T07:41:30Z 最终 sha256：v6 构建脚本 `349a2086be5d9caba8f5c0d03d7dfd6b861b83bf6781b3a4cc6dc273b2e29cdf`；核查脚本 `044aefa1349bdabee23b96dd106f6670b15cd897bb8e673d20242abf4def0889`；裁切脚本 `b30aa1e3ac016e11a2c9726e01d4c3c6f890d7cf4d6da6b57db4ebb88c4a6e15`；.blend `2847a66054fd57bcd4203063404baf5e09e4ec3d5d4cc9c56601200350721a7a`；总览 PNG `a93fe93d81ab4b8924166c30bb5c74238d9f7eb27e6c2f46f8904c7078f60271`；两裁图 `0f6d005af3a824c3dd6209c1427a914b966bbb929e88202644a5181d14e4ecca` / `ba7f67c7eea1987a6d03e4f32b257da97e9ec66efff3016053c51c3f591850ce`；核查结果 `a623d3a873737a17408bd02fbce529671f2228e733fb6a8f370ee083289fdb5d`。

## K · R14 激光出口 v7（2026-10-11，AGH 工具事件摘要）
- `functions.read` 读取 v6 建模脚本多个片段和 v6 真实面/公共轴验证片段。`functions.shell` 拷贝为 v7 并用 `functions.edit` 更改：真网格机壳面求交、外置空心出光嘴、安装圈/孔圈、首束嘴尖开口锚点与重新共线；其余系统不修改。
- 第一次 `functions.shell`：Blender `-b --factory-startup -P build_case2_v7_overview.py` 保存 v7 .blend/PNG、parts 95、exit 0；`Blender -b --factory-startup --python verify_case2_v7_overview.py` → GEOMETRY 0 failed / exit 0。随后 `functions.shell` 发现 3 个 v7 `.py` 文件短暂消失、原因未知；保留旧 .blend/PNG/结果，不宣称脚本已交付。用 v6 源加本轮相同修正重新生成 3 个 v7 脚本；**再次构建/验证**成功，且无 `.blend1` 自动备份。历史两个运行过程以工具结果为证，不能推断文件消失原因。
- `functions.shell` 重跑 `python3 crop_case2_v7.py`：总览、两旧检查范围和新出光口局部均生成；嘴局部 bounds=(816,472,1104,645)，288×173，早期裁图逐像素与总览片段相同。`functions.computer_use list_windows` 仍返回 `Computer Use windows discovery failed`，没有实际 PNG 视觉评审。
- 最终进程验证 `verify_case2_v7_overview_results.txt`：260 PASS / 0 FAIL；出口首点—环顶点重算圆心误差约 0.00003 mm；内孔半径 4.50 mm vs 2.00 mm 示意红束；法兰壳面间隙 0；嘴尖距壳约 29 mm；五条抽样光线不穿金属。重新核对上述几何，不将 PASS 冒充视觉通过。
- `functions.shell` 最终 source/scene/image SHA-256（重跑后）：建模脚本 `e3275adc9e9e0912d7e162df80d9c52caacf696a027dec0ec419b56f6363d9c0`；验证脚本 `e0a8b5c7703c3f297d20f04eb947cd62524f197674c4652d90c2a5841a0cfd04`；裁图脚本 `8ec2ad629621a9143cea6616b3fc51ba4d15586afd80372c198331f3171b960c`；saved blend `895c41f0024dba0625b05b3c0b7aebd09ce6d6f55ee033a945be69d72aae8b1b`；总览 PNG `949e4589d00255467a3e5907de851ebcb1c60b802d349f8c16bb7c13b3c3618c`；嘴裁图 `2256bec058509f2318c3e9dcc269d5dbbe9354189f636dd0890ec0708e828a97`；验证结果 `3fa09e144cfaf3186c1073429ab078be7d42948876aee0b714a93e81cfd7a373`。文件哈希是版本定位，不是图片观察。
