"""User-directed exterior repair. Actual dimensions remain schematic; input immutable."""
import bpy,sys,math,hashlib,json
from pathlib import Path
src=Path(bpy.data.filepath).resolve();before=hashlib.sha256(src.read_bytes()).hexdigest()
out=Path(sys.argv[sys.argv.index('--')+1]).resolve();assert not out.exists()
O=bpy.data.objects;changes=[]
def cylinder_mesh(obj,radius,depth,location,rotation=(0,0,0),bevel=.008):
 old={'dimensions':list(obj.dimensions),'location':list(obj.location),'rotation':list(obj.rotation_euler)}
 materials=list(obj.data.materials)
 bpy.ops.mesh.primitive_cylinder_add(vertices=128,radius=radius,depth=depth)
 temp=bpy.context.object;mesh=temp.data.copy();bpy.data.objects.remove(temp,do_unlink=True)
 obj.data=mesh;obj.location=location;obj.rotation_euler=rotation;obj.scale=(1,1,1)
 for mod in list(obj.modifiers):obj.modifiers.remove(mod)
 obj.data.materials.clear()
 for m in materials:obj.data.materials.append(m)
 for f in obj.data.polygons:f.use_smooth=len(f.vertices)==4
 if bevel:
  b=obj.modifiers.new('Small edge radius','BEVEL');b.width=bevel;b.segments=3
  n=obj.modifiers.new('Face normals','WEIGHTED_NORMAL');n.keep_sharp=True
 changes.append({'object':obj.name,'before':old,'cylinder_radius':radius,'cylinder_depth':depth,'location':list(location),'rotation':list(rotation)})
 obj['revision_basis']='User review: supports too small and round source exterior became rectangular. Display proportions only, no physical dimension claim.'
for lab,z,cz in [('lower',.68,.52),('upper',2.52,2.64)]:
 cylinder_mesh(O[lab+'_circular_grip_body'],.43,.24,(0,.20,z),(math.pi/2,0,0),.006)
 cylinder_mesh(O[('Lower' if lab=='lower' else 'Upper')+'_jaw_carriage'],.24,.25,(0,.20,cz),bevel=.01)
 shaft=O[lab+'_mount_shaft'];depth=.29 if lab=='lower' else .37
 cylinder_mesh(shaft,.17,depth,(0,.26,.26 if lab=='lower' else 2.94),bevel=.004)
sc=bpy.context.scene;sc['revision']='robotics_v08_user_review_round_silhouette';sc['user_acceptance']='pending on new renders; v07 was conditionally accepted'
bpy.context.view_layer.update();bpy.ops.wm.save_as_mainfile(filepath=str(out))
assert hashlib.sha256(src.read_bytes()).hexdigest()==before
(out.parent/'changes.json').write_text(json.dumps({'source_sha256':before,'result_sha256':hashlib.sha256(out.read_bytes()).hexdigest(),'changed':changes,'scope':'Round grip bodies, cylindrical support collars, thicker support shafts; all other geometry, cameras and materials inherited.'},indent=2)+'\n')
