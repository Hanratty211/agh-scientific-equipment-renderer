# V21 Revision Log

本日志记录此前版本变化；本次收口只更新状态与视频说明，不修改 Python、.blend 或 PNG。

## v02 — 2026-10-13

- **反馈**：上传的旧版像素中，V21 只是横向排列的通用白盒，分支、样品、BPD/RFSA 和三类路径不清；旧记录还把线性串联拓扑写得过度简化。
- **理解**：论文支持的是双分支 OPA 泵浦/种子、SHG/PPLN、seed delay、twin signal/idler、正交 QCL/AOM-MIP 样品和 BPD→RFSA；不能把三色线当作一条串联光路。
- **修改**：增加分支节点、FBG/fiber amplifier、SHG/PPLN、seed filter/delay、OPA waveguide、twin separator、CaF2 cell、Fourier iris、正交 MIR QCL/AOM、BPD 双输入与 RFSA。未添加论文没有的厂家外观。
- **核验**：构建 PNG 与独立重开复渲曾记录；构建与重开进程写出后返回 `0xC0000374`。

## v03–v04 — 2026-10-13

- 保持 v02 来源拓扑，针对曝光、材质明度、发光和全景构图做渲染修订；v04 输出 `overview_v04.png` 与 `branch_detail_v04.png`。
- 将对照 reference 纠正为论文 Fig.1 精确裁图，而非整页缩略图。
- v04 独立重开、结构审计和复渲均记录通过；构建与成功重开进程正常退出 `0x00000000`。
- **视觉更新**：外部 Codex 已实际查看最新版 v04；右侧设备有边缘裁切。现接受该裁切，不再返工，剪辑时避免该设备特写。v04 仅为第二展示。
- **未完成**：真实光纤接口、隐藏连接和精确厂家形态未知；结构审计/复渲不是功能验证。
