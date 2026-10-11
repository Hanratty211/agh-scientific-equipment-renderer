"""AGH-authored v01 records from declared visible apparatus, not image recognition.
Runs after Blender scenes exist. No broad physical/visual validation inferred.
python3 public-validation-11-20/cases/build_records_v01.py
"""
from pathlib import Path
import json
from PIL import Image
ROOT=Path(__file__).resolve().parents[1]
PAPERS={x['id']:x for x in json.loads((ROOT/'targets.json').read_text())['papers']}
# The object strings below are literal names authored in each build_v01.py. Each case uses
# source-visible parts, illustrative dimensions and no invented port-to-port topology.
PARTS={
11:[('optical table','optical table'),('illumination module','illumination module'),('optics','optic holder'),('sample stage','sample stage'),('glass sample','glass liquid cell'),('detector','detector housing'),('camera','camera body')],
12:[('pump 1','syringe pump'),('pump 2','syringe pump.001'),('capillary','glass capillary'),('inverted microscope','microscope base'),('high-speed camera','high speed camera'),('waste vessel','waste vessel'),('computer','computer')],
13:[('printer frame','printer plinth'),('gantry','gantry crossbar'),('extruder head','extruder carriage'),('print bed','heated bed'),('display','display module'),('sensor','visible sensor'),('laptop','laptop base')],
14:[('transducer array','ultrasonic array element'),('reflector','facing reflector'),('probe','probe microphone'),('camera','high-speed camera'),('LED','LED lamp'),('amplifier','amplifier'),('oscilloscope','oscilloscope'),('computer','computer')],
15:[('lid','lid cap'),('rotor','rotor shell'),('stator','stator exterior'),('spring','coil spring illustrated'),('retractable cord','visible retractable cord'),('electrode rings','stator electrode outer')],
16:[('Perspex chamber','chamber end pane'),('syringe dispenser','syringe barrel'),('PTFE tube','visible PTFE tube'),('needle','metal needle'),('collector','collector disk'),('Vee shield','PTFE Vee-shield edge'),('controller','syringe dispenser controller'),('heat source','infrared heat source'),('supply','high voltage supply')],
17:[('Helmholtz coil left','Helmholtz coil winding'),('Helmholtz coil right','Helmholtz coil winding.001'),('magnetic shell','center magnetic shell'),('syringe pump','syringe pump'),('pressure sensor','pressure sensor'),('DC supply','DC supply')],
18:[('exploded end plate 1','exploded 1 end plate'),('exploded gasket 2','exploded 2 silicone gasket'),('exploded bipolar plate 3','exploded 3 bipolar self-breathing plate'),('exploded GDE 4','exploded 4 GDE'),('exploded cathode flow 6','exploded 6 cathode flow plate'),('exploded membrane 7','exploded 7 proton exchange membrane'),('exploded anode 8','exploded 8 anode'),('exploded anode flow 10','exploded 10 anode flow plate'),('exploded collector 16','exploded 12 anode current collector'),('exploded end plate 17','exploded 13 end plate'),('four-cell assembled','assembled rear end plate')],
19:[('tilted test fixture','tilted glass support'),('TeRC glass','transparent TeRC glass'),('film','thin film on glass'),('drop dispenser','drop dispenser'),('electrical readout','electrical readout')],
20:[('Peltier module','Peltier module'),('copper block left','copper thermal block'),('copper block right','copper thermal block.001'),('grease contacts','grease interface patch'),('sample','bridged sample'),('electrode pads','sample electrode pad'),('nanovoltmeter one','nanovoltmeter'),('nanovoltmeter two','nanovoltmeter.001')],
}
# No ports are asserted in v01: source-visible routes have not yet been tied to independently
# verified physical interface surfaces. Do not turn component centers into self-proving ports.
# This is an explicit incomplete scope record, not an interface/route PASS.
STATES={15:'exploded presentation',18:'exploded presentation and assembled comparison',12:'during experiment, flush needle sealed'}
for id_,part_rows in PARTS.items():
 q=PAPERS[id_];folder=ROOT/'cases'/f"{id_}_{q['slug']}"
 components=[]
 for j,(label,obj) in enumerate(part_rows):
  components.append({'id':f'c{j+1}','label':label,'object':obj,'evidence':'paper','size_basis':'illustrative','state':STATES.get(id_,'one illustrated setup')})
 rec={'schema':'agh-equipment/0.6','task':{
  'kind':'physical_setup' if id_ not in (15,18) else 'device',
  'scope':q['scope']+' Panel '+q['panel']+'; SOURCE_LEDGER.md and publisher caption govern. Unclear hidden paths omitted.',
  'operating_state':STATES.get(id_,'one illustrated setup'),
  'outputs':{'views':['overview'],'annotations':'none','background':'opaque'},
  'required_components':[x['id'] for x in components],
  'required_connections':[],'required_supports':[]},
 'components':components,'ports':[],'connections':[],'supports':[],'labels':[],
 'world_units':'illustrative Blender units, no measured unit scale; no geometric tolerance asserted',
 'source':{'doi':q['doi'],'figure_url':q['figure_url'],'input_sha256':q['target_sha256']},
 'unverified':['complete visual scope vs reference','interface identity','hidden fluid/electric/optical topology','functional contact','occlusion/readability']}
 # Scope relations are NOT automatically cleared by empty required_connections: explicit follow-up.
 if id_ in (11,12,16,17,19,20):rec['unverified'].append('required visible routes not independently mapped to actual world-face ports in v01')
 rec['task']['outputs']['width'],rec['task']['outputs']['height']=Image.open(folder/'overview_v01.png').size
 (folder/'record_v01.json').write_text(json.dumps(rec,ensure_ascii=False,indent=2)+'\n')
 print(id_,folder/'record_v01.json')
