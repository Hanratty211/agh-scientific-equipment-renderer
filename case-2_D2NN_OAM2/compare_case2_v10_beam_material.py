#!/usr/bin/env python3
"""Reproduce ONE three-column material comparison from the frozen v10 scene.
Run: python3 compare_case2_v10_beam_material.py
Blender renders three small identical camera-border crops in a temporary dir;
Pillow (system Python) assembles the only persistent PNG. Do not save a blend.
"""
import os, subprocess
from pathlib import Path
from tempfile import TemporaryDirectory
from PIL import Image, ImageDraw

BASE=Path(__file__).resolve().parent
SOURCE=BASE/'render-output'/'scene_case2_v10_overview.blend'
OUTPUT=BASE/'render-output'/'case2_v10_material_comparison.png'
BLENDER=Path('/Applications/Blender.app/Contents/MacOS/Blender')
assert SOURCE.is_file() and BLENDER.is_file()
variants=((.6,.90),(.8,.70),(1.0,.56))
with TemporaryDirectory(prefix='case2_mat_compare_') as tmp:
    env=os.environ.copy();env['CASE2_COMPARE_TILE_DIR']=tmp
    subprocess.run([str(BLENDER),'-b','--factory-startup','-P',
                    str(BASE/'render_case2_material_tiles.py')],
                   check=True,cwd=BASE,env=env)
    tiles=[]
    for j in range(3):
        with Image.open(Path(tmp)/f'crop_{j}.png') as img:
            tiles.append(img.convert('RGB').copy())
    assert len({tile.size for tile in tiles})==1,'camera/crop not equal across tiles'
    width,height=tiles[0].size
    gap=12;header=54;footer=52
    sheet=Image.new('RGB',(width*3+gap*4,height+header+footer),(31,38,47))
    draw=ImageDraw.Draw(sheet)
    for j,((weight,strength),tile) in enumerate(zip(variants,tiles)):
        x=gap+j*(width+gap)
        sheet.paste(tile,(x,header))
        draw.text((x+8,16),f'RED WEIGHT {weight:.1f}   /   EMISSION {strength:.2f}',
                  fill=(248,249,251))
    draw.text((gap,header+height+15),
              'Same v10 optics / camera / lighting; Iris2 - L6 - L7 - Holder. Display-only 1064 nm schematic, NOT visible beam color.',
              fill=(205,212,220))
    sheet.save(OUTPUT)
    print('WROTE_COMPARISON',OUTPUT,'size',sheet.size,'source',SOURCE,flush=True)
