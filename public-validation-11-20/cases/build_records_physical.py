"""Preserve ALL source-required component IDs; rebind changed owners/visible routes.
Explicit physical interface semantic notes supplement v0.6 schema; static/saved audit
cannot certify BNC seating, exact manufacturer CAD or unknown hidden circuit.
"""
import json
from pathlib import Path
from PIL import Image
root=Path(__file__).resolve().parent
cases={12:('v03','v04'),13:('v03','v04'),14:('v04','v05'),16:('v03','v04'),17:('v03','v04'),19:('v04','v05')}
for n,(old,new) in cases.items():
 d=next(root.glob(f'{n}_*'));r=json.loads((d/f'record_{old}.json').read_text());cm={c['label']:c for c in r['components']};pm={p['id']:p for p in r['ports']};rm={c['id']:c for c in r['connections']}
 w,h=Image.open(d/f'overview_{new}.png').size;r['task']['outputs'].update(width=w,height=h,views=['overview'])
 r['task']['scope']+=' Physical hardware batch after installed v0.7: preserve original whole apparatus and add explicit real exterior socket/plug representation; no proprietary connector claim.'
 r['physical_evidence']={'level':'representative exterior geometry unless source explicitly names device/port','source':'PHYSICAL_HARDWARE_SOURCE_AND_SCOPE.md; figure/caption/method; manufacturer hosts blocked this turn','hidden_circuits':'UNVERIFIED','exact_CAD':'NOT_CLAIMED'}
 r['hardware_routes']=[];r['unknown_interfaces']=[]
 def change(label,obj):cm[label]['object']=obj
 def port(pid,obj,owner=None):
  pm[pid]['object']=obj
  if owner:pm[pid]['owner']=cm[owner]['id']
  pm[pid]['surface_tolerance']=.09
  pm[pid]['evidence_note']='Representative socket/plug on physically shown owner surface; role conditional, exact commercial interface not confirmed.'
 def link(id,obj):rm[id]['object']=obj;rm[id]['tolerance']=.08
 def extra_component(id,label,obj):
  c={'id':id,'label':label,'object':obj,'evidence':'schematic','size_basis':'illustrative','state':r['task']['operating_state']}
  r['components'].append(c);cm[label]=c;r['task']['required_components'].append(id)
 def extra_port(id,owner,obj,medium='unknown',direction='unknown'):
  r['ports'].append({'id':id,'owner':owner,'object':obj,'medium':medium,'direction':direction,'state':'connected','surface_tolerance':.09,'evidence_note':'Representative visible exterior connector; actual type and hidden system path not validated.'})
 def extra_route(id,a,b,obj,medium='unknown'):
  r['connections'].append({'id':id,'a':a,'b':b,'kind':'electric','medium':medium,'object':obj,'required':True,'tolerance':.08,'evidence_note':'Illustrative exterior signal segment; actual interface/connection not proven by source alone.'});r['task']['required_connections'].append(id)
 if n==12:
  change('upper pump','upper syringe pump');change('lower pump','lower syringe pump');change('laptop','laptop base')
  port('upper-pump','upper pump exit','upper pump');port('lower-pump','lower pump exit','lower pump')
  change('upper pump','upper visible syringe tip');change('lower pump','lower visible syringe tip')
  extra_port('cam-data','c6','camera representative DATA data socket');extra_port('laptop-data','c10','laptop DATA data socket')
  extra_route('camera-data','cam-data','laptop-data','camera to laptop exterior DATA cable')
  r['hardware_routes'].append({'id':'camera-data','source':'MotionPro X4 camera representative DATA exterior','output':'camera representative DATA data socket','medium':'image-data role, physical connector unknown','input':'laptop DATA data socket','destination':'coherent laptop, source figure','coverage':'representative only; exact IDT interface not verified'})
  r['unknown_interfaces']=['MotionPro X4 proprietary signal connector: NOT assigned USB or RJ45','C-mount identity source-supported; mounted coupler geometry illustrative','pump controls unspecified']
 if n==13:
  change('laptop','adjacent laptop base');r['unknown_interfaces']=['Laptop model, connector and printer control wiring not shown; no added cable']
 if n==14:
  change('left camera','LEFT high speed camera');change('amplifier','microphone/array amplifier');change('oscilloscope','representative oscilloscope');change('laptop','laptop base')
  port('camera','camera DATA output data socket');port('amp-mic','amplifier microphone representative input ring');port('amp-array','amplifier array representative input ring');port('computer','laptop DATA data socket')
  link('camera-to-laptop','camera-to-laptop exterior DATA cable');link('microphone-to-amp','microphone-to-amplifier exterior cable');link('array-to-amp','array-to-amplifier exterior cable')
  extra_port('amp-output','c7','amp representative signal output ring');extra_port('scope-signal','c8','representative oscilloscope ANALOG INPUT BNC input ring',medium='electric')
  extra_route('amp-to-scope','amp-output','scope-signal','representative amplifier-to-scope signal lead')
  r['hardware_routes']=[{'id':'camera-to-laptop','source':'FASTCAM Mini UX100','output':'camera DATA output data socket','medium':'image data, type unverified','input':'laptop DATA data socket','destination':'laptop','coverage':'representative exterior'}, {'id':'microphone-to-amp','source':'microphone exterior','output':'microphone cable surface','medium':'signal role unspecified','input':'amplifier microphone representative input ring','destination':'amp','coverage':'source visible segment'}, {'id':'array-to-amp','source':'top array boundary','output':'array upper signal boundary','medium':'role unspecified','input':'amplifier array representative input ring','destination':'amp','coverage':'source visible segment'}, {'id':'amp-to-scope','source':'amplifier','output':'amp representative signal output ring','medium':'illustrative analog signal','input':'representative oscilloscope ANALOG INPUT BNC input ring','destination':'oscilloscope','coverage':'representative connectivity, NOT confirmed source wiring'}]
  r['unknown_interfaces']=['Photron product Gigabit Ethernet claim from user prompt not independently opened due web_fetch block: data port unspecified','Unnamed amp/scope are not Keysight19; analog BNC representative; amp output→scope line explicitly illustrative','Microphone/array signal protocol and internal circuit unknown']
 if n==16:
  change('external DC supply','representative Genvolt 73030 body')
  port('dc-red','positive HV insulated source plug');port('dc-green','return/ground insulated source plug')
  link('red-lead','positive HV visible external lead');link('green-lead','return/ground visible external lead')
  # Represent plug ownership explicitly; the supply housing is not the plug surface.
  extra_component('c12','positive HV source plug','positive HV insulated source plug')
  extra_component('c13','return/ground source plug','return/ground insulated source plug')
  port('dc-red','HV positive HV QA owner','positive HV source plug');port('dc-green','HV return/ground QA owner','return/ground source plug')
  r['hardware_routes']=[{'id':'red-lead','source':'Genvolt 73030 representative output','output':'positive HV insulated source plug','medium':'high voltage positive exterior','input':'chamber red boundary','destination':'needle ultimately, internal route not pictured','coverage':'exterior only'}, {'id':'green-lead','source':'supply return/ground','output':'return/ground insulated source plug','medium':'ground/return exterior','input':'chamber green boundary','destination':'grounded collector ultimately, internal route not pictured','coverage':'exterior only'}]
  r['unknown_interfaces']=['Exact Genvolt 73030 connector identity and chamber feedthrough unverified','No ordinary USB/low-voltage banana modeled','Positive to needle / grounded collector cited in paper but not drawn as hidden enclosed circuit']
 if n==17:
  change('left supply','representative EA-PSI9200-25T body');change('right pump','right syringe pump')
  r['hardware_routes']=[{'id':x['id'],'source':x['a'],'output':x['a'],'medium':'visible pneumatic','input':x['b'],'destination':x['b'],'coverage':'visible tube boundaries only'} for x in r['connections']]
  r['unknown_interfaces']=['EA-Elektro-Automatik exact terminal positions and coil power leads not visible; no invented DC cable','Pump syringe/ferrule visually representative; pressure internal path unknown']
 if n==19:
  change('resistance substituter','resistance substituter');change('oscilloscope','representative Keysight DSOX1204A front')
  change('lead one','glass to resistance exterior lead');change('lead two','glass to analog input exterior coax')
  port('resistor','resistance actual terminal ring');port('scope','representative Keysight DSOX1204A front ANALOG INPUT BNC input ring')
  link('glass-to-resistor','glass to resistance exterior lead');link('glass-to-scope','glass to analog input exterior coax')
  r['hardware_routes']=[{'id':'glass-to-resistor','source':'tilted film left electrode','output':'QA glass left contact','medium':'electrical exterior','input':'resistance actual terminal ring','destination':'resistance substituter','coverage':'representative terminal'}, {'id':'glass-to-scope','source':'tilted film right electrode','output':'QA glass right contact','medium':'analog exterior/probe attenuator role','input':'representative Keysight DSOX1204A front ANALOG INPUT BNC input ring','destination':'DSOX1204A','coverage':'BNC channel family given by user-provided official manual link, live fetch blocked; channel number assumption'}]
  r['unknown_interfaces']=['GTP-100A-4 1:10 attenuator is Methods-named, but exact exterior location/mating wiring unknown','BNC analog input is source-provided manufacturer manual clue; official page blocked live this turn','Ground return and CH number unknown; chosen port demonstrative only']
 r['task']['outputs']['background']='light';r['unverified']=r.get('unverified',[])+['Current hardware-version output PNG awaits actual external pixel reading','Manufacturer CAD and exact port identity beyond documented evidence unverified','Circuit integrity, contact load and hidden paths not implied by mesh nearpoints']
 (d/f'record_{new}.json').write_text(json.dumps(r,ensure_ascii=False,indent=2)+'\n')
 print(n,new,len(r['components']),len(r['ports']),len(r['connections']))
