# REVIEW_GUIDE — 视觉验收指南（V21–V30）

日期：2026-10-13
审阅人：外部 Codex 审阅者（非 AGH 自身读图）
AGH 读图工具状态：**不可用**（vision-skill → qwen3-vl-flash 404 model_not_found，本会话记录一次，不再重试）

## 如何看每张图
对每个 case 目录，打开 `overview_vNN.png`（最新版本），对照下方各案"应见组件"清单，逐项勾选。

## 各案应见组件清单

### V21 — MIP twin beams（B 类，v01）
- [ ] 1.5 µm 飞秒激光器（黑盒 + 红色输出光）
- [ ] FBG / fiber amplifier
- [ ] PPLN OPA（SHG）
- [ ] seed filter + delay line
- [ ] QCL / AOM
- [ ] 样品池（sample cell）
- [ ] BPD（balanced photodetector）+ RFSA 链路
- [ ] 三色光路（泵 / 信号 / 种子）各自可辨认

### V22 — soft pneumatic skin（C 类，v01）
- [ ] 多层柔性气动皮肤（半透明多层结构）
- [ ] 气管接口（tube ports）
- [ ] 泵 / 控制模块
- [ ] 实验台架 / 测试框

### V23 — EO flat comb（B 类，v01）
- [ ] 1550 nm CW 激光器
- [ ] PM + AM 电光调制器（含偏置 T 接头）
- [ ] EDFA（含 1480 nm 泵浦激光器）
- [ ] Ring A + Ring B 微环（torus + Si 芯片基底）
- [ ] OSA（含屏幕）
- [ ] 示波器（RF 驱动）
- [ ] 光纤连线 6 段（绿/蓝/黄三色）
- [ ] 光学面包板（4 腿 + V-groove）

### V24 — soliton microcomb（D 类，v01）
- [ ] 可调激光器（1550 nm，黑盒）
- [ ] 光纤耦合器
- [ ] 微环芯片（Si 基底 + 通孔波导 + 微环 torus）
- [ ] 热调谐器（金色螺旋，微环上方）
- [ ] 透明封装盖（alpha≈0.7，内部微环可见）
- [ ] OSA（带屏幕）
- [ ] 热控盒
- [ ] 泵浦光路（红）/ 输出光路（绿）

### V25 — OoTrap（C 类，v01）
- [ ] 可部署微流单元主体
- [ ] 入口 / 出口端口
- [ ] 捕获 / 培养腔
- [ ] 机械 / 流体接口
- [ ] 外部管路（保守示意）

### V26 — microfluidic T-junction（A 类，v03 最新）
- [ ] T 形通道（开顶，无盖，三壁可见）
- [ ] 高对比度蓝色流体（alpha≈0.45）
- [ ] 发光橙色粒子（嵌套双球）
- [ ] 三个金色环端口（通道顶部）
- [ ] 激光输入块 + 绿色观察光束
- [ ] 探测器 + 相机（置于实心光学面包板上，有 4 条腿，无悬空）
- [ ] 面包板（0.20×0.08×0.01 m）

### V27 — acoustic levitation LM（A 类，v01）
- [ ] 声学悬浮腔（顶部 / 底部共振器 + 锥形过渡 + 中央窄部）
- [ ] PZT 换能器（腔体底部黑盘）
- [ ] 液滴核心（半透明蓝）
- [ ] Lycopodium 粒子外壳（浅棕发光球）
- [ ] BOS 背光（黄色发光面板，-X 侧）
- [ ] BOS 光束（穿透腔体至 +X）
- [ ] 相机（+Y 侧，含 schlieren 镜片）
- [ ] 支撑底座 + 控制电子盒

### V28 — acoustic metamaterial nano（B 类，v01）
- [ ] 超材料面板（半透明底板 + 5×3 周期单元框）
- [ ] 压电圆盘（各单元中心，紫粉色）
- [ ] 金电极盘
- [ ] 扬声器（左侧）+ 麦克风（右侧）
- [ ] 放大器 + 示波器 + 信号发生器
- [ ] 声束（蓝色锥体）
- [ ] 各线缆（压电→放大 / 扬声器←信号源 / 麦克风→放大 / 放大→示波器）

### V29 — ABH metamaterial beam（C 类，v01）
- [ ] 6 周期 ABH 梁体（h2=8 mm，h1=1 mm，t=1 mm，l1=50 mm，l2=5 mm，s=110 mm，m=2，r=8 mm）
- [ ] 锥形楔块交替 180°
- [ ] V-groove 支撑 ×3
- [ ] shaker 激励器
- [ ] 激光测振头（红色光束）
- [ ] DAQ 盒
- [ ] 线缆

### V30 — UV fluorescence chip（D 类，v02 最新）
- [ ] 蓝宝石芯片体（20×50×4 mm，极低 alpha 或已移除）
- [ ] VCSEL DBR / AlN / active mesa（280/310 nm）
- [ ] Si PD + 长通滤光片
- [ ] 4 个电子芯片（LD driver / TIA / ADC / MCU-ESP32）
- [ ] LiPo 电池
- [ ] USB-C 口
- [ ] TP4056 / Boost / LDO
- [ ] Wi-Fi 天线（蛇形走线）
- [ ] 3.3 V / 7 V 金走线
- [ ] 样品凹槽
- [ ] UV 激光锥（3.7° FWHM，0.4 mm spot）
- [ ] 荧光路径（样品→PD）
- [ ] 外壳壳体 + 4 条腿 + 顶部玻璃盖（极低 alpha）

## 像素统计参考值（AGH 侧，PIL/numpy）
| 案 | 版本 | 尺寸 | frac_dark | frac_mid | frac_bright | mean_rgb |
|---|---|---|---|---|---|---|
| V26 | v01 | 1024×768 | 0.0000 | 0.7606 | 0.2394 | — |
| V26 | v02 | 1280×960 | 0.0000 | 0.9475 | 0.0525 | — |
| V30 | v01 | 1280×960 | 0.0000 | 0.8814 | 0.1186 | [77,93,111] |
（各案 v01 均为非黑帧，mid-band 主导）

## 验收结论填写
各案 verification_notes.md 中记录：
- 通过项（逐条勾选）
- 失败项（说明 + 版本号）
- 是否需下一版修复（v04 或已足够）
