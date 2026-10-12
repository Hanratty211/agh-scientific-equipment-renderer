"""R4 only camera rear DATA chain. Begin from saved v05; do not change pumps,
capillary feeds, computer socket, whole camera placement or other apparatus.
Camera rear world +Y. Actual housing rear face y=+0.265. Plug and new boot
are coaxial +Y, and old cable's off-axis -X start is replaced by same-axis
connector-to-boot-to-cable segment. Representative port model, not IDT CAD.
"""
import bpy,sys
from pathlib import Path
from mathutils import Vector
p=Path(__file__).resolve().parent;sys.path.insert(0,str(p.parent))
from scene_parts_v03 import box,MAT
from physical_parts_v01 import bind_existing_materials
bpy.ops.wm.open_mainfile(filepath=str(p/'scene_v05.blend'));bind_existing_materials()
body=bpy.data.objects['high speed camera'];assert abs(body.location.y)<.001 and abs(body.dimensions.y-.53)<.001
axis=Vector((0,1,0));socket=bpy.data.objects['camera representative DATA data socket'];plug=bpy.data.objects['camera representative DATA seated data plug'];boot=bpy.data.objects['camera representative DATA cable boot'];lead=bpy.data.objects['camera to laptop exterior DATA cable']
assert all(o.type=='MESH' for o in (body,socket,plug,boot)) and lead.data.splines[0].type=='BEZIER'
# Body rear surface y=.265. New recessed socket, inserted plug, long stress
# buffer share x=.205, z=2.59. The long boot straddles the existing lead's
# first outside waypoint (-.5,1.02,2.78) only after that waypoint is rebuilt.
x=.205;z=2.59
socket.location=(x,.267,z);socket.dimensions=(.088,.026,.050)
plug.location=(x,.320,z);plug.dimensions=(.074,.092,.037)
boot.location=(x,.402,z);boot.dimensions=(.058,.098,.040)
# Remove only prior camera cable spline and create one continuous editable
# cubic Bezier with correct world coordinates. Body rear plug and boot are on
# +Y normal; cable START is within the actual boot volume at y=.425.
spline=lead.data.splines[0];old=[tuple(q.co) for q in spline.bezier_points]
assert len(old)==11
cable_pts=[Vector((x,.425,z)),Vector((x,.482,z)),Vector((x,.605,z)),
 Vector((.15,.84,2.70)),Vector((-.50,1.02,2.78)),*[Vector(q) for q in old[4:]]]
bpy.data.objects.remove(lead,do_unlink=True)
from physical_parts_r1 import bent_cable
new=bent_cable('camera to laptop exterior DATA cable',cable_pts,.014,'black',.20)
# Set explicit first controls along +Y to hold the physical exit axis, not a
# tangent automatically bent toward an off-axis waypoint.
b=new.data.splines[0].bezier_points
b[0].handle_left=(x,.405,z);b[0].handle_right=(x,.445,z)
b[1].handle_left=(x,.462,z);b[1].handle_right=(x,.502,z)
b[2].handle_left=(x,.575,z);b[2].handle_right=(x,.635,z)
bpy.context.view_layer.update();bpy.context.preferences.filepaths.save_version=0
scene=bpy.context.scene;scene.render.filepath=str(p/'overview_v06_build_only.png')
bpy.ops.wm.save_as_mainfile(filepath=str(p/'scene_v06.blend'))
