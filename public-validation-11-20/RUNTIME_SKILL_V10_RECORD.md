# agh-scientific-equipment-renderer v1.0｜受管安装与实际读取记录

本记录是 AGH 工具返回的执行摘要，不修改已安装 Skill 或源包；下列会话转达的外部操作不冒充 AGH 亲自执行。源码的安装前 `PROVENANCE.md` 保持原样，v0.7 的历史记录与备份保留。

## 源包与外部准备

- 仓库源包 commit：`e764812c23e189916487dd203dec83b2f3e0a2f5`；包路径：`runtime-packages/v1.0-e764812/agh-scientific-equipment-renderer`。用户会话转达：该干净包含 **22 个 Git 跟踪文件**、已去缓存，逐文件清单位于其上层 `PACKAGE_MANIFEST.json`；旧 v0.7 的 32 文件逐哈希备份位于 `runtime-backups/v07-before-v1.0-20261012/`。这些包清理、逐文件核验和旧备份均非本轮 AGH 亲自执行。
- 用户会话转达：人类明确同意“备份后替换为 v1.0”，管理页随后永久删除了**这一个**旧 v0.7，并经外部检查确认旧 target 不存在。删除及 target 检查非 AGH 执行；这也不是普遍删除其他旧安装的授权。
- AGH 首次只从指定干净包 `read` 核对 `SKILL.md` 标题 `科研装置三维渲染｜v1.0`，未据磁盘文件冒充运行时加载。

## 受管提案：失败史与成功安装状态

1. 首次 `skill_helper_import(kind=local, scope=user, enable=true)` 返回 prepared，22 文件，digest `16cfbe2e721d7014ba97a3ef899d74b7ede017cc23120a0f52da3cb813ed37eb`。提案 `skill-install-42edbe9e-a7e8-48d7-9382-143577c45955` 的 `commit` 返回 running/publish；随后 `status` 返回 **failed**, code `SKILL_TARGET_CONFLICT`, `retryable=false`，message「目标位置已有不同内容，请换目录名或通过现有管理流程处理，不会覆盖。」当时停止，没有覆盖/删除/绕过。
2. 在用户转达外部人类授权、管理页删除与核验后，AGH **另建** `skill-install-10d971fc-dc7d-47e3-8f96-f0391c34c1dc`：同一包正常 `skill_helper_import(kind=local, scope=user, enable=true)` 返回 prepared；`skill_helper_install(action=commit)` 返回 running/publish；`skill_helper_install(action=status)` 返回 **ready**, phase `complete`, `effective: next-turn`。返回的 `fileCount=22`、`scope=user`、digest `16cfbe2e721d7014ba97a3ef899d74b7ede017cc23120a0f52da3cb813ed37eb`、revision `dd9d764a3ec32396818499f03d5deea81121823bcda3dca07fc33dfb29597cde`。旧 failed 提案没有重复提交。ready 是安装状态，**不是**当轮 `skill_read` 已读正文。

## 后续实际入口读取（与 ready 分开）

- ready 后的下一轮发生一次 **TRANSPORT 失败**；该次没有可作为成功正文读取的证据，也没有重新安装。再下一次按用户要求仅调用 `tool_search(query=agh-scientific-equipment-renderer)`，返回 v1.0 描述和可用 Skill；随后的 `skill_read(name=agh-scientific-equipment-renderer)` 实际返回入口正文，标题 **`科研装置三维渲染｜v1.0`**，并包含 `[实物与接口方法](references/physical_equipment_and_interfaces.md)` 入口。
- 该次 `skill_read` 真实返回 `resourceId=skill/user/user-agnes/9c1cae1d1c3aee1a971160ce46dd52ab10785e28ea8577da22cde9ef6a7d4bcf`；`revision=dd9d764a3ec32396818499f03d5deea81121823bcda3dca07fc33dfb29597cde`。这证明本轮实际入口正文已可读取，不臆造工具未单列的 trust/desired/actual/winner 字段；未声称逐篇读完所有参考或验证制造/功能。
- 历史 v0.7 实际读取 revision `ed51c725de3dd1c46c151900fce32bbc9bd571b3a14c6d3ee1538e219accc48d` 及早先因 `__pycache__` 改变的漂移记录仍属旧快照历史，不能写为新包/当前入口版本；来源见原仓库检查点与安装前 Skill `PROVENANCE.md`。

除上述受管工具操作和 `tool_search`/`skill_read` 外，本记录不宣称 AGH 对安装目录进行过文件复制、删除、验证或脚本/图件执行；R4 独立像素审查继续保留其外部作者署名。
