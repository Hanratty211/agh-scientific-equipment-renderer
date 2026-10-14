# 18_mechanical_nature｜低成本示意预览检查点（未验收）

DOI: https://doi.org/10.1038/s41467-026-77199-4。日期 2026-08-26。依据：Methods PDF p.9：ZwickRoell Z100 拉伸测试机与试样；Fig.2d仅后版核测量情境；图/正文中文解释：Methods ZwickRoell Z100 实验机。类别 D，指定完整范围：ZwickRoell Z100 文字明确的双夹持机与代表性格构短试样；不冒称 ASTM IV 为 PIM 样品。

当前场景 `v01/scene.blend` / `v01/overview.png`；最新版 `v01`。构建脚本 `../../build_cases.py`、`../../build_more.py`、`../../render_core.py`；修订使用 `../../revise_cases.py`。Blender 5.1.2 EEVEE，900×640；独立进程重开 scene 并在该版本目录生成 `render_report.json`，存两 SHA256。v01 scene `e74171901bf6db0eedacfc00e72e5dba2326e9530b7afb6806876b0726005878`；PNG `26f54e1eee166a397f5f52ef256ad14c712a1c2733694abd99de7be08fd5ce35`。这不证明像素、物理或装配。

主要三项差异：机身代表性；格构状如梯子无图证；夹钳距离存疑。建模假设：所有相对比例/尺寸/背景；未见的接口和内部结构不能按场景推为论文事实。开放未知：机器外形需核公开型号资料，未核前仅代表性。本版变化：仅 v01 首版，未伪造失败后的 v02。人工优先核验：型号外观及真实试样参 Supplementary Fig.17–20。实际审阅：AGH 批次拼图捕获 3378，粗看而非逐例高清；其余无逐例 PNG 专项读图。外部模型未审，人工未审。

|检查点|来源位置|输出位置|证据类型|结论|待人工确认|
|---|---|---|---|---|---|
|范围与身份|Methods PDF p.9：ZwickRoell Z100 拉伸测试机与试样；Fig.2d仅后版核测量情境|`v01/overview.png`|论文图/正文 + AGH 粗看|示意阶段/未验收|型号外观及真实试样参 Supplementary Fig.17–20|
|可见线路/装配|Methods PDF p.9：ZwickRoell Z100 拉伸测试机与试样；Fig.2d仅后版核测量情境|`v01/scene.blend`|有限网格+渲染|未完成实端口逐跳验证|开孔、接头、遮挡及支撑|
|图像外观|见本地 `../../demo-assets/18_mechanical_nature/source/SOURCE.md`|`v01/overview.png`|AGH 实际读批次拼图|不作通过声明|对应实物形态|
