"""Retrieve publicly accessible candidate PDFs and extract captions without altering prior cases."""
from pathlib import Path
import json, re, hashlib, time
import requests
import pymupdf

ROOT = Path(__file__).resolve().parent
OUT = ROOT / 'sources'; OUT.mkdir(exist_ok=True)
CANDIDATES = [
 ('01_optics','10.1364/boe.579684'),
 ('02_robotics','10.1038/s41467-025-56025-3'),
 ('03_radio','10.1016/j.ohx.2025.e00695'),
 ('04_microfluidics','10.1038/s41526-025-00470-3'),
 ('05_energy','10.1021/acs.jchemed.5c00647'),
 ('06_acoustics','10.1073/pnas.2502112122'),
 ('07_thermal','10.3390/en18082039'),
 ('08_biomedical','10.3991/ijoe.v22i03.59657'),
 ('09_electronics','10.1126/sciadv.adt5620'),
 ('10_mechanical','10.1016/j.ohx.2025.e00687'),
 ('11_optics_alt','10.1364/oe.571630'),
 ('12_robotics_alt','10.1109/robosoft63089.2025.11020818'),
]
S=requests.Session(); S.headers['User-Agent']='Research visual validation (metadata and open-access PDFs)'
rows=[]
for name,doi in CANDIDATES:
 row={'id':name,'doi':doi,'metadata_status':'pending','pdf_status':'pending'}
 try:
  r=S.get('https://api.openalex.org/works/https://doi.org/'+doi,timeout=19);r.raise_for_status();m=r.json()
  row.update(title=m.get('title'),date=m.get('publication_date'),landing=(m.get('best_oa_location') or {}).get('landing_page_url'))
  url=(m.get('best_oa_location') or {}).get('pdf_url');row['pdf_url']=url;row['metadata_status']='verified_openalex'
  if url and not (OUT / (name+'.pdf')).exists():
   try:
    v=S.get(url,timeout=22);v.raise_for_status()
    if v.content.startswith(b'%PDF'):
     (OUT/(name+'.pdf')).write_bytes(v.content);row['pdf_status']='saved';row['pdf_sha256']=hashlib.sha256(v.content).hexdigest()
    else:row['pdf_status']='not_pdf_'+v.headers.get('content-type','')
   except Exception as e:row['pdf_status']='failed_'+str(e)[:100]
  elif (OUT/(name+'.pdf')).exists():
   row['pdf_status']='saved_existing';row['pdf_sha256']=hashlib.sha256((OUT/(name+'.pdf')).read_bytes()).hexdigest()
  if row['pdf_status'] in ('saved','saved_existing'):
   doc=pymupdf.open(OUT/(name+'.pdf'));row['pages']=len(doc)
   lines=[]
   for i,p in enumerate(doc):
    t=p.get_text().replace('\n',' ')
    for match in re.finditer(r'Fig(?:ure)?\.\s*\d+\s*[|.:-]',t,re.I):
     lines.append({'page':i+1,'excerpt':t[match.start():match.start()+420]})
   row['figure_mentions']=lines[:18]
 except Exception as e:row['metadata_status']='failed_'+str(e)[:150]
 rows.append(row);(ROOT/'candidate_metadata.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2))
 print(name,row['metadata_status'],row['pdf_status'],row.get('pages',''),flush=True)
 time.sleep(.35)
