# 科研装置实物三维渲染 Skill 开发项目

## 规范独立 Skill 包（2026-10-14）

- **唯一规范源码**：[根目录 `agh-scientific-equipment-renderer/`](agh-scientific-equipment-renderer/README.md)；[入口](agh-scientific-equipment-renderer/SKILL.md) · [版本与安装状态边界](agh-scientific-equipment-renderer/PROVENANCE.md)。完整拷贝此目录即可读方法与运行合成测试；旧 `skills/agh-scientific-equipment-renderer/` 仅是 Git 历史，不是第二个安装源。
- [案例证据档案](validation-next/2026-10-14/skill-evidence/README.md)保留 v1.0/11–20 及新十例证据，与独立 Skill 分开；[十例验证工程](validation-next/2026-10-14/STAGE9_REVIEW_QUEUE.md)的 PNG/审阅者/未知状态保持原样。出版方 PDF、原图、含原图画布只本地，不发布。
- 之前 v1.0 运行时曾加载 revision `dd9d764…`；v1.1 从 main `a0b946b…` 发布源码，但同名受管更新返回 `SKILL_TARGET_CONFLICT`，**没有 v1.1 运行时加载证据**。安装需 AGH 合法受管流程解决冲突，不用复制/删旧安装绕过。
- 历史六例 R4 归档属于 v0.7 时代，其记录见 Git 历史和 `skill-evidence/` 的旧索引；此稀疏 main 工作树未检出该目录，不能误作当前规范 Skill 包或可用链接。

以下保留项目早期任务与案例记录；**以下旧交付属于历史时期**，当前 Skill 规范源以上述根目录为准。

## 任务目标（当前轮次）

根据已公开发表的科研材料（论文、图注、补充材料），制作**科研装置或系统的实物三维渲染图**：
- 图中能看见仪器、器件、安装结构及其空间关系
- 通过实际光路、线缆、管路或其他连接表达系统
- 用户能看出装置的实体形态、摆放和工作关系
- **三维渲染是主交付要求**

## 当前案例

**候选 C（第一案例）**：87Sr 光晶格钟 + 低温(77 K)腔 + 光晶格机械移动
- 论文：Middelmann et al., *Tackling the blackbody shift in a strontium optical lattice clock*, arXiv:1009.2017 (2010)
- 材料：正文详细描述（真空室、MOT 线圈、低温铜腔、平移台、光路），Fig. 7 布局图
- 炉子(480°C)/Zeeman slower 在正文有明确依据，可画

**候选 A（探索稿，功能流程图）**：¹⁷¹Yb 光晶格钟（PRL 2009, arXiv:0906.1219）
- 该论文无装置图/照片，仅支撑功能流程图，不支持实物三维渲染
- 探索稿保留在 case-1_spin12_yb_oac/，不作为主目标

## 文件布局

```
case-1_87sr_cryo_lattice/
  source-materials/   下载的 PDF/HTML/图（cand_C_bbrSr.pdf, fig7_layout_candC.png）
  render-output/      三维渲染 PNG + 可编辑场景(.blend) + 生成脚本
case-1_spin12_yb_oac/  探索稿（功能流程图，保留）
```

## 自检修正记录

- **2026-10-10 自检错误修正**：对 SVG 示意图序列步骤与图例的重叠判断，原记录称"最后步骤盒右缘 1050 < 图例左缘 1010"，
  此判断**错误**（1050 > 1010，实际重叠 40 px）。该图件为探索稿，此错误不影响主目标，但记录保留以纠正。

## 完成状态

- [x] 环境检查（Blender 5.1.2 可用，matplotlib/numpy 可用）
- [x] 候选论文检索与材料下载
- [ ] 候选 C 三维渲染初版
- [ ] 用户反馈迭代
