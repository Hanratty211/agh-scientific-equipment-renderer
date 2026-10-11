#!/usr/bin/env python3
"""Editable SVG annotation layer from record labels and actual saved-scene mesh geometry.
blender --background scene.blend --python make_svg_labels.py -- record.json output.svg
No-text tasks fail closed. Label anchors use projected evaluated MESH geometry centroid,
not custom object-origin or caller-provided pixel coordinates. Output is SVG only.
"""
import bpy,json,sys,html
from pathlib import Path
from mathutils import Vector
from bpy_extras.object_utils import world_to_camera_view
args=sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else []
if len(args)!=2:raise SystemExit('record and output.svg required')
record=json.loads(Path(args[0]).read_text(encoding='utf-8'));out=Path(args[1]);task=record.get('task',{});labels=record.get('labels',[])
if task.get('outputs',{}).get('annotations')!='svg':raise SystemExit('SVG labels forbidden for no-text task')
if not labels:raise SystemExit('No requested labels: no SVG produced')
scene=bpy.context.scene;cam=scene.camera
if not cam:raise SystemExit('Saved scene has no active camera')
width=task['outputs'].get('width');height=task['outputs'].get('height')
if not isinstance(width,int) or not isinstance(height,int) or width<1 or height<1:raise SystemExit('width/height required')
components={c['id']:c for c in record.get('components',[])};ports={p['id']:p for p in record.get('ports',[])}
def target(name):
 item=components.get(name) or ports.get(name)
 if not item:raise ValueError('Unknown label target '+name)
 obj=bpy.data.objects.get(item.get('object',''))
 if not obj or obj.type!='MESH':raise ValueError('Target must be actual mesh '+name)
 ev=obj.evaluated_get(bpy.context.evaluated_depsgraph_get());mesh=ev.to_mesh()
 try:
  if not mesh.vertices:raise ValueError('Empty geometry '+name)
  p=sum((ev.matrix_world@v.co for v in mesh.vertices),Vector())/len(mesh.vertices)
 finally:ev.to_mesh_clear()
 q=world_to_camera_view(scene,cam,p)
 if not 0<=q.x<=1 or not 0<=q.y<=1 or q.z<cam.data.clip_start or q.z>cam.data.clip_end:raise ValueError('Target out of frame '+name)
 return round(q.x*width,2),round((1-q.y)*height,2)
parts=[f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">']
for item in labels:
 x,y=target(item['target']);side=item.get('side','right');sign=-1 if side=='left' else 1
 end=min(width-8,max(8,x+sign*70));textx=min(width-8,max(8,end+sign*5));align='end' if sign<0 else 'start'
 parts.append(f'<g id="{html.escape(item["id"],quote=True)}" data-target="{html.escape(item["target"],quote=True)}">')
 parts.append(f'<line x1="{x}" y1="{y}" x2="{end}" y2="{y}" stroke="#1c333d" stroke-width="1.5"/>')
 parts.append(f'<text x="{textx}" y="{y-5}" text-anchor="{align}" font-size="14" font-family="sans-serif" fill="#1c333d">{html.escape(item["text"])}</text></g>')
parts.append('</svg>');out.write_text('\n'.join(parts)+'\n',encoding='utf-8');print('LABELS',len(labels),out)
