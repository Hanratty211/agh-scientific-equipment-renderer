# AGH 新批次 v01 执行检查点

- 阶段 0 / AGH：本轮实际读取 `SOURCE_LEDGER.md`、`targets.json` 与本地 v0.6 `SKILL.md`，10 个 `inputs/11–20_*.png` 的 SHA-256 和尺寸均与 Codex 清单匹配；清单/来源图片由 Codex 先前获取/检查，**不是 AGH 获取/检查或渲染认可**。文章图注已读取，18 明确按 Fig.6(c) 组件层序，15 拆解状态无工作接触。
- 过程限制：此处只允许公开图页与本地 Skill；不读取原 Scientific-System-Renderer 文件/脚本，不调用其初始化或 benchmark。当前运行时加载的 `scientific-system-renderer` 不是本地 v0.6；本批实际使用本仓库 `skills/agh-scientific-equipment-renderer`。
- 下一步：十例完整低成本总览第一阶段逐一落盘；第二阶段在磁盘重开场景跑本地 v0.6 的静态/几何审计与 PNG 数值报告；视觉由用户/Codex 外审，不能以工具 PASS 替代。每例独立日志记录真实执行，失败留痕续做。

- 阶段 1 / AGH：十例 `build_v01.py`、`scene_v01.blend`、`overview_v01.png` 已实际落盘；Blender 5.1.2 十例成功。11 首次材料节点名假设失败，改按节点 type 查找后重试；每例单独日志/检查点。当前全部没有 AGH 像素审查结论，下一阶段进行记录/独立审计/数值图审。

- 阶段 2 / AGH：十例基于可确认组件而非编造接口写 `record_v01.json`；十例静态 `UNKNOWN`（无 port/route/support 物理主张），独立重开场景十例最终审计 `UNVERIFIED`，图片数值工具十例 `NUMERIC_ONLY`。18 初版独立审计 `VERTICAL:c11` exit 2，保留初始审计报告，改相机并独立复查 exit 3。实际可见路径未绑定真实界面，用户完整范围并未被工具证明；这些结果不是科学系统通过。十例参考–v01 拼图已存 `reference_vs_v01_local.png`，需要 Codex/用户读图。

- 阶段 3 / AGH：10 例 `CASE_NOTES.md` / 10 行 `BATCH_STATUS_v01.md` 与 900×3380 本地并排拼图已落盘；已留 pair_11..20 单例配对图供 Codex/用户输出像素外审。未做形式渲染。18 重建产生 Blender 自动 `.blend1` 备份，因不是交付版本且老状态已在 initial audit 留痕，将备份清理，只保留 v01 scene。

- 重要范围不足：十例 `record_v01.json` 仅 5–11 件存在证据组件，**ports=connections=supports=0**。这不是充分的第二阶段实物系统核查：尤其 11/12/16/17/19/20 原需求可见路径尚未逐端绑定世界作用面，不能宣称真正核过功能链。工具 UNKNOWN/UNVERIFIED 的具体原因被保存于 case 报告；后续 Codex 出图审查应要求重建与路径修订，而不是拿这次静态分数当通过。

- Git staging policy: curated 87 light text/data files only (`SOURCE_LEDGER.md`, `targets.json`, AGH-authored scene helpers/scripts, per-case records/reports/notes/checkpoints); all `inputs/`, `sources/`, PNG, `.blend`, HTML, PDF, raw logs, `.blend1` excluded from Git. New paper images are Codex source artifacts and remain local.

- R1：本轮实际读取 Codex `CODEX_FEEDBACK_R1.md`，十个真实 v01 像素审查结果均需修订。原版 v01 不覆盖，下一阶段批量 v02 结构修正；外部输入反馈不是 AGH 亲自打开输出 PNG，也不等于用户验收。

- R1 v02 / AGH：10 个独立 `build_v02.py` 批量后台 Blender 5.1.2 exit 0，`scene_v02.blend` 与无字 `overview_v02.png` 均落盘且 v01 未覆盖。按 Codex v01 实际像素反馈纠正装置方向/装配与缺件；本轮没有 AGH v02 输出像素验收。10 个源范围组件清单 `record_v02.json`，静态全部 UNKNOWN(exit 3)，独立读盘场景全部 UNVERIFIED(exit 3)，图片数值全部 NUMERIC_ONLY(exit 0)。v02 ports/routes/supports 仍未实际绑定：是诚实的不完整 QA，用户范围还没通过；每例 `V02_CHECKPOINT.md` 与全批 `BATCH_STATUS_v02.md`。参考–v01–v02 图已落盘给 Codex/用户外审，v02 状态 pending，不宣称认可。

- R2 / AGH：接收 Codex 于 2026-10-12 逐幅阅读 `codex-review/pair_11_v02.png`…`pair_20_v02.png` 的十例修订意见，均非 v02 接受。目标 v03：按意见做局部结构与可证路线修正，分项独立审计，保留 v01/v02，v03 仍待 Codex 实际输出像素复核。未读取原 Scientific-System-Renderer Skill 或脚本；本地 Skill 维持 v0.6。

- v03 第一轮真实路由审计：11/16 所列可见端点核查无 FAIL；12/17/19 被真实网格 surface-gap 拒绝（泵锚不在外壳、废液口锚在孔中心而非壁面、17 样品/泵锚离所属表面、19 玻璃倾角面与拟定锚错位），12 outlet-to-waste 终点与口锚相差 0.10 > 声明 0.08。报告 `cases/*/audit_scene_v03.json/.log` 保留，不能调大容差、改 required 或宣称 route PASS；需移动表面锚或标未证，重审独立保存场景。

- v03 审计修正：12/17/19 初次路由/所有者表面拒绝已保存 `audit_scene_v03_initial.json/.log`（12/17/19）；独立读取三例真实 mesh 最近面定位而非调宽容差。12 将 pump owner 指向实际 syringe 表面、waste mouth 锚移到实体开口 rim、route 终点同锚；17 owner 指向 fixture top 和实际 syringe interface；19 原玻璃锚落错倾斜侧，按旋转后的真实表面重定位。重建 12/17/19 并重新记录，12/17/19 audit exit 3、无分项 FAIL；仍不意味着功能拓扑或全路径已证。

- v03 / AGH：十例 `build_v03.py`、saved `.blend`、no-text low-cost PNG 全批后台 Blender exit 0。十例 v0.6 static UNKNOWN exit 3、独立 saved-scene audit UNVERIFIED exit 3，PNG 数值审查 NUMERIC_ONLY exit 0。11/12/16/17/19 仅对声明的源图可见片段加入 10/3/2/2/2 条端点路由；owner 最近面与 route 端点分项已重开实际场景查。13/14/20 缺源核对的端点未冒充通过；15/18 拆解展示不强加工作连接。18 独立网格 Y 射线对 1–17 面孔类别 17/17 分项符合脚本建模分类，总体 UNVERIFIED；11 二色镜实际评估网格面法向反射 -X→+Z dot 1.0、总体 UNVERIFIED。v03 仍待 Codex 实际读 PNG 并独立复核。

- R3 / 2026-10-12：本轮读 Codex `CODEX_FEEDBACK_R3.md`，Codex 已实际看十例 v03 像素并独立只读几何 probe；11/12/13/16/17/20 仅有限整体示意预览水平（且 11/12/17 端点最终修复/重读仍有条件），不是用户最终验收。14/15/18/19 指定 v04。核对当前 v03 10 张 PNG SHA 与本轮 `review_numeric_v03.json` 完全一致；Codex 早先捕获部分配对图在 12/17/19 端点修复前，必须用最终已刷新 PNG 重新对照，不能把旧截图当最后版本复核。历史失败 JSON `audit_scene_v03_initial.json` 留档，不删除。

- R3 限定 v04 / AGH：仅 14/15/18/19 运行 Blender 5.1.2 build/render exit 0，原 v01/v02/v03 未动。四例 static UNKNOWN(3)，独立重开场景终版 UNVERIFIED(3)，PNG NUMERIC_ONLY(0)；已声明可见线 14=3/3、19=2/2；15/18 拆解 0（不强求假连接）。19 首轮 QA marker 隐藏导致 PORT_RENDER FAIL，初始 JSON/log 保留；改极小黑色表面标而非金块、复审未有 FAIL（仍不证像素）。18 v03 中央孔 checker 直接套到 v04 内板会误报 12–14 封口 FAIL，旧报告保留；新 checker 首轮空 basic mesh 的 None 判断错误又 FAIL，保留 probe_bug 报告，修逻辑后对 1–17 中央孔/内板模型分类 17/17，综合 UNVERIFIED；不是全板或密封认证。19 独立 film 实网格最近面 lead 两端约 8.43e-8 与 3.73e-9 世界单位，非视觉/电路验收。混合六例 v03＋四例 v04 并排已本地落盘，全部等待 Codex 最终像素重读。

- 14 额外自查：第一份 v04 审计虽然 PASS，其 array 锚点曾处 top holder 体内部距最近实网格面 0.07 展示世界单位；报告 `audit_scene_v04_pre_surface.*` 留档。没有扩大容差，而是移向真实顶面，重建/重开/重做数值，最终最近面 0.0050001，PNG hash 已重新写进 V04_CHECKPOINT，混合总图已更新。

- R4 2026-10-12 独立审查：`EXTERNAL_VALIDATION_STATUS.md` 由 Codex 著述，真实像素读图及独立十例保存场景审计为 Codex 执行，AGH 不冒领；九例 11/12/13/14/15/16/17/19/20 仅有限 schematic-preview 阶段批准，非用户最终/工程验收，冻结本轮不重做。18 v04 实际高分辨率审阅 FAIL：12–14 内板被前层遮住，几何存在不等于可读；仅 case18 制作 v05 展示间距/视角与同几何补充细节；不改 Skill v0.6，最终视觉仍待 Codex。

- R4 AGH 仅 case18 v05：source/审查作者 Codex；v04 R4 否决理由重复单元前侧挡内板。前三次 v05 展示/探针尝试分别是0/9遮挡、0/9遮挡、16/17入框 FAIL（历史 JSON 留档）；第三次探针也发现射线终点错误，修探针并重跑。最终只改展示 X/Y 错层与主镜头、同 mesh 补充细节镜头，v01–v04 和九例不动。最终 build0/static UNKNOWN3/saved-audit UNVERIFIED3（0 FAIL）/numeric NUMERIC_ONLY0，sampled 12–14 面各9/9且入框，17位置中心类别采样 17/17；像素尚未给 Codex 重读，所以不称 v05 通过。附本地 case18_reference_v04_v05_detail_local.png；原图、场景、PNG、日志不提交。Skill v0.6 不变。

- R5 Codex 独立实际读 v05 overview/detail 全分辨率，12–14 本体面彩色板/黑纹局部可读，但整图 FAIL：前 1–11 多数遮住，assembled 堆叠不在相对右侧，极平正面/空白过多且 detail 第一单元被端板部分遮挡。Codex 修复自己的 MeshVertex.co.y 探针后另证 12–14 内面/肋条各9/9 本体先命中（Codex 独立工具，非 AGH 执行）；局部几何不替代整体通过。仅 case18 v06，九例冻结、Skill v0.6 暂不改。

- R5 AGH v06（仅 18）：保存 v04 主总图完整状态并重渲，PIL RGB/RGBA 像素逐项对比无差异（PNG 文件 hash 不同）；从同一 .blend 几何临时对 12/13/14 各做单元面隔离补图，每次复原所有 hide_render；最终 scene_v06.blend 主镜头及无隐藏 primary。首轮 import 错误保留初始 log，改用 Blender --python-exit-code1 后 build0，static UNKNOWN3，独立重开审计 UNVERIFIED3 零 FAIL；17/17 中心 Y 射线类别/组装体存在/无隐藏已采样，NUMERIC_ONLY0 四张。v04 主图内部 12–14 面仍遮挡，改以补图展示，真实 v06 像素尚待 Codex 判断，这不是自认整图验收；九例冻结、Skill v0.6 未动。
