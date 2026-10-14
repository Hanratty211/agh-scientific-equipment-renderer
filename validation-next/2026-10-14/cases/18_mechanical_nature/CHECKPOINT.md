# 18_mechanical_nature｜低成本示意预览检查点（未验收）

DOI: https://doi.org/10.1038/s41467-026-77199-4。日期 2026-08-26。依据：Methods PDF p.9：ZwickRoell Z100 拉伸测试机与试样；Fig.2d仅后版核测量情境；图/正文中文解释：Methods ZwickRoell Z100 实验机。类别 D，指定完整范围：ZwickRoell Z100 文字明确的双夹持机与代表性格构短试样；不冒称 ASTM IV 为 PIM 样品。

当前场景 `v01/scene.blend` / `v01/overview.png`；最新版 `v01`。构建脚本 `../../build_cases.py`、`../../build_more.py`、`../../render_core.py`；修订使用 `../../revise_cases.py`。Blender 5.1.2 EEVEE，900×640；独立进程重开 scene 并在该版本目录生成 `render_report.json`，存两 SHA256。v01 scene `e74171901bf6db0eedacfc00e72e5dba2326e9530b7afb6806876b0726005878`；PNG `26f54e1eee166a397f5f52ef256ad14c712a1c2733694abd99de7be08fd5ce35`。这不证明像素、物理或装配。

主要三项差异：机身代表性；格构状如梯子无图证；夹钳距离存疑。建模假设：所有相对比例/尺寸/背景；未见的接口和内部结构不能按场景推为论文事实。开放未知：机器外形需核公开型号资料，未核前仅代表性。本版变化：仅 v01 首版，未伪造失败后的 v02。人工优先核验：型号外观及真实试样参 Supplementary Fig.17–20。实际审阅：AGH 批次拼图捕获 3378，粗看而非逐例高清；其余无逐例 PNG 专项读图。外部模型未审，人工未审。

|检查点|来源位置|输出位置|证据类型|结论|待人工确认|
|---|---|---|---|---|---|
|范围与身份|Methods PDF p.9：ZwickRoell Z100 拉伸测试机与试样；Fig.2d仅后版核测量情境|`v01/overview.png`|论文图/正文 + AGH 粗看|示意阶段/未验收|型号外观及真实试样参 Supplementary Fig.17–20|
|可见线路/装配|Methods PDF p.9：ZwickRoell Z100 拉伸测试机与试样；Fig.2d仅后版核测量情境|`v01/scene.blend`|有限网格+渲染|未完成实端口逐跳验证|开孔、接头、遮挡及支撑|
|图像外观|见本地 `../../demo-assets/18_mechanical_nature/source/SOURCE.md`|`v01/overview.png`|AGH 实际读批次拼图|不作通过声明|对应实物形态|

## 外部人工复核后的非破坏候选版（尚未验收）
外部人工逐例读源依据与旧版 PNG 后指出的差异详见 `../../EXTERNAL_HUMAN_REVIEW.md`（审阅者：外部复核，目视，**针对旧版**）。新 `v02` 保存于 [`v02/scene.blend`](v02/scene.blend)、[`v02/overview.png`](v02/overview.png)，独立 Blender 进程重载并渲染。针对性修改：移除梯形 PIM 假试样，建 parent-material Type IV 示意哑铃和上下夹持；PIM另案。绝对尺寸、比例、不可见接口与内部机理仍为建模假设/开放未知。 scene SHA256 `1531ccbf79169b00f4231e6ac090149ff9f53f0d13bd6ba8074a5225bab3311d`；PNG SHA256 `8845c9129ef8979eecc69f729dd7a2c304a93b465c050d8e6d56dda66cdda7fc`。**新图 AGH 未能 capture（apps discovery failed），也尚无新版本外部人工或用户验收；重载成功/几何项 PASS 不等于目视通过。**来源锚点在 `../../demo-assets/18_mechanical_nature/source/SOURCE.md`，本地含原图画布 `../../demo-assets/18_mechanical_nature/new_source_v01_v02_LOCAL.png` 不提交。 正文 p9 明言 ASTM D638 Type IV 对 parent materials；v02 不可称 PIM 格构拉伸样。

### 第二轮外部复核/补充材料核对
审阅者：**外部复核**，明确 v02 dogbone 只代表 parent-material ASTM Type IV，不能等于机械记忆结构。下载论文开放的补充 PDF 51 页至本地，定位 Supplementary Fig.17–20 于 PDF pp.32–35，核到图注：17 parent materials、18 PIM/CIM、19 composites、20 tissue；**AGH 图像服务仍失败，尚未看见补图像素/铰接细节，故不建 PIM v03**。详情 `../../CASE18_SUPPLEMENT_AUDIT.md`。旧 v02 保持 parent-material 示意，未通过本任务整体目标。
