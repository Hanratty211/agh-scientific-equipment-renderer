#!/usr/bin/env python3
"""Numeric PNG review & optional normalized crops/contact sheet. Not visual QA.
python3 review_images.py config.json --report report.json
Config: {"images":[{"id":"source","path":"source.png","regions":[{"id":"detail","xyxy":[0,0,0.5,0.5]}]}],"contact_sheet":"sheet.png"}
All paths relative to config file. Requires Pillow. Fails on out-of-bounds regions.
"""
import argparse,json,hashlib
from pathlib import Path
from PIL import Image,ImageOps,ImageDraw

def run(config):
 cfg=Path(config).resolve();data=json.loads(cfg.read_text(encoding='utf-8'));rows=data.get('images',[])
 if not isinstance(rows,list) or not rows:raise ValueError('images must be nonempty')
 seen=set();imgs=[];results=[]
 for row in rows:
  ident=row['id'];source=(cfg.parent/row['path']).resolve()
  if ident in seen:raise ValueError('duplicate image id '+ident)
  seen.add(ident);raw=source.read_bytes();sha=hashlib.sha256(raw).hexdigest()
  with Image.open(source) as im:
   if im.format!='PNG':raise ValueError('PNG required: '+str(source))
   im.load();width,height=im.size
   results.append({'id':ident,'source':str(source),'sha256':sha,'width':width,'height':height,
                   'mode':im.mode,'alpha_channel':('A' in im.getbands()),'regions':[]})
   imgs.append((ident,im.copy()))
   for region in row.get('regions',[]):
    name=region['id'];bb=region['xyxy']
    if len(bb)!=4 or not all(isinstance(v,(int,float)) for v in bb):raise ValueError('bad xyxy')
    x0,y0,x1,y1=bb
    if not (0<=x0<x1<=1 and 0<=y0<y1<=1):raise ValueError('normalized xyxy must be within [0,1]')
    pixels=(round(x0*width),round(y0*height),round(x1*width),round(y1*height))
    if pixels[0]>=pixels[2] or pixels[1]>=pixels[3]:raise ValueError('zero pixel region')
    crop=im.crop(pixels);target=(cfg.parent/region.get('output',f'{ident}_{name}.png')).resolve()
    target.parent.mkdir(parents=True,exist_ok=True);crop.save(target)
    results[-1]['regions'].append({'id':name,'normalized_xyxy':bb,'pixel_xyxy':pixels,'path':str(target),'size':crop.size,'source_sha256':sha})
    imgs.append((f'{ident}:{name}',crop))
 sheet=data.get('contact_sheet')
 if sheet:
  thumb=(330,230);canvas=Image.new('RGB',(thumb[0]*len(imgs),thumb[1]+26),'#e7e7e7');draw=ImageDraw.Draw(canvas)
  for i,(name,im) in enumerate(imgs):
   fit=ImageOps.contain(im.convert('RGBA'),thumb);bg=Image.new('RGBA',fit.size,'white');bg.alpha_composite(fit)
   canvas.paste(bg.convert('RGB'),(i*thumb[0]+(thumb[0]-fit.width)//2,(thumb[1]-fit.height)//2));draw.text((i*thumb[0]+4,thumb[1]+4),name,fill='black')
  output=(cfg.parent/sheet).resolve();output.parent.mkdir(parents=True,exist_ok=True);canvas.save(output)
 result={'status':'NUMERIC_ONLY','images':results,'contact_sheet':str(output) if sheet else None,
         'not_verified':['clarity','contact','topology','labels_correct','photographic_similarity']}
 return result

def main():
 ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('config');ap.add_argument('--report');args=ap.parse_args()
 try:result=run(args.config)
 except (OSError,ValueError,KeyError) as exc:
  print('FAIL',str(exc));return 2
 txt=json.dumps(result,ensure_ascii=False,indent=2)
 if args.report:Path(args.report).write_text(txt+'\n',encoding='utf-8')
 print(txt);return 0
if __name__=='__main__':raise SystemExit(main())
