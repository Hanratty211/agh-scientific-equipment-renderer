#!/usr/bin/env python3
"""
A1/A2：在参考图独立副本上标注器件位置与关键作用点。
依据：
  - 官方图注（pymupdf 抽取）：L1~L7 plano-convex lens, M1~M3 mirrors, HWP, BS beam splitter,
    MMF, BC 3×1, PD InGaAs
  - 正文光路：laser(1064nm)→4f 准直扩束→DMD(显示 CGH)→4f 取+1 级→SLM(相调制,D2NN)
    →dichroic/BS→M3→4f→聚焦→3×MMF delay lines→BC 3×1→MMF→PD→oscilloscope
  - 外部 R7 判读：激光器在右下、DMD 在左侧、SLM 在右侧、光纤盘绕在左上
标注类型：
  [实] 有直接文字标签或明确形状依据
  [推] 按光路顺序与参考图形状推断（未逐字核实）
  [未确认] 无法从参考图直接识别
"""
from PIL import Image, ImageDraw, ImageFont
import os

HERE = os.path.dirname(os.path.abspath(__file__))
REF = os.path.join(HERE, "reference_Fig2a.png")
OUT = os.path.join(HERE, "reference_Fig2a_annotated.png")
MD  = os.path.join(HERE, "reference_Fig2a_annotated.md")

im = Image.open(REF).convert("RGB")
dr = ImageDraw.Draw(im)
font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 20)
font_s = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 16)

# 颜色编码
C_CONF = (0, 150, 0)     # 绿：有标签/明确形状
C_INFER = (0, 0, 200)    # 蓝：按光路顺序推断
C_UNK = (200, 100, 0)    # 橙：未确认
C_TURN = (200, 0, 0)     # 红点：转向/作用点

def mark(name, status, x, y, note=""):
    """在 (x,y) 画圆点 + 标签。status: CONF/INF/UNK。"""
    col = C_CONF if status=="CONF" else (C_INFER if status=="INF" else C_UNK)
    r = 22
    dr.ellipse([x-r,y-r,x+r,y+r], outline=col, width=3, fill=None)
    label = f"{name} [{status}]"
    dr.text((x+r+4, y-r-12), label, fill=col, font=font_s)
    if note:
        dr.text((x+r+4, y+4), note, fill=(80,80,80), font=font_s)

# ---- 参考图像素坐标标注（1152×692，y 从上往下）----
# 外部 R7 判读 + 官方图注 + 正文光路顺序综合
# 激光器在右下、DMD 在左侧、SLM 在右侧、光纤盘绕在左上

# 激光器（右下）—— 未确认（参考图右下方无明确激光盒形状，按外部判读 + 正文 1064nm 激光源）
mark("Laser(1064nm)", "UNK", 950, 580, note="外部判读在右下；形状未逐字核实")

# DMD 在左侧（参考图左中部，大矩形器件区）
mark("DMD", "INF", 200, 250, note="外部判读在左侧；CGH 显示区")

# L1/L2（4f 准直扩束，DMD 前）—— 推断在 DMD 左侧或上方
mark("L1", "INF", 130, 250, note="4f 系统，DMD 前")
mark("L2", "INF", 80, 250, note="4f 系统，DMD 前")

# M1/M2（DMD 附近折叠镜）
mark("M1", "INF", 280, 280, note="折叠镜")
mark("M2", "INF", 330, 300, note="折叠镜")

# SLM 在右侧（参考图右中部）
mark("SLM", "INF", 720, 300, note="外部判读在右侧；相调制(D2NN)")

# L3/L4（4f 取+1 级，DMD 与 SLM 之间）
mark("L3", "INF", 420, 300, note="4f 滤波")
mark("L4", "INF", 500, 300, note="4f 滤波")

# BS(dichroic) + HWP + Polarizer（SLM 附近）
mark("BS", "INF", 780, 300, note="beam splitter（图注）/dichroic prism（正文）")
mark("HWP", "INF", 820, 320, note="half-wave plate")
mark("Pol", "INF", 860, 340, note="polarizer")

# M3（SLM 后折叠镜）
mark("M3", "INF", 900, 360, note="折叠镜")

# L5/L6/L7（第二组 4f + 聚焦）
mark("L5", "INF", 940, 380, note="4f")
mark("L6", "INF", 980, 400, note="4f")
mark("L7", "INF", 1010, 420, note="聚焦到光纤")

# 3×MMF 盘绕在左上（外部 R7 判读）
mark("MMF×3", "UNK", 300, 130, note="外部判盘绕在左上；2/4/6m delay lines")
mark("BC(3×1)", "UNK", 400, 130, note="合束器")

# 输出 MMF → PD → oscilloscope
mark("MMF(out)", "UNK", 500, 150, note="输出光纤")
mark("PD", "UNK", 600, 170, note="InGaAs PD")
mark("Scope", "UNK", 700, 190, note="oscilloscope")

# 关键作用点（红色小圆点）
turns = [
    (280, 280, "M1 转向"),
    (330, 300, "M2 转向"),
    (900, 360, "M3 转向"),
    (1010, 420, "L7 聚焦到光纤"),
    (300, 130, "MMF 盘绕入口"),
]
for x,y,note in turns:
    r=8
    dr.ellipse([x-r,y-r,x+r,y+r], outline=C_TURN, width=2, fill=(255,200,200))
    dr.text((x+r+2, y-r-2), note, fill=C_TURN, font=font_s)

# 图例
dr.rectangle([10,10,260,80], outline=(0,0,0), width=1, fill=(255,255,255))
dr.text((16,14), "图例：绿=[实]有标签 蓝=[推]按光路推断 橙=[未确认] 红点=转向/作用点", fill=(0,0,0), font=font_s)
dr.text((16,44), "依据：官方图注 + 正文光路 + 外部 R7 判读（激光右下/DMD 左/SLM 右/光纤左上）", fill=(80,80,80), font=font_s)
dr.text((16,62), "未逐字核实的标记一律 [未确认] 或 [推]，不写虚构像素结论", fill=(80,80,80), font=font_s)

im.save(OUT)
print("标注副本已生成:", OUT, os.path.getsize(OUT), "B")

# 标注数据（可编辑 .md，与标注图对应）
md = """# 参考图标注数据（reference_Fig2a_annotated.png 对应）
> 依据：官方图注（L1~L7 plano-convex lens, M1~M3 mirrors, HWP, BS beam splitter, MMF, BC 3×1, PD InGaAs）
> + 正文光路（laser→4f→DMD(CGH)→4f→SLM(D2NN)→BS/M3→4f→L7→3×MMF delay lines→BC→MMF→PD→scope）
> + 外部 R7 判读（激光器右下、DMD 左侧、SLM 右侧、光纤盘绕左上）
> 标注类型：[实]=有直接文字标签/明确形状；[推]=按光路顺序与参考图形状推断；[未确认]=无法从参考图直接识别

| 器件 | 像素坐标(x,y) | 标注类型 | 依据 |
|------|------|------|------|
| Laser(1064nm) | (950,580) | [未确认] | 外部判读在右下；形状未逐字核实 |
| DMD | (200,250) | [推] | 外部判读在左侧；CGH 显示区 |
| L1 | (130,250) | [推] | 4f 系统，DMD 前 |
| L2 | (80,250) | [推] | 4f 系统，DMD 前 |
| M1 | (280,280) | [推] | 折叠镜 |
| M2 | (330,300) | [推] | 折叠镜 |
| SLM | (720,300) | [推] | 外部判读在右侧；相调制(D2NN) |
| L3 | (420,300) | [推] | 4f 滤波 |
| L4 | (500,300) | [推] | 4f 滤波 |
| BS | (780,300) | [推] | 图注 beam splitter / 正文 dichroic prism |
| HWP | (820,320) | [推] | half-wave plate |
| Pol | (860,340) | [推] | polarizer |
| M3 | (900,360) | [推] | 折叠镜 |
| L5 | (940,380) | [推] | 4f |
| L6 | (980,400) | [推] | 4f |
| L7 | (1010,420) | [推] | 聚焦到光纤 |
| MMF×3 | (300,130) | [未确认] | 外部判盘绕在左上；2/4/6m delay lines |
| BC(3×1) | (400,130) | [未确认] | 合束器 |
| MMF(out) | (500,150) | [未确认] | 输出光纤 |
| PD | (600,170) | [未确认] | InGaAs PD |
| Scope | (700,190) | [未确认] | oscilloscope |

## 关键转向/作用点（红色圆点）
- M1 转向 (280,280)；M2 转向 (330,300)；M3 转向 (900,360)；L7 聚焦到光纤 (1010,420)；MMF 盘绕入口 (300,130)

## 完整输入→输出路径（按正文光路，参考图相对位置）
Laser(右下) → L1/L2(4f 准直扩束) → DMD(左,CGH) → L3/L4(4f 取+1 级) → SLM(右,相调制/D2NN)
→ BS(dichroic)/HWP/Pol → M3(折叠) → L5/L6/L7(4f+聚焦) → 3×MMF delay lines(左上盘绕,2/4/6m)
→ BC(3×1 合束) → 输出 MMF → PD(InGaAs) → Oscilloscope(32GHz)

## SLM 返回/BS 分出（按正文重新判断，不称"反射式共光路"）
- 正文："The OAM beams generated by these holograms are filtered through a 4 f system, with the +1 order
  diffraction light directed onto a phase-only SLM"——SLM **入射**是 4f 取 +1 级后的光（非"共光路"）。
- "The phase distribution loaded on the SLM is trained on computers using the error-backpropagation
  algorithm"——SLM 加载相位分布（相调制），**出射**光经过 dichroic/BS 分出（零级/共光路分离）。
- **不得**把 SLM 入射/出射仍沿 +x 称为"反射式共光路"；SLM 是透射式相调制器件（入射→调制→出射）。
- BS(dichroic) 按波长/偏振把零级（未调制）分出到 M3 折叠段，调制光（D2NN 输出）走主探测段。

## DMD 12° 入射角（对应明确入射线与参考法向）
- 论文给出 DMD 入射角 12°：指入射光束与 DMD **参考法向**的夹角 = 12°。
- **不得**靠"旋转某个欧拉角"声称满足；须对应明确的入射线方向与 DMD 参考法向（微镜面法线）。
- 本处保留为**建模假设**（具体入射线方向与参考法向在参考图上未逐字标注，列为未确认）。

## 未确认项（不写虚构像素结论）
- 激光器在参考图右下的**具体位置与形状**：外部判读，未逐字核实（参考图无明确"laser"文字标签）。
- MMF 盘绕在左上的**具体圈数/束半径/走向**：外部判读"盘绕在左上"，圈数/尺寸未逐字核实（视觉示意）。
- DMD/SLM 的具体像素边界：按外部判读相对位置（DMD 左/SLM 右），具体边界未逐字核实。
- M1/M2/M3 的具体入射/反射角：参考图未标注角度，列为建模假设。
- BS(dichroic) 的具体分光角度/位置：参考图未标注，列为建模假设。
"""
with open(MD, "w") as f:
    f.write(md)
print("标注数据已生成:", MD, os.path.getsize(MD), "B")
