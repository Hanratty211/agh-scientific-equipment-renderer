#!/usr/bin/env python3
"""
A（R9）：第一段识别标注 Pulse laser → L1 → L2 → M1 → M2 → DMD。
标签坐标来自 PDF 内嵌文本层（pymupdf 抽取，第 4 页 get_text("dict")），
经 page.get_image_rects(17) 映射到参考 PNG 像素坐标 —— 不是颜色统计猜测。
标注用编号 + 指引线，**不遮挡原标签**；使用支持中文的字体（STHeiti/Hiragino）。
"""
from PIL import Image, ImageDraw, ImageFont
import pymupdf, os

HERE = os.path.dirname(os.path.abspath(__file__))
PDF = os.path.join(HERE, "source_paper.pdf")
REF = os.path.join(HERE, "reference_Fig2a.png")
OUT = os.path.join(HERE, "reference_Fig2a_seg1_annotated.png")
MD  = os.path.join(HERE, "reference_Fig2a_seg1_table.md")

# ---- 1. 从 PDF 文本层抽取 Fig.2a 标签坐标 ----
doc = pymupdf.open(PDF)
page = doc[3]
rect = page.get_image_rects(17)[0]
PW, PH = Image.open(REF).size
sx, sy = PW / rect.width, PH / rect.height
def pdf2png(x, y):
    return ((x - rect.x0) * sx, (y - rect.y0) * sy)

d = page.get_text("dict")
raw = {}
for b in d["blocks"]:
    if b.get("type") == 0:
        for l in b["lines"]:
            t = "".join(s["text"] for s in l["spans"]).strip()
            if not t:
                continue
            x0, y0, x1, y1 = l["bbox"]
            if y0 < 400:  # Fig.2a 区域
                raw.setdefault(t, []).append((x0, y0, x1, y1))

# 第一段需要的 6 个标签（+ 原位文字）。PDF 文本层实际拼写：
# 'Pulse laser', 'Ll'(=L1), 'L2', 'Ml'(=M1), 'M2', 'DMD', 'Hologram'
# 字形 l/1、I/l 在文本层被抽混：'Ll'即L1、'Ml'即M1。
ALIAS = {"L1": "Ll", "M1": "Ml"}
SEG1 = ["Pulse laser", "L1", "L2", "M1", "M2", "DMD", "Hologram"]
labels = {}
for k in SEG1:
    key = ALIAS.get(k, k)
    cand = raw.get(key) or raw.get(k)
    if cand:
        x0, y0, x1, y1 = cand[0]
        labels[k] = {"pdf": (x0, y0, x1, y1), "png": pdf2png(x0, y1), "raw": key}

# ---- 2. 绘制标注副本 ----
im = Image.open(REF).convert("RGB")
dr = ImageDraw.Draw(im)
def load_font(size):
    for p in ["/System/Library/Fonts/STHeiti Medium.ttc",
              "/System/Library/Fonts/Hiragino Sans GB.ttc",
              "/System/Library/Fonts/STHeiti Light.ttc",
              "/System/Library/Fonts/Helvetica.ttc"]:
        try: return ImageFont.truetype(p, size)
        except: pass
    return ImageFont.load_default()
f_num = load_font(30)
f_txt = load_font(20)

# 编号与标签对应（第一段光路顺序）
ORDER = [("Pulse laser", "1"), ("L1", "2"), ("L2", "3"), ("M1", "4"), ("M2", "5"), ("DMD", "6")]

# 编号圆放到原标签的左上/上方，避免遮挡原标签文字
offset = {"Pulse laser": (-70, 30), "L1": (-30, -58), "L2": (-30, -58),
          "M1": (30, -58), "M2": (30, -58), "DMD": (30, -58)}

for name, num in ORDER:
    if name not in labels:
        continue
    lx, ly = labels[name]["png"]
    # 原标签文字框（PNG 像素）
    px0, py0, px1, py1 = labels[name]["pdf"]
    bx0, by0 = pdf2png(px0, py0)
    bx1, by1 = pdf2png(px1, py1)
    ox, oy = offset.get(name, (0, -60))
    cx, cy = bx0 + ox, by0 + oy
    # 编号圆（醒目，但不压原标签：放在框外侧）
    R = 20
    dr.ellipse([cx-R, cy-R, cx+R, cy+R], fill=(255, 235, 60), outline=(180, 0, 0), width=3)
    tb = dr.textbbox((0,0), num, font=f_num)
    dr.text((cx - (tb[2]-tb[0])/2, cy - (tb[3]-tb[1])/2 - 3), num, fill=(150,0,0), font=f_num)
    # 指引线：从编号圆边缘 → 原标签框中心
    tcx, tcy = (bx0+bx1)/2, (by0+by1)/2
    import math
    ang = math.atan2(tcy-cy, tcx-cx)
    sx_, sy_ = cx + R*math.cos(ang), cy + R*math.sin(ang)
    dr.line([(sx_, sy_), (tcx, tcy)], fill=(180,0,0), width=2)
    dr.ellipse([tcx-4, tcy-4, tcx+4, tcy+4], fill=(180,0,0))

# ---- 3. 连续描出这段原有红色光路（保留原图折叠走向）----
# 第一段红色光路像素点（按标签位置与红色骨架拟合；标为"描摹"）
seg1_path = [(520, 400), (455, 380), (400, 370), (331, 359), (300, 350),
             (256, 345), (230, 320), (213, 289), (150, 300), (100, 305),
             (71, 310), (60, 260), (70, 210), (81, 154)]
dr.line(seg1_path, fill=(255, 0, 255), width=3, joint="curve")
for p in seg1_path:
    dr.ellipse([p[0]-3, p[1]-3, p[0]+3, p[1]+3], fill=(255,0,255))
dr.text((540, 375), "红色光路描摹（第一段，洋红）", fill=(200,0,200), font=f_txt)

# 图例
dr.rectangle([8, 8, 470, 78], outline=(0,0,0), width=1, fill=(255,255,255))
dr.text((14, 12), "第一段：Pulse laser→L1→L2→M1→M2→DMD（编号=光路顺序 1..6）", fill=(0,0,0), font=f_txt)
dr.text((14, 38), "黄圆=编号（不遮挡原标签）；红线=指引线→原标签中心；洋红线=该段红色光路描摹", fill=(60,60,60), font=f_txt)
dr.text((14, 60), "标签坐标=PDF 文本层抽取（非颜色统计）；字体=STHeiti（支持中文）", fill=(60,60,60), font=f_txt)

im.save(OUT)
print("第一段标注副本:", OUT, os.path.getsize(OUT), "B")

# ---- 4. 六行对应表 ----
rows = [
    ("1", "Pulse laser", labels.get("Pulse laser"), "上游：无（光源）；下游：L2"),
    ("2", "L1", labels.get("L1"), "上游：L2；下游：M2"),
    ("3", "L2", labels.get("L2"), "上游：Pulse laser；下游：L1"),
    ("4", "M1", labels.get("M1"), "上游：M2；下游：DMD"),
    ("5", "M2", labels.get("M2"), "上游：L1；下游：M1"),
    ("6", "DMD", labels.get("DMD"), "上游：M1；下游：L3（第二段）"),
]
md = ["# 第一段六行对应表（Pulse laser → L1 → L2 → M1 → M2 → DMD）", "",
      "> 标签坐标来自 PDF 第 4 页文本层（pymupdf `get_text(\"dict\")`），经 `page.get_image_rects(17)` 映射到参考 PNG 像素。",
      "> **非颜色统计猜测**；屏幕像素坐标**不作为世界高度**（本表只说图面位置，不给 z 高度）。",
      "> **文本层拼写差异**：L1 在文本层抽取为 `Ll`、M1 抽取为 `Ml`（字形 l/1 混淆）；下表给出原始抽取拼写。", "",
      "| 编号 | 原标签 | 文本层抽取拼写 | 器件位置（参考 PNG 像素） | 连接上下游 |",
      "|------|--------|----------------|--------------------------|------------|"]
for num, name, lab, conn in rows:
    if lab:
        x, y = lab["png"]
        px0, py0, px1, py1 = lab["pdf"]
        md.append(f"| {num} | {name} | `{lab['raw']}` | 标签文字锚点 PNG({x:.0f},{y:.0f})；PDF({px0:.1f},{py0:.1f}) | {conn} |")
    else:
        md.append(f"| {num} | {name} | — | **未在文本层找到** | {conn} |")
md += ["", "## 说明",
       "- 编号 1..6 = 光路传播顺序；Pulse laser 在图面**右侧中部**，光路向左经 L1、L2 到 M1/M2 折叠后进入 DMD（图面**左上**）。",
       "- 图面另有 `Hologram` 标签（DMD 旁，示意显示图案）与 `Iris`；本段不含 Iris。",
       "- **未确认**：M1/M2 的具体反射角（文本层无角度标注）；本段红色光路的具体转折点以描摹近似。",
       "- 本表**不推断世界坐标/高度**；三维布局需在外部确认本段理解正确后再做。"]
open(MD, "w", encoding="utf-8").write("\n".join(md))
print("六行对应表:", MD)
for line in md[5:12]:
    print("  ", line)
