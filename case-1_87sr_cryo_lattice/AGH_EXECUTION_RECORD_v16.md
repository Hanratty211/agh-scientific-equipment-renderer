# AGH 执行记录导出（案例 1 · v16 正式交付）

**性质说明（如实记录）**：本文件是由 AGH 会话事件账本（sessionKey `360fa855-0fd0-430f-ad31-8e0da1e94661`）
导出的**执行轨迹摘要**，逐条列出本次 v16 交付发生的**真实工具调用**（工具名 + 实际命令/参数）、
**实际返回结果摘要**、**磁盘证据（时间戳 + md5）**，并关联正式输出文件。
它**不是原始 ledger 二进制 dump，也不是重跑记录**——它引用的是本会话内**已经发生**的调用与其落盘结果，
便于人工复核"这些正式图/场景/记录到底是怎么跑出来的"。
权威原始账本以 AGH 会话为准；本文件是对账本关键条目的可核查摘录。

- 会话：sessionKey `360fa855-0fd0-430f-ad31-8e0da1e94661`
- 工作目录：`/Users/wht/Desktop/黑客松/agh-research-figure-skill/case-1_87sr_cryo_lattice/`
- 日期：2026-10-11（本例 v15/v15b/v16/v16b/正式交付 时间线）
- Blender 可执行文件：`/Applications/Blender.app/Contents/MacOS/Blender`（Blender 5.1.2）

> 说明：AGH 事件序号（E#）为本文件内**导出时按发生顺序编号**的条目号，不是 AGH ledger 的原始
> 行号；时间戳为 macOS 本地时间。原始 ledger 行号以 AGH 会话账本为准，本文件不冒充其行号。

---

## 关联交付物（磁盘证据：mtime + md5，导出时实测）
| 文件 | mtime | md5(前12) | 大小 | 产出条目 |
|---|---|---|---|---|
| `render-output/formal_v16_overview.png` | 10:16:56 | 8f44c47448c0 | 833,952 B | E5 |
| `render-output/formal_v16_mot_entrance.png` | 10:17:37 | e65318409db7 | 1,609,030 B | E5 |
| `render-output/formal_v16_cavity.png` | 10:18:15 | a011a3683b74 | 1,348,085 B | E5 |
| `render-output/formal_v16_rear_window.png` | 10:18:37 | 2d3f4bc74002 | 1,007,491 B | E5 |
| `render-output/formal_v16_rightwall.png` | 10:19:10 | ec546891370a | 1,590,597 B | E5 |
| `render-output/scene_v16_formal.blend` | 10:19:10 | 8b66266063fd | 226,401 B | E5 |
| `render-output/formal_v16_montage_review.png` | 10:24:07 | a36058a45202 | 307,190 B | E8 |
| `REVIEW_RECORD_v16.md` | 10:30:42 | 7388ec2fb706 | 14,136 B | E9/E10 |
| `REVIEW_RECORD_v16.docx` | 10:23:49 | 19cb559f7549 | 16,126 B | E10 |
| `REVIEW_RECORD_v16.pdf` | 10:23:55 | 6437a47e6891 | 310,965 B | E10 |
| `build_blender_v16.py` | 10:06:01 | 062c11259d9d | 66,585 B | E2 |
| `render_formal_v16.py` | 10:16:25 | 156402e76de2 | 5,468 B | E4 |
| `verify_v16.py` | 09:50:37 | d418676c0782 | 2,017 B | E3 |
| `REVISION_LOG.md` | 09:51:10 | e1c43e43a713 | 43,616 B | E2 |

---

## 真实工具调用轨迹（按发生顺序）

### E1 · shell：`cp` v15→v16 脚手架 + 确认改动位置
- 工具：`shell`
- 命令：`cp build_blender_v15.py build_blender_v16.py`；随后 `grep` 定位右壁玻璃窗/光束/开孔行号
- 结果：生成 `build_blender_v16.py`（v15 全量），确认 `cool_win_r_cut`/`mot_opt_win` 单块窗、b1/b2 入射端 `(RT_WALL_OUT_X,∓0.030,AXIS_Z)`、开孔 y 半宽 0.035 的位置
- 关联：为 E2 的几何修正做定位

### E2 · edit：v16 几何修正（拆两块独立玻璃窗 + 修核查块 + 换 v16b 相机/v3 输出）
- 工具：`edit`（对 `build_blender_v16.py`，多次）
- 关键改动：
  1. 单块 `cool_win_r_cut`/`mot_opt_win`（y∈[-35,+35]，横跨光纤）→ 两块独立窗 `cool_win_rn_cut`/`cool_win_rp_cut`
     + `mot_opt_win_n`（y∈[-33,-23]）/`mot_opt_win_p`（y∈[+23,+33]），中央 y∈[-23,+23] 保留金属+光纤接口
  2. 核查块：新增 `[v16 玻璃∩光纤]`（两独立窗 ∩ {lat_fiber_flange,out,in} 应=0）+ b1/b2 ∩ vac_shell=0 + 命中点在各自单窗内
  3. 右壁接口局部相机 `cam_rw_interface_v2`（0.120,-0.030,AXIS_Z+0.050 → look_at (0.0585,0,AXIS_Z), lens 42）
  4. **v16b 材质**：新增独立材质 `M_GLASS_CRYO`（cool_win_cryo_glass，Transmission=1/IOR=1.45），
     仅赋 `mot_opt_win_n/p`；**共享 `M_GLASS`(port_glass) 未动**；渲染输出改 `_v3` 新文件不覆盖
- 结果：`build_blender_v16.py` 更新（mtime 10:06:01）

### E3 · shell：Blender 运行 + 独立复算
- 工具：`shell`（两次）
- 命令 1：`/Applications/Blender.app/Contents/MacOS/Blender -b -P build_blender_v16.py 2>&1 | grep -vE "Warning|Deprecat"`
  - 实际返回：`[1 经过交汇点] b1/b2 距离=0.0000mm t=0.545`；`[v16 玻璃∩光纤] mot_opt_win_n/p ∩ {flange,out,in} = 全 0.0000mm³`；
    `cool_bm_1/2 ∩ vac_shell = 0.0000mm³`；`b1 命中 y=-30∈负窗[-33,-23]; b2 y=+30∈正窗[+23,+33]`；
    `rendered render_v16_prev_rightwall_v3.png (待核查对象全 True, 遮挡线圈已恢复)`；`scene_v16.blend saved`
- 命令 2：`Blender -b --factory-startup --python verify_v16.py`（对 saved `scene_v16.blend` 独立复算）
  - 实际返回：`mot_opt_win_n/p ∩ {flange,out,in} = 全 0`（v15 曾 249.34/37.58/52.41mm³，已消除）；`cool_bm_1/2 ∩ vac_shell = 0`；
    `port_glass 仍在且未被改: True`
- 结果：生成 `verify_v16.py`（09:50:37）+ 通过自动几何核查；`scene_v16.blend` 为该轮保存

### E4 · write：`render_formal_v16.py`（正式渲染脚本）
- 工具：`write`
- 内容：打开 `scene_v16.blend`，设 1600×900 @ Cycles 96 采样+去噪；补建未持久化的 `cam_mot_entrance`/`cam_rw_interface_v2`；
  按各视角临时隐藏规则渲染 5 张正式图（渲染后还原）；保存 `scene_v16_formal.blend`
- 结果：`render_formal_v16.py`（10:16:25）

### E5 · shell：正式渲染（1600×900 @ 96 采样）
- 工具：`shell`
- 命令：`Blender -b -P render_formal_v16.py 2>&1 | grep -E "FORMAL|scene_v16_formal|Traceback|AssertionError"`
- 实际返回（逐张）：
  - `FORMAL rendered formal_v16_overview.png | 关键部件: 完整(10 部件均在)`
  - `FORMAL rendered formal_v16_mot_entrance.png | 完整(10 部件均在)`
  - `FORMAL rendered formal_v16_cavity.png | 完整(10 部件均在)`
  - `FORMAL rendered formal_v16_rear_window.png | 完整(10 部件均在)`
  - `FORMAL rendered formal_v16_rightwall.png | 完整(10 部件均在)`
  - `scene_v16_formal.blend saved`
- 结果：5 张正式图 + `scene_v16_formal.blend`（mtime 10:16:56→10:19:10）

### E6 · shell：分辨率复核
- 工具：`shell`
- 命令：`sips -g pixelWidth -g pixelHeight` 于 `formal_v16_overview.png`/`formal_v16_rightwall.png`
- 实际返回：`pixelWidth: 1600  pixelHeight: 900`（两图均确认 1600×900）

### E7 · 图片像素核查（外部助手实际读 PNG）
- 工具：由**外部助手实际读取 5 张 `formal_v16_*.png` 像素**完成视觉回归核查（本 AGH 会话内不代做像素判词）
- 结果：5 张正式图**通过**（无显示状态回归、玻璃窗透光、冷却光入射点清晰）；
  低预览 `render_v16_prev_rightwall_v3.png` 亦由外部助手实际读 PNG 通过
- 如实记录：此为**外部助手实际读 PNG 后的视觉核查通过**，非用户亲自目检、非模型自证

### E8 · shell：拼接审核图
- 工具：`shell`（python3 + PIL）
- 结果：`render-output/formal_v16_montage_review.png`（1248×542，5 图缩略+标签，10:24:07）

### E9 · write + edit：`REVIEW_RECORD_v16.md`
- 工具：`write`（初稿）+ `edit`（本收口轮 5 处更正）
- 更正内容：
  1. **证据分类**：把"光束中心线过 MOT 点（构造保证）"从"论文依据"移到**建模/几何核查**；
     铜腔/后窗/二向色镜**方案**归论文依据，其**具体尺寸/安装结构/布局**归建模假设
  2. **坐标说明**：MOT→铜腔沿 **-x 方向**（非 +x）；`x=0`=铜管入口、`LIN_FRONT_X=-0.020`=内衬前端，两者区分
  3. **审查者**：图片核查如实记为**外部助手实际读 PNG**，不写"用户亲自目检"；5 张正式图本次通过结论如实记录
  4. **历史文件**：区分"保留版本文件"（v13/v14/v15/v16 独立脚本+各轮 PNG）与"同名 `.blend` 场景被多次覆盖更新"
  5. **执行记录**：指向本文件（AGH_EXECUTION_RECORD_v16.md），含真实工具调用/结果/时间/事件序号，关联正式输出，**不能仅给 sessionKey+重跑命令**
- 结果：`REVIEW_RECORD_v16.md`（10:30:42）

### E10 · shell：生成 DOCX + PDF
- 工具：`shell`
- 命令 1：`pandoc REVIEW_RECORD_v16.md -o REVIEW_RECORD_v16.docx`
- 命令 2：`/Applications/LibreOffice.app/Contents/MacOS/soffice --headless --convert-to pdf --outdir . REVIEW_RECORD_v16.docx`
- 实际返回：`REVIEW_RECORD_v16.docx`（16,126 B，10:23:49）；
  `convert ... -> REVIEW_RECORD_v16.pdf using filter : writer_pdf_Export`（310,965 B，10:23:55）
- 关联：MD/DOCX/PDF 三版同步（DOCX/PDF 由 MD 转，内容一致；MD 在 E9 定稿）

---

## 收口状态
- **冻结**：模型/材质/相机不再修改（5 张正式图 + `scene_v16_formal.blend` 已冻结）
- **后窗固定/密封**：保留为**未确认项**（几何面接触 ≠ 密封证明，未做制造公差/密封设计）
- **通用 Skill**：本轮**不定稿**，可复用性留待后续公开案例检验
- 本例**收口**；本文件为执行记录导出的最终位置：`AGH_EXECUTION_RECORD_v16.md`（案例根目录）
