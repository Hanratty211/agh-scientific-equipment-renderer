# 独立 Skill 包的版本与来源边界

- 名称 `agh-scientific-equipment-renderer`；**唯一规范源码目录**：本文件所在仓库根目录的 `agh-scientific-equipment-renderer/`。只拷贝此完整目录即可读 `SKILL.md`、`references/` 并运行 `scripts/`、`examples/`；无需当前验证工程、PDF、图像、逐例表或其他案例目录。旧 `skills/agh-scientific-equipment-renderer/` 的历史内容可经 Git 历史查看，**不是并行安装源**。
- v1.0 曾在受管 AGH 安装并于运行时 `skill_read` 得到 revision `dd9d764a3ec32396818499f03d5deea81121823bcda3dca07fc33dfb29597cde`，且在其加载情况下运行了十例建模；这说明方法已读取，不意味着调用了 Skill 自带 Blender 函数或已完成视觉/功能验收。v1.1 源码曾在 main 的 `a0b946b44b495c4da44e6e232f4cf656701f5775` 提交；对旧的已安装名称尝试受管更新得到 `SKILL_TARGET_CONFLICT`（已有不同内容、拒绝覆盖）。**迁移后的目录仍属源码；没有受管更新成功/新轮次读取证据就不得写运行时 v1.1 已加载。**
- 既往十例的 AGH 自写脚本构建/独立保存场景重开渲染与后续**独立**图片排版不是一回事；Skill 的可选 `review_images.py` 不可在缺调用证据时记为实际使用。合成正反例用于说明代码边界，非某论文的制造、密封、仪器接线、光学/力学或人工接受证据。
- 论文验证工程（仓库里但不在 Skill 包内）：`validation-next/2026-10-14/skill-evidence/` 保存十例台账、历史 provenance、早期故障/证据记录及旧结果；`validation-next/2026-10-14/EXTERNAL_HUMAN_REVIEW.md` 与逐例 CHECKPOINT 留外部读图与未知；出版方 PDF/原图及含源画布未经许可仅本地。它们均非 Skill 运行时依赖。旧原始 PROVENANCE 完整归档，避免历史被新简介覆盖。
- 受管安装应由 AGH 的 `skill_helper_import`（指定**本文件夹**）准备后经安装确认；同名冲突时尊重拒绝，不删除既有安装、改名重装或借 shell 复制绕过。源码版本、安装状态与后续实际 `skill_read` 版本分别记录。
