"""R3 only cases 14/15/18/19. Preserves v03 scope; actual displayed routed segments are explicit.
No fake exploded contacts or unsupported instrument circuitry.
"""
from pathlib import Path
from PIL import Image
import json
ROOT=Path(__file__).resolve().parents[1]
PARTS={
14:[('upper array','downward transducer'),('reflector','flat rectangular reflector'),('gap droplet','single working-gap drop'),('microphone','microphone exterior body'),('left camera','LEFT high speed camera'),('right LED','RIGHT LED housing'),('amplifier','amplifier electronics'),('oscilloscope','oscilloscope instrument'),('laptop','laptop open screen'),('array support','top array support')],
15:[('aperture lid','lid true center aperture'),('rotor','rotor translucent platter'),('spring ribbon','flat dark spiral spring'),('cord','retractable rope'),('stator','stator base cup'),('stator stripe','stator fine gold stripe 0'),('rotor stripe','rotor fine gold stripe 0')],
18:[*(('position '+str(i),f'position {i:02d} '+{1:'endplate',2:'gasket',3:'bipolar frame',4:'thin GDE',5:'gasket',6:'cathode patterned flow',7:'thin proton membrane',8:'thin anode',9:'gasket',10:'anode patterned flow',11:'gasket',12:'framed cell A',13:'framed cell B',14:'framed cell C',15:'unresolved layer',16:'caption conflict layer',17:'endplate'}[i]+(' left' if i not in (1,4,7,8,15,16,17) else '')) for i in range(1,18)),('assembled four-cell','assembled rear endplate'),('assembled tie rods','assembled long tie rod')],
19:[('glass','TeRC transparent coating'),('reservoir','raised clear reservoir'),('U regulator','continuous U regulator'),('down nozzle','downward nozzle'),('resistance substituter','resistance substituter'),('oscilloscope','oscilloscope'),('lead one','visible signal to resistance socket'),('lead two','visible signal to scope socket')]
}
P14=[('camera','left camera','camera lead owner surface'),('microphone','microphone','microphone cable surface'),('array','array support','array upper signal boundary'),('amp-mic','amplifier','amp microphone socket'),('amp-array','amplifier','amp array socket'),('computer','laptop','laptop input socket')]
R14=[('camera-to-laptop','camera','computer','camera-to-laptop visible wire'),('microphone-to-amp','microphone','amp-mic','microphone-to-amplifier visible wire'),('array-to-amp','array','amp-array','array-to-amplifier visible wire')]
P19=[('glass-left','glass','QA glass left contact'),('glass-right','glass','QA glass right contact'),('resistor','resistance substituter','QA resistor terminal'),('scope','oscilloscope','QA scope terminal')]
R19=[('glass-to-resistor','glass-left','resistor','visible signal to resistance socket'),('glass-to-scope','glass-right','scope','visible signal to scope socket')]
for n,parts in PARTS.items():
 d=next((ROOT/'cases').glob(f'{n}_*'));r=json.loads((d/'record_v03.json').read_text());w,h=Image.open(d/'overview_v04.png').size
 comp=[{'id':f'c{i+1}','label':name,'object':obj,'evidence':'paper','size_basis':'illustrative','state':r['task']['operating_state']} for i,(name,obj) in enumerate(parts)]
 ids={c['label']:c['id'] for c in comp};port_list=P14 if n==14 else P19 if n==19 else [];route_list=R14 if n==14 else R19 if n==19 else []
 ports=[{'id':pid,'owner':ids[owner],'object':obj,'medium':'electric' if n==19 else 'unknown',
         'direction':'unknown','state':'connected','surface_tolerance':.09,
         'evidence_note':'R3 source-visible terminal; geometry QA only, no hidden wiring identity.'} for pid,owner,obj in port_list]
 links=[{'id':name,'a':a,'b':b,'kind':'electric',
         'medium':'electric' if n==19 else 'unknown','object':obj,
         'required':True,'tolerance':.08,
         'evidence_note':'visible segment only; actual optics/acoustics/internal electricity unverified'} for name,a,b,obj in route_list]
 # 14 visible physical cable segments have unknown signal modality: schema permits electric +
 # medium unknown but static stays UNKNOWN. No pretend logical route that bypasses endpoint QA.
 rec={**r,'task':{**r['task'],'scope':r['task']['scope']+' R3 Codex targeted pixel correction; original panel scope retained.',
  'outputs':{**r['task']['outputs'],'width':w,'height':h},
  'required_components':[c['id'] for c in comp],'required_connections':[c['id'] for c in links],
  'required_supports':[]},'components':comp,'ports':ports,'connections':links,'supports':[],
  'world_units':'illustrative Blender scene units; port tolerance 0.09 / route endpoint 0.08 limited to visible model marker rounding; never engineering fit.',
  'unverified':['v04 source-output visual comparison pending','hidden signal or fluid topology','physical operation and occlusion'],
  'coverage_gap':'Only declared source-visible segments audited; no complete system path approval.'}
 if n in (15,18):rec['not_applicable_routes']='Exploded presentation: no evidenced working-state attachment or wiring between separated layers; zero route checks not success.'
 if n==18:rec['source_ambiguity']='Publisher caption duplicates item 16 as gasket/current collector; position15 identity unresolved. Repeated cells are patterned display modules, not independently identified electrodes.'
 (d/'record_v04.json').write_text(json.dumps(rec,ensure_ascii=False,indent=2)+'\n')
 print(n,len(comp),len(ports),len(links))
