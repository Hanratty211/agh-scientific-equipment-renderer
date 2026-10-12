"""Local R4 PNG sheet: regenerate 12 and 16, reuse four unchanged R3 PNGs."""
import json,hashlib
from pathlib import Path
from PIL import Image,ImageDraw
root=Path(__file__).resolve().parent.parent;r=json.loads((root/'physical_feedback_r4_manifest.json').read_text());sheet=Image.new('RGB',(2550,1250),(246,248,250));d=ImageDraw.Draw(sheet)
for i,row in enumerate(r['cases']):
 image=row['images'][0];p=Path(image['path']);assert hashlib.sha256(p.read_bytes()).hexdigest()==image['sha256']
 im=Image.open(p).convert('RGB');im.thumbnail((818,540));x=i%3*850+(850-im.width)//2;y=i//3*625+46;sheet.paste(im,(x,y))
 d.text((i%3*850+14,i//3*625+14),f"Case {row['case']} {row['version']} saved-scene preview",fill=(18,32,45))
 d.text((i%3*850+14,i//3*625+596),f"SHA256 {image['sha256'][:18]}...",fill=(65,79,95))
out=root/'physical_feedback_r4_six_overviews.png';sheet.save(out)
proof={'author':'AGH','sheet':str(out),'sha256':hashlib.sha256(out.read_bytes()).hexdigest(),'case12_and_16':'new case12 v06 and case16 v07 independent reload','other_four':'case13/14/17/19 unchanged R2 overview PNG SHA256 (also carried unchanged in R3 manifest)','inputs':[{'case':x['case'],'sha256':x['images'][0]['sha256'],'image':x['images'][0]['path']} for x in r['cases']]}
(root/'physical_feedback_r4_six_overviews.json').write_text(json.dumps(proof,indent=2,ensure_ascii=False)+'\n')
print(out,proof['sha256'])
