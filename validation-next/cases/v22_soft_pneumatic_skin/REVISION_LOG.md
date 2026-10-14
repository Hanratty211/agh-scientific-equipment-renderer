# V22 Revision Log

## v02 — 2026-10-13

- **反馈**：上传的旧版像素中，V22 主体像被台架腿遮挡的三层白色薄饼，气动层级和端口不清；旧版还加入了没有明确来源依据的砝码平台和四支柱。
- **理解**：论文正文支持 thin flexible sheet-like actuator、multilayer pneumatic chambers/circuits、外部 pressure pump/MFCS、输入端口和 hose；论文文字没有为本低成本总览指定一个通用砝码台几何。
- **修改**：新建 `build_v02.py`、`scene_v02.blend`、`overview_v02.png`；保留旧 v01。提高三层主体和通道的区分度，收紧相机到皮肤与供气链，删除 `weight_plat`、`strut_*`、`test_weight`。
- **新图证据**：构建输出 overview SHA-256 `d420cdbf9403c8c57d2f7e087fce59540627d245178b64df7b7bbbbc4e0e9e42`；独立重开复渲 `reopen_render_v02.png` SHA-256 `aa7e268e20c80c1068e03ac78cde91e3b61757951636209a1a5d4eaa8256382b`。
- **未解决**：当前附件中的 V22 参考栏只是论文首页，未提供装置照片像素对照；实际多层共形轮廓、端口拓扑和实验台架仍未知。新版 PNG 尚未由 AGH 在用户附件中复读。构建与重开进程写出后均返回 `0xC0000374`，单独记录为退出阶段异常。
