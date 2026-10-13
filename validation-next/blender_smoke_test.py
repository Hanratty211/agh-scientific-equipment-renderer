import bpy, sys
def add_box(name, x=0.0, y=0.0, z=0.0, size=1.0):
    bpy.ops.mesh.primitive_cube_add(size=size, location=(x,y,z))
    o = bpy.context.active_object
    o.name = name
    return o
bpy.context.scene.unit_settings.system = 'METRIC'
add_box('smoke_box', 0, 0, 0, 1.0)
scene = bpy.context.scene
scene.render.resolution_x = 64
scene.render.resolution_y = 64
scene.render.engine = 'BLENDER_EEVEE'
scene.render.image_settings.file_format = 'PNG'
scene.render.filepath = r'D:\Document\MyCodeProject\AGH\agh-scientific-equipment-renderer\validation-next\smoke.png'
bpy.ops.render.render(write_still=True)
print('BLENDER_SMOKE_OK', scene.render.resolution_x, scene.render.resolution_y)
sys.exit(0)
