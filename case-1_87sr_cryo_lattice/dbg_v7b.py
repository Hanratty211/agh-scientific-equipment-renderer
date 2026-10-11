import bpy, mathutils, math
bpy.ops.wm.open_mainfile(filepath="render-output/scene_v6.blend")
scene=bpy.context.scene
deps=bpy.context.evaluated_depsgraph_get()
# Proper solid-vs-solid intersection: boolean INTERSECT between copper tube (solid body, ignoring hollow) and the glass window slab.
# Reconstruct a solid copper tube (no bore) to test against win_left glass.
CAV_X=-0.080; AXIS_Z=0.020; CAV_R_OUT=0.0065; CAV_LEN=0.160
bpy.ops.mesh.primitive_cylinder_add(radius=CAV_R_OUT, depth=CAV_LEN, location=(CAV_X,0,AXIS_Z), rotation=(0,math.radians(90),0), vertices=64)
solid=bpy.context.object; solid.name="test_solid_cav"
# win_left glass slab geometry: 20mm x 20mm x 0.45mm at x=-0.1385, z=0.020
bpy.ops.mesh.primitive_cube_add(size=1, location=(-0.1385,0,AXIS_Z), rotation=(0,math.radians(90),0))
glass=bpy.context.object; glass.name="test_glass"
glass.scale=(0.00045,0.020,0.020)
bpy.ops.object.transform_apply(scale=True)
# boolean intersect
md=solid.modifiers.new("b",'BOOLEAN'); md.operation='INTERSECT'; md.object=glass
bpy.context.view_layer.objects.active=solid
bpy.ops.object.modifier_apply(modifier="b")
ev=solid.evaluated_get(deps); me=ev.data
print("boolean INTERSECT(solid copper tube, glass slab) vertex count:", len(me.vertices), "face count:", len(me.polygons))
# Also: does the copper tube cross the left wall METAL slab (x -0.140..-0.137, excluding glass)?
wall_slab_outer=mathutils.Vector((-0.140,-0.075,0)); wall_slab_inner=mathutils.Vector((-0.137,0.075,0))
# Check copper tube vertices in the wall metal ring around the glass hole
bpy.data.objects.remove(solid,do_unlink=True); bpy.data.objects.remove(glass,do_unlink=True)
