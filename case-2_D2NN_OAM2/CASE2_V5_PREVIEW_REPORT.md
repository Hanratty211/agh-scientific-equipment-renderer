# Fig.2(a) v5 低成本无字预览（2026-10-11）

**交付**：`build_case2_v5_overview.py`、`render-output/scene_case2_v5_overview.blend`、`render-output/case2_v5_overview_wordless.png`（1200×750、Cycles 24 samples），`verify_case2_v5_overview.py` / `verify_case2_v5_overview_results.txt`。v4 的脚本、.blend、PNG 哈希复核不变。本轮无标注、新布局或正式图；Skill 仍草案。

## 实际修改
1. 光路拓扑与器件粗位置沿用 v4。分段直线管改为**首尾等宽连续的渐变光束包络**：由激光约 2 mm 示意半径，经 L1/L2 扩大，Iris1/Iris2 附近收窄，末段向 Holder 收窄；光束中心线与原作用面锚点一致。红色仅代表 1064 nm 光路的图示色，调低发光强度以免遮挡。
2. 镜片改成有弧度的双凸闭合网格＋深色边圈；Blender Principled BSDF **Transmission Weight=.94，IOR=1.47**。保留透镜中心入射/出射点，添加网格有效性检查。BS 用透射材质加框边；DMD/SLM 有不同暗色正面、外壳和边框，镜面/光阑分别保持原形态和方向。
3. 激光器加进出光孔边圈和顶部散热片；PD 加入口边圈、输出端口；示波器加边框、独立屏幕、三个旋钮与**纯示意**波形（绝非论文测量迹线）。这些不是厂家 CAD。
4. Holder→BC 三根纤维沿旧路径连续，但各圈半径/中心/高度缓变，减少同一纤维多圈完全重合；BC→PD 与 PD→示波器电缆采用端点保持的柔性曲线，端点重新落在**真实网格面**。没有改变光纤、检测支路拓扑。
5. 相机 orthographic scale 2.25→2.05、aim y .02→.14，意在收紧下方空桌面；未挪动光路器件。

## 几何核查（不等于图像可读性）
从 saved `.blend` 独立重读：`verify_case2_v5_overview.py` **196 PASS / 0 FAIL，进程 exit 0**。新增检查透射材质、7 个镜片合法网格及入/出点在网格表面、19 个光学段起止锚点与包络半径/相邻段连续、三根 Holder→BC / BC→PD / PD→示波器线的实物端口求交、全部纤维点入框；原镜面真实网格法向、反射式 SLM 返回 BS、所有主要部件地面以上及完整入框检查仍通过。未将 bbox 极值当作实际作用面；没有量测挡光或视觉遮挡。

## 实际图片观察
**本轮模型没有看到 v5 PNG**：`computer_use list_apps` 返回 `Computer Use apps discovery failed`，此前 `list_windows` 亦失败。PIL 仅读出 1200×750、PNG 有像素及哈希；没有进行与原图并排的实际视觉判断或基于图像的自修。用户先前对 v4 的外部观察“整体布局基本对应，尚未通过”是 v4 的反馈，不能自动套用 v5。请外部按下方 SHA-256 对 v5 实际读图，尤其观察透射镜片是否可辨、装置是否被红束遮挡、三根纤维是否分离、屏幕与底部桌面的视觉占比。

## 与原图剩余的已知差异 / 仍属假设
- 宽度函数、束腰、焦距和间距**都非论文实测值**；真实透镜曲率/IOR/涂层与实际光束尺寸未得知。透射材质参数是低成本渲染的图示设定，非厂家玻璃数据。
- 机箱、屏幕 UI、示意波形与三根 2/4/6 m 延迟线的盘绕尺寸/颜色不复刻真实型号或量测；无字预览省略原图文字与 Hologram/Phase 插图。
- BS/dichroic 返回端口细节、零级另一支路及整体与原图的**视觉差异排序**仍待实际读图；已知 SLM 正面反射、BS→M3 后续路径未改。空间分离依据仍是 SLM 相位中的 blazed grating，不臆造波长/偏振分光机制。

**最终 PNG SHA-256** `b1ccd71909c97608d438ad8889b76b617b39e065c5f195b8daf42200fa3c2dfe`；saved .blend `5e57f74d0162a1f175090a09b7fdc300feeda304b28ee8c35bf12936afee8620`；构建脚本 `e88c8b37643bf73daa17d4596b854120d7d9e9ccd4e7bdf7809291b58effdddc`。07:11 UTC 为防重跑留下 `.blend1` 而设置 `save_version=0` 后重建/复验，早前同名制品哈希作废。这是文件版本指纹，不是像素视觉通过证据。
