#!/usr/bin/env python3
"""
A3：二维布局草图（保留参考图相对位置/折叠方向/连接）。
依据 reference_Fig2a_annotated.md 的识别结论（官方图注 + 正文光路 + 外部 R7 判读）。
**不写虚构像素分析结论**：相对位置按外部判读（激光右下/DMD 左/SLM 右/光纤左上），
器件间连接按正文光路顺序；未核实项标橙色"未确认"。
"""
import os
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "layout_v4_2d.png")

W, H = 1200, 700
img = Image.new("RGB", (W, H), (245, 245, 245))
dr = ImageDraw.Draw(img)
font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 18)
font_s = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 14)

# 颜色
C_BEAM = (220, 40, 40)        # 红色示意光路（1064nm 示意配色，非真实可见色）
C_FIBER = (60, 120, 220)      # 蓝色光纤
C_ELEC = (150, 80, 200)       # 紫色电信号线
C_PART = (40, 40, 40)         # 器件
C_UNK = (200, 100, 0)         # 未确认（橙色）
C_BG = (245, 245, 245)

def part(name, x, y, w, h, unk=False):
    col = C_UNK if unk else C_PART
    dr.rectangle([x, y, x+w, y+h], outline=col, width=2, fill=(255,255,255) if not unk else (255,240,220))
    dr.text((x+4, y+4), name, fill=col, font=font_s)

def lens_mark(x, y, label):
    """透镜符号：竖椭圆"""
    dr.ellipse([x-8, y-30, x+8, y+30], outline=C_PART, width=2, fill=(220,235,250))
    dr.text((x+10, y-6), label, fill=C_PART, font=font_s)

def mirror_mark(x, y, label, angle_deg=45):
    """镜符号：斜线（45°）"""
    import math
    L = 40
    dx = L * math.cos(math.radians(angle_deg))
    dy = L * math.sin(math.radians(angle_deg))
    dr.line([x-dx, y-dy, x+dx, y+dy], fill=C_PART, width=3)
    dr.text((x+14, y-8), label, fill=C_PART, font=font_s)

def fiber_coil(x, y, w, h, label, unk=True):
    """光纤盘绕（简化螺旋，蓝色）"""
    import math
    n = 6
    for i in range(n):
        t = i / (n - 1)
        yy = y + t * h
        xx = x + w/2 + (w/2 - 6) * math.sin(t * math.pi * 3)
        dr.ellipse([xx-5, yy-5, xx+5, yy+5], outline=C_FIBER, width=2)
    dr.ellipse([x, y, x+w, y+h], outline=C_FIBER, width=1)
    dr.text((x+4, y-18), label, fill=C_FIBER, font=font_s)

# ===== 按参考图相对位置布置（外部 R7 判读：激光右下/DMD 左/SLM 右/光纤左上）=====
# 主光路（红色示意，1064nm 示意配色）

# 激光器（右下）—— 未确认形状
part("Laser\n(1064nm)", 980, 480, 90, 60, unk=True)

# DMD（左侧）—— 推断
part("DMD\n(CGH)", 80, 240, 80, 80)

# 4f 准直扩束（L1/L2，DMD 前，激光→DMD 段）
lens_mark(200, 400, "L1")
lens_mark(260, 440, "L2")

# 折叠镜 M1/M2（DMD 附近）
mirror_mark(360, 300, "M1")
mirror_mark(420, 320, "M2")

# 4f 滤波（L3/L4，DMD 与 SLM 之间）
lens_mark(500, 280, "L3")
lens_mark(560, 280, "L4")

# SLM（右侧）—— 推断
part("SLM\n(D2NN)", 640, 240, 80, 80)

# BS(dichroic) + HWP + Pol（SLM 附近）
part("BS", 760, 260, 50, 40)
part("HWP", 820, 260, 40, 30)
part("Pol", 870, 260, 40, 30)

# M3（SLM 后折叠镜）
mirror_mark(920, 300, "M3")

# 4f + 聚焦（L5/L6/L7）
lens_mark(960, 340, "L5")
lens_mark(1000, 360, "L6")
lens_mark(1040, 380, "L7")

# 3×MMF 盘绕在左上（外部 R7 判读）—— 未确认圈数
fiber_coil(80, 40, 140, 140, "MMF×3\n(2/4/6m)")

# BC 合束器
part("BC\n(3×1)", 280, 60, 60, 50, unk=True)

# 输出 MMF → PD → oscilloscope
part("MMF\n(out)", 380, 70, 50, 30, unk=True)
part("PD", 470, 70, 40, 40, unk=True)
part("Scope", 560, 60, 80, 50, unk=True)

# ===== 光路连接（红色示意）=====
# Laser → L1/L2 → DMD
dr.line([(980, 510), (260, 440)], fill=C_BEAM, width=2)
dr.line([(260, 440), (200, 400)], fill=C_BEAM, width=2)
dr.line([(200, 400), (120, 320)], fill=C_BEAM, width=2)
# DMD → M1/M2 → L3/L4 → SLM
dr.line([(120, 320), (360, 300)], fill=C_BEAM, width=2)
dr.line([(360, 300), (420, 320)], fill=C_BEAM, width=2)
dr.line([(420, 320), (500, 280)], fill=C_BEAM, width=2)
dr.line([(500, 280), (560, 280)], fill=C_BEAM, width=2)
dr.line([(560, 280), (680, 280)], fill=C_BEAM, width=2)
# SLM → BS → HWP → Pol → M3
dr.line([(720, 280), (780, 280)], fill=C_BEAM, width=2)
dr.line([(780, 280), (840, 280)], fill=C_BEAM, width=2)
dr.line([(840, 280), (890, 280)], fill=C_BEAM, width=2)
dr.line([(890, 280), (920, 300)], fill=C_BEAM, width=2)
# M3 → L5/L6/L7 → MMF（左上）
dr.line([(920, 300), (960, 340)], fill=C_BEAM, width=2)
dr.line([(960, 340), (1000, 360)], fill=C_BEAM, width=2)
dr.line([(1000, 360), (1040, 380)], fill=C_BEAM, width=2)
# L7 → MMF 盘绕（左上）
dr.line([(1040, 380), (150, 180)], fill=C_FIBER, width=2)

# ===== 光纤连接（蓝色）=====
# MMF×3 → BC → 输出 MMF → PD
dr.line([(220, 120), (310, 100)], fill=C_FIBER, width=3)
dr.line([(340, 100), (405, 90)], fill=C_FIBER, width=3)
dr.line([(430, 90), (490, 100)], fill=C_FIBER, width=3)

# ===== 电信号线（紫色，PD→示波器，与光纤/光束可区分）=====
dr.line([(510, 110), (600, 90)], fill=C_ELEC, width=2)

# ===== 图例 =====
dr.rectangle([10, 600, 400, 690], outline=(0,0,0), width=1, fill=(255,255,255))
dr.text((16, 606), "图例：", fill=(0,0,0), font=font_s)
dr.line([40, 630, 80, 630], fill=C_BEAM, width=2)
dr.text((85, 622), "红色=光路(1064nm示意配色,非真实可见色)", fill=(0,0,0), font=font_s)
dr.line([40, 650, 80, 650], fill=C_FIBER, width=3)
dr.text((85, 642), "蓝色=光纤", fill=(0,0,0), font=font_s)
dr.line([40, 670, 80, 670], fill=C_ELEC, width=2)
dr.text((85, 662), "紫色=电信号线(PD→示波器,与光纤/光束可区分)", fill=(0,0,0), font=font_s)
dr.text((200, 622), "黑框=推断 橙框=未确认", fill=(100,100,100), font=font_s)

img.save(OUT)
print("二维布局草图已生成:", OUT, os.path.getsize(OUT), "B")

# 连接表（md）
conn = """# 二维布局草图连接表（layout_v4_2d.png 对应）
> 依据：reference_Fig2a_annotated.md（官方图注 + 正文光路 + 外部 R7 判读）。
> 相对位置按外部判读（激光右下/DMD 左/SLM 右/光纤左上）；未核实项标橙。

## 完整输入→输出路径（按正文光路）
1. **Laser(1064nm, 右下, 未确认)** → L1/L2(4f 准直扩束) → **DMD(CGH, 左)**
2. DMD → M1/M2(折叠镜) → L3/L4(4f 取+1 级) → **SLM(D2NN, 右)**
3. SLM → BS(dichroic) + HWP + Pol → M3(折叠镜)
4. M3 → L5/L6/L7(4f+聚焦) → **3×MMF delay lines(左上盘绕, 2/4/6m, 未确认圈数)**
5. 3×MMF → **BC(3×1 合束)** → 输出 MMF → **PD(InGaAs)** → **Oscilloscope(32GHz)**
   - PD→示波器用**电信号线**（紫色，与光纤/光束可区分）

## SLM 返回/BS 分出（按正文重新判断，不称"反射式共光路"）
- SLM 是**透射式相调制**器件：入射光（4f 取+1 级后的光）→ SLM 加载相位分布（D2NN）→ 出射光。
- **不得**把 SLM 入射/出射仍沿 +x 称为"反射式共光路"。
- BS(dichroic) 按波长/偏振把**零级（未调制光）**分出到 M3 折叠段；**调制光（D2NN 输出）**走主探测段。
- 正文："The OAM beams generated by these holograms are filtered through a 4 f system, with the +1 order
  diffraction light directed onto a phase-only SLM"——SLM 入射是 4f 取+1 级（非"共光路"）。

## DMD 12° 入射角（对应明确入射线与参考法向）
- 论文：DMD 入射角 12° = 入射光束与 DMD **参考法向**（微镜面法线）的夹角。
- **不得**靠"旋转某个欧拉角"声称满足；须对应明确入射线方向与 DMD 参考法向。
- 本处保留为**建模假设**（具体入射线方向与参考法向在参考图上未逐字标注，列为未确认）。

## 未确认项（不写虚构像素结论）
- 激光器在参考图右下的**具体位置与形状**：外部判读，未逐字核实（参考图无明确"laser"文字标签）。
- MMF 盘绕在左上的**具体圈数/束半径/走向**：外部判读"盘绕在左上"，圈数/尺寸未逐字核实（视觉示意）。
- DMD/SLM 的具体像素边界：按外部判读相对位置（DMD 左/SLM 右），具体边界未逐字核实。
- M1/M2/M3 的具体入射/反射角：参考图未标注角度，列为建模假设。
- BS(dichroic) 的具体分光角度/位置：参考图未标注，列为建模假设。
"""
with open(os.path.join(HERE, "layout_v4_2d.md"), "w") as f:
    f.write(conn)
print("连接表已生成:", os.path.join(HERE, "layout_v4_2d.md"))
