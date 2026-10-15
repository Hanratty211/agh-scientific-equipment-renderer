# 共享 Blender 验收执行器

`accept_case.py` 在独立 Blender 进程中重开保存场景，以案例契约固定审计脚本 SHA-256 和检查 ID 集合。覆盖遗漏、重复 ID、非 PASS、错误计数、路径或哈希不符、超时、进程错误均不能通过；输出目录必须为新目录，已有证据不覆盖。

```bash
python3 -m unittest discover -s tools/acceptance -p 'test_*.py' -v
python3 tools/acceptance/accept_case.py SCENE.blend NEW_OUTPUT_DIR \
  --contract CONTRACT.json --blender /path/to/blender
```

环境变量 `AGH_BLENDER` 可配置默认 Blender，未设置时从 PATH 查找 `blender`。仅依赖 Python 标准库；案例审计在 Blender Python 中执行。几何契约由案例提供，视觉复核另行执行。完整案例命令见 `results/2026-10-15/REPRODUCE.md`。
