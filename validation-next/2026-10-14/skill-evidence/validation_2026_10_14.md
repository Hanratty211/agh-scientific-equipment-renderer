# v1.1 依据：2026-10-14 新十篇｜案例证据，不是新版方法的自动验收

上轮加载的是 AGH `agh-scientific-equipment-renderer` v1.0 revision `dd9d764…`，在此条件下 AGH 运行批次 `build_cases.py`/`build_more.py`/`render_core.py` 保存可编辑 Blender 场景，`render_saved.py` 另进程重开出 PNG 与 SHA；阶段修复脚本及有限专项审计各记其版本。此处**不**声称调用了 Skill 内可选 `blender_core.py` 或 `review_images.py`。独立后处理单篇来源—旧—新比较画布，不是 Skill 自带脚本自动生成。源版图/PDF/含源图本地 `validation-next/2026-10-14/demo-assets/<id>/source/` 和 `*_LOCAL.png` 均不随 Skill 分发。可核 Git 文字记录：`SOURCES.md`、`selected_cases.json`、每例 `CHECKPOINT.md`、`EXTERNAL_HUMAN_REVIEW.md` 与 `STAGE9_REVIEW_QUEUE.md`；本参考仅给安全文字/哈希，目录是开发仓库可选档案。

|类/案例与公开 DOI|来源锚点；外部逐例**目视**旧版差异|选定输出版本 · PNG SHA-256；独立**有限**数值/未知|
|---|---|---|
|C 02 软机 [10.1038/s41467-025-56025-3](https://doi.org/10.1038/s41467-025-56025-3)|Fig.3b PDF p4 实拍；v01 矩形夹块/悬杆不像夹试样的拉伸机，v04 支柱改善但夹面仍弱|v05 `daf2a49a5bc5d540097091212649088efcbd88e791cc9434c84ccd0bf40fc6dc`；8项几何零 FAIL，夹力/身份未验收|
|B 04 微流 [10.1038/s41526-025-00470-3](https://doi.org/10.1038/s41526-025-00470-3)|Fig.3C PDF p4 五泵/芯片/五出口，Fig.3A仅外形；v01 浮空环/断管，v04 五条泵端 owner 错；v05 数值零FAIL但视觉仍败，v06 外部称五路关系可读**非密封**|v06 `88dc7e90184b07490e9bd12adec1e4c264e2b18a091aaee79e62cf8d67824199`；40项外边界零FAIL，内流/密封/逐孔未证|
|A 08 可穿戴 [10.3991/ijoe.v22i03.59657](https://doi.org/10.3991/ijoe.v22i03.59657)|Fig.3 左 PDF p6 装配；v01 泛化板/P1 不辨，v02 铜线伸板且未接触点|v03 `a47417101c64de02457e69f3e53fed9e5aaaad9f9ed30804d104dee3b75ccff7`；14项范围近接零FAIL，层边界仍略浮|
|B 13 内窥 [10.1038/s44303-026-00161-y](https://doi.org/10.1038/s44303-026-00161-y)|Fig.1a,c PDF p3 临床车/三纤维，Fig.1f/g 远端外形后补；v01 泛推车+浮屏、硬探头，v06 头窗看不清|v07 `5201684242f676a0a086e5b7331545f5e1e4999ff3e0088b7e3c1f96c2910c88`；6项几何零FAIL；同几何细节 PNG `fed19e439095582c70c8aefc5df7176255dccfd3436711c2690b6b1fb8bb177f` 被外部见前窗/圈层，仅局部身份候选，内部光路未知|
|C 14 声学 [10.1038/s41598-025-24666-5](https://doi.org/10.1038/s41598-025-24666-5)|Fig.1c PDF p3 实拍（a 只作连接逻辑），v01 LDV 斜视，v02 悬空，v04 数值命中样本但**视觉穿实体顶板**|v05 `2b1dd837e8eb14a8a8c1ba8b886bff17fabb393bfc185d7c9e4d69203f1fc8d5`；5项孔轴有限检查零FAIL，外部称支架/真孔/样品这一具体问题解决；不是全图/悬浮功能通过。Fig.1a 有笔电/示波器**仅示意**，不能假称在 c 照片可见或本案例已修好笔电/示波器|
|A 15 贴片 [10.1038/s41467-025-60911-1](https://doi.org/10.1038/s41467-025-60911-1)|Fig.3a 图 p5/图注 p6；v03 层像浮块，v04 同 footprint 改善而顶层身份仍弱|v05 `aca06694ec9a823bbcfcaf14ce14a9cc49dbf6516ce30b915a9c7423c6412f4b`；3项粗层序零FAIL，顶层/电连接未核|
|D 16 CO2 [10.1038/s41467-025-64306-0](https://doi.org/10.1038/s41467-025-64306-0)|Methods PDF p9 先据文字建液泵，后来追加 CO2/Ar+MFC；v01 无源两杯，v03 外部仍见悬管，v04源端 FAIL|v05 `e4d91f20ab5e9abd9fed1a898d81942811d121e352802a5f9b3f3d2731a7772e`；10项有限零FAIL；隐藏池结构/三段视觉接续仍待核，文本不能证明厂家外壳|
|A 17 射频 [10.1038/s41598-026-39831-7](https://doi.org/10.1038/s41598-026-39831-7)|Fig.1a–d PDF p4；v01 双板偏置槽/馈线脱，v02 浮辐射体|v03 `b66c011a53de07c58c5ddee27ac05a3ced92104d8ef76b818f67d743b36ba557`；5项层/馈点近接零FAIL，RF 性能未知|
|D 18 机械 [10.1038/s41467-026-77199-4](https://doi.org/10.1038/s41467-026-77199-4)|Methods PDF p9 Z100，Type IV 仅 parent-material；后查 Supplementary Fig18 PDF p33 左 20×20mm PIM/CIM 面、中压板；v03 直杆、v04 粗绳、v05 细正交、v06 加粗**仍栅栏**均外部指失真|v07 `e4780436f6420065c1ce55fec06ff29733b5211c9e85eeb55910ee2e315d9eeb`；6项曲线/压板零FAIL，**新图未被 AGH/外部目视**；真实节点/深度/材料功能未知|
|D 20 热 [10.1038/s41467-025-56960-1](https://doi.org/10.1038/s41467-025-56960-1)|Materials PDF p11 与正文 p2 铝塑壳/铜网芯；v01 刚槽，v03 最终态露网，预封与封态混淆|v04 `c40b0e9212ab2e0e7db924cec45dc2f4b03948a6d94181a5405936fecf920d2f`；4项封边存在零FAIL，膜/封装真实性未知|

**状态与覆盖**：A=3，B=2，C=2，D=3；多轮外部目视/自动零FAIL与用户最终验收是不同等级。来源图/照片与正文不能互相替代；14 的示意笔电/示波器不在所选 c 照片交付范围内。需做更大系统版本时先明确输入范围，不得以十例没有的示波器成功样例宣称通用可用。本表 SHA 是旧运行记录及现存报告的索引而非新自测 v1.1 渲染。
