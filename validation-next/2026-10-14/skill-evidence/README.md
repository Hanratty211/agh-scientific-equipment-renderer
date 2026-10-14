# 验证工程 Skill 证据归档（不是可安装 Skill 包）

`../../../agh-scientific-equipment-renderer/` 是唯一通用规范源；本目录只保留 Git 历史中的独立案例/论文证据或旧测试结果，不是安装依赖：

|归档|原 Skill 包位置|说明|
|---|---|---|
|`validation_2026_10_14.md`|`references/validation_2026_10_14.md`|2026 十篇 A/B/C/D DOI、页锚点、渲染 SHA、审阅者/未知，18 v07 **未目视验收**|
|`evidence_index_v10.md`|`references/evidence_index.md`|旧 case-1/2/3 与 03–20 证据链接（旧相对路径按旧布局保留，可能已不工作；用 Git 历史及仓库根目录查）|
|`public_validation_11_20_v10.md`|`references/public_validation_11_20.md`|旧 11–20 文献逐篇验证表|
|`pitfalls_and_fixes_v10.md`|`references/pitfalls_and_fixes.md`|有案例细节/坐标/外审的旧 P1–P32，非通用包方法|
|`PROVENANCE_ARCHIVE_v10_v11.md`|`PROVENANCE.md`|旧安装/版本/案例轨迹原文，保持历史不覆盖；其中旧源码状态指相应时点|
|`v06_results_legacy.json`|`examples/v06_results.json`|合成回归历史结果、版本与运行环境记录，不是必要 fixture|
|`behavior_results_legacy.txt`|`behavior_results.txt`|合成几何反例历史输出（新检查产物写临时目录）|

当前主审查仍在 `../EXTERNAL_HUMAN_REVIEW.md`、`../STAGE9_REVIEW_QUEUE.md` 和 `../cases/<id>/CHECKPOINT.md`；本轮**不修改**原十篇场景/PNG/审阅状态。原论文 PDF、原图和含原图对照画布始终仅本地，不发布。v1.0 加载与十例建模脚本不同；比较画布后续独立处理，未有证据表明由 Skill 自带 `review_images.py` 生成。此目录只是证据档案，不据其内容升级软件运行时状态。
