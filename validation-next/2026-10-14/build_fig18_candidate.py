"""18 Fig.18 standalone PIM/CIM compression candidate; does NOT replace parent Type IV v02.
Input: saved v01 Z100 frame only to preserve editable machine objects; erase unsupported ladder
before making a source-limited 20x20 mm face schematic lattice. Thickness/depth unspecified.
"""
import bpy,sys,math
from pathlib import Path
from mathutils import Vector
root=Path(__file__).resolve().parent;sys.path.insert(0,str(root))
import render_core as r
r.M.clear()
for m in bpy.data.materials:
 if m.name.startswith('MAT_'):r.M[m.name[4:]]=m
def mat(k,col):
 if k not in r.M:
  a=bpy.data.materials.new('MAT_'+k);a.diffuse_color=(*col,1);a.use_nodes=True;p=a.node_tree.nodes.get('Principled BSDF')
  if p:p.inputs['Base Color'].default_value=(*col,1)
  r.M[k]=a
for n,c in {'metal':(.43,.52,.59),'dark':(.09,.14,.20),'soft':(.85,.60,.37),'blue':(.16,.48,.78),'copper':(.60,.34,.18),'base':(.22,.30,.36),'white':(.79,.85,.86)}.items():mat(n,c)
for ob in list(bpy.data.objects):
 if ob.name.startswith('PIM_chain_') or ob.name in ('lower_jaw_working_face','upper_jaw_working_face') or ob.type=='CAMERA':bpy.data.objects.remove(ob,do_unlink=True)
# Face corresponds only to Fig18 left 20 x 20 mm field; illustration units scale 1.35 x 1.35.
# No asserted physical depth or literal internal bonded topology of visible crossed motifs.
xspan=1.34;z0=1.42;z1=2.76;yc=.22
for j in range(7):
 x=-xspan/2+j*xspan/6
 r.segment(f'PIM_vertical_visible_strand_{j}',(x,yc-.04,z0),(x,yc-.04,z1),.021,'blue','assumption')['scope']='Fig18 interweave silhouette; individual polymer connection/joint unknown'
for j in range(7):
 z=z0+j*(z1-z0)/6
 r.segment(f'CIM_cross_visible_strand_{j}',(-xspan/2,yc+.045,z),(xspan/2,yc+.045,z),.022,'soft','assumption')['scope']='cross-strand separated in schematic depth to avoid claiming welded joints'
# Two plates parallel and covering opposite sample faces for the compression configuration in Fig18 middle.
for label,z in [('lower',z0-.08),('upper',z1+.08)]:
 p=r.box(f'Fig18_{label}_compression_plate',(0,yc,z),(1.68,.56,.16),'metal','source-visible',bevel=.018)
 p['contact']='flat compression face overlaps outer sample boundary; pressure/load not tested'
for label,z in [('lower',z0-.22),('upper',z1+.22)]:
 a=r.box(f'Fig18_{label}_machine_mount',(0,yc,z),(1.02,.58,.12),'base','assumption',bevel=.01)
 a['owner']='Z100 testing machine frame (representative mount)'
# Fig18 right DIC speckle is a different panel/surface view: not placed over this lattice.
for o in list(bpy.data.objects):
 if o.name.startswith('Z100_') and o.type=='MESH':o['type_scope']='representative ZwickRoell Z100 shape, not manufacturer CAD'
r.camera((5.0,-8.1,5.0),(0,.19,2.0),6.5)
sc=bpy.context.scene;sc['revision_version']='v03_fig18_PIM_CIM';sc['source_location']='Supplementary Fig.18 left face + middle compression arrangement; NOT Fig17/19/20';sc['known_size']='20 mm x 20 mm visible specimen face ONLY; scene world-unit scale and depth assumed';sc['visual_review']='external_human_new_version_pending';sc['unknowns']='interweave internal bonding, support fixtures and actual thickness unknown; no strength validation'
out=root/'cases/18_mechanical_nature/v03_fig18_PIM_CIM'
if out.exists():raise RuntimeError('refusing overwrite '+str(out))
bpy.context.view_layer.update();out.mkdir(parents=True);bpy.ops.wm.save_as_mainfile(filepath=str(out/'scene.blend'));print('FIG18_CANDIDATE_SAVED',out/'scene.blend',flush=True)
