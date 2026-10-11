# 87Sr 光晶格钟 + 低温腔 — 装置状态与波长核对记录
来源：arXiv:1009.2017 (Middelmann et al., 2010)，全文已下载 source-materials/cand_C_bbrSr.pdf

## 波长核对（本轮修正）
| 光束/跃迁 | 波长 | 论文出处 | 备注 |
|---|---|---|---|
| 钟跃迁 ³P₀−¹S₀ | 698 nm | "spectroscopy on the clock transition 3P0−1S0 at 698 nm" | 这是**钟激光**，不是晶格激光 |
| 晶格激光 (magic wavelength) | 759 nm（本篇未写数字，引用 [11]） | "loaded into a 1D optical lattice at the magic wavelength [11]. Light is provided by a Ti:Sapphire laser" | **不能标 698 nm**；⁸⁷Sr magic=759 nm 是已知值，但本篇只引用 [11] 未列数字，图中写 "magic wavelength (Ti:Sapphire)" |
| 冷却 ¹P₁−¹S₀ | 461 nm | "trapped and cooled on the 461 nm transition" | 主 MOT |
| repump ³S₁−³P₀ | 679 nm | "repumping ... (679 nm)" | |
| repump ³S₁−³P₂ | 707 nm | "(707 nm)" | 扫 5 GHz |
| 第二级 MOT ³P₁−¹S₀ | 689 nm | "second MOT stage on the 689 nm intercombination line" | 冷却到 3 mK |

## 装置实现状态（Fig.7 = proposed，勿与已实现合并）
**已实现/已测试（正文 + Fig.8）**：
- 真空室（MOT 线圈位于真空室内）
- 炉子 480 °C → 热原子束 → Zeeman 慢速 → 2D 光粘滞偏转 → MOT
- 第一级 MOT (461 nm) → 第二级 MOT (689 nm, 3 mK) → 光晶格装载
- 晶格激光 Ti:Sapphire，600 mW 光纤输出（通常 150 mW 聚焦）
- 移动晶格测试：两个 air-bearing 平移台，synchronized by real-time control，mounted on adjustment frames（4 自由度：2 平移 + 2 角向）。Fig.8 已展示 50 mm 移动 / 300 ms，amax=7 m/s²。

**拟建（proposed，Fig.7 原文明确 "proposed setup"）**：
- 低温铜腔：cylindrical copper structure，内径 ~10 mm，长 160 mm；内衬 CuO（100 µm）；
  aperture 分隔 interrogation volume 与后段；tilted sapphire window（对晶格光透明、吸收 BBR）
- 目标 77 K（液氮温区）
- dc Stark 场板（Fig.3，Zerodur + 半透金层）

## 本轮对 Blender 场景的修正
1. 晶格激光颜色/标签改为 759 nm (magic)，不再误标 698 nm
2. MOT 线圈改为**环形/螺线管示意**（空心圆筒线圈，非实心圆柱）
3. 铜腔改为**空心管**（有内腔，CuO 内衬示意为内层）
4. 移除 3D 文字标注（交无文字预览）
5. 相机自动取景包围全部部件 + 边缘余量
6. 真空室不画成巨大实体箱（无外形依据），改以剖切/线框方式表达，内部可观察
7. 低温铜腔标注为 "proposed"，不与已实现部件混淆

## 更正与补充（v3 轮）

### magic wavelength [11] 核实
- 原文只写 "magic wavelength [11]"，未给出数值。
- 参考文献 [11] = Katori, Takamoto, Pal'chikov, Ovsianikov, *Phys. Rev. Lett.* 91:173005 (2003)，
  该文首次定义 Sr 的 magic wavelength。⁸⁷Sr 的 magic wavelength 在后续文献中常被引用为
  **813 nm**（⁸⁸Sr 的 magic 值也有 759 nm 附近的报道，取决于同位素与跃迁）。
- **本次未能在线核实 Katori 2003 原文中的具体数值**（网络检索受限），因此：
  - 图中标注统一写 "magic wavelength (Ti:Sapphire, [11])"，**不写具体 nm 数字**，避免冒充已核实依据。
  - 若后续需标注数值，须先核实 Katori PRL 91:173005 或引其后续 Sr 晶格钟论文。

### 冷却温度序列（正文核实）
1. 第一级 MOT (461 nm) → 冷却到 **约 3 mK**
2. 第二级 MOT (689 nm 间组跃迁，开启 frequency modulation + stirring) → **约 50 µK**
3. 关闭频率调制与搅拌光、降低光强 → **约 4 µK**，此时装载进 1D 光晶格
（原文："Having cooled the strontium atoms to about 3 mK the first MOT stage is replaced by a
second MOT stage on the 689 nm intercombination line ... we achieve a temperature of the atoms
of about 50 µK. The temperature is further reduced to about 4 µK by switching off the frequency
modulation and the stirring laser beams"）

### 装置性质
- 本论文（1009.2017）是 **PTB 提出的方案论文**：Fig.7 图注明确写 "**Layout of the proposed
  setup**"。低温铜腔（77 K）+ dc Stark 场板为 **拟建（proposed）**；移动晶格测试
（air-bearing 台，Fig.8）在文中以 "In the present test setup" 表述为**已测试**。
- 本次三维渲染是**拟建方案的三维重构示意**，不是已建成整体实验装置的实物照片。

### 上一轮（v2）自检更正记录
- v2 报告曾称"全部部件完整可见"——**不实**。用户核查实际 PNG 后确认整图几乎全灰、
  装置不可辨识（vac_top/vac 后墙等大面积灰色面片 + 相机角度导致内部被遮挡）。
- 更正：`display_type='WIRE'` 仅改视口显示，**不影响 Cycles 最终渲染**（v2 曾误以为 wire
  对象在渲染中消失/透明）。v3 改为不依赖 wire 属性，通过几何剖切（布尔/实体管壁）+ 相机
  位置保证可见性。

### 假设记录（外径/壁厚，论文未给出）
- 铜腔内径 ~10 mm（=半径 5 mm）、长 160 mm：来自原文。
- **外径、壁厚：论文未给出，v3 假设壁厚 1.5 mm（外径半径 6.5 mm）**，仅为示意，
  图外说明中须注明为假设值，不能冒充论文尺寸。
