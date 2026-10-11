import re
s = open('build_blender_v5.py').read()

# ---------- 1) 文档头 ----------
s = s.replace(
'''"""v5 — 87Sr optical lattice clock, proposed 77 K cryo cavity + MOT
Focused on Fig.7 scope only: furnace/Zeeman slower/stages excluded this round.''',
'''"""v6 — 87Sr optical lattice clock, proposed 77 K cryo cavity + MOT
基于 v5，集中修正 4 类连接/局部展示问题（保留 v5 通过项：
总览完整取景、MOT 光束共同交点、光束降粗降亮、铜腔实际剖切）：
 1. 左壁铜腔穿墙：窗口高度对齐铜腔轴线(z=0.020)；明确"铜腔后窗端伸出
    真空边界、中段管壁经左壁穿腔窗口"为假设安装结构（论文未给尺寸/位置）
 2. 钟光路径：二向色镜改为带明确朝向的薄片，入射段(垂直穿顶壁开孔)→镜面
    反射→出射段(沿晶格轴 x 入腔)，三段首尾相接于镜面中心，方向自洽
 3. 接口局部图重做：右壁/顶壁开孔局部均改为"明确局部剖切"(切掉开孔附近
    1/4 金属面)，相机从斜下方看，展示窗口/法兰/墙厚/连接关系；
    渲染局部图时临时隐藏干扰光束(粗晶格光束/冷却光束)，避免遮挡检查对象
 4. 新增铜腔内部聚焦视角(cam_cavo)：相机贴近腔内，正对隔膜通孔/内壁/
    探测区/后窗，减少无关外壳与线圈入画

Output (render-output/):
  scene_v6.blend
  render_v6_overview.png      (保留 v5 通过项: 总览完整取景)
  render_v6_cavity_cut.png    (保留 v5 通过项: 铜腔 -y 侧 1/4 剖切)
  render_v6_cavity_focus.png  (新增: 铜腔内部聚焦, 隔膜通孔/内壁/探测区/后窗)
  render_v6_port_right.png    (重做: 右壁局部剖切, 窗口/法兰/墙厚/光纤)
  render_v6_port_top.png      (重做: 顶壁局部剖切, 窗口/墙厚/二向色镜位置)
""")'''.replace('"""', '"""') if False else s  # placeholder, replaced properly below

s = s.replace(
'''"""v5 — 87Sr optical lattice clock, proposed 77 K cryo cavity + MOT
Focused on Fig.7 scope only: furnace/Zeeman slower/stages excluded this round.''',
'''"""v6 — 87Sr optical lattice clock, proposed 77 K cryo cavity + MOT
基于 v5，集中修正 4 类连接/局部展示问题（保留 v5 通过项：
总览完整取景、MOT 光束共同交点、光束降粗降亮、铜腔实际剖切）：
 1. 左壁铜腔穿墙：窗口高度对齐铜腔轴线(z=0.020)；明确"铜腔后窗端伸出
    真空边界、中段管壁经左壁穿腔窗口"为假设安装结构（论文未给尺寸/位置）
 2. 钟光路径：二向色镜改为带明确朝向的薄片，入射段(垂直穿顶壁开孔)→镜面
    反射→出射段(沿晶格轴 x 入腔)，三段首尾相接于镜面中心，方向自洽
 3. 接口局部图重做：右壁/顶壁开孔局部均改为"明确局部剖切"(切掉开孔附近
    1/4 金属面)，相机从斜下方看，展示窗口/法兰/墙厚/连接关系；
    渲染局部图时临时隐藏干扰光束，避免遮挡检查对象
 4. 新增铜腔内部聚焦视角(cam_cavo)：相机贴近腔内，正对隔膜通孔/内壁/
    探测区/后窗，减少无关外壳与线圈入画

Output (render-output/):
  scene_v6.blend
  render_v6_overview.png      (保留 v5 通过项: 总览完整取景)
  render_v6_cavity_cut.png    (保留 v5 通过项: 铜腔 -y 侧 1/4 剖切)
  render_v6_cavity_focus.png  (新增: 铜腔内部聚焦)
  render_v6_port_right.png    (重做: 右壁局部剖切)
  render_v6_port_top.png      (重做: 顶壁局部剖切)
""")''')

open('build_blender_v6.py','w').write(s)
print("v6 scaffold written (header only), len=", len(s))
