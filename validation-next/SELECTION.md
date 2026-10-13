# 本轮新增公开案例选题表（validation-next）

# 本轮新增公开案例选题表（validation-next）

日期：2026-10-13。执行分支：`agh/validation-next-2026`。运行时装载：`agh-scientific-equipment-renderer` v1.0，`resourceId=skill/user/user-agnes/9c1cae1d1c3aee1a971160ce46dd52ab10785e28ea8577da22cde9ef6a7d4bcf`，`revision=a15cb3a96c0acead420e6ee12d8f525dc0a2c988a5e28b80ebfa309bb9d93ac6`。

本表把“元数据已核验”和“图版/正文已取得”分开。进入首批建模批次的条目必须满足：目标图版或方法文字已取得，来源不是 decision letter/review/SSRN 占位，且不与旧 10 例 DOI 重复。未能取得图版/正文的候选不进入首版批次，只能列为用户可提供附件的候补项。

## 输入类别定义
- A：工程图、装配图、剖面图、CAD 示意图。
- B：系统架构图，有可辨认器件和物理连接。
- C：实验装置实拍图/安装照片。
- D：正文/方法文字为主要建模依据。

## 最终 v01 批量建模批次（10 篇，全部可执行）

说明：本轮使用你补给的官方来源与 arXiv PDF 实际取得目标图版/正文；V27 AIP 不再使用，已由已下载 arXiv:2610.07703 替换。V30 替换为 arXiv:2610.13525（AlGaN/Si-on-Sapphire UV 荧光光电芯片，生物医学/光电芯片领域，D 类）；V26 替换为 arXiv:2610.13796（microfluidic T-junction，流体/微流控领域，A 类）。两例均已落盘本地 PDF，不保留“待补”进入 v01。

| 编号 | 领域 | 论文题目 | 发表时间 | DOI/公开链接 | 输入类别 | 目标图版/文字位置 | 重建对象与范围 | 主要难点 | 元数据核验 | 图版/正文取得状态 |
|---|---|---|---|---|---|---|---|---|---|---|
| V21 | 光学/量子光探测 | Sub-shot-noise mid-infrared photothermal measurements using twin beams | 2026-10-07 | arXiv:2610.10294; https://arxiv.org/abs/2610.10294 | B | arXiv HTML Fig. 1a 及 Methods/Detection 段 | twin-beam MIP 系统：1.5 µm 飞秒激光、FBG/fiber amplifier、SHG/PPLN OPA、seed 滤波与延迟线、QCL/AOM、sample cell、BPD/RFSA 链路 | 光路、电信号与机械布局；不把逻辑分束画成不存在设备 | arXiv Atom API 返回标题、日期和作者 | HTML 正文与 Fig.1/Fig.2 链接已取得，可获取 |
| V22 | 机器人/软体 | Soft and flexible robot skin actuator using multilayer 3D pneumatic network | 2025-07-01 | 10.1038/s41467-025-60496-9; https://www.nature.com/articles/s41467-025-60496-9 | C | Fig. 1 及方法实验装置照片 | 多层柔性气动皮肤执行器、气管接口、泵/控制模块和实验台架 | 柔性曲面、气路入口、多层装配；未知尺寸标假设 | Crossref 元数据已核验 | Nature Communications OA HTML/PDF 可公开获取，待逐图裁取 |
| V23 | 电子/射频 | Topologically steerable ultra-flat electro-optic combs via non-Hermitian frequency lattices | 2026-10-09 | arXiv:2610.12867; https://arxiv.org/abs/2610.12867 | B | arXiv PDF Fig.1/2 及方法段（实验装置示意所在页） | EO 梳系统：microwave source、EO modulator、laser、detection/spectrum 链 | 电信号连接、芯片/光纤接口不假设厂家外观 | arXiv Atom API 已核验标题/日期；HTML 暂无，PDF 可下载 | 已下载 `validation-next/source-check/arXiv-2610.12867.pdf`（1,508,139 B；8 页），PyMuPDF 打开成功 |
| V24 | 光学/微梳 | Broadband soliton microcombs in the biological window enabled by a resonant coupler | 2026-10-08 | arXiv:2610.12603; https://arxiv.org/abs/2610.12603 | D | Fig.1b/c、Fig.2 与方法中 chip photograph、pump/drop 光路描述 | 激光、光纤耦合、chip package、thermal tuning 与光谱测量链；首版以文字/图注为主 | 文字主导、未知包装尺寸、隐藏光纤；不造内部结构 | arXiv Atom API 已核验 | HTML 正文、Fig.1/Fig.2 链接已取得，可获取 |
| V25 | 流体/微流控 | OoTrap: enhancing oocyte collection and maturation with a field-deployable fluidic device | 2025 | 10.1039/d4lc00660g; https://pubs.rsc.org/en/content/articlehtml/2025/lc/d4lc00660g | C | 官方 HTML Fig.1 设备结构、微孔阵列与管路 | OoTrap 可部署微流单元：入口/出口、捕获/培养腔、机械/流体接口 | 生物装置外部接口、可辨认流体路径；内部未证不画 | Crossref 已核验标题/日期/容器 | 用户给出官方完整 HTML，正文和 Fig.1 可读，进入建模 |
| V26 | 流体/微流控 | Particle dynamics in a microfluidic T-junction vortex flow: the role of history force | 2026 | arXiv:2610.13796; https://arxiv.org/abs/2610.13796 | A | 本地 PDF Fig. 1（T-junction 数值域：5L×L 主臂，L 分支，Rc=0.4L） | microfluidic T-junction：inflow/outflow/branch outflow 三出口、通道壁、内部流体、particle tracer、BOS 光路与相机 | 通道绝对尺寸（无量纲化）、粒子材质、端口尺寸均为保守假设 | 本地 PDF 已下载并打开成功 | 已下载 `validation-next/source-check/arXiv-2610.13796.pdf`（30页，PyMuPDF 打开成功），进入建模 |
| V27 | 声学/流体 | Airborne liquid marble: Evaporation dynamics of liquid marble in acoustic levitation | 2026-10-06 | arXiv:2610.07703; https://arxiv.org/abs/2610.07703 | A | 已下载 arXiv PDF `validation-next/source-check/arXiv-2610.07703.pdf`（8页）中的实验装置/样品示意 | 声学悬浮腔、液体弹样品、BOS/背光观测与支架 | 样品可见性、声学端口与样品台 | arXiv Atom API + PDF 已下载并打开 | 已取得，进入建模 |
| V28 | 声学/材料 | Acoustic Metamaterial Nanogenerator for Multi-Band Sound Insulation and Acoustic–Electric Conversion | 2025-11-02 | 10.3390/s25216693; https://www.mdpi.com/1424-8220/25/21/6693 | B | 官方正文中的声电转换/隔音装置示意 | 声学超材料单元、传感/电转换接口与样品台 | 电信号连接、多层单元，不凭空画内部 | Crossref 已核验 OA/BY 许可 | 用户给出官方正文，进入建模 |
| V29 | 材料/机械/声学 | Elastic Wave Modulation of Metamaterial Beams in Bidirectional Asymmetric Acoustic Black Holes: Finite Element Method and Experiment | 2025-01 | 10.1007/s42417-024-01645-0; https://link.springer.com/article/10.1007/s42417-024-01645-0 | C | 用户提供的 Springer 官方 PDF `validation-next/cases/v29_acoustic_black_hole_beam/source-materials/V29_springer_official.pdf`，目标 Fig.2/实验梁照片 | 双端不对称声学黑洞梁、激励/传感布局、实验台架 | 梁体曲面/边界、实验台架与传感器连接 | 官方 PDF 已保存并由 PyMuPDF 打开成功 | 已取得，进入建模 |
| V30 | 生物医学/光电芯片 | UV Fluorescence Sensing of Medical-Chemical-Biological Analytes by an AlGaN/Si-on-Sapphire Optoelectronic Chip | 2026 | arXiv:2610.13525; https://arxiv.org/abs/2610.13525 | D | 本地 PDF Fig. 4/5（VCSEL 底面/3D 透视）、Fig. 10/11/12（芯片布局/剖面/底部 Wi-Fi 芯片） | 蓝宝石芯片体（20×50×4 mm）、VCSEL/DBR/mesa/AlN 衬底、Si PD + 长通滤光片、电子芯片（LD drv/TIA/ADC/ESP32/TP4056/Boost/LDO）、LiPo、USB-C、Wi-Fi 天线、UV 激光锥、样品凹槽 | 无本地 Fig 高清 PNG（全部依据正文文字）、IC 厂家型号未定、天线拓扑为保守蛇形 | 本地 PDF 已下载并打开成功 | 已下载 `validation-next/source-check/arXiv-2610.13525.pdf`（31页，PyMuPDF 打开成功），进入建模 |

## 候补与需附件清单（不进入首版批次）

| 编号 | 论文 | 需要用户提供/下载的内容 | 建议保存路径 |
|---|---|---|---|
| V23 | arXiv:2610.12867 | 已由 AGH 实际下载 PDF，不再需要附件 | `validation-next/source-check/arXiv-2610.12867.pdf`（已落盘） |
| V25 | 10.1039/d4lc00660g | RSC PDF 或 HTML 图版 Fig.1/device layout（官方 HTML 已取得） | `validation-next/cases/v25_oostrap_fluidic/source-materials` |
| V27 | arXiv:2610.07703 | 已由 AGH 实际下载 PDF，不再需要附件 | `validation-next/source-check/arXiv-2610.07703.pdf`（已落盘） |
| V28 | 10.3390/s25216693 | MDPI OA PDF（403，无法自动下载） | `validation-next/cases/v28_acoustic_metamaterial_nanogenerator/source-materials` |
| V29 | 10.1007/s42417-024-01645-0 | Springer PDF（用户已提供，已落盘） | `validation-next/cases/v29_acoustic_black_hole_beam/source-materials/V29_springer_official.pdf`（已落盘） |

## 领域覆盖检查
进入首批建模批次的 10 篇覆盖：光学/量子光探测（V21、V24）、机器人/软体（V22）、电子/射频（V23）、流体/微流控（V25、V26）、声学（V27、V28）、材料/机械（V29）、生物医学/光电芯片（V30），共 7 个领域。若某些条目因附件延迟未进首版，需要用同领域可公开获取的替代论文补足，不能只报元数据。

## 输入类别检查
- A：V26、V27，满足≥2。
- B：V21、V23、V28，满足≥2。
- C：V22、V25、V29，满足≥2。
- D：V24、V30，满足≥2。
注意：只有“图版/正文已取得”的条目才算当前建模批次；未取得的不得写成已完成选题。
（V26 已从 RSC d6lc00133e 替换为 arXiv:2610.13796；V30 已从能源/热学占位替换为 arXiv:2610.13525。旧条目已移除，无“待补”进入 v01 批次。）

## DOI/旧案例去重检查
旧 10 例 DOI 已列出（10.1038/s41467-022-33070-w、10.1038/srep11102、10.1038/s41598-025-17304-7、10.1038/s41598-019-53281-4、10.1038/s41467-021-23207-8、10.1038/s41598-021-99890-w、10.1038/s41467-021-22776-y、10.1038/s41467-026-68436-x、10.1038/s41467-024-50872-2、10.1038/s41563-020-00884-2）。本表新条目字符串不重复；已排除 decision letter、review 与 SSRN 占位。
