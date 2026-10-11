# Fig.2(a) v7 低成本无字草案：激光出口纠错

**撤回** v5/v6 中“激光源接口已通过”的说法：当时 `laser_exit` 实心小盒处于 `laser_housing` 内，光束起点和孔圈没有建立有效外部接口；原先的“锚点共线/在 laser_exit 表面”不能证明它不穿金属。v6 与以前的制品保留，仅作纠错历史。

## 本轮实际修改
保留 v6 的其余光路、平凸镜、BS/SLM、光纤、材质和相机。参考 Fig.2(a) 激光器朝 L1 的相对方向，选机壳**朝 L1 的左向外表面**；该图未给具体厂家孔位，故本版是**外置出光嘴示意假设**，不是产品 CAD。脚本从机壳真实网格中向 M1 方向射线求交，取得安装面；在此处装入深约 1 mm 的空心圆筒基座（外径 16 mm、内径 9 mm，均示意），向外伸出约 29 mm。安装法兰置于实际机壳面，孔圈置于空心嘴外端，中心未用实心盖封住。光束从外端开口**中心**沿嘴轴向外发出，未画机壳内部光束；L1/L2 根据新的开口中心→M1 轴重新投影，无凭空折角。未扩大系统部件。

**文件**：`build_case2_v7_overview.py` → `render-output/scene_case2_v7_overview.blend`、`render-output/case2_v7_overview_wordless.png`；`crop_case2_v7.py` 直接从总览裁出 `render-output/case2_v7_crop_laser_outlet.png`（288×173 原像素）及保留的两张旧检查范围的新 v7 裁图；`verify_case2_v7_overview.py` / `verify_case2_v7_overview_results.txt`。

## 几何核查（非视觉通过）
独立重读 saved .blend：**260 PASS / 0 FAIL，进程 exit 0**。从出口网格四组环顶点重算外端圆心/轴向（不信任自定义 `aperture_center`）：光束首点与圆心差约 0.00003 mm，轴向与首段一致；内孔半径 4.5 mm > 示意首段光束半径 2 mm；真实机壳与安装圈中心表面间隙 0，外端到机壳真实射线命中点约 29 mm。出口中心、L1/L2 中心及入/出面锚点、M1 作用点同轴；出射中心及 ±2 mm 四条平行抽样射线均**不命中机壳实心网格**。这只证明所抽射线和本模型几何关系，不是束流的真实安装公差测量，也不证明成图可辨。

## 实际图片观察 / 待核对
本轮 `computer_use list_windows` 再次返回 `Computer Use windows discovery failed`，没有新窗口 pid/window_id，未能直接看 v7 总览或裁图。请外部**实际读** `case2_v7_crop_laser_outlet.png`（必要时放大原像素查看），尤其核查嘴是否贴壳、开口是否看得到、是否有新遮挡。裁图已从最终总览逐像素裁出；文件与哈希不能代替人眼/模型视觉复核。

**仍属假设**：出光嘴在机壳左向面的具体偏心位置、16/9 mm 直径与伸出量、产品真实装配构造。1064 nm 红色仅是示意，不是肉眼可见红激光。Skill 仍是草案，不出正式图。
