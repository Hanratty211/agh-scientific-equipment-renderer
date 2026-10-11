"""AGH R1 v02 task-derived component inventory; preserves user scope and UNKNOWN interfaces.
Run after rendering v02. Literal names come from AGH build_v02.py, not original Skill.
"""
from pathlib import Path
from PIL import Image
import json
ROOT=Path(__file__).resolve().parents[1]
P={q['id']:q for q in json.loads((ROOT/'targets.json').read_text())['papers']}
# Source/Codex requested sets, not the set of everything the generator happened to make.
REQUIRED={
 11:[('laser','laser housing'),('waveplate A','half wave plate 1'),('waveplate B','half wave plate 2'),('power BS','power-control BS optical face'),('collimating lens A','collimating lens 1'),('collimating lens B','collimating lens 2'),('tilted dichroic','tilted dichroic active face'),('objective','objective body'),('sample','sample and upper glass cell'),('halogen lamp','halogen lamp'),('dark-field condenser','dark field condenser'),('short-pass filter','short-pass filter'),('imaging lens','imaging lens'),('sCMOS','sCMOS camera')],
 12:[('pump upper','upper syringe pump'),('pump lower','lower syringe pump'),('capillary','horizontal capillary shell'),('upper inlet','upper inlet fitting'),('lower inlet','lower inlet fitting'),('high-speed camera','high-speed digital camera'),('inverted microscope','inverted microscope body'),('sealed flush branch tip','sealed flush tip'),('waste','waste vessel'),('computer','computer monitor')],
 13:[('printer front frame','silver vertical rail'),('gantry','gantry crossbar'),('mounted head','head carriage'),('print bed','heated build bed'),('emissions display','left emission display'),('front sensor/display','front sensor display'),('laptop','laptop screen')],
 14:[('top array','downward ultrasound transducer'),('bottom reflector','horizontal reflector'),('gap droplet','levitated droplet'),('probe','angled microphone probe'),('camera','side high-speed camera'),('LED','opposed LED light'),('amplifier','amplifier'),('oscilloscope','oscilloscope'),('computer','computer')],
 15:[('aperture lid','lid with genuine center aperture'),('rotor','rotor transparent disk'),('spring','flat spiral spring'),('cord','retractable rope'),('stator','stator transparent tray'),('stator grating','stator vertical electrode strip'),('rotor grating','rotor vertical electrode strip')],
 16:[('clear chamber','Perspex chamber side'),('top dispenser','top dispenser drive'),('syringe','syringe barrel'),('feed tube','PTFE vertical feed'),('needle/support','metal needle'),('collector','circular copper collector'),('Vee shield pair','upright angled PTFE Vee shield'),('front heater','front lower heater support'),('side heat source','side infrared heat source'),('DC supply','black high-voltage DC supply')],
 17:[('four post frame','structural frame post'),('top coil','upper coil housing'),('bottom coil','lower coil housing'),('hemispherical shell','hemispherical shell specimen'),('sample loading fixture','hemisphere loading fixture top'),('left supply','left DC supply'),('right syringe pump','right red syringe pump'),('pressure sensor','front pressure sensor')],
 18:[('1 end plate','position 01 endplate left'),('2 gasket','position 02 gasket left'),('3 bipolar plate','position 03 self-breathing bipolar plate left'),('4 GDE','position 04 GDE left'),('5 gasket','position 05 gasket left'),('6 cathode flow plate','position 06 cathode flow plate left'),('7 membrane','position 07 proton exchange membrane left'),('8 anode','position 08 anode left'),('9 gasket','position 09 gasket left'),('10 anode flow plate','position 10 anode flow plate left'),('11 gasket','position 11 gasket left'),('12 cell A','position 12 grouped cell unit A left'),('13 cell B','position 13 grouped cell unit B left'),('14 cell C','position 14 grouped cell unit C left'),('15 unresolved','position 15 unresolved identity left'),('16 caption conflict','position 16 caption-conflicted gasket or collector left'),('17 end plate','position 17 endplate left'),('assembled four-cell','assembled rear endplate left'),('tie rods','visible assembled tie rod')],
 19:[('tilted glass','tilted glass TeRC plane'),('reservoir','water reservoir'),('flow regulator','U-shaped flow regulator'),('nozzle','dropper nozzle'),('resistance substituter','resistance substituter'),('oscilloscope','oscilloscope'),('visible lead','visible glass electrical lead')],
 20:[('Peltier','Peltier module fixture'),('left Cu','copper heat block'),('right Cu','copper heat block.001'),('grease contact','thermal grease inner face'),('sample','bridging thermoelectric sample'),('edge electrodes','sample-edge electrode pad'),('visible leads','sample edge measurement lead')]
}
STATES={12:'experiment (flush branch sealed)',15:'exploded presentation only',18:'exploded presentation + assembled comparison'}
for id_,rows in REQUIRED.items():
 q=P[id_];d=ROOT/'cases'/f"{id_}_{q['slug']}";prev=json.loads((d/'record_v01.json').read_text());size=Image.open(d/'overview_v02.png').size
 components=[{'id':f'c{j+1}','label':label,'object':obj,'evidence':'paper','size_basis':'illustrative','state':STATES.get(id_,'one diagram/photo state')} for j,(label,obj) in enumerate(rows)]
 rec={'schema':'agh-equipment/0.6','task':{'kind':'device' if id_ in (15,18) else 'physical_setup',
  'scope':prev['task']['scope']+' R1 external visual corrections in CODEX_FEEDBACK_R1.md; retain full panel scope, not a component-only reinterpretation.',
  'operating_state':STATES.get(id_,'one diagram/photo state'),
  'outputs':{'views':['overview'],'annotations':'none','width':size[0],'height':size[1],'background':'light'},
  'required_components':[x['id'] for x in components],
  'required_connections':[],'required_supports':[]},
  'components':components,'ports':[],'connections':[],'supports':[],'labels':[],
  'world_units':'illustrative Blender world units; no measured scale; no arbitrary tolerance chosen',
  'source':{'doi':q['doi'],'figure_url':q['figure_url'],'target_sha256':q['target_sha256']},
  'unverified':['actual interface/port owner and route geometry not bound','occlusion and output-vs-source pixels unreviewed','true material/physical operation unverified'],
  'coverage_gap':'Task asks to trace visible relations. v02 mesh record has only source/Codex-required components; NOT a complete task pass.'}
 if id_==18:rec['source_ambiguity']='Publisher caption assigns 16 to both silicone gasket list and anode current collector; visible 15 not resolved. Visual layers are generic, not authoritative identity.'
 (d/'record_v02.json').write_text(json.dumps(rec,ensure_ascii=False,indent=2)+'\n')
 print(id_,len(components),d/'record_v02.json')
