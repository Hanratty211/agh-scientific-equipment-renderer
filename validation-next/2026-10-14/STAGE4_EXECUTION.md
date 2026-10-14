# 第四阶段执行记录｜第二轮外部复核后

- 工作树：`main`，起点 SHA `9ae8d68c5f7d8d9f1700733761a2982d85ca37df`；未检查、合并或 cherry-pick 协作者分支。旧文件一律保留，新场景由 `revise_connectivity_stage4.py` 从已有保存场景读取到新版本，脚本检查目标不存在方可写。
- 外部人工视觉判词逐例已写 `EXTERNAL_HUMAN_REVIEW.md` 第二轮表，审阅者固定“外部复核”；原 04 v06 大体可读但未过，18 v02 仅 parent-material 示意。
- 优先 02 v03→v04、08 v02→v03、13 v02→v03、14 v02→v03、16 v02→v03、17 v02→v03、20 v02→v03，之后 15 v04→v05；04 v06 保留不伪造 v07。
- 每例 Blender 5.1.2 建场景后由**独立后台进程重开保存的 .blend** 用 `render_saved.py` 生成 900×640 PNG/`render_report.json`，核场景及 PNG SHA。独立重载再用 `audit_stage4.py` 进行作用面/对象存在的有限几何断言；8/8 新场景各自 `target_audit.json` 零 FAIL（6,14,9,4,8,5,4,3 项）。仅代表测试覆盖项，**不是完整端到端物理审计、图像或功能验收**。
- 几何审核曾因 Python Blender 对象迭代不是名字而报 `AttributeError`；修成 `o.keys()` 后重跑，保留旧失败 `audit.log` 和新 `audit_retry.log` 于本地未提交；没有把审核脚本错误称新场景正确。
- 下载公开 18 补图 PDF 至本地，补图 17–20 在 pp32–35，图注定位完成；GUI apps discovery 仍失败，AGH 未看到补图或八例新 PNG 像素，不能建未经见图的 PIM。
- 十张单例来源—被审旧版—当前版画布落于 `demo-assets/<id>/stage4_source_*_LOCAL.png` 仅本地，列在 `STAGE4_REVIEW_QUEUE.md`；含论文原图/文字不入 Git。
