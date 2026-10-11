import bpy, mathutils, math
bpy.ops.wm.open_mainfile(filepath="render-output/scene_v11.blend")
# CAV_R_IN=0.005 (bore r 5mm, ID 10mm), CAV_R_OUT=0.0065 (OD r 6.5mm), wall 1.5mm
# lining r_in? cuo_lining 是内衬, 半径 ~ CAV_R_IN=5mm
# 镜盘实心外缘 5.75mm > 管壁内径 5.0mm -> 镜盘缘伸入管壁/内衬末端
print("CAV_R_IN=0.005(孔) CAV_R_OUT=0.0065(外)")
# 镜盘 5.75mm 实心外缘 必须 <= 管壁内径(5.0mm) 才不会插穿末端铜壁/内衬
# 但倾斜 20° 后投影半宽=5.40mm 需 >= 孔 5.0mm 才关闭开口 -> 镜盘实心外缘须 >= 5.40/cos20=5.75mm
# 冲突: 实心外缘 5.75mm > 内径 5.0mm -> 镜盘缘必然伸入管壁/内衬末端, 除非镜盘整体后移到
# 腔内(离末端一段距离), 让镜盘实心边缘落在腔内空腔里, 不碰末端铜壁/内衬端面.
# 即镜盘嵌入承座槽, 槽在腔内(离末端 0.2mm 深处), 镜盘向外(朝腔内)偏移, 边缘悬在空腔中.
