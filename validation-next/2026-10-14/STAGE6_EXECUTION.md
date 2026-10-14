# Stage6 执行记录｜第四轮外部复核后

- 核 `main` 与远端同基线 `69f197b768d536c3625169fb5d20f3b5c1a9f9ba`；未碰协作者分支。外部复核确实从磁盘逐图看 stage5 的十例，判词列 `EXTERNAL_HUMAN_REVIEW.md` 第四表，目视和结构分栏，全部未验收。
- 仅三例改图：13 v04→v05→v06（后端三彩束不动，主缆套环接实物细长远端头、前光学窗；v06 加长轮廓）、14 v04→v05（Fig1b 图注支持 top-plate 真钻孔，布尔孔后同一光轴朝样品，中心射线穿孔/离轴撞板）、18 v03_fig18_PIM_CIM→v04_fig18_woven（交错双族连续波状前视织构，原 20×20 mm 正面锚点/压板保留，深度和节点标假设）。其它七例不改。
- Blender 5.1.2 每个新 scene 保存为独立目录，用**另进程重开保存 .blend** 后渲染并写 `render_report.json` 两 SHA。`audit_stage6.py` 有局部网格/射线/曲线断言，仍不是像素或功能验收。
- 真实审核失败史：初次 13 v05 `longer_than_previous_short_cap` FAIL 实为审计误用了绕 X 旋转 cylinder 的 local dimensions.y，改用世界轴包围后重跑 v05 零 FAIL；v06 是独立更细长形态而非假装修了确定的几何断连。14 审计曾遇 `ray_cast` distance 必须 keyword、以及输出路径变量被物体覆盖，修脚本后独立重跑，并留本地失败日志（不推 Git）。18 v04 有独立有限检查且保留 v03 正交错误版。
- 本地十例源—被审旧版—当前版三栏 `demo-assets/<id>/stage6_source_*_LOCAL.png`，均含出版方来源，**不入 Git**。队列 `STAGE6_REVIEW_QUEUE.md`。`computer_use.list_apps` 再次失败，新三图 AGH 尚未读像素，待外部下一轮复核。
