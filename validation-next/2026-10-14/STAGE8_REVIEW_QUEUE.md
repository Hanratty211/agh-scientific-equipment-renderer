# Stage8 局部视觉复核队列｜新图未目视通过

第六轮**外部人工视觉复核**从磁盘真实看 13 v07、18 Fig18 v05，目视判词与旧局部数值分栏见 `EXTERNAL_HUMAN_REVIEW.md`。只更新：13 **同一 v07 场景**另出近景（没有另建/保存新 .blend），18 基于 v05 另建 v06。14 v05“支架/孔/目标”这一具体问题已解决，但整图、尺寸/悬浮方式及功能仍未验收。AGH GUI 仍 apps discovery failed。第七轮外部随后已实际读这两张图，见下方追加记录；此段保留 Stage8 出图时状态。

|目标|被审旧图→新图（自制）|自动证据/哈希|本地/自制比较|目视状态|
|---|---|---|---|---|
|13 Fig1a/c/g 远端局部|[v07 总览](cases/13_biomed_optics/v07/overview.png) → [**v07 同几何探头细节**](cases/13_biomed_optics/v07/detail_tip.png)|源场景 SHA `50892655bdc49af239bb0a24f21cabcc5c946ec55311881be23a51216fd69ffc` 重载前后不变；局部 PNG SHA `fed19e439095582c70c8aefc5df7176255dccfd3436711c2690b6b1fb8bb177f`；1200×840 正交新临时相机，无对象/材质变更|[纯自制前后同几何对比](demo-assets/13_biomed_optics/stage8_overview_detail_OWN.png)|外部已确认 v07 总览前窗双圈可辨、远端身份仍待核；**细节新图未读**，不能代替整机验收|
|18 Supp Fig18 左栏 20×20 mm 面 + 中栏压缩态|[v05 正交细波纹旧图](cases/18_mechanical_nature/v05_fig18_dense_weave/overview.png) → [**v06 宽厚交错候选**](cases/18_mechanical_nature/v06_fig18_broad_weave/overview.png) · [可编辑场景](cases/18_mechanical_nature/v06_fig18_broad_weave/scene.blend)|scene SHA `94369e5ac8acc5beb8718c3fae474c72f20b3037a716c343cae75b40f21c8f8e`；PNG SHA `308c91459259e9e135daabdef5de3a836dec7425346ada1d2d1165cde1244029`；[有限审计](cases/18_mechanical_nature/v06_fig18_broad_weave/target_audit.json) 6 项零 FAIL，只验曲线族/自动柄/压板保留|[纯自制旧—新](demo-assets/18_mechanical_nature/stage8_v05_v06_OWN.png)；本地含源图 `demo-assets/18_mechanical_nature/stage8_fig18_source_v05_v06_LOCAL.png` **不入 Git**|外部判 v05 细而过于规则；v06 **待外部读**。杆实际深度/交织节点、材料连接和力学未知|

04/02/08/14/15/16/17/20 均沿用既存图/版本，全部候选待整图验收；各自最新路径与来源见 `STAGE7_REVIEW_QUEUE.md`。18 Fig17 Type IV v02、Fig18 v03 正交、v04 结团、v05 细网均原样保留。纯自制比较图仅用于 demo；版权源图/PDF/含源比较画布只本地。

## 第七轮读图后的状态（旧队列历史保留）
13 细节图外部读到主缆—套环—锥头—同心端窗，局部候选保留，但不是整机/光学验收。18 v06 更粗更密却仍被明确指出**规则栅栏/短横杆**，视觉失败并由 Stage9 v07 替代；6 项有限数值零 FAIL 不可抵消目视。当前新图队列以 `STAGE9_REVIEW_QUEUE.md` 为准。
