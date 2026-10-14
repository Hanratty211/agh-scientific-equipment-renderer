# 第五阶段真实执行记录

- 起点：`main`，本地与 `origin/main` 同 SHA `86840ba428abbe3eebcd2976fd5131aaf8b8c5f0`，未查看或合并任何协作者分支。
- 第三轮外部复核判词见 `EXTERNAL_HUMAN_REVIEW.md` 第三表；反馈针对 stage4 PNG 和 Fig17–20 补图，只证旧版目视，不是新图验收。
- 按限定另建 `02 v05`（夹爪工作面）、`13 v04`（远端真实头/端窗）、`14 v04`（LDV 到样品中心测量路径）、`16 v04`（两气源代表性 socket）、`20 v04`（最终右端薄膜封面）、`18 v03_fig18_PIM_CIM`（独立 20×20 mm 面层+压板）。保存均拒绝覆盖已存版本，Blender 5.1.2 另进程重载保存场景渲染 PNG/SHA；Fig18 以原 v01 框架并删除无据梯状旧试样，未覆盖 v02 Type IV。
- 独立 `audit_stage5.py` 发现 **16 v04 两个气源首端 FAIL**；保留 v04 场景/PNG/FAIL 报告，另建 v05 只纠正两世界管端，独立重载渲染后十项零 FAIL。其余局部结构 02 8项、13 9项、14 3项、18 5项、20 4项无 FAIL。审计不核像素遮挡、内部功能/密封或材料力学。
- 04 v06、08 v03、15 v05、17 v03 不重做，不把“改善”升级“通过”。十例本地 `stage5_source_..._LOCAL.png` 用源—旧—当前版逐例并排生成；出版方素材只本地。
- AGH `computer_use.list_apps` 仍 `Computer Use apps discovery failed`，新 PNG 尚未获实际图像视觉判断；外部人工请按 `STAGE5_REVIEW_QUEUE.md` 单张逐例复核。
