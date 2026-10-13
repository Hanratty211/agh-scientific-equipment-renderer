# BATCH_STATUS — validation-next V21–V30

日期：2026-10-13
分支：agh/validation-next-2026
Blender：5.2.2 LTS（C:\Program Files\Blender Foundation\Blender 5.2\blender.exe）
渲染引擎：BLENDER_EEVEE

## 各案状态表

| 编号 | 论文 | 输入类别 | v01 落盘 | 最新版本 | 视觉验收 | 备注 |
|---|---|---|---|---|---|---|
| V21 | MIP twin beams | B | ✓ scene_v01.blend + overview_v01.png | v01 | 外部审阅 | 无本地 PDF；B 类系统架构保守重建 |
| V22 | soft pneumatic skin | C | ✓ scene_v01.blend + overview_v01.png | v01 | 外部审阅 | 无本地 PDF；C 类实验台架保守重建 |
| V23 | EO flat comb | B | ✓ scene_v01.blend + overview_v01.png | v01 | 外部审阅 | 本地 PDF 已落盘（8页） |
| V24 | soliton microcomb | D | ✓ scene_v01.blend + overview_v01.png | v01 | 外部审阅 | 无本地 PDF；D 类文字主导 |
| V25 | OoTrap | C | ✓ scene_v01.blend + overview_v01.png | v01 | 外部审阅 | 无本地 PDF；C 类外部接口保守重建 |
| V26 | microfluidic T-junction | A | ✓ scene_v01.blend + overview_v01.png | **v03** | 外部审阅 | 本地 PDF 已落盘；v02 外部反馈：T 通道仍不可见→v03 开顶通道 + 高对比流体 + 发光粒子 + 光学面包板 |
| V27 | acoustic levitation LM | A | ✓ scene_v01.blend + overview_v01.png | v01 | 外部审阅 | 本地 PDF 已落盘（8页） |
| V28 | acoustic metamaterial nano | B | ✓ scene_v01.blend + overview_v01.png | v01 | 外部审阅 | 无本地 PDF；B 类保守重建 |
| V29 | ABH metamaterial beam | C | ✓ scene_v01.blend + overview_v01.png | v01 | 外部审阅 | 本地 PDF 已落盘（21页） |
| V30 | UV fluorescence chip | D | ✓ scene_v01.blend + overview_v01.png | **v02** | 外部审阅 | 本地 PDF 已落盘（31页）；v01 外部反馈：外壳全白半透明遮挡一切→v02 翻转底面视角 + 极低 alpha |

## 读图验收说明
- AGH 本会话内建视觉读图工具（vision-skill → qwen3-vl-flash）返回 404 model_not_found，**记录为"AGH 实际读图工具不可用"**，不再重试。
- 视觉验收由外部 Codex 审阅者完成，反馈已在各案 CHECKPOINT.md 单独署名记录。
- AGH 侧像素统计（PIL/numpy：frac_dark / frac_mid / frac_bright / mean_rgb）已对每张 PNG 完成，结果记录于各案 CHECKPOINT.md。

## 交付物清单
- 各案：build_v0X.py + scene_v0X.blend + overview_v0X.png + SOURCE_NOTES.md + CHECKPOINT.md + verification_notes.md
- 批量：SELECTION.md（已更新 V26/V30 来源）、BATCH_STATUS.md、REVIEW_GUIDE.md、contact_sheets/overview_grid.png
