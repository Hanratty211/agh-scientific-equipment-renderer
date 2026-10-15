# 仓库地图

|目录/文件|用途|
|---|---|
|`agh-scientific-equipment-renderer/`|唯一规范 Skill 源码；独立安装包|
|`results/2026-10-15/`|当前可编辑场景、原始渲染、验收契约、图片对照和复核命令|
|`tools/acceptance/`|可独立运行的共享验收工具和测试|
|`integrations/agnes-visual-guard/`|可选 Agnes 视觉复核保护插件|
|`validation-next/2026-10-14/`|既往十例工程及历史证据，保留原路径|
|`public-validation-11-20/`、`case-*`|更早批次与探索工程|
|`VIDEO_DEMO_HANDOFF.md`|历史视频素材协作说明，当前成果以前述 results 为准|
|`docs/history/`|旧状态、README 与文件清单归档|

本次发布以首页、独立 Skill、公开成果和可复用工具为入口，未批量移动历史案例或重写 Git 历史。详细本地会话证据位于被忽略的 `validation-next/2026-10-15/`，发布整理前的文档备份位于被忽略的 `.local-publication/`；本地 SDK 驱动脚本也不纳入公共工具包。

稀疏检出可运行 `git sparse-checkout add results tools integrations docs` 获取新目录。历史文档中的“私有仓库”“仅本地”及版本状态描述对应其记录日期；当前仓库为公开仓库，本次 results 为公开发布内容。

当前主案例为微流控 v11 和机器人 v08；`results/2026-10-15/robotics/` 保留 v07，`robotics-v08/` 为用户复核接受的新版。[用户图像验收](../results/2026-10-15/HUMAN_REVIEW.md)。本地互动对照页和来源图不随公开成果同步。
