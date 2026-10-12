# 科研装置实物三维渲染 Skill 开发项目

## 最新交付（2026-10-12）

- [科研装置渲染 Skill v0.7](skills/agh-scientific-equipment-renderer/SKILL.md)
- [六例实物与接口修订 R4：图件、可编辑场景及审查索引](public-validation-11-20/GITHUB_DELIVERY_R4.md)

以下保留项目早期任务与案例记录；当前交付状态以以上索引及各轮检查点为准。

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
