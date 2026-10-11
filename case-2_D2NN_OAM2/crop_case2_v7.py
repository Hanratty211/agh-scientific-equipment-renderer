#!/usr/bin/env python3
"""Pixel crops from the exact v7 overview PNG, no rerendering or annotation.
ROIs are normalized top-left rectangles chosen from the SAVED overview camera
projection (outlet x .741, housing x .755–.866; old ROIs retained).
Run: python3 crop_case2_v7.py
"""
from pathlib import Path
from PIL import Image
import hashlib
BASE=Path(__file__).resolve().parent/'render-output'
source=BASE/'case2_v7_overview_wordless.png'
rois={
    'case2_v7_crop_laser_L1_L2.png':(.32,.52,.84,.81),
    'case2_v7_crop_BS_SLM_M3.png':(.68,.39,1.,.77),
    'case2_v7_crop_laser_outlet.png':(.68,.63,.92,.86),
}
with Image.open(source) as im:
    im.load(); w,h=im.size
    assert (w,h)==(1200,750),f'unexpected overview dimensions: {im.size}'
    print('SOURCE_SHA256',hashlib.sha256(source.read_bytes()).hexdigest())
    for filename,(x0,y0,x1,y1) in rois.items():
        bounds=tuple(round(n*d) for n,d in zip((x0,y0,x1,y1),(w,h,w,h)))
        assert 0<=bounds[0]<bounds[2]<=w and 0<=bounds[1]<bounds[3]<=h
        target=BASE/filename
        im.crop(bounds).save(target)
        print('CROPPED',target,bounds,Image.open(target).size)
