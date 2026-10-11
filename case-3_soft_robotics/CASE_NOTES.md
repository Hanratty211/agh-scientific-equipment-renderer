# Case 3 · v01 低成本整体预览（待外部视觉反馈）

## 来源与范围
- 指定局部参考：`/Volumes/wht/苏大/Skills开发过程_20261010/assets/validation/inputs/01_soft_robotics.jpg`，494×817，实际在 macOS 预览中观看；仅作视觉对照，未拷入交付目录。
- Choe et al., *A soft, self-sensing tensile valve for perceptive soft robots*, Nature Communications (2023), https://www.nature.com/articles/s41467-023-39691-z ，Fig. 3b 图版及图注；阅读同页“Untethered and electronics-free soft gripper”正文；补充信息 PDF 第 5–7、13 页检索相关用途/实用特性，未据此推断本抓手背面安装。Fig. 3b 展示两软执行器、body、CO₂ canister、mechanical pressure regulator、STV、handle。正文说明罐经机械调压后以恒定供气压力给 STV，STV 室压力通向两软执行器；STV 两端连于主体和手柄，拉柄调节张力。论文的 L₀=80 mm、n=2、p=10 mm 属于阀设计，不拿来推断全装配尺寸。
- 目标为图 3b 的**完整抓手装配**的单张无文字低成本三维总览；不包含松果、人手、实验台或外置控制箱。

## v01 建模假设与未知
- Blender 单位和外形比例按照片目测，**非实测 CAD**。软指使用两条向内弯曲的浅色弧形器件与可见深色分段；主体为深灰软质包覆，折角/织物纹理极简；调压器和读数盘位于可见表面，下端管件和拉柄可辨。
- 原图的白色虚线罐轮廓和蓝色箭头是图文标示，不生成实体虚线罐和箭头；罐大部位于主体覆盖内，仅展示前侧可见端部形状，不声称安装位置/接口几何已确证。
- 外露浅色软管依可见轮廓连接软指附近与下方 STV/调压区域；蓝色调压器→STV 段及具体接头位置是示意级假设。STV 下端管路与拉环的位置参考可见照片，暗处真实三通、背面气路、固定/密封结构仍**未确认**。场景的曲线端点为视觉近似，不代表独立证明真实端口、气密连接或实际流向。
- 色彩、材质、段数和厚度仅用于区分软硅胶/织物/硬调压器，非材料测定；压力表不主张任何读数。

## 实际读图（模型直接读参考与 PNG）
- 读图途径：`computer_use capture(mode=vision)`，参考 `01_soft_robotics.jpg`、论文 Fig. 3 全图与 `overview_v01.png` 均已实际观看。v01 呈现两臂、深色主体、前部旋钮/表盘、沿主体弯曲的管线和下部拉柄，单张图可辨成套抓手而非孤立软指。
- 明显差距：原照片右软指更高且末端向中心收拢，v01 两指较对称、稍显刚硬；照片主体顶部口沿有不规则软包纹理，v01 是平直硬边；原图低部配件拥挤，v01 显得有条理但不够贴近真实。v01 整体位于灰背景中而非图版黑底；管线交汇/终端在遮挡处仍不能作为真实连接审查。**模型自查不等于用户验收。**

## 有限几何核查
- 在保存的 `.blend` 重新加载后检查：51 个 Blender 对象、主相机仍是 `v01 no-text overview`、FONT 0、850×1050 像素；四条声明为 pneumatic-route 的曲线各有 3–7 个控制点；左右软指底座分别位于 x=−0.75/+0.75。实际 PNG 视觉核对整套部件在画面内、未用文字/箭头替代器件。未核验隐藏端口、精确管路避障、软材物理形变、实物尺寸或压力计量；上述数字**不能证明视觉复刻成功**。

## 版本、复现与反馈
- 只保留 v01 首版低成本预览。初次 Blender 执行因 5.1 的材质节点创建、渲染引擎枚举差异失败，修正脚本后重新生成；没有伪造一个几何失败版本。待外部反馈时冻结 v01，写入具体纠错再出 v02；经验候选先限于本案例，不修改通用 Skill。
- 复现：`cd /Users/wht/Desktop/黑客松/agh-research-figure-skill/case-3_soft_robotics && /Applications/Blender.app/Contents/MacOS/Blender --background --python build_scene.py`。脚本会重写 v01 `.blend` 与 `.png`；复现前如有修订请改版本号另存。
- 文件 SHA-256 前 16 位（本次执行）：`build_scene.py` 4a6282df502ef1e0，`overview_v01.png` 296bc68b29860864，`soft_gripper_v01.blend` 297965256ae79d55。

## 真实 AGH 执行记录索引
- 会话 key：`6c3f530d-b445-4069-9d1a-ba958fed30ba`（用户 runtime context）；AGH 的 append-only 会话 ledger 为原始记录，本文件仅作事件索引，不伪造独立导出日志。
- 读取已安装 Skill：`skill_read` 调用；参考照片 `computer_use` Preview capture；论文 Fig.3b 与正文 `shell requests` 下载/读取、Fig.3 全图 Preview capture；补充 PDF 请求及 `fitz` 检索；`write` 建模脚本、`edit` 修复两处 Blender API 差异；`shell` 最终 Blender 保存并渲染；`computer_use` Preview capture 查看 PNG；`shell` 重新打开 `.blend` 完成有限核查。以上均在本次 AGH ledger 中可检索。无外部视觉反馈、无通用 Skill 更新。
