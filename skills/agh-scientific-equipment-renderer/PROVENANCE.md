# Skill v0.6 试用版｜编写、更正与 AGH 执行记录

**Skill**：`agh-research-figure-skill/skills/agh-scientific-equipment-renderer/`
**版本**：v0.1 草案 → v0.2 纠错 → v0.3 试用版 → v0.4 本地候选 → v0.5 本地/Git → **v0.6 本地开发（2026-10-11；安装与运行时版本独立）**。
**来源**：两个公开光学案例：case-1 ⁸⁷Sr 冷冻光晶格钟与 case-2 D2NN OAM-STM Fig.2(a) 的真实迭代、失败版本和撤回记录。case-1 有正式图；case-2 仅有低成本预览，用户允许本轮更新 Skill，**未出正式图**；材质对比**未应用总览**。
**状态**：有限案例经验的试用版，不宣称全领域或 CAD 级复刻验证。旧 NOT_FOUND 是 v0.3 起草时的历史事实；后续已按第 77–80 行所载在运行时成功读取 v0.3。**本地 v0.6 / Git 同步本身不等于已安装、已启用或运行时已读到 v0.6；此前 SKILL_TARGET_CONFLICT 不得以 shell 覆盖安装快照。**

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
  当时报告 exists/renders/in_frame；其中 in_frame 实际仅调用 clip_check 检轴向，这一旧命名误导在 v0.5 更正，历史使用者不可据旧键断言完整入框。
- **A6 去 case-1 硬编码**：五视角/9-10 关键件/1600×900@96 降级为“案例配置示例”；已实现/拟建由当前来源决定。
- **A7 经验与记录更正**：P2 不把构造保证改写为“包围盒假阳性”；P6 读 PNG 不符哈希记为未确认现象；
  视觉审查区分模型/人读图；E1–E10 是可在会话账本内审计的**动作摘要**，非原始 ledger 行号。
- **A8 结构检查强化**：`check_structure.py` 校验 frontmatter/引用文件/退出码，并新增 `behavior_tests.py`
  当时的 Blender 反例验证（T1 世界缩放/T2 自称相机后方/T3 自称过期端点），结果当时保留于 `behavior_results.txt`；**T2/T3 后经数值审查有误，见下方更正**；
  不再只靠字符串黑名单宣称通用性。

## v0.3 本轮修订（试用版；AGH 会话内真实执行）
- `skill_read` 按现名请求先于文件编辑，返回 `NOT_FOUND`；随后只读用户指定目录。文件系统文档更新**不等于运行时 Skill 已可调用**，本轮不声称安装/启用成功。
- `read` 核对 SKILL、PROVENANCE、三份 references、结构脚本及 case-2 旧修订/执行/材质候选记录；`write`/`edit` 更新五份 Skill 文档。保留 P2/P6 和 case-2 R4/R7/R10/R14 的撤回链，不修改任何 case-1/case-2 模型、PNG 或 .blend。
- 仅针对已存在的**引用检查漏查实际 Markdown 链接**这一功能缺口修 `scripts/check_structure.py`；并要求 Blender 反例进程退出码为 0。`scripts/blender_core.py` 原来把 case-1 的 32 采样/1600×900、mm 相机裁剪及窗材质 RGB/粗糙度/IOR 作为默认值，本轮改成任务显式传参（`setup_scene` 缺样本/尺寸即报错；相机未给参数才沿用 Blender 本机值）；理想透射玻璃助手仍提供可覆盖的 `transmission=1.0` 预设，并明确不能据此断定视觉通过。没有扩建几何框架。
- 本轮运行 `python3 scripts/check_structure.py`：frontmatter/name/description、SKILL 中 6 条真实引用、通用文件静态检查及 Blender 行为测试 T1/T2/T3 **全部通过，exit 0**；结果覆盖写入 `behavior_results.txt`。另逐条解析 5 份 Markdown 的**41 个本地链接**，缺失 0；五份文档均明示 v0.3。受影响链接功能又以**内存注入缺失链接**反例验证：报告缺失、结构检查返回 1，真实文件没有改动。以上只证明结构/已有反例功能，不证明 Skill 加载或三维复刻泛化。
- 受影响功能实际在 Blender 验证：`setup_scene()` 无参数按设计报错、显式 7 采样/312×188 生效；未指定相机光学参数使用 Blender 本机值，显式 lens/clip 生效（首次测试用浮点精确相等误失败，改为 1e-6 容差后四项通过）；`glass_mat` 显式材质配置的透射/IOR 参数通过。**兼容边界**：历史 `case-2_D2NN_OAM2/build_case2.py` 的无参 `bc.setup_scene()` 现在需显式补参数才能重跑；未修改该失败版脚本、未重渲案例。case-1 是正式图案例；case-2 是低成本预览迭代且获用户许可沉淀方法，尚无正式图，v10 灰粉材质未通过外部读图，材质候选比较未应用总览。其他科研装置、厂家 CAD、源端安装强度、未给出的光学参数、自动外观通过均未验证。

## v0.3 定向更正｜T2/T3、端点坐标系与加载边界（2026-10-11）
- **撤回**：旧 `behavior_results.txt` 的“T2 相机后方 11m PASS”实际是相机 z=11 向 -z 看，物体 z=0 在相机**前方** 11m、超过 far=2m；旧测试靠消息带“后方”文字断言，不能证明真后方。旧 T3 用原点对称轴，世界端点被 `matrix_world` 重乘且属性/世界 bbox 的长度差 0.1m 阈值无效；“过期端点”不是准确坐标系解释。历史文字保留为撤回说明，当前 `behavior_results.txt` 用真实反例覆盖。
- **修复**：`clip_check` 对混合前后 8 角返回 False，不把跳过的后方角点称为完整轴向裁剪通过；`beam()` 将创建时世界端点逆变换存入局部属性，`beam_axis_world` 核对局部网格端截面中心后转当前世界，`beam_crosses_point` 不再二次乘世界矩阵。旧端点属性（若按世界坐标存储）不能不经迁移直接复用；轴校验仅适用于直圆柱且局部网格未重塑，不涵盖镜面/曲线光束。
- **本轮实际执行**：2026-10-11 本会话先误调用 `skill_helper_creator`，返回 `WEB_BLOCKED_URL` 并要求停止；当时已停止，**本轮未重试 creator，也未绕过安装审批**。随后收到用户新的明确要求，直接编辑已有本地 Skill；`edit` 更新 `scripts/blender_core.py`、`behavior_tests.py` 与本文/P2/P10，`shell` 运行 `python3 scripts/check_structure.py` 退出 0；真实 Blender 输出 T1=8.000 m³，T2 四类深度 [0.95,1.05]/[10.95,11.05]/[-1.05,-0.95]/[-0.2,0.2] m，4/4 PASS；T3 非原点非对称及平移、旋转、父级变换网格中心最大误差 0.0000003m，旧点不通过、属性篡改及缺失失败关闭，8/8 PASS。**这些是局部行为测试，不等于案例渲染通过。**

## v0.3 运行时资源加载核验（2026-10-11，后续轮次）
- `skill_helper_import` 对已有本地目录以 `scope=user, enable=true` 提交审核，proposalId `skill-install-38147046-d05b-49e9-9713-02851b1bc0bd`；前一轮 `skill_helper_install(action=commit)` 返回 `running`，当时**不算成功**。
- 本轮 `skill_helper_install(action=status)` 返回 `state=ready`、`phase=complete`、`effective=next-turn`，`resourceId=skill/user/user-agnes/9c1cae1d1c3aee1a971160ce46dd52ab10785e28ea8577da22cde9ef6a7d4bcf`、`revision=d15965f5e5ee534aaea1e5121d35c19b8d64799a1280c6bd4b148fbc8455a962`、`scope=user`、`fileCount=11`。该响应未单独提供 trust/desired/actual/winner 字段，不将其推断为已核对。
- 本轮 `tool_search` 找到唯一同名可读 Skill（描述明确为 v0.3 试用版）；随后实际调用 `skill_read(name=agh-scientific-equipment-renderer)` **成功**，返回与上述一致的 `resourceId`、`revision`，目录 `/Users/wht/.agh/skills/agh-scientific-equipment-renderer`，正文标题为「科研装置三维渲染｜v0.3 试用版」。这证明该资源在本轮可发现且可读取，不证明跨领域效果。**本段追加在导入后，已安装 revision 对应导入时快照；本地此后追加的 PROVENANCE 核验记录不能据此声称已同步到已安装快照。**

## v0.4 本地候选｜软体机器人 case-3 阶段收口（2026-10-11）
- 本会话实际调用运行时 `skill_read(name=agh-scientific-equipment-renderer)`，成功读取的是**已安装 v0.3**（revision `d15965f5e5ee534aaea1e5121d35c19b8d64799a1280c6bd4b148fbc8455a962`）；此时本地 v0.4 尚未安装，不可拿这次读回宣称 v0.4 生效。
- 用户明确接受 case-3 **限定修正的阶段预览**，而非全部装置功能或正式图。五版脚本/场景/总览、局部图与纠错记录保留，见 [阶段收口](../../case-3_soft_robotics/STAGE_ACCEPTANCE.md)。本例实际发生：v01 方块软指/平顶与「织物」误称；v02 以管端位于短节体积误近似连接；v03 收窄结论但仍留示意端点；v04 独立灰夹体仅改善外观附着，外部指出流体连接未解决；v05 查出版方高清 Fig.3b，删除无来源夹体，管线只延续至蓝套/深色双线组件遮挡，隐藏接口、孔道、密封、供/室压身份仍未知。论文 Methods 明确 `soft-foamed body`，旧织物是外观假设。
- 本轮将**可推广方法**而非本例几何参数写入 `SKILL.md`、`references/workflow_checklist.md`、`references/pitfalls_and_fixes.md`（P21–P24）和 `references/evidence_index.md`：逐跳核对管线→接口→所属器件；机械/流体/电连接分判；遮挡后不猜；锁装配轮廓与来源材料；用户阶段接受即可沉淀，但不虚报隐藏连接。现有 `scripts/blender_core.py` 与行为测试已经覆盖其原有光学局部反例，本例没有抽象出可靠的通用几何助手接口，**本轮不扩建脚本、不将气路检查伪装自动化**。
- **尚未验证**：其他材料/气动/电气系统精确端口、密封与连续流道、厂家 CAD、跨域批量渲染、自动识别遮挡与图像复刻质量。P22 的电连接为分类原则，非已实测电连接案例；v05 只获阶段认可，不把未知接口写为 PASS。按现有流程运行 `scripts/check_structure.py` 是结构/旧行为测试，不是本例气路功能或九案例视觉验收。
- **本地核查**：本轮从仓库根目录实际运行 `python3 skills/agh-scientific-equipment-renderer/scripts/check_structure.py`，退出 0；结构、frontmatter、引用与原有 Blender T1/T2/T3 反例通过。另检查主文件/PROVENANCE/references 合计 61 个本地 Markdown 链接，缺失 0。首次误用根目录 `scripts/check_structure.py` 报不存在，改用正确路径后才成功；首次链接检查发现 PROVENANCE 从 Skill 根引用 case-3 多了一层 `../`，更正后复检 0 缺失。上述均不验证气路、视觉泛化或未来九例。
- **当时流程边界**：本地文件更新、受控安装提交/完成、后续轮次 `skill_read` 读到 v0.4 是三个独立状态；安装状态与运行时读回须在实际工具结果出现后追加记录。当时未收到其余案例材料清单，这只是该时间点的历史限制；后续用户已指定 03–10 来源并完成低成本迭代，见 v0.5 段。

## v0.5 本地修订｜03–10 批次有限外部读图（2026-10-11）
- 本轮用户明确授权本地 Skill 与现有 Git upstream 同步。输入限本地 v0.4、已记录的八例源码/检查点与用户转述的**外部模型实际读图**；不读取/复制/引用原 Scientific-System-Renderer Skill/代码或未发表结果。case-03/04/10 的最新 v04，05 v05，06/09 v02，07/08 v03；全部为低成本阶段形态，不是用户最终验收。外部模型后来实际看 07 v3 裁图，确认 b、顶部/右侧 Reference Electrode、底部三标签完整且排除 a/数据图；仅证明裁图审查范围正确，不证明流路功能。
- 抽取 P25–P28 并与既有 P1/P9/P10/P21–P24 合并：先锁整体装配/朝向/比例（08 竖板与 10 顶面条片），布尔实孔与图形标记分离（05/03）；连接两端与归属分列（09 视觉贴合不是受力、07 完整装配范围不是功能闭环）；透明材质随引擎与真实 PNG 调整，05 v04 先修入框，v05 换透射后**外部模型**认为孔壁/板间可辨。03 v04 删重复跨柱线，10 v04 删无源前壁灰件；其它已改善项无需重渲。具体孔参数/材质与裁框留于案例检查点，不作默认。
- 修 `scripts/blender_core.py`：`clip_check` 保持仅轴向 near/far；`key_parts_ok` 从误导的 `in_frame` 改为 `in_clip_range`，删除旧键而不将其默认映射成全入框（旧调用者须显式迁移）；横/纵投影与遮挡**不在该助手内实现**，按任务独立报告。`behavior_tests.py` 新增 T4 反例：目标轴向在裁剪内但水平/垂直画外、无相机/缺失对象为 None。此行为变化不追溯改变 case-2 旧脚本或旧通过表，旧 `in_frame` 宣称不可作为全角点入框证据。
- 保留 v0.1–v0.4 的历史更正和 AGH 索引；新批次落盘执行及外部反馈见 [最终审查状态](../../FINAL_EXTERNAL_REVIEW_STATUS.md)、[07 裁切检查点](../../FINAL_REFERENCE_CROP_V3_CHECKPOINT.md)、[批次 v05 状态](../../V05_BATCH_STATUS.md)。07 仍只称**范围改善、功能拓扑未验证**；外部模型阶段反馈不是用户验收或跨领域验证。该会话已加载的仍是 revision `d15965f5e5ee534aaea1e5121d35c19b8d64799a1280c6bd4b148fbc8455a962` 对应的 v0.3，更新本地/Git 不能替代受控安装和后续 skill_read。
- **本地行为核查**：`python3 skills/agh-scientific-equipment-renderer/scripts/check_structure.py` 实际退出 0，Blender T1 8m³、T2 4/4、T3 8/8、T4 10/10（水平/垂直越界但轴向通过）均 PASS；91 条本地 Markdown 引用缺失 0，`git diff --check` 无报错。该结果不验证 03–10 PNG 外观或 07 功能拓扑。此轮修改以前已存在的 v0.4 工作区未提交差异（尤其 T2/T3 更正）一并审查提交，原始历史与撤回保留。新 `in_clip_range` 是有意破坏旧 `in_frame` 字典键的兼容变更；case-2 早期调用脚本只读 exists/renders，其他使用者须迁移，不在本轮重渲旧案例。

## v0.6 本地能力补齐｜合成工具而非科研验收
- 只读本项目现有 Skill、公开案例检查点及当前用户/外部模型实际反馈；**未读原 Scientific-System-Renderer Skill、脚本或历史制品，未用未发表成果**。保持先整体 3D 预览。新增独立可拷贝的可选记录/例子与静态校验，保存场景审计，以及 PNG 数值裁图和目标网格锚定的可编辑 SVG 标签层；按需域检查保留在 `references/domain_checks.md`。既有开发仓库旧案例链接属可选证据档案，新工具/例子均在 Skill 内，不依赖本机 `/Users/wht`。
- **记录/审计边界**：无必需范围 UNKNOWN，缺 required 组件/连接/支撑与错端口/介质 FAIL；场景审核读磁盘 `.blend`，评估后网格三角面求锚点归属及有限支持近接，曲线/简单直圆柱取真实端点，投影分水平/垂直/near-far。未支持复杂曲面束、遮挡、碰撞、受力、密封、真实流路/电路则 UNVERIFIED；无字任务拒绝 SVG 标签，数值图片报告不判视觉。部件/端口改动的依赖记录重查，不替旧结论静默过关。
- **真实修订轨迹**：首次有效场景审核发生局部变量 `checks` 覆盖报告列表的 Python 异常（`10468`），修成 `projections_checks` 后独立重开场景 PASS（`10502`）。首次水平画外反例以世界 X 平移误使物体越相机背面、深度 FAIL，回查数值后改为相机局部横向平移；第一次回归 `10656` 16/17，修后 `10690` 17/17，后续补场景渲染状态再次 `10742` 17/17。该通过仅是合成测试工具覆盖项，非公开案例再验或视觉验收。PNG 小样合成 RGBA 图，`review_images.py` 的哈希/裁框/alpha 结果见本轮轻量结果；SVG 确有 Plate/引线、无字拒绝生效。不重渲历史案例。
- **外部独立复核后的更正（同一 v0.6 试用版）**：最初提交 `63f1650d2c85c25c6b64b5141361606fce2305e2` 的 validator 在 `kind=optical, medium=mechanical`（端口亦 mechanical）和 `support.tolerance=NaN` 错误返回 PASS；`port.owner=[]`、`required_components=[{}]` TypeError。另保存场景审计默认未声明的 `.03`、仅看 connection.required、只看 `hide_render`，尺寸依据 unknown 错报 PASS。这些是**实际缺陷**，撤回此前相关 PASS 外推；不把缺记录等同物理错误。更正后 kind→medium 映射，field/logical/temporal 的物理介质不妄断；引用坏类型结构化 FAIL，bool/NaN/Infinity 非法 FAIL，size_basis unknown 为 UNKNOWN。容差明确采用 Blender 场景世界单位，缺时单项 UNVERIFIED；任务 required_connections 也决定缺 route 为 FAIL；render 排除仅局部检测，未完全覆盖 view layer/collection/像素可见，改为 UNVERIFIED。SVG Plate 小例有字有引线，但文本实际宽度/长字出框**未核**，锚点入框不等于完整文字。
- **更正后的实测**：`python3 examples/run_v06_regression.py --blender /Applications/Blender.app/Contents/MacOS/Blender --report /tmp/agh-v06-revision.json` 31/31、exit 0（含 5 个额外场景反例），有效场景几何分项 PASS 但总状态 UNVERIFIED（render inclusion）。将 Skill 复制到临时独立目录再次回归 31/31、exit 0；`check_structure.py` exit 0，110 个 Markdown 相对链接缺失 0，`git diff --check` 无报错。最初版本 17/17 的“有效场景总 PASS”只在旧渲染状态逻辑下成立，不再用来声称可见性。原用户复核给出的反例已作为可失败案例加入脚本；没有旧案例重渲。
- v0.5 Git 基线为 `f6dfd9d2eebaf1c9bdf10becfd42b5ba2b8ed8d7`，当时本地/`private/main`/远端 SHA 一致。此次 v0.6 提交/远端验证单独以本轮实际 Git 结果为准；**运行时当前加载资源不是本地 v0.6**，此前安装快照冲突不通过 shell 覆盖。合成反例的轻量数值摘录见 [`examples/v06_results.json`](examples/v06_results.json)；脚本放到独立临时目录后，静态记录检查与 17 案例回归再次 exit 0（`10913`）。本轮没有借用旧案例 PNG/场景训练或重渲。
