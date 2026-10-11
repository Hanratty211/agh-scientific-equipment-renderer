"""R2: select source-supported visible routes; no global physical validation.
Anchor meshes are actual Blender world-space marker objects tied to owner surfaces and
independently audited with saved-scene evaluated geometry. Errors remain errors, never auto-scope shrink.
"""
from pathlib import Path
import json
from PIL import Image
ROOT=Path(__file__).resolve().parents[1]
TARGETS={x['id']:x for x in json.loads((ROOT/'targets.json').read_text())['papers']}
# IDs are target required identities, not object-count-driven. Strings name actual v03 objects.
PARTS={
11:[('laser','laser housing'),('HWP 1','half wave plate 1'),('power BS','power BS cube'),('HWP 2','half wave plate 2'),('lens 1','collimating lens 1'),('lens 2','collimating lens 2'),('dichroic','tilted dichroic active plate'),('objective','objective'),('sample','glass sample'),('dark field condenser','dark-field condenser'),('halogen','halogen source'),('shortpass','short pass filter'),('imaging lens','imaging lens'),('sCMOS','sCMOS camera')],
12:[('upper pump','upper syringe'),('lower pump','lower syringe'),('sample capillary','horizontal clear capillary'),('upper inlet','upper inlet fitting'),('lower inlet','lower inlet fitting'),('imaging camera','high speed camera'),('inverted microscope','inverted microscope'),('flush cap','sealed branch cap'),('waste vessel','waste vessel rim'),('laptop','laptop open screen')],
13:[('printer front rail','printer upright'),('gantry','anchored gantry beam'),('extruder','red extruder carriage'),('bed','heated print bed'),('mounted emission display','attached emissions display'),('front-center sensor display','front-center sensor display'),('laptop','laptop open screen')],
14:[('upper array','down-facing transducer'),('reflector','flat rectangular reflector'),('working gap droplet','working-gap droplet'),('probe','angled microphone stem'),('camera','side imaging camera'),('LED','opposite LED light'),('amplifier','amplifier electronics'),('oscilloscope','oscilloscope instrument'),('laptop','laptop open screen')],
15:[('aperture lid','aperture lid thin resin'),('rotor','rotor clear body'),('spring ribbon','flat spiral spring ribbon'),('cord','single retractable rope'),('stator','stator translucent housing'),('stator stripe band','stator alternating stripe band 0'),('rotor stripe band','rotor alternating stripe band 0')],
16:[('chamber','clear Perspex side'),('top drive','drive upper red housing'),('syringe','syringe barrel'),('PTFE feed','visible PTFE feed'),('needle','vertical metal needle'),('needle support','needle Perspex support'),('collector','copper collector'),('Vee plates','upright PTFE Vee plate'),('front heater','horizontal front heater'),('IR source','angled IR red source'),('external DC supply','external LEFT high voltage DC supply')],
17:[('frame','mechanical frame post'),('upper coil','upper coil housing'),('lower coil','lower coil housing'),('hemisphere','hemispherical sample'),('supported stage','supported loading stage'),('sample fixture','sample fixture top'),('pump syringe interface','red pump syringe interface'),('left supply','left compact DC supply'),('right pump','right red syringe pump'),('pressure sensor','front pressure sensor')],
18:[*(('position '+str(i),f'position {i:02d} '+{1:'endplate',2:'gasket',3:'bipolar frame',4:'thin GDE',5:'gasket',6:'cathode patterned flow',7:'thin proton membrane',8:'thin anode',9:'gasket',10:'anode patterned flow',11:'gasket',12:'framed cell A',13:'framed cell B',14:'framed cell C',15:'unresolved layer',16:'caption conflict layer',17:'endplate'}[i]+(' left' if i not in (1,4,7,8,15,16,17) else '')) for i in range(1,18)),('assembled four-cell','assembled rear endplate'),('assembled tie rods','assembled long tie rod')],
19:[('glass','tilted transparent TeRC glass'),('reservoir','raised fluid reservoir'),('U regulator','continuous U regulator'),('downward nozzle','downward terminal nozzle'),('resistance substituter','resistance substituter'),('oscilloscope','oscilloscope'),('signal lead one','visible signal to resistance socket'),('signal lead two','visible signal to scope socket')],
20:[('thin vertical Peltier','thin vertical Peltier module'),('left Cu','copper thermal block'),('right Cu','copper thermal block.001'),('left grease','grease inner contact'),('right grease','grease inner contact.001'),('sample','narrow bridging thermoelectric sample'),('edge pad sets','sample edge electrode')]
}
# (id, owner_component_label, anchor_name, medium, source-visible coordinate interpretation)
# Tolerances are scene-specific illustrative world units: mesh marker half-width ≈ .011–.033,
# these ranges span only intended marker-to-owner surface rounding; NOT a physical gasket tolerance.
PORTS={
11:[('laser-out','laser','laser output face'),('hwp1-right','HWP 1','HWP 1 right port'),('hwp1-left','HWP 1','HWP 1 left port'),('bs-right','power BS','BS incoming surface'),('bs-left','power BS','BS exiting surface'),('hwp2-right','HWP 2','HWP 2 right port'),('hwp2-left','HWP 2','HWP 2 left port'),('lens1-right','lens 1','lens 1 right face'),('lens1-left','lens 1','lens 1 left face'),('lens2-right','lens 2','lens 2 right face'),('lens2-left','lens 2','lens 2 left face'),('dich-in','dichroic','dichroic incoming interface'),('dich-up','dichroic','dichroic upper interface'),('dich-down','dichroic','dichroic lower interface'),('objective-in','objective','objective lower face'),('filter-top','shortpass','filter upper'),('filter-bottom','shortpass','filter lower'),('imaging-top','imaging lens','imaging upper'),('imaging-bottom','imaging lens','imaging lower'),('scmos-top','sCMOS','sCMOS sensor top')],
12:[('upper-pump','upper pump','upper pump exit'),('lower-pump','lower pump','lower pump exit'),('upper-inlet','upper inlet','upper inlet contact'),('lower-inlet','lower inlet','lower inlet contact'),('capillary-out','sample capillary','capillary outlet face'),('waste-mouth','waste vessel','waste mouth boundary')],
16:[('dc-red','external DC supply','DC red output terminal'),('dc-green','external DC supply','DC green output terminal'),('chamber-red','chamber','chamber red boundary'),('chamber-green','chamber','chamber green boundary')],
17:[('sample-pneumatic','sample fixture','sample tube fitting'),('pump-pneumatic','pump syringe interface','pump visible tube fitting'),('sensor-pneumatic','pressure sensor','sensor tube fitting')],
19:[('glass-left','glass','glass left electrode socket'),('glass-right','glass','glass right electrode socket'),('resistor-socket','resistance substituter','resistance instrument side socket'),('scope-socket','oscilloscope','scope instrument side socket')]
}
ROUTES={
11:[('laser-hwp1','laser-out','hwp1-right','laser-HWP1 axis'),('hwp1-bs','hwp1-left','bs-right','HWP1-BS axis'),('bs-hwp2','bs-left','hwp2-right','BS-HWP2 axis'),('hwp2-lens1','hwp2-left','lens1-right','HWP2-lens1 axis'),('lens1-lens2','lens1-left','lens2-right','lens1-lens2 axis'),('lens2-dich','lens2-left','dich-in','lens2-dichroic axis'),('dich-objective','dich-up','objective-in','dichroic to objective axis'),('dich-filter','dich-down','filter-top','dichroic-filter imaging axis'),('filter-imaging','filter-bottom','imaging-top','filter-imaging lens axis'),('imaging-scmos','imaging-bottom','scmos-top','imaging lens-sCMOS axis')],
12:[('upper-feed','upper-pump','upper-inlet','upper pump to capillary'),('lower-feed','lower-pump','lower-inlet','lower pump to capillary'),('outlet-waste','capillary-out','waste-mouth','capillary outlet to waste')],
16:[('red-lead','dc-red','chamber-red','visible red DC lead'),('green-lead','dc-green','chamber-green','visible green DC lead')],
17:[('sample-pump','sample-pneumatic','pump-pneumatic','sample to pump visible pneumatic segment'),('sample-sensor','sample-pneumatic','sensor-pneumatic','sample to pressure sensor visible segment')],
19:[('glass-resistor','glass-left','resistor-socket','visible signal to resistance socket'),('glass-scope','glass-right','scope-socket','visible signal to scope socket')]
}
MEDIUM={11:'optical',12:'fluid',16:'electric',17:'fluid',19:'electric'}
for id_,rows in PARTS.items():
 q=TARGETS[id_];d=ROOT/'cases'/f"{id_}_{q['slug']}";prev=json.loads((d/'record_v02.json').read_text());w,h=Image.open(d/'overview_v03.png').size
 comps=[{'id':f'c{j+1}','label':label,'object':obj,'evidence':'paper','size_basis':'illustrative','state':prev['task']['operating_state']} for j,(label,obj) in enumerate(rows)]
 comp_ids={c['label']:c['id'] for c in comps};medium=MEDIUM.get(id_)
 ports=[{'id':pid,'owner':comp_ids[owner],'object':obj,'medium':medium,'direction':'unknown','state':'connected','surface_tolerance':.09,
         'evidence_note':'R2 visible surface marker; owner/route independently audited against saved scene, not source CAD.'} for pid,owner,obj in PORTS.get(id_,[])]
 kind={11:'optical',12:'transport',16:'electric',17:'transport',19:'electric'}.get(id_)
 links=[{'id':rid,'a':a,'b':b,'kind':kind,'medium':medium,'object':obj,'required':True,'tolerance':.08,
         'evidence_note':'R2 source-visible segment only; hidden downstream topology unknown.'} for rid,a,b,obj in ROUTES.get(id_,[])]
 rec={**prev,'task':{**prev['task'],'scope':prev['task']['scope']+' R2 corrections as user feedback; retain full original scope.',
   'outputs':{**prev['task']['outputs'],'width':w,'height':h},
   'required_components':[c['id'] for c in comps],
   'required_connections':[x['id'] for x in links],'required_supports':[]},
   'components':comps,'ports':ports,'connections':links,'supports':[],
   'world_units':'illustrative Blender scene units. Port tolerance 0.09 around actual marker/owner mesh; route tolerance 0.08 for visible centerline/marker rounding only, not real engineering fit.',
   'source':{**prev['source'],'feedback':'Codex R2 actual pixels; source figure publisher caption'},
   'coverage_gap':'Only explicit visible relations in connections[] were routed; remaining task scope not certified by validator. Empty route list = no warranted physical route (exploded 15/18) or no supported endpoints in this v03 model, not route success.',
   'unverified':['user/Codex v03 output pixels','hidden optical/fluid/electric paths and operation','true physical support/contact/occlusion']}
 if id_ in (15,18):rec['not_applicable_routes']='Exploded display state; no source warranted working contact/pipe between separated pieces. No false required connection.'
 if id_ in (13,14,20):rec['route_coverage']='Visible wiring/electrode/stage details remain unbound or source topology ambiguous; do not interpret zero as absent routes in real device.'
 (d/'record_v03.json').write_text(json.dumps(rec,ensure_ascii=False,indent=2)+'\n')
 print(id_,len(comps),len(ports),len(links))
