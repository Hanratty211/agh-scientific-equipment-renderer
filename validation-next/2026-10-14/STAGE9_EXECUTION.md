# Stage8—9 AGH 执行记录（任务从磁盘续做）

- 起始 `main` HEAD = origin/main `35725d09407e8530c41a219496b3c9633f429448`。未读、检出、合并或 cherry-pick 协作者分支。用户在本次中断后明确第七轮 **外部人工实际目视**：13 v07 局部候选可读；18 v06 仍像规则栅栏。记录于 `EXTERNAL_HUMAN_REVIEW.md` 与自动栏分离。
- Stage8 已从磁盘产出：13 v07 同几何近景 `detail_tip.png`，源 `.blend` 原样 hash；18 Fig18 v06 正面尝试，独立 Blender 重开渲染，有限6项零FAIL，但被外部**视觉拒绝**。不重复运行或覆盖。
- Stage9 仅 18 v06→v07：`revise_fig18_v07.py` 只删除 v06 的 30 条正面族，另存17+17 条弯曲斜向持续路径，压板/框架未修改。Blender 5.1.2 独立新进程打开 v07 `.blend`，`render_saved.py` 生成900×640 PNG，`audit_fig18_v07.py` 从磁盘重开查曲线/压板 6 项零 FAIL；先前不适用的边缘长对角线检查报告/日志只留本地，未把“通过”扩展成视觉。
- AGH `computer_use.list_apps` 再次 apps discovery failed，无本会话对 v07 PNG 的真实图像读入，因此无法履行 AGH 自己“再次从磁盘看 v07”的要求，也不能判断它是否仍像栅栏；提交 v07 为**待外部复核候选**。用户可用 `STAGE9_REVIEW_QUEUE.md` 自制 v06→v07 比较明确决定是否仍需局部修订。并未凭有限审核自行宣称“更接近”。
- Fig18 源 PDF/图片及含源图比较 PNG 均留本地；纯自制前后图可入 Git。旧 `.blend`/PNG/失败历史原样留存，日志和缓存不入 Git。
