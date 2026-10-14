# 演示素材索引｜2026-10-14

AGH 在会话 e3897ec9-dd7e-4bc7-bc55-a3ec72d67bd6 用已加载 v1.0 读取来源与生成十张 v01；渲染是**未验收首稿**。按案例查 `../cases/<id>/v01/{scene.blend,overview.png,render_report.json}`，输入来源查 `<id>/source/SOURCE.md` 和相邻本地 PNG / `../sources/<id>.pdf`。原出版方页图/PDF许可未核不入公开 Git；含源图的比较 PNG 也暂不提交，文字索引会指向本地素材。

|故事|画面|问题→变化|审阅者/边界|执行证据|
|---|---|---|---|---|
|04 B 微流控|04_microfluidics/source/target_fig3C.png → ../cases/04_microfluidics/v01–v03/overview.png → 04_microfluidics/comparison_source_v01_v02_v03.png|v01 假孔→v02 修订回退→v03 补左侧储液仍断连；失败过程真实保留|AGH 阅读源/总览；无人类确认|../RUN_V01.md；捕获 3223|
|02 C 机器人实拍|02_robotics/source/target_fig3b.png → ../cases/02_robotics/v01/overview.png|夹爪/试样弱连接→尚待修|AGH 总览拼图粗看|捕获 3378|
|15 A 多层传感器|15_biomed_energy/source/target_fig3a.png → ../cases/15_biomed_energy/v01/overview.png → 15_biomed_energy/comparison_source_v01_v02.png|v01 上封装实心遮 PV→v02 真实布尔开窗，局部改善；总体未通过|AGH 源图捕获 2437，总览粗看 3378|../VISUAL_REVIEW_V01.md|
|16 D 文字能源|16_energy_nature/source/text_p9.txt → ../cases/16_energy_nature/v01/overview.png|首版仅文字→若引图必须 v02|AGH 方法文本核，未视觉细节审|../selected_cases.json|
|其余六例|相应 `<id>/source/` 和 `../cases/<id>/v01/overview.png`|待逐例查核|无人工/外部模型确认|../VISUAL_REVIEW_V01.md|

总览拼图 `v01_contact_sheet.png`（捕获 3378），版本逐文件独立，不在无字原图上加字幕。界面截图工具返回仅本会话 artifact，**未取得本地屏幕截图文件**；视频用源PNG与比较画布代替，不冒称截图。已取得 04 的三版比较图及 15 的前后拼图；高质量 16:9 演示版仍缺，不为视频额外高成本重渲。

## 当前轮追加（保留失败及私有源图）
- 04：`../cases/04_microfluidics/v04/`（泵端 audit 五路 FAIL），`v05/`（5×6 外部边界 audit 0；PNG 未实读），数值报告 `v05/boundary_audit.json`；本地含论文图画布 `04_microfluidics/comparison_source_v01_v03_v04_v05_LOCAL.png`。证据 `../REVISIONS_04_V04_V05.md`。
- 15：`../cases/15_biomed_energy/v03/`（隔离分层候选，PNG 未实读）；本地含论文图 `15_biomed_energy/comparison_source_v01_v02_v03_LOCAL.png`；证据 `../REVISIONS_15_V03.md`。
- 十例单幅源—当前版 `*/source_and_current_LOCAL.png` 仅本地，不入 Git；**04/15 两张单幅生成时还是旧 v03/v02**，查看最新要用上面的多栏图。十例具体源/当前链接见 `../INDIVIDUAL_REVIEW_TABLE.md`。GUI Computer Use 窗口发现失败，未得到新截图；不得在视频标'十例已审'。

## 人工十例复核后：新候选帧及真实失败史
- 审阅者：**外部人工视觉复核**，逐例旧版图/正文与 v01（04 v05、15 v03）比较；十例均指出身份、接口或承载缺陷，详见 `../EXTERNAL_HUMAN_REVIEW.md`。这不是 AGH 对新图的 capture。
- 本次十例新渲染帧/可编辑 scene/哈希：`../NEW_VERSION_REVIEW_QUEUE.md`；04 v06、15 v04、02 v03、其余 v02。自制新 PNG 可用于候选演示，但字幕须标“新图目视待审”。
- 04 v05 30/30 数值与外部人工判视觉失败同时保留；v06 40/40 外部几何也不是像素或功能验收。`../cases/04_microfluidics/v06/boundary_audit.json`。
- 20 final 主览 `../cases/20_thermal/v02/overview.png` 与预封口单独状态 `../cases/20_thermal/v02_preseal_detail/overview.png` 不混剪为同一实体状态。
- 本地十张 `demo-assets/<id>/new_source_v01_<v>_LOCAL.png` 含出版方源图，只在本机，**不可提交、不可直接当公开视频镜头**。没有恢复的 AGH GUI 截图文件，不能伪称界面录屏。

- 02 又多一段真实失败史：v02 上夹爪端位置 audit FAIL，v03 定点修复后仍待目视；本地四栏画布 `02_robotics/new_source_v01_v02_v03_LOCAL.png`。

准确版本更正：02 最新是 v03（v02 上夹端检测 FAIL），04 v06，15 v04，其余 v02。
