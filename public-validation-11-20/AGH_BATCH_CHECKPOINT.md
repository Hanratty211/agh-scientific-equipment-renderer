# AGH 新批次 v01 执行检查点

- 阶段 0 / AGH：本轮实际读取 `SOURCE_LEDGER.md`、`targets.json` 与本地 v0.6 `SKILL.md`，10 个 `inputs/11–20_*.png` 的 SHA-256 和尺寸均与 Codex 清单匹配；清单/来源图片由 Codex 先前获取/检查，**不是 AGH 获取/检查或渲染认可**。文章图注已读取，18 明确按 Fig.6(c) 组件层序，15 拆解状态无工作接触。
- 过程限制：此处只允许公开图页与本地 Skill；不读取原 Scientific-System-Renderer 文件/脚本，不调用其初始化或 benchmark。当前运行时加载的 `scientific-system-renderer` 不是本地 v0.6；本批实际使用本仓库 `skills/agh-scientific-equipment-renderer`。
- 下一步：十例完整低成本总览第一阶段逐一落盘；第二阶段在磁盘重开场景跑本地 v0.6 的静态/几何审计与 PNG 数值报告；视觉由用户/Codex 外审，不能以工具 PASS 替代。每例独立日志记录真实执行，失败留痕续做。

- 阶段 1 / AGH：十例 `build_v01.py`、`scene_v01.blend`、`overview_v01.png` 已实际落盘；Blender 5.1.2 十例成功。11 首次材料节点名假设失败，改按节点 type 查找后重试；每例单独日志/检查点。当前全部没有 AGH 像素审查结论，下一阶段进行记录/独立审计/数值图审。

- 阶段 2 / AGH：十例基于可确认组件而非编造接口写 `record_v01.json`；十例静态 `UNKNOWN`（无 port/route/support 物理主张），独立重开场景十例最终审计 `UNVERIFIED`，图片数值工具十例 `NUMERIC_ONLY`。18 初版独立审计 `VERTICAL:c11` exit 2，保留初始审计报告，改相机并独立复查 exit 3。实际可见路径未绑定真实界面，用户完整范围并未被工具证明；这些结果不是科学系统通过。十例参考–v01 拼图已存 `reference_vs_v01_local.png`，需要 Codex/用户读图。

- 阶段 3 / AGH：10 例 `CASE_NOTES.md` / 10 行 `BATCH_STATUS_v01.md` 与 900×3380 本地并排拼图已落盘；已留 pair_11..20 单例配对图供 Codex/用户输出像素外审。未做形式渲染。18 重建产生 Blender 自动 `.blend1` 备份，因不是交付版本且老状态已在 initial audit 留痕，将备份清理，只保留 v01 scene。

- 重要范围不足：十例 `record_v01.json` 仅 5–11 件存在证据组件，**ports=connections=supports=0**。这不是充分的第二阶段实物系统核查：尤其 11/12/16/17/19/20 原需求可见路径尚未逐端绑定世界作用面，不能宣称真正核过功能链。工具 UNKNOWN/UNVERIFIED 的具体原因被保存于 case 报告；后续 Codex 出图审查应要求重建与路径修订，而不是拿这次静态分数当通过。

- Git staging policy: curated 87 light text/data files only (`SOURCE_LEDGER.md`, `targets.json`, AGH-authored scene helpers/scripts, per-case records/reports/notes/checkpoints); all `inputs/`, `sources/`, PNG, `.blend`, HTML, PDF, raw logs, `.blend1` excluded from Git. New paper images are Codex source artifacts and remain local.
