# 04 Fig.3C 接口链 v04–v05｜几何复核而非像素/功能验收

源：DOI `10.1038/s41526-025-00470-3`，PDF p.4 Fig.3C，图注直接写“panel-mounted sample system with syringe-rack, inlet ports (right) and outlet ports in green (left). Not to scale”；正文称 5 syringes、5-channel slides、与废液端由 silicone tubing 相连。本地正确定域源裁图：`demo-assets/04_microfluidics/source/target_fig3C.png`；旧裁错/全文页保留。前版 v03 经上轮 AGH 实际读图断连、假孔，仍 FAIL。

v04 自 v01 重建两侧外管而不继承 v03 错误；五路右侧蓝色外线、中央固体芯片、五路左侧绿色出口示意端各独立对象。两侧金属外部接头仅代表**可见外部作用面**，平端贴芯片外壁，芯片未钻孔/未建内部流道、密封或循环。v04 保存 `scene.blend` 并独立重载渲染 `overview.png`；Blender 5.1.2，场景 SHA `157ba0ce92cd759c91b813b15af8514e12cff34fd4941dee35566c5fff295906`、PNG SHA `dcedc27c26896a5f53d8df5ca2b16d722812142ee2082411ae7588d27c58a97e`。独立几何 audit 首次暴露五根入口管起点 -0.44 来自误认的 `Pump_i_hub`，而真实 `Syringe_hub_connector_i` 的外向帽面 y=0.07；v04 五路泵端均 **FAIL**。失败不覆盖。

v05 在保存的 v04 基础上仅移动五根入口管首点至各自注射器 hub 真实网格外端；不挪接头或芯片来凑报告。独立重载，按世界网格核了 5×6 项：注射器 hub→蓝线、蓝线→外接头、右接头→芯片边界、芯片另一边界→左接头、左接头→绿线、五路 y 分离；详见 `cases/04_microfluidics/v05/boundary_audit.json`，零 FAIL。v05 场景 SHA `0c04967e4a8e4ebe7ca8619731f805bda66eac3e8cbe2ff8a86f18c2c5ed1dcb`、PNG SHA `030be22f931483b2cbc5ff1110a2dd5b793856b740a243225e0bb0a30c1d2904`。**这个零 FAIL 仅证明被检查的外部网格端点，不能证明实孔、内流、密封、画面可读或与论文像素相符。**原图—v01—v03—v04—v05 的本地含源图比较 `demo-assets/04_microfluidics/comparison_source_v01_v03_v04_v05_LOCAL.png` 不提交。

审查者：AGH 模型仅做 PDF 图注/正文文本定位、代码、独立脚本数值审查；本轮 computer_use 返回 windows/apps discovery failed，**未实际打开 v04/v05 PNG 像素**。外部模型/人均未审。待恢复时首先在单例高清画布检查五路、出口构图/颜色、接口可辨性，若遮挡/浮空继续 v06；不能把 v05 称视觉通过。建模假设：所有实际坐标、接头外形、绿端终止形状；未知：芯片孔、通道、流体连续、密封和真实比例。无源图的缩放比例证据不得断言尺寸。
