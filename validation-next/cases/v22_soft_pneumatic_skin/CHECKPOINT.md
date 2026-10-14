# V22 CHECKPOINT v02

日期：2026-10-13
分支：agh/validation-next-2026
来源：10.1038/s41467-025-60496-9；本轮 PDF 临时下载哈希记录于 SOURCE_NOTES

## 反馈闭环
- **反馈**：v01 像被台架腿遮挡的白色三层薄饼，端口/气路层级不清。
- **理解**：论文支持薄柔性多层 pneumatic chambers/circuits、输入端口、外部 pump/MFCS 与 hoses；v01 砝码平台和四支柱没有本例来源依据。
- **修改**：v02 提高层/通道对比、收紧相机、删除 weight platform/四支柱；旧 v01 保留。
- **新图证据**：`overview_v02.png` SHA-256 `d420cdbf9403c8c57d2f7e087fce59540627d245178b64df7b7bbbbc4e0e9e42`。

## 独立重开核验
- [x] 全新 Blender 进程读取 `scene_v02.blend`
- [x] 必需对象 0 缺失；29 对象；无 hide_render
- [x] 全新 Blender 进程复渲 `reopen_render_v02.png`，SHA-256 `aa7e268e20c80c1068e03ac78cde91e3b61757951636209a1a5d4eaa8256382b`
- [ ] 像素视觉确认：新版图尚未作为用户附件回传；不宣称通过
- [!] 构建与重开进程产物写出后均返回 Windows `0xC0000374`，作为退出阶段异常记录

## 未解决
实际照片构图、真实共形轮廓、总层数、端口拓扑和实验台架仍需来源图核对。
