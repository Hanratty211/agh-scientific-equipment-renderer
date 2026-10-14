# AGH 科研装置实物三维 Skill（独立包）

**规范源**：仓库根目录 `agh-scientific-equipment-renderer/`，不要安装历史路径 `skills/agh-scientific-equipment-renderer/`。只复制整个文件夹，放在任意目录即可工作；案例验证档案不随包复制、不作为加载依赖。

```text
agh-scientific-equipment-renderer/
  SKILL.md             # AGH 路由入口/强制门槛
  README.md            # 此安装说明
  CHANGELOG.md         # 方法变更
  PROVENANCE.md        # 版本与运行时边界
  references/          # 仅通用识别、端口、对照、记录和按需域检查
  scripts/             # 通用辅助、结构/抽象反例检查
  examples/            # 合成 JSON/Blender 测试 fixture（不是论文示例）
  behavior_tests.py    # 合成几何行为反例
```

## 安装、调用与测试

在 AGH 使用受管 Skill 导入流程，从此目录作 `local` 来源，随后按宿主确认安装；用户已有同名安装时若返回 `SKILL_TARGET_CONFLICT`，**停止**，不得手动覆盖已安装目录、改名绕过或宣称新版已加载。等待合法的管理流程解决冲突，再于下一轮通过 `skill_read` 的正文和 revision 核实生效版本。仓库提交 ≠ 运行时安装。

`SKILL.md` 的描述用于路由：当用户需要论文装置的实物可编辑三维场景、端口/管线修复或逐篇源图—生成图审查时读取该 Skill；按 `references/identity_port_gate_v11.md` 的四表门槛建模，按 `references/source_render_and_demo_v11.md` 逐版对照，必要时运行工具。自行创建的 Blender 场景生成器与图片比较脚本应在**项目**目录存档，不能假称本包自动生成。

```bash
python3 agh-scientific-equipment-renderer/scripts/test_v11_workflow.py
python3 agh-scientific-equipment-renderer/scripts/check_structure.py
python3 agh-scientific-equipment-renderer/examples/run_v06_regression.py \
  --blender /path/to/blender --report /tmp/agh-equipment-synthetic.json
```

`check_structure.py` 还运行 Blender 反例，需本机 Blender 和 PyYAML；图片数值脚本另需 Pillow。脚本默认 Blender 可执行文件路径可由 `AGH_BLENDER` 环境变量设定，检查产物写系统临时目录而不污染本包。`examples/valid_record.json`、`make_synthetic_scene.py` 只为工具回归，不是论文装置模板。工具通过不等于视觉/科学/安全验证。出版方 PDF、原图、含原图画布不得打包或未经许可提交公开仓库；仅自制通用工具与说明可发布。
