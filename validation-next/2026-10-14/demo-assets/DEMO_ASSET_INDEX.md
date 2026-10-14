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
