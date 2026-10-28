# Submission checks / 提交检查

Checked on / 检查日期：**2026-10-28**

| Item / 项目 | Result / 结果 |
| --- | --- |
| Public repository / 公开仓库 | GitHub metadata reports `visibility: public`; default branch `main` / GitHub 元数据确认为 Public，默认分支 main |
| Default English README / 默认英文首页 | `README.md`; links to Chinese / 提供中文切换入口 |
| Chinese README / 中文首页 | `README.zh-CN.md`; links to English / 提供英文切换入口 |
| Required information / 必需内容 | Overview, demo link, architecture, integration contracts, environment and run commands in both languages / 两种语言均含项目介绍、视频链接、架构、集成规范、环境与运行方法 |
| License / 许可证 | MIT for original code, Skill and documentation; license also included in the standalone package / 原创代码、Skill 与文档采用 MIT，独立包包含许可证 |
| Attribution / 来源署名 | Third-party software, paper sources and music listed in `THIRD_PARTY_NOTICES.md` / 第三方软件、论文及音乐来源另列 |
| Acceptance runner tests / 验收执行器测试 | 10 existing tests passed / 现有 10 项测试通过 |
| Skill workflow checks / Skill 流程检查 | 13 existing checks passed / 现有 13 项检查通过 |
| Package checks / 包检查 | Structure, internal links, frontmatter and Blender synthetic behavior passed / 结构、包内链接、frontmatter 与 Blender 合成行为检查通过 |
| Optional plugin / 可选插件 | Existing Node.js test suite passed / 现有 Node.js 测试通过 |
| README run command / 首页运行命令 | Independently reopened the published microfluidics scene; 141/141 checks passed; scene unchanged / 独立重开已发布微流控场景，141/141 通过，场景未改动 |
| Credential scan / 凭据扫描 | 1,013 tracked text files scanned; no matches for the selected model/GitHub/AWS key and private-key patterns / 扫描 1,013 个受版本管理文本文件，选定模型、GitHub、AWS 密钥及私钥特征未命中 |

The credential scan covers current text snapshots, with sparse files read from identical Git blobs or verified matching local copies. It is a pattern check, not a guarantee about all secret formats, binary content or Git history. Local environment files, private keys and visual-review state are ignored by `.gitignore`.

凭据扫描针对当前文本快照；稀疏检出之外的文件使用相同 Git blob 或经 blob 哈希核对的本地副本。特征扫描不保证覆盖全部秘密格式、二进制内容或 Git 历史。`.gitignore` 忽略本地环境文件、私钥与视觉复核状态。

Historical research assets retain their own rights. Missing asset-level permissions are not resolved by adding MIT; see [third-party notices](../THIRD_PARTY_NOTICES.md). Existing case audits and results were preserved. This update did not run a new Agnes model-generation task or establish new image acceptance.

历史科研素材保留各自权利；添加 MIT 不补足缺失的素材级许可，见[第三方说明](../THIRD_PARTY_NOTICES.md)。既有案例审计和成果保留，本轮未发起新的 Agnes 模型生成任务，也未新增图像验收结论。
