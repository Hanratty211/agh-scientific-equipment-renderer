# Agnes 视觉复核保护

可选的本地 AGH 插件，使用公开 `registerHook` 接口；不修改 AGH 内核。仅在会话工作目录存在 `.scirender-visual-review.json` 且包含非空 `run_id` 时启用。

```json
{"run_id":"my-review-001"}
```

同一 `computer_use capture` 目标最多3次（首次+两次重试），同一图像digest出现3次停止，总共最多12次；从首次落盘尝试起180秒后在下一个步骤/调用边界停止。它不会中断正在执行的工具，工具自身仍受平台超时限制；不拦截shell、其他截图工具或故意改run_id的绕过，不是安全沙箱。

状态逐次原子写入工作目录 `.scirender-review-state/<run-id-sha256>.json`，同run_id重启不清零，触发后记NEEDS_EXTERNAL_REVIEW，下一模型步骤阻断。结果不含“视觉通过”。无需保护的普通任务不创建标记。恢复时先核保存文件hash，显式新run_id和原因另行记录，不删除旧状态。

安装：在 AGH 启动工作目录使用 `agh package inspect file:./<本目录相对路径>`，按正常 `install → trust（实际完整性和能力hash）→ enable → status` 流程。已安装更新走受支持SDK或界面 update-from-source，不手工改受管快照。关闭用 `agh package disable @scirender/visual-review-guard`。

验证：在本目录运行 `node test.mjs`。v0.1.1 已修正未启用时的空 hook 返回；已有本地集成记录确认截图上限拦截和同会话恢复后继续拦截。详细调试记录本地保留，公开版不重复上传。更换 AGH 构建后应重新核对集成行为。
