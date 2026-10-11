#!/usr/bin/env python3
"""Fig.2(a) ONLY: PDF clip (64,95,352,268) at 4x; six-label annotation.
Device and optical-contact anchors were checked in Preview against the reference image;
they are independent of extracted text boxes. Keep earlier versions unchanged.
"""
from pathlib import Path
import pymupdf
from PIL import Image, ImageDraw, ImageFont

BASE = Path(__file__).resolve().parent
CLIP = (64, 95, 352, 268)
NAMES = ('Pulse laser', 'L1', 'L2', 'M1', 'M2', 'DMD')
ALIAS = {'L1': 'Ll', 'M1': 'Ml'}  # PDF text-layer glyph extraction, not optical labels
# Original image pixels: body point and red-beam interaction point are deliberately separate.
# Approximate manually identified from the actual reference shown in Preview (image origin, not window origin).
DEVICE = {'Pulse laser': (925, 587), 'L1': (568, 541), 'L2': (440, 506),
          'M1': (130, 462), 'M2': (372, 435), 'DMD': (111, 309)}
HIT = {'Pulse laser': (863, 553), 'L1': (566, 533), 'L2': (440, 504),
       'M1': (133, 460), 'M2': (373, 430), 'DMD': (107, 307)}
# Trace the observed red route, not label centers. The short endpoints inside the
# colored beam have finite width, so listed points are schematic center-line picks.
PATH = [HIT['Pulse laser'], HIT['L1'], HIT['L2'], HIT['M1'],
        HIT['M2'], HIT['DMD']]
# Number circles are placed in clear photo margins/blank regions, never over original text.
CALLOUTS = [(1150, 668), (716, 630), (486, 625), (32, 585), (344, 586), (30, 372)]

def txt_bboxes(page):
    out = {}
    for block in page.get_text('dict')['blocks']:
        if block.get('type') != 0:
            continue
        for line in block['lines']:
            s = ''.join(span['text'] for span in line['spans']).strip()
            if s:
                out.setdefault(s, []).append(tuple(line['bbox']))
    return out

def mapped(box):
    return tuple((v - CLIP[i % 2]) * 4 for i, v in enumerate(box))

def font(size):
    return ImageFont.truetype('/System/Library/Fonts/STHeiti Medium.ttc', size)

def main():
    im = Image.open(BASE / 'reference_Fig2a.png').convert('RGB')
    assert im.size == (1152, 692), im.size
    with pymupdf.open(BASE / 'source_paper.pdf') as doc:
        boxes = txt_bboxes(doc[3])
    bounds = {name: mapped(boxes[ALIAS.get(name, name)][0]) for name in NAMES}
    # Independent visual calibration: mapped rectangles coincide with the three
    # legible original labels in the displayed PNG (not merely algebraically in bounds).
    print('VISUAL_CALIBRATION: Preview reference_Fig2a.png image origin y=80 in window capture')
    for name in ('Pulse laser', 'L2', 'DMD'):
        print(name, 'mapped text bbox=', tuple(round(v) for v in bounds[name]),
              'visually checked label region: yes')
    # Draw on a padded, separate copy so callouts and Chinese legend do not cover original labels.
    padx, pady = 110, 88
    canvas = Image.new('RGB', (im.width + 2 * padx, im.height + 2 * pady + 68), '#f5f5f5')
    canvas.paste(im, (padx, pady))
    d = ImageDraw.Draw(canvas)
    ff, small = font(24), font(17)
    tr = lambda xy: (xy[0] + padx, xy[1] + pady)
    # Cyan stroke laid on the observed red centerline; numbered arrows show propagation.
    route = list(map(tr, PATH))
    d.line(route, fill=(3, 125, 151), width=3, joint='curve')
    import math
    for a, b in zip(route, route[1:]):
        mid = ((a[0] + b[0]) / 2, (a[1] + b[1]) / 2)
        dx, dy = b[0] - a[0], b[1] - a[1]
        L = math.hypot(dx, dy)
        if L:
            ux, uy = dx / L, dy / L
            x, y = mid
            d.polygon([(x + ux * 12, y + uy * 12),
                       (x - ux * 7 - uy * 6, y - uy * 7 + ux * 6),
                       (x - ux * 7 + uy * 6, y - uy * 7 - ux * 6)], fill=(3, 125, 151))
    for i, name in enumerate(NAMES):
        x, y = tr(DEVICE[name]); hx, hy = tr(HIT[name])
        cx, cy = tr(CALLOUTS[i]); r = 17
        d.line([(cx, cy), (x, y)], fill=(12, 58, 104), width=2)
        d.ellipse((x - 4, y - 4, x + 4, y + 4), fill=(12, 58, 104))
        d.ellipse((hx - 3, hy - 3, hx + 3, hy + 3), fill=(255, 240, 40))
        d.ellipse((cx-r, cy-r, cx+r, cy+r), fill=(255, 245, 182), outline=(12, 58, 104), width=2)
        d.text((cx - 7, cy - 14), str(i+1), fill=(12, 58, 104), font=ff)
    d.text((24, 15), '第一段：Pulse laser → L1 → L2 → M1 → M2 → DMD', font=ff, fill='#17344f')
    d.text((26, canvas.height-57), '蓝线：六件指引；青色箭头：原图红色光路描摹；黄色点：光束作用点（近似）',
           font=small, fill='#17344f')
    out = BASE / 'reference_Fig2a_seg1_r10.png'
    canvas.save(out)
    names = NAMES
    rows = ['# Fig.2(a) 第一段六行对应表（R10）', '',
            '仅图面像素；不推定世界高度。PDF 第4页 clip=(64,95,352,268)，倍率4，映射 `(x-64)*4,(y-95)*4`。',
            'Preview 目视独立核对原标签 Pulse laser、L2、DMD；文字框、器件位置、光束作用点不混用。',
            '器件/作用点是看图近似锚点；光路按原红线描摹，待外部逐点复核。', '',
            '| 编号 | 原标签（PDF文本层） | 原标签文字框 px | 实际器件 px（目视） | 光束作用点 px（目视近似） | 上游 → 下游 |',
            '|---|---|---|---|---|---|']
    for i, name in enumerate(names):
        before = names[i-1] if i else '光源'
        after = names[i+1] if i+1 < len(names) else '本轮止于 DMD'
        box = ','.join(str(round(v)) for v in bounds[name])
        rows.append(f'| {i+1} | {name} (`{ALIAS.get(name,name)}`) | ({box}) | {DEVICE[name]} | {HIT[name]} | {before} → {after} |')
    rows += ['', '文字框来自 PDF 文本层：`Ll` 对应 L1，`Ml` 对应 M1；文字框不是器件中心。',
             '光束沿图右下激光器→L1→L2→左下M1→斜返M2→左上DMD；无后续支路标注。']
    (BASE/'reference_Fig2a_seg1_r10.md').write_text('\n'.join(rows)+'\n', encoding='utf-8')
    print('WROTE', out.name, 'and reference_Fig2a_seg1_r10.md')
if __name__ == '__main__': main()
