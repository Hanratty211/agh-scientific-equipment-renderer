# 限定 R1 版本，待用户集中读图

**运行版本证据**：本轮 `skill_read` 实际加载 `agh-scientific-equipment-renderer` v0.7，resource `skill/user/user-agnes/9c1cae1d1c3aee1a971160ce46dd52ab10785e28ea8577da22cde9ef6a7d4bcf`，本轮读出的 revision `ed51c725de3dd1c46c151900fce32bbc9bd571b3a14c6d3ee1538e219accc48d`（不是上轮记录的旧 revision）；未更新或重装 Skill。执行了安装目录内 `scripts/validate_project_record.py` 和 `scripts/audit_saved_scene.py`，以及本仓库自写 `cases/check_feedback_r1_saved.py`。用户外部实际读图结论单独见 `PHYSICAL_FEEDBACK_R1.md`，此前12/14/17原始 .blend、PNG、失败检查文件保留。

**路径事故与真实执行**：最初四个新源码文件由 `write` 的相对路径误写至 `/Users/wht/Desktop/黑客松/agnes-harness/public-validation-11-20/cases`，首次三次 Blender 启动分别报源码不存在，日志已保留 `build_vXX_wrong_workspace_attempt.log`。核对原内容和 SHA-256 后通过 `mv` 将四个源码移到目标仓库 `/Users/wht/Desktop/黑客松/agh-research-figure-skill/public-validation-11-20/cases`；后续写/改均绝对路径、shell 均指定目标仓库 cwd。没有把误写内容当成目标仓库已执行的成果。

| 例 | 新保存版本、修正与边界 | 审核结果 |
|---|---|---|
|12|`cases/12_capillary_microfluidics/scene_v05.blend`、`overview_v05.png`、5 张局部图；v04 已补回的上/下供液线仍在。重新让真实 barrel 世界 X 轴与 collar/nozzle/tube 共轴；新 open annulus 位于原两根管入口。布尔切开笔电真实基座侧壁、移除实心挡板；Bezier 数据线避开屏幕。|静态 UNKNOWN；重开场景审计 UNVERIFIED、0 声明 FAIL；限定实网格链检查 22 项零 FAIL。先前旋转圆柱量测 bug、错误 owner 与未开孔的 FAIL 保留。|
|14|`cases/14_acoustic_levitation/scene_v06.blend`、`overview_v06.png`、3 张局部图；原图 Fig.5(b) 在 Preview 重新实际读到 microphone→amplifier(4)→oscilloscope(5) 与 camera(2)→computer(6)；**无 array→amplifier 线**。删除原图没有的 array→amp 路由/误标，array drive 留开放未知。示波器线落到代表性模拟 BNC 输入，不接显示屏，沿插头轴进入，三根可见线改连续 Bezier；笔电切开端口。|静态 UNKNOWN；重开场景审计 UNVERIFIED、0 声明 FAIL；限定实体/曲线 11 项零 FAIL。实际电缆型号、阵列供电未知；amp→scope 拓扑图示可见但商用接口身份仍未确认。|
|17|`cases/17_magnetic_shell/scene_v05.blend`、`overview_v05.png`、2 张泵局部图；从真实 barrel 朝向样品的 X 轴作用端面接 collar→金属喷嘴→环形出口→保留原样品端点的气动曲线；删旧独立代理球/接口，不动 sample→sensor 与框架。|静态 UNKNOWN；重开场景审计 UNVERIFIED、0 声明 FAIL；限定实网格链 9 项零 FAIL。内部流体/电路不能由近接推出。|

局部图片名称和全部 `.blend`、PNG 的 SHA-256 均在 `physical_feedback_r1_manifest.json`。辅助局部图由**重新打开保存场景后，临时相机**渲染；主镜头仍在保存的 `.blend` 中。`cases/render_feedback_r1.sh` 可重现。有限自动检查依据真实圆柱网格世界作用端面、环形出口、曲线端点、布尔开口射线及屏幕距离；不是功能/接触受力证明。

本轮未得到稳定的 `computer_use` 最终 PNG 窗口捕获，故不能声称 AGH 已逐像素目视通过。原稿、错误中间审计及实际读图者严格区分；**交用户集中审阅新整体和局部图，不称本轮用户认可**。商业 CAD、未知内部线路、全面遮挡和完整像素可读性仍 UNVERIFIED。
