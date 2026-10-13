# V30 verification notes

日期：2026-10-13
AGH 视觉读图：**不可用**（vision-skill 404）
像素统计：v01 1280×960 mid=0.88 bright=0.12 mean_rgb=[77,93,111]

## v01 → 外部审阅者反馈
- 全图基本为白色半透明外壳 + 底板
- VCSEL / PD / 芯片 / LiPo / USB-C / 金线 / 光束均不可见
- 无法验证论文目标器件

## v02 修复内容（build_v02.py）
- 翻转底面视角（相机朝下看芯片底面）
- 蓝宝石 alpha=0.08（近乎透明）
- 外壳 alpha=0.30
- 三盏底部补光，使底面器件透射可见
- 金色走线 / 焊线 / UV 光锥 / 荧光路径保留

## AGH 已验证
- [x] Blender 运行成功 → scene_v02.blend + overview_v02.png（sha256=c2b3e1…）
- [x] 场景重开保存成功

## 待外部审阅
- [ ] overview_v02.png 中底面器件（VCSEL / PD / 芯片 / LiPo / USB-C / 天线 / 走线）是否清晰可见
