# 14 acoustic_levitation / v02 R1 结构修订

- 审查来源：Codex 于 2026-10-12 实际阅读 v01 参考–输出像素，判 **requires revision**；具体反馈 `../../CODEX_FEEDBACK_R1.md`。未声称 AGH 亲自读图或 v02 已获视觉验收。
- 修订：阵列从桌面左侧移至顶部下向，水平反射板在正下，液滴位于间隙；一侧摄像机一侧 LED、斜入麦克风，功放/示波器/电脑分别建模；阵列数量简化，需依据源详查。
- 保留 v01；新版本 `build_v02.py`, `scene_v02.blend`, `overview_v02.png` (1120×800; SHA256 `4cdc59bbde232f5001a7bc710218be9d4d8882a766bb1938d55c46a8a5ecf419`)，Blender 5.1.2 低成本整体渲染，源图与输出 PNG/.blend 都留本地，不入 Git。
- `record_v02.json` 按 **外部要求的源中部件**列 9 项，非按 build 里任意物体凑 required。静态 UNKNOWN (exit 3)，独立重开 v02 场景审核 UNVERIFIED (exit 3，FAIL 0，UNVERIFIED 13)；图片数值工具 NUMERIC_ONLY(exit 0)。实际 JSON/日志均在本目录。
- 重大缺口：`ports=connections=supports=0`，仍未逐端证实源图可见接口/光路/流路/线缆/力学近接；立体摆放和图上相交不是功能拓扑。v02 各段是否真实作用面、孔洞/清透、透视遮挡和相片材料比例必须由 Codex/用户查看 `../../pair_14_v01_v02_local.png`，不能借自动分项 PASS 代替。
- 读图状态：v02 未经过外部像素复核；可能继续 v03。
