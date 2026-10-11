# Skill v0.3 试用版｜编写、更正与 AGH 执行记录

**Skill**：`agh-research-figure-skill/skills/agh-scientific-equipment-renderer/`
**版本**：v0.1 草案 → v0.2 纠错 → **v0.3 试用版（2026-10-11）**。
**来源**：两个公开光学案例：case-1 ⁸⁷Sr 冷冻光晶格钟与 case-2 D2NN OAM-STM Fig.2(a) 的真实迭代、失败版本和撤回记录。case-1 有正式图；case-2 仅有低成本预览，用户允许本轮更新 Skill，**未出正式图**；材质对比**未应用总览**。
**状态**：有限案例经验的试用版，不宣称全领域或 CAD 级复刻验证。文件系统可发现≠此会话已成功通过 Skill 加载工具：本轮 `skill_read(name="agh-scientific-equipment-renderer")` 返回 NOT_FOUND。

## v0.1–v0.2 历史轨迹（E# 为动作摘要，见会话 sessionKey `360fa855-0fd0-430f-ad31-8e0da1e94661`；非原始 ledger 行号）

以下“下一案例门槛”等仅为**当时的历史计划**，v0.3 状态以后文为准。
| E# | 工具 | 动作 | 结果 |
|---|---|---|---|
| E1 | `skill_helper_creator` | 读取上游 skill-creator 指导（Anthropic skills，commit 34040c9…） | 按指导起草；name 用 ASCII 目录标识，SKILL.md frontmatter 可用中文显示名 |
| E2 | `read`/`shell` | 复读 case-1 `build_blender_v16.py`（100/220/500/560/690/770 行等）、`verify_v16.py`、`notes_wavelengths_and_state.md`、`REVISION_LOG.md` | 定位可提取的通用助手与失败→修正证据链 |
| E3 | `shell` | 建目录 `skills/agh-scientific-equipment-renderer/{references,scripts}` | 目录就绪 |
| E4 | `write` | `SKILL.md`（主文件：名称/用途/适用范围/六阶段流程/验收方式/v0.1 草案标注） | 主文件 ≤3k 字，简洁；详细经验链接到 references |
| E5 | `write` | `references/pitfalls_and_fixes.md`（P1–P14，每条含 触发/适用/行动/本案例证据 + 通用性标注） | 故障经验按需放置 |
| E6 | `write` | `scripts/blender_core.py`（几何/材质/相机/布尔/核查/渲染助手，去 case-1 对象名与硬编码坐标） | 可复用脚本，`beam()` 记录端点、`glass_mat()` 输入名兼容、`solid_inter_mm3()`、`LocalRenderRule`、`clip_check` 有符号 8 角 |
| E7 | `edit` | 清理 `blender_core.py` 中 `beam_via_point` 冗余分支（P3 表述简化） | 脚本收敛 |
| E8 | `write` | `references/workflow_checklist.md`（分阶段可勾选清单 + 验收标准，逐条挂 P 编号） | 清单齐 |
| E9 | `write` | `references/evidence_index.md`（每条可复用方法 → case-1 证据文件位置 + 通用/case-1/假设/待验证 分列） | 证据索引 |
| E10 | `write` | `scripts/check_structure.py`（结构 + 通用性检查：确认通用文件未混入 case-1 对象名/硬编码坐标） | 结构检查脚本 |

## 结构检查结果
运行 `scripts/check_structure.py`（在案例目录）应输出：
- 5 个必需文件（SKILL.md / references 三件 / scripts/blender_core.py）均存在；
- `SKILL.md` 与 `scripts/blender_core.py` **无** case-1 对象名/硬编码坐标混入（通用默认值干净）；
- case-1 特定证据只允许出现在 `references/`（明确标注"本案例证据"）与 `evidence_index.md`。

## 通用性边界（草案标注，非定稿）
- **可推广原则**：证据基础先行、低成本预览→正式、中轴线端点核查、入射端真接壁面、独立玻璃材质、
  自动核查≠图片核查（红线）、剖切不充光学界面、独立复算、局部隐藏还原、mm 近裁剪面、文件版本区分、
  执行记录可核查。
- **仅 case-1 验证**：右壁双独立玻璃窗布局、45° 斜向冷却光、具体隐藏集合与相机参数、`key_parts_ok` 对象清单。
- **装置特定假设**：铜腔/蓝宝石后窗/二向色镜=拟建；壁厚/窗口/承座尺寸无论文依据；后窗固定/密封 UNCONFIRMED。
- **仍待验证**：跨公开案例的可触发性、核查模板参数化迁移、局部隐藏规则自动推导、无人读 PNG 时的诚实降级。

## 当时拟用于下一公开案例的检查项（历史计划，现已有 case-2 迭代）
1. 证据基础表能否跨装置结构复用。
2. 自动几何核查模板能否参数化迁移（不同对象名/拓扑）。
3. 局部隐藏规则能否自动推导而非手工挑对象名。
4. 实际图片核查流程（缓存/版本判定 + 诚实降级）在无真人读 PNG 时是否成立。
5. 相机/近裁剪经验在不同尺度装置上是否适用。

## 修订约定
- 后续公开案例运行本 Skill 后，按真实结果修订 P 编号与通用性边界；**保留本文件的 AGH 编写/修订轨迹**。
- 不得把装置特定默认值（尺寸/坐标/相机/隐藏件）提升为通用默认；只把**方法与原则**提升。

## v0.2 修订记录（外部核查修复，2026-10-11）
- **A1 frontmatter**：SKILL.md 补 YAML frontmatter（name/description）；当时按扫描根设置 `.agh/skills/` 软链接。目标路径可读到 frontmatter 只是**文件系统证据**，不等于当前 AGH 运行时可调用；v0.3 本会话 `skill_read` 为 NOT_FOUND，需另行确认实际启用/加载。
- **A2 clip_check**：目标 bbox 先 `o.matrix_world` 到世界坐标，再 `cam.matrix_world.inverted()` 到相机系；
  全 8 角在相机后方时不得判“完整通过”（返回 in_range=False + 注明）。
- **A3 solid_inter_mm3**：按 A 的世界变换 `det(matrix_world)` 归一世界体积；文档化 depsgraph 刷新前提。
- **A4 beam_crosses_point**：新增 `beam_axis_world`，端点属性过期（与当前世界 bbox 对角线不符）时返回
  None → `axis_known=False`，不作“经过目标”通过证据；无端点属性不回退包围盒对角线。
- **A5 LocalRenderRule/key_parts_ok**：must_keep 缺失/被隐藏时**阻止渲染**；异常也还原；关键件分层报告
  exists/renders/in_frame，不把“可见”混为一谈。
- **A6 去 case-1 硬编码**：五视角/9-10 关键件/1600×900@96 降级为“案例配置示例”；已实现/拟建由当前来源决定。
- **A7 经验与记录更正**：P2 不把构造保证改写为“包围盒假阳性”；P6 读 PNG 不符哈希记为未确认现象；
  视觉审查区分模型/人读图；E1–E10 是可在会话账本内审计的**动作摘要**，非原始 ledger 行号。
- **A8 结构检查强化**：`check_structure.py` 校验 frontmatter/引用文件/退出码，并新增 `behavior_tests.py`
  真实 Blender 反例行为验证（T1 世界缩放/T2 相机后方/T3 过期端点），结果保留 `behavior_results.txt`；
  不再只靠字符串黑名单宣称通用性。

## v0.3 本轮修订（试用版；AGH 会话内真实执行）
- `skill_read` 按现名请求先于文件编辑，返回 `NOT_FOUND`；随后只读用户指定目录。文件系统文档更新**不等于运行时 Skill 已可调用**，本轮不声称安装/启用成功。
- `read` 核对 SKILL、PROVENANCE、三份 references、结构脚本及 case-2 旧修订/执行/材质候选记录；`write`/`edit` 更新五份 Skill 文档。保留 P2/P6 和 case-2 R4/R7/R10/R14 的撤回链，不修改任何 case-1/case-2 模型、PNG 或 .blend。
- 仅针对已存在的**引用检查漏查实际 Markdown 链接**这一功能缺口修 `scripts/check_structure.py`；并要求 Blender 反例进程退出码为 0。`scripts/blender_core.py` 原来把 case-1 的 32 采样/1600×900、mm 相机裁剪及窗材质 RGB/粗糙度/IOR 作为默认值，本轮改成任务显式传参（`setup_scene` 缺样本/尺寸即报错；相机未给参数才沿用 Blender 本机值）；理想透射玻璃助手仍提供可覆盖的 `transmission=1.0` 预设，并明确不能据此断定视觉通过。没有扩建几何框架。
- 本轮运行 `python3 scripts/check_structure.py`：frontmatter/name/description、SKILL 中 6 条真实引用、通用文件静态检查及 Blender 行为测试 T1/T2/T3 **全部通过，exit 0**；结果覆盖写入 `behavior_results.txt`。另逐条解析 5 份 Markdown 的**41 个本地链接**，缺失 0；五份文档均明示 v0.3。受影响链接功能又以**内存注入缺失链接**反例验证：报告缺失、结构检查返回 1，真实文件没有改动。以上只证明结构/已有反例功能，不证明 Skill 加载或三维复刻泛化。
- 受影响功能实际在 Blender 验证：`setup_scene()` 无参数按设计报错、显式 7 采样/312×188 生效；未指定相机光学参数使用 Blender 本机值，显式 lens/clip 生效（首次测试用浮点精确相等误失败，改为 1e-6 容差后四项通过）；`glass_mat` 显式材质配置的透射/IOR 参数通过。**兼容边界**：历史 `case-2_D2NN_OAM2/build_case2.py` 的无参 `bc.setup_scene()` 现在需显式补参数才能重跑；未修改该失败版脚本、未重渲案例。case-1 是正式图案例；case-2 是低成本预览迭代且获用户许可沉淀方法，尚无正式图，v10 灰粉材质未通过外部读图，材质候选比较未应用总览。其他科研装置、厂家 CAD、源端安装强度、未给出的光学参数、自动外观通过均未验证。
