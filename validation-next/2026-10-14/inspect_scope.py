import bpy
for n in ('Distal_long_scope_head','Distal_scope_shaft_sleeve'):
 o=bpy.data.objects[n]
 print(n,'loc',list(o.location),'scale',list(o.scale),'dims',list(o.dimensions),'rot',list(o.rotation_euler))
