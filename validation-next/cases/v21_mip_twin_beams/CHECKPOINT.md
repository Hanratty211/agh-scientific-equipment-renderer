# V21 CHECKPOINT v04

日期：2026-10-13
分支：agh/validation-next-2026

## 最终构图修订
- 保留 v02 来源拓扑；v04 只调整总览构图、曝光、材质亮度和局部输出，不重做来源结构。
- `overview_v04.png` SHA-256 `f699fb4301374b39d41c112acff956ac0fee8e7166a5cb5b90cdfd420e3139d8`
- `branch_detail_v04.png` SHA-256 `90583b1f4aafca7e0f1d3631c79d33e5d41b72fe50a4834b48bbb0b0f543b562`
- 准确参考裁图：论文 Fig.1，`validation-next/video-review/V21_reference_Fig1.png`，SHA-256 `fb978c8e292fcd238e083619ab3eaabec7fcfa73c0652062799b8207e3fa01bd`
- 四联对比图：`validation-next/video-review/V21_reference_previous_latest_detail.png`，SHA-256 `39dbe17f20104d0e87d75e589bec0cb92b0da5c54e0fd9c35cfebab32891dccb`

## 独立重开
- [x] 全新 Blender 进程读取 `scene_v04.blend`
- [x] 40 对象；必需对象缺失 0；`hidden_render` 为空
- [x] 复渲 `reopen_render_v04.png`，SHA-256 `6c0d655324378cbe885563a52699b2b47f6427505f9e42381aa917df71686f35`
- [x] scene audit：`validation-next/scene-audits/v21_reopen_v04.json`，状态 `PASS_REOPEN_STRUCTURE_AND_RERENDER_ONLY`
- [x] 构建与成功重开进程均正常退出 `0x00000000`；本版未出现 `0xC0000374`
- [x] 外部 Codex 已实际查看最新版 PNG；v04 作为第二视频展示。右侧设备有边缘裁切，接受现状、不再返工，避免该设备特写

## 未解决
右侧设备边缘裁切已由外部查看确认并接受，不返工；真实光纤与隐藏接口、精确厂家形态仍未知。结构审计/复渲不是功能验证。