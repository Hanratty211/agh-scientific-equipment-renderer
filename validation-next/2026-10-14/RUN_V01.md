# v01 执行与视觉问题索引（AGH）

- 已加载 v1.0：本轮 `skill_read` revision `dd9d764...`。main 基线 `b350776`，在当前可访问稀疏 main 工作树 `validation-source-check` 执行；未触碰协作者分支。
- 首次运行 `build_cases.py 04_microfluidics v01`：`ModuleNotFoundError: render_core`，加脚本目录入 sys.path；二次运行 Blender 5.1.2 报 `BLENDER_EEVEE_NEXT` 不存在，改 `BLENDER_EEVEE`；三次成功保存 `cases/04_microfluidics/v01/scene.blend`。两次失败日志保留于 `cases_04_build.log` 与 `_retry.log`，均未生成有效场景。
- 独立 Blender 重载并渲染：`cases/04_microfluidics/v01/render.log` 返回 `RELOAD_RENDER_OK`；场景 SHA256 `18999ba90b2a7ce18cac3c6b4061aea55d2974fb4007416312d9224c60e1c293`，PNG SHA256 `e382f344bf06fdbe90113b0718b5633b7406bb63d54c04adb3ce20a4318ae186`，900×640，54 个物理对象。非功能/视觉证明。
- AGH 通过 macOS Preview 的 `computer_use.capture(mode=vision)` 真正读了 v01（本会话调用索引 3223）：相对 Fig.3C 的逻辑示意，输出呈现五条分散悬空线端/接头环（源码为五路），芯片孔口用浮空环而非真实透明芯片开孔，注射泵支架同质化；**严重身份/连接 FAIL**，不是验收。图上泵架右端部分靠画幅，必须修复连接/孔和总览比例；不应为十例赶进度宣称通过。
- 实际读原文目标来源见 `demo-assets/04_microfluidics/source/SOURCE.md`，来源裁错与修正保留。人工反馈：本轮未收到；外部模型：未委托。详细几何检查尚未进行。
