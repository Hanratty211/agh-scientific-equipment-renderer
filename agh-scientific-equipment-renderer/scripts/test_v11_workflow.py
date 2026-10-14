#!/usr/bin/env python3
"""Abstract instructional counterexamples; no paper/case evidence or visual approval."""
from pathlib import Path
import sys
S=Path(__file__).resolve().parent.parent
skill=(S/'SKILL.md').read_text();identity=(S/'references/identity_port_gate_v11.md').read_text();source=(S/'references/source_render_and_demo_v11.md').read_text();change=(S/'CHANGELOG.md').read_text()

def identity_gate(device,parts,evidence_flag,port_kind='unknown'):
 if not evidence_flag or not parts:return False
 if device=='laptop':return {'screen','base','keyboard','hinge'}<=set(parts) and port_kind in {'supported','schematic','unknown'}
 if device=='oscilloscope':return {'display','housing','signal_input'}<=set(parts) and port_kind in {'supported','schematic'}
 return True

def route_gate(owner,medium,target_face,port_status,claims_function=False):
 return bool(owner and medium) and target_face not in {'screen','housing_any','bbox_center'} and port_status in {'supported','schematic'} and not claims_function

def qa_gate(source_anchor,png_hash,reviewer,actual_pixel_read):
 return bool(source_anchor and len(png_hash)==64) and reviewer in {'AGH','external_human','external_model'} and actual_pixel_read

tests={
 'laptop_positive':identity_gate('laptop',['screen','base','keyboard','hinge'],True,'schematic'),
 'laptop_two_rectangles_rejected':not identity_gate('laptop',['screen','base'],True,'unknown'),
 'oscilloscope_signal_face_positive':identity_gate('oscilloscope',['display','housing','signal_input'],True,'supported') and route_gate('scope','electrical','signal_input','supported'),
 'oscilloscope_screen_rejected':not route_gate('scope','electrical','screen','supported'),
 'oscilloscope_bbox_rejected':not route_gate('scope','electrical','bbox_center','supported'),
 'oscilloscope_unknown_port_rejected':not route_gate('scope','electrical','signal_input','unknown'),
 'coincident_endpoint_not_function':not route_gate('scope','electrical','signal_input','supported',True),
 'pixel_report_not_review':not qa_gate('figure page','a'*64,'AGH',False),
 'pixel_external_real_review':qa_gate('figure page','a'*64,'external_human',True),
 'router_required_docs':all('references/'+x in skill for x in ('identity_port_gate_v11.md','source_render_and_demo_v11.md')),
 'copyright_boundary':'本地' in source and '不在 Skill 包' in (S/'PROVENANCE.md').read_text(),
 'routing_attribution':'review_images.py' in source and '独立' in source and '图片排版' in source,
 'old_principles_not_denied':'v1.0 已规定' in identity and 'v1.0 原已要求' in change,
}
for k,v in tests.items():print(('PASS' if v else 'FAIL'),k)
sys.exit(0 if all(tests.values()) else 1)
