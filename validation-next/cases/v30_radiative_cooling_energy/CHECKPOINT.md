# V30 CHECKPOINT v05

日期：2026-10-13
分支：agh/validation-next-2026

## 最终构图与采样修订
- 保留 v03 的无腿、样品接触顶面、底面器件与来源支持的开壳/剖切表达。
- v05 只调整曝光、材质对比、镜头和 EEVEE 采样，不重做来源结构。
- `overview_v05.png` SHA-256 `fa218521caf3ea9037a6937b00fb2c7a5e6aeb1b149ba7e288e101b061d40330`
- `detail_bottom_v05.png` SHA-256 `7f98bc3cb5c79e33d6d74b17635eb118860904def0dac6a6fe8a14fb46b7f88f`
- 准确参考裁图：论文 Fig.12，`validation-next/video-review/V30_reference_Fig12.png`，SHA-256 `3751af026ea9d326cf6873ced06fc26ba2d8e1018cf054e4d19eda8186419a7d`
- 四联对比图：`validation-next/video-review/V30_reference_previous_latest_detail.png`，SHA-256 `cb43765b2592f9f73fe575f14519a12712b47a56ec588d34d111af3d12bc23e4`

## 独立重开
- [x] 全新 Blender 进程读取 `scene_v05.blend`
- [x] 48 对象；必需对象缺失 0；`hidden_render` 为空
- [x] 复渲 `reopen_render_v05.png`，SHA-256 `1c11fa715be67cc795e5180d5235fe24c3d0ff61d8180d70974897a25347f36b`
- [x] scene audit：`validation-next/scene-audits/v30_reopen_v05.json`，状态 `PASS_REOPEN_STRUCTURE_AND_RERENDER_ONLY`
- [x] 构建与重开进程均正常退出 `0x00000000`；本版未出现 `0xC0000374`
- [x] 外部 Codex 已实际查看最新版 PNG；v05 作为视频主展示候选

## 未解决
外部视觉查看不等于器件功能或所有接口验证；固定细节、真实天线拓扑和厂家外观仍未知。