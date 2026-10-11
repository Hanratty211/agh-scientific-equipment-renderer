# Case-2 证据基础：D2NN OAM-STM 系统 Fig. 2(a) 实验装置

> **历史文件，以下旧布局/光纤/SLM/BS 机制条目已被 R4–R11 撤回，不可作为 v4 建模依据。** 旧称“全部器件沿左→右单水平光路”、短圆柱光纤、透射式/从 SLM 背面出射，以及“BS 分出零级”等均错误或无依据。请以原 Fig.2(a)、PDF p.3/4/8/9 和 `REVISION_LOG_case2.md` R11 为准。保留以下原文仅作纠错历史。
来源：Feng et al., "High-speed all-optical neural networks empowered...", Light: Sci. & Appl. 14:342 (2025), arXiv/PDF `source_paper.pdf`
目标图：PDF 第 4 页 Fig. 2(a) "Experimental setup"（参考图 `reference_Fig2a.png`，本轮仅复刻 2(a)）
装置性质：**已实现**的 proof-of-concept 实验系统（正文："a proof-of-concept system was constructed, as illustrated in Fig. 2a"）——与 case-1 的"proposed setup"不同，本例为已搭建实物，按已实现处理。

## 一、光路顺序（按 Fig.2(a) 标签与正文）
1. **Pulse laser**（EKSPLA FPS200，1064 nm，10 ps，10.21 MHz）→ 高斯脉冲激光
2. **L1 + L2**：4f 扩束/准直（"expanded and collimated using two lenses (L1 and L2)"）
3. **M1 + M2**：两面反射镜折叠光路（"reflected by two mirrors (M1 and M2)"）→ 照射 DMD
4. **DMD**（Vialux V-650L，1280×800，10.8 µm 像素）：显示 Lee 全息图（CGH，"Hologram" 标签）→ 生成 7 组 OAM 光束（3-bit 编码）
   - 图注标签 "Hologram" 指 DMD 上显示的 CGH，是**示意图插入/概念**，不是独立物理光学元件（需求 B2：Hologram/Phase patterns 判为示意，不造实体）
5. **4f 滤波（L3 + L4 + Iris）**："filtered through a 4 f system, with the +1 order diffraction light directed onto SLM"
6. **SLM**（Meadowlark E19×12，1920×1080，8 µm）："Phase" 标签；单一 D2NN 层（相位全息相位板，垂直入射）
   - SLM 前：HWP（半波片）+ Polarizer（"passing through a half-wave plate and a polarizer"，调偏振）
   - 图注 "Phase" 指 SLM 加载的相位分布，同 Hologram 一样是示意，不造实体
7. **Dichroic prism + M3**："After SLM modulation, a dichroic prism and a mirror (M3) reflect the outgoing light" → 反射 90°/偏转
8. **4f 滤波（L5 + L6 + Iris）**："another 4 f system (L5 and L6) and an iris were used to filter out the diffracted light"
9. **L7**：聚焦到光纤延迟线输入端（"focused by a lens into the input ends of the optical fiber delay lines"；"input ends were fixed at the focal plane by a customized holder"）
   - "Holder" 标签
10. **3× MMF（optical fiber delay lines）**：2 m / 4 m / 6 m（S3/S2/S1），"arranged... ends of the fibers coinciding with the output plane of the D2NN"
11. **BC（3×1 beam combiner）**："combined and incident into an MMF via a 3 × 1 beam combiner"
12. **MMF（单模/多模耦合光纤）**："incident into an MMF"
13. **PD（InGaAs 光电探测器，Thorlabs DET08CFC/M）** + **Oscilloscope（Keysight DSAV164A）**

## 二、相对布局（Fig.2(a) 视觉组织，复刻对象）
- 整体为**单条水平光路**，从左到右：Pulse laser → L1 → L2 → M1 → M2 → DMD → L3 → Iris → L4 → BS(图注写 BS，但正文为 dichroic prism) → HWP/Polarizer → SLM → M3 → L5 → Iris → L6 → L7 → MMF×3(Holder) → BC → MMF → PD → Oscilloscope
- **关键空间关系**：
  - L3/L4 4f 在 DMD 与 SLM 之间，用于取 +1 级并扩束；**正文 p.9：“The distance between the DMD and SLM is 0.7 m after subtracting the length of the 4 f system”——0.7 m 是扣除 4f 系统长度后的净距，不得写成含 4f 的总间距**（R1 曾误读为“总间距 0.7 m 含 4f”，R4 更正）。
  - M1/M2 把激光从光源折到 DMD（折叠光路，故 M1/M2 在 L2 与 DMD 之间做 90°/180° 转向）
  - M3 在 SLM 后把出射光反射（dichroic prism + M3 把共光路分开/转向）
  - **三条 MMF 延迟线**在 L7 后并排（S1/S2/S3 激活区），各自输入端对准 D2NN 输出面，经 Holder 固定；这是"光纤延迟线"折叠成束的关键视觉元素
  - BC 把 3 束合成 1 束进 MMF → PD
- **红色光束**：Fig.2(a) 中光路用红色线条表示——**仅为示意图着色，不代表 1064 nm 实际可见颜色**（记录为 schematic coloring，不渲染成红色实体，光路用中性/示意色或透明）

## 三、命名/表达差异（如实记录，不遮盖）
1. 图注写 **"BS beam splitter"**，但正文该位置实际是 **dichroic prism**（"a dichroic prism and a mirror (M3)"）→ 图注用 BS 泛指，按正文记 dichroic prism，建模用分光棱镜，标签记 "BS(dichroic prism)"。
2. "Hologram"(DMD) 与 "Phase"(SLM) 是**图案/相位分布示意**，不是独立物理板 → 判为示意插入，不造实体光学件（DMD/SLM 本身是实体，其上图案概念用标签/浅色面表示）。
3. 正文 4f 系统 L3+L4（DMD→SLM）与 L5+L6（SLM→MMF）共 4 片透镜 + 各 1 Iris；图注 L1~L7 共 7 片，M1~M3 共 3 镜。
4. 图注 "BC 3×1 beam combiner"；正文 "3 × 1 beam combiner"。一致。

## 四、可建模部件清单（3D 场景）
| 对象名 | 类型 | 依据 |
|---|---|---|
| pulse_laser | 激光盒 | 正文 |
| lens_L1..L7 | 平凸透镜(薄镜盘) | 图注 |
| mirror_M1..M3 | 反射镜(薄板) | 图注 |
| dmd | DMD 板 | 正文 Vialux |
| slm | SLM 板 | 正文 Meadowlark |
| hwp / polarizer | 半波片/偏振片(薄片) | 正文 |
| bs_dichroic | 分光棱镜(楔形/平板) | 正文 dichroic prism |
| iris1 / iris2 | 光圈(带孔板) | 正文 Iris |
| mmf_delay_1/2/3 | 3 条多模光纤延迟线(圆柱, 2/4/6 m→折叠成束) | 正文 |
| holder | 定制夹持器 | 正文 Holder |
| bc_combiner | 3×1 合束器(楔/盒) | 图注 |
| mmf_single | 输出 MMF | 正文 |
| pd | InGaAs 探测器(盒/圆柱) | 图注 |
| oscilloscope | 示波器(盒) | 图注 |
| beam_seg_* | 光路段(示意, 中性色) | 光路连接 |

> 光纤延迟线 2/4/6 m 实际为长光纤，图中折叠成一小束 → 3D 中用**多根并排短圆柱 + 标注 2/4/6 m**，不画 6 m 长直线（复刻参考图的折叠视觉组织）。

## 五、建模假设 / 不确定项（不得写成已测量事实）
- 各透镜焦距、镜/透镜间距：正文仅给 DMD–SLM 0.7 m；其余间距为**建模假设**（等距/示意），不标具体数值。
- 光纤"折叠"角度与束半径：建模假设。
- 光路 1064 nm 红外不可见 → 3D 中光路段用**半透明示意色**（非红），红为参考图着色习惯，记录为 schematic。
- dichroic prism 具体角度/位置：按"SLM 后反射 90°"示意。
- 所有未给定安装细节（透镜尺寸、镜座）→ 用简约薄板/圆盘表达，标注为示意。
