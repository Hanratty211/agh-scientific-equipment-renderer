# 下载后的独立复核

从仓库根目录执行，推荐本次实际使用的 Blender **5.1.2**。Python 3 用于验收执行器；无需 Agnes 会话。以下 `rerun/` 被 Git 忽略，重复执行时请换用新输出目录。

```bash
# macOS 示例；其他系统将变量改为实际 Blender 路径
export AGH_BLENDER="/Applications/Blender.app/Contents/MacOS/Blender"
python3 tools/acceptance/accept_case.py results/2026-10-15/microfluidics/scene.blend rerun/microfluidics \
  --contract results/2026-10-15/microfluidics/contract.json
python3 tools/acceptance/accept_case.py results/2026-10-15/microfluidics/scene.blend rerun/microfluidics-support \
  --contract results/2026-10-15/microfluidics/support-contract.json
python3 tools/acceptance/accept_case.py results/2026-10-15/robotics/scene.blend rerun/robotics \
  --contract results/2026-10-15/robotics/contract.json
```

预期为 PASS：141 项、5 项、32 项。新输出包含本次 `gate.json`、`geometry.json` 与执行日志；这些是自己的复核记录，不会替换原始记录。

多视图重渲染（从相同保存场景读取几何与材质）：

```bash
"$AGH_BLENDER" -b results/2026-10-15/microfluidics/scene.blend --python-exit-code 1 \
  --python results/2026-10-15/microfluidics/render.py -- rerun/microfluidics-renders
"$AGH_BLENDER" -b results/2026-10-15/robotics/scene.blend --python-exit-code 1 \
  --python results/2026-10-15/robotics/render.py -- rerun/robotics-renders
```

图片对照的最终场景重放：

```bash
"$AGH_BLENDER" -b results/2026-10-15/visual-comparison/baseline/scene.blend --python-exit-code 1 \
  --python results/2026-10-15/visual-comparison/replay.py -- rerun/comparison-baseline
"$AGH_BLENDER" -b results/2026-10-15/visual-comparison/skill/scene.blend --python-exit-code 1 \
  --python results/2026-10-15/visual-comparison/replay.py -- rerun/comparison-skill
```

重放只复核已生成场景，不等同于重新采样模型。原环境两组重放像素完全一致；跨 Blender 版本、设备或渲染后端不保证逐像素相同。取得论文来源图后，另作来源—生成图的实际视觉复核。

核对发布文件：在 `results/2026-10-15/` 中运行 `shasum -a 256 -c SHA256SUMS.txt`（Linux 可用 `sha256sum -c`）。

## 用户接受的机器人 v08

旧 `robotics/` 保留 v07；新版复用相同的32项冻结契约和渲染脚本。

```bash
python3 tools/acceptance/accept_case.py results/2026-10-15/robotics-v08/scene.blend rerun/robotics-v08 \
  --contract results/2026-10-15/robotics/contract.json
"$AGH_BLENDER" -b results/2026-10-15/robotics-v08/scene.blend --python-exit-code 1 \
  --python results/2026-10-15/robotics-v08/verify_revision.py -- rerun/robotics-v08-shapes.json
"$AGH_BLENDER" -b results/2026-10-15/robotics-v08/scene.blend --python-exit-code 1 \
  --python results/2026-10-15/robotics/render.py -- rerun/robotics-v08-renders
```

预期：原32项 PASS，补充10项 PASS。补充脚本相对于自身定位 v07 基线；不会修改任一场景。输出文件请使用新路径以保留每次记录。

可选：从 v07 重新执行修复（输出场景必须不存在）：

```bash
mkdir -p rerun/robotics-v08-rebuild
"$AGH_BLENDER" -b results/2026-10-15/robotics/scene.blend --python-exit-code 1 \
  --python results/2026-10-15/robotics-v08/repair.py -- rerun/robotics-v08-rebuild/scene.blend
```

重建会输出场景和 changes.json；Blender 场景重新保存的文件哈希不承诺与发布件一致，发布件仍按 SHA256SUMS.txt 校验。
