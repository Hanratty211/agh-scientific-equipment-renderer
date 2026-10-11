import bpy, mathutils
bpy.ops.wm.open_mainfile(filepath="render-output/scene_v8.blend")
CLK_TOP_Z = 0.0+0.075-0.0015  # CHAM_CZ=0, CHAM_H/2-T/2 = 0.075-0.0015
CLK_HOLE_X=0.0; MIR_X=0.0; AXIS_Z=0.020; CAV_X=-0.080
print("CLK_TOP_Z =", CLK_TOP_Z)
_p_in = mathutils.Vector((CLK_HOLE_X,0,CLK_TOP_Z+0.030))
_p_mir= mathutils.Vector((MIR_X,0,AXIS_Z))
_p_out= mathutils.Vector((CAV_X,0,AXIS_Z))
print("p_in start =", _p_in, " p_mir =", _p_mir, " p_out =", _p_out)
d_in =(_p_mir-_p_in).normalized(); print("d_in =", [round(v,3) for v in d_in])
d_out=(_p_out-_p_mir).normalized(); print("d_out =",[round(v,3) for v in d_out])
n=(d_in-d_out).normalized(); print("n =", [round(v,3) for v in n])
ref=d_in-2*(d_in.dot(n))*n; print("reflect(d_in) =", [round(v,3) for v in ref], " (should equal d_out)")
# 实际镜面 local z (世界法向)
o=bpy.data.objects['dichroic_mir']
lz=o.matrix_world.to_quaternion() @ mathutils.Vector((0,0,1))
print("实际镜面世界法向(local z) =", [round(v,3) for v in lz])
