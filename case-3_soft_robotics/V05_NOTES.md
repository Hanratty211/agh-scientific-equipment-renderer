# Case 3 v05｜只补白管可见延续；气路仍未定

## 新证据与允许的修正
公开原图：https://www.nature.com/articles/s41467-023-39691-z ，Fig. 3b；本轮取得出版方 2001×1572 PNG（`https://media.springernature.com/original/springer-static/image/art%3A10.1038%2Fs41467-023-39691-z/MediaObjects/41467_2023_39691_Fig3_HTML.png`），实际在 Preview 中查看 Fig.3b 局部，作为 v04 的 494×817 本地裁图之外的较高清证据。局部显示左侧横跨软体的**白管连续弯向右下**，末段带一小段蓝色套/管，随后在压力表**上方**的深色双管组件区域被遮挡；旁边还有另一条从上方下行、穿过同一组件附近的白管。此处可辨认的是可见延续与遮挡，不是贯通孔、仪表接口、完整气路。原图上的虚线、箭头和标签均非实体。

论文 Methods—“Soft gripper”：`The soft gripper was fabricated by integrating a soft pneumatic actuator, a CO2 canister (95 g; UP), a mechanical pressure regulator (IR2000-02G-A; SMC), and an STV into a soft-foamed body.` 来源定性为 **soft-foamed body**。v01–v04 的“织物主体”表述、程序化布纹与外观为旧建模推测，不是论文事实。本轮只更正文字证据身份，不改变其他外观；后续如修材质另立版本。

补充信息 PDF `https://media.springernature.com/original/springer-static/esm/art%3A10.1038%2Fs41467-023-39691-z/MediaObjects/41467_2023_39691_MOESM1_ESM.pdf` 检视第 5–7、13 页及相关图注，未找到这条白管与深色组件的实物端口身份和背面走线。正文所述 CO₂→机械调压→STV、STV 室压→两软执行器，为**功能关系**，不证明眼前白管是哪一条供/室压支路。论文 PDF 的另一次尝试超时，未依赖它。

## v05 改动与未确认
保留 v04 其他外形、气压表、右管、相机和渲染设定。删除 v04 自行增加、未证实是气路终端的灰夹体、压带及两个虚构的暗色孔；延长左白管到参考中蓝色短套，随后终止在照片中遮挡白管的深色双管组件边缘。新增的深色块只代理**原图确实可见**的组件轮廓；右侧浅色圆片也是该组件在图像中的可见对比，非精密型号复制、非已认证的实际接头/气路部件。没有增设压力表气管、背面管或三通。

**确认层级：**照片和 v05 近景可追踪“连续白管→蓝套→深色组件边缘遮挡”，这是视觉延续；软体与组件之间的安装方式只能称可见邻接，**不能确认机械固定**；深色组件内部孔口、白管流体是否连通及供/室压身份、密封与后续隐藏路线仍**未知**。不把几何重叠当作“气动连接修复通过”。此前 v04 的“已修复”只限外观附着而非气路，本版本更正这一结论。

## 实际检查和交付状态
Blender 5.1.2 生成 `overview_v05.png`、`soft_gripper_v05.blend`；保存后重新打开场景，确认旧灰夹体与压带已移除、相机为 v05、无文字。`detail_left_tube_v05.png` 是总览像素框 `(270,365,680,780)` 裁切并放大到 820×830；验证其像素确实来自当前总览。模型通过 Preview 的 computer_use 实际查看出版方 Fig.3b 局部及 v05 局部：蓝套不再孤立悬挂，白管在深色可见组件边缘被遮挡；**只能算图像外观自审，未获得外部 v05 验收**。内部连接仍不确定。

复跑：在此目录 `/Applications/Blender.app/Contents/MacOS/Blender --background --python build_scene_v05.py`，另用 Pillow crop 上述矩形生成近景。保留 v01–v04。AGH append-only ledger 的本轮索引：`skill_read(agh-scientific-equipment-renderer)`、读取 v04 脚本/记录、HTTP 拉取高清 Fig.3b 与论文方法、补充 PDF 检索、Preview `computer_use` 读高清/生成局部、复制脚本及 `edit` 修正、Blender 渲染和重开检查、Pillow 裁图。本轮经验只在案例记录，通用 Skill 未更新。
