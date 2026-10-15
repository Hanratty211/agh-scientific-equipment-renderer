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
