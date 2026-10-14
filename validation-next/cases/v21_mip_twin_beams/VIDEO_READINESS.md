# V21 VIDEO_READINESS

日期：2026-10-14

- **选用**：第二展示，使用最新版 v04。外部 Codex 已实际查看 `overview_v04.png`，不是仅凭结构审计或像素统计推断视觉通过。
- **实际修改**：v04 保留 v02 来源拓扑，只调整总览构图、曝光、器件材质亮度并输出 `branch_detail_v04.png`；未改 Python、场景结构或来源拓扑作为本次收口操作。
- **产物**：`overview_v04.png` SHA-256 `f699fb4301374b39d41c112acff956ac0fee8e7166a5cb5b90cdfd420e3139d8`；`branch_detail_v04.png` SHA-256 `90583b1f4aafca7e0f1d3631c79d33e5d41b72fe50a4834b48bbb0b0f543b562`。
- **已完成验证**：全新 Blender 进程独立重开 `scene_v04.blend`、结构审计及复渲；40 对象、必需对象缺失 0、`hidden_render` 为空，复渲 `reopen_render_v04.png` SHA-256 `6c0d655324378cbe885563a52699b2b47f6427505f9e42381aa917df71686f35`。audit 为 `PASS_REOPEN_STRUCTURE_AND_RERENDER_ONLY`；构建与成功重开进程正常退出 `0x00000000`。
- **外部视觉反馈/剪辑限制**：右侧设备有边缘裁切。接受此限制，不再返工；避免把右侧设备作为特写主体。可作第二展示，但不声称裁切已修复。
- **未完成**：真实光纤接口、隐藏连接和精确厂家形态仍未知；外部查看不等于功能验证。
