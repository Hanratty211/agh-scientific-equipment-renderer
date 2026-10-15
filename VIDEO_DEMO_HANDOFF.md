> **当前入口（2026-10-15）**：[公开成果与复核](results/2026-10-15/README.md)。本仓库当前为公开仓库；以下为 2026-10-14 历史交接内容，其中仓库可见性和版本状态仅对应当时。

# 功能演示协作交接｜2026-10-14 私有仓库 main

**拿到仓库后**：`git clone https://github.com/Hanratty211/agh-scientific-equipment-renderer.git`，在 `main` 阅读本文件；仓库经 AGH 检查为 GitHub **PRIVATE**。十篇项目根为 [`validation-next/2026-10-14/`](validation-next/2026-10-14/)。Skill 唯一规范源码在 [`agh-scientific-equipment-renderer/`](agh-scientific-equipment-renderer/README.md)，与论文工程分开。十例是在加载 AGH Skill v1.0 时用本项目自写 Blender 脚本做场景/渲染；后续源—图画布是**独立排版成果**，不是 Skill 直接生成，也不是十例通过验证。

## 先看的三个入口

1. [十篇 2×5 来源—渲染导航拼图](validation-next/2026-10-14/demo-assets/ten_papers_source_render_LOCAL/TEN_PAPERS_SOURCE_VS_RENDER_LOCAL.png)；[交互 HTML 逐例画廊](validation-next/2026-10-14/demo-assets/ten_papers_source_render_LOCAL/index.html) 和 [逐张高清对照 README](validation-next/2026-10-14/demo-assets/ten_papers_source_render_LOCAL/README.md)。拼图只导航，须逐张看高清源和单张 PNG。
2. [完整十篇 DOI/范围/四类选题](validation-next/2026-10-14/SOURCES.md)；每篇 `demo-assets/<id>/source/SOURCE.md` 对应 `sources/<id>.pdf`（18 另有 supplementary PDF/页图），`cases/<id>/CHECKPOINT.md` 记范围、场景/PNG SHA 和假设。
3. [外部人工逐轮判词](validation-next/2026-10-14/EXTERNAL_HUMAN_REVIEW.md)与 [Stage9 最新局部审阅队列](validation-next/2026-10-14/STAGE9_REVIEW_QUEUE.md)、[Stage7 十例版本/哈希队列](validation-next/2026-10-14/STAGE7_REVIEW_QUEUE.md)；前者视觉意见，自动审计独立列。`BATCH_STATUS.md`/`STAGE*_EXECUTION.md` 是实做与阻塞。**全为候选或过程版本，无十例整体验收。**

## 十例定位（所有路径相对 `validation-next/2026-10-14/`）

表中“当前版”仅为**已有可用素材的最高版本**，不是已被目视接受的终版。每行的 `scene.blend` 与 `overview.png` 在同一 `cases/<id>/<版本>/` 目录，`render_report.json` 记双哈希；`SOURCE.md` 中给精确 PDF 页与局部锚点。独立逐例画廊链接按编号 01–10。

|编号/类别|原文锚点和源目录|已有版（PNG 与同目录 scene）|画廊对照与特别过程|审阅界限|
|---|---|---|---|---|
|02 / C 实拍软机器人|Fig.3b PDF p4 · `demo-assets/02_robotics/source/`|`cases/02_robotics/v05/overview.png`|画廊 01；v01 矩夹块→v02 上夹 audit FAIL→v03 悬柱→v04/v05 夹面改善|v05 外部称夹面改善，非夹力证明|
|04 / B 物理流路架构|Fig.3C PDF p4，Fig3A 仅泵外形 · `demo-assets/04_microfluidics/source/`|`cases/04_microfluidics/v06/overview.png`|画廊 02；v01 假孔→v02 回退→v03 断连→v04 五源端 FAIL→v05 数值零 FAIL 而视觉仍不通过→v06|v06 五路关系可读候选，内流道/密封未核|
|08 / A 装配层|Fig.3 左 PDF p6 · `demo-assets/08_biomedical/source/`|`cases/08_biomedical/v03/overview.png`|画廊 03；v01 泛板、v02 铜线越界→v03|层边界略浮，电接点仍待核|
|13 / B 内窥系统/接口|Fig.1a,c PDF p3；远端后核 Fig1f/g · `demo-assets/13_biomed_optics/source/`|`cases/13_biomed_optics/v07/overview.png`|画廊 04；[同一场景局部 `detail_tip.png`](validation-next/2026-10-14/cases/13_biomed_optics/v07/detail_tip.png)；v06→v07 前端窗|外部读局部形态可辨，不代替总览/光学功能|
|14 / C 声悬浮实拍|Fig.1c PDF p3，1a 仅逻辑 · `demo-assets/14_acoustic_alt/source/`|`cases/14_acoustic_alt/v05/overview.png`|画廊 05；v04 光穿实板→v05 真孔|仅“LDV 支架→真孔→样品”具体问题外部称解决，整图/功能未验收|
|15 / A 穿戴贴片装配|Fig.3a 图 p5/图注 p6 · `demo-assets/15_biomed_energy/source/`|`cases/15_biomed_energy/v05/overview.png`|画廊 06；v01 实心盖遮 PV→v02 开窗→v03/04 浮层→v05|顶层身份/空隙仍待核|
|16 / D Methods 文字|Methods PDF p9 单程泵、CO₂/Ar MFC · `demo-assets/16_energy_nature/source/`|`cases/16_energy_nature/v05/overview.png`|画廊 07；v01 只用文字、v04 起点 FAIL→v05 数值修复|三段外路仍待目视，内池未知|
|17 / A 天线装配|Fig.1a–d PDF p4 · `demo-assets/17_rf_nature/source/`|`cases/17_rf_nature/v03/overview.png`|画廊 08；v01 双错位板→v02→v03 单板馈线|电磁性能和真实馈点未知|
|18 / D Methods→补图|Methods PDF p9 Z100；Supplementary Fig18 PDF p33 左格构/中压板 · `demo-assets/18_mechanical_nature/source/`|`cases/18_mechanical_nature/v07_fig18_diagonal_weave/overview.png`|画廊 09；Fig17 parent Type IV v02 **另任务**；Fig18 v03 直杆→v04 结团→v05 细网→v06 栅栏（外部视觉失败）→v07 斜向候选|**v07 新 PNG 未经外部/AGH 目视**；节点/层深/力学未知|
|20 / D Materials 文字|Materials p11 + 正文 p2 · `demo-assets/20_thermal/source/`|`cases/20_thermal/v04/overview.png`|画廊 10；v03 右端露芯→v04 封闭候选；`v02_preseal_detail/` 是不同预封工艺态|v04 薄膜/封边仍待核，不能说密封已证|

A=工程/装配，B=架构与物理接线，C=实拍，D=正文先行；D 后续若引补图须按版本区别。**逐轮对照**：`demo-assets/<id>/*_LOCAL.png`、画廊逐篇 PNG、`demo-assets/<id>/stage*_OWN.png`；`cases/<id>/v*/` 中所有旧渲染、失败审核和日志不覆盖。脚本在工程根 `build_cases.py`、`build_more.py`、`render_core.py`、`render_saved.py`、`revise_*.py`、`audit_*.py`；真实调用/退出及 SHA 看 `RUN_V01.md`、`STAGE4_EXECUTION.md` 至 `STAGE9_EXECUTION.md`。旧阶段 README 的“local-only/不入 Git”是**当时公开仓库或授权未确定时期的历史表述**，本次在私人协作仓库获得完整上传授权，不能倒改旧判词。

## 可剪片段与需新录的镜头

**已有素材可剪**：每例 PNG、同目录 editable `.blend`、画廊高分辨率双栏、十例总览导航、v01 首版拼图、13 同场景探头近景、18 v05→v06→v07 自制版图、20 成品/预封两种**不同状态**、各次审计失败文本与场景独立重开 SHA。既有拼版是静态图，**不是软件 UI 录屏**；任何 0 FAIL 只说明对应有限检查对象。对照画布引用出版方图，**仅在本私有项目内交协作者内部看/制作草片**，并不意味着取得公开发表、公开演示或再次分发许可；外发前需确认许可或改用自绘/无源图片。

**尚需重新录制/制作**：真人/AGH 操作屏录（本批 Computer Use 后期 apps discovery failed，没有可靠新截图文件）、Blender 打开/选物/旋转场景的画面、16:9 成片背景/镜头运动、旁白字幕、对版权图的发布替换和最终视频导出。没有已经完成的视频文件。运行时 v1.0 的 `skill_read` 事实可在项目文本转述，不伪造过去的界面截图或说已加载 v1.1。

### 推荐 60–90 秒顺序

1. **0–10s** 四类材料范围＋2×5 导航，字幕“十篇、低成本可编辑模型，非功能验证”。
2. **10–30s** 04 五路微流 v01 假孔/断路→v04 五端 FAIL→v06 候选，旧失败保留。可用自制 PNG；如加入源 Fig3C 只限获许可/内部草片。
3. **30–48s** 13 v07 总览→同几何 `detail_tip.png`，讲近景仅身份局部；或 14 v04 穿板错误→v05 真孔，字幕“只解决具体可见问题”。
4. **48–70s** 18 Fig18 v03 直杆→v06 栅栏**外部已否定**→v07 斜向**待目视**；穿插 20 的成品/预封状态对比。不要把 Fig17 Type IV 和 Fig18 PIM 当同一试样。
5. **70–90s** 十例目录 `.blend` 可编辑与 source/PNG SHA；明确“外部目视、有限自动检查、功能三列分开，最终未验收”。

### 推荐 2–3 分钟顺序

0–20s 来源/分类与真实 v1.0 运行记录；20–45s A/B/C/D 各取一篇源锚点与新版总览；45–95s 04/13 的接口与可辨身份、连线 FAIL→定点修复（限具体已被复核的旧/候选版）；95–135s 14 真孔与 18 v03→v07 失败迭代；135–160s 20 最终封与预封工艺态分屏；160–180s 局部细节、独立重载哈希和待人工逐例复核清单。**所有宣传性结论仅限定于已实际外部目视的版本。**旧 [素材索引](validation-next/2026-10-14/demo-assets/DEMO_ASSET_INDEX.md)/[分镜草案](validation-next/2026-10-14/demo-assets/DEMO_STORYBOARD.md)保留真实失败史，新片按此处最终入口/状态选帧。

### 打开与复现

图片可在 clone 后直接用系统预览或浏览器打开 `.png`，本地浏览器打开画廊 `index.html`（相邻图使用相对文件名）。Blender 5.1.2 或兼容版本通过 File → Open 打开对应 `scene.blend`；不应把生成时 Blender 路径当必须存在的协作者路径。需要重算时在 `validation-next/2026-10-14/` 查版本构建脚本与运行记录，**不要覆盖已交付场景**；新输出另建版本。`docs/history/GIT_FILE_MANIFEST_VIDEO_DEMO.txt` 含这次上传文件路径、字节数与 SHA-256，用来核对 clone 完整性。上传不是许可声明，也不是改判旧图通过。
