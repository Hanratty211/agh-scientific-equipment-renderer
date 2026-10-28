# Licensing scope and third-party notices / 许可范围与第三方说明

## Original work / 原创部分

The root [MIT License](LICENSE) applies to original SciRender code, Skill instructions and documentation, including original Python tools and the optional review plugin. Existing copyright and license notices remain in force. It does not grant rights to third-party papers, figures, photographs, audio, logos or software. Generated `.blend` scenes, PNG renders and the composite demo video are outside this blanket code/documentation grant; consult their sources before redistribution. Public availability alone does not establish a reuse license.

根目录 [MIT 许可证](LICENSE)适用于研境原创代码、Skill 方法与文档，包括原创 Python 工具和可选复核插件；既有版权和许可声明继续保留。论文、图版、照片、音频、标志与第三方软件不在其重新授权范围内。生成的 `.blend` 场景、PNG 渲染与合成视频不纳入这项统一代码/文档授权，转载时应核对其来源。公开可访问不等于已授予使用许可。

## Software dependencies / 软件依赖

| Dependency / 依赖 | Use / 用途 | Upstream license / 上游许可与来源 |
| --- | --- | --- |
| [Agnes Harness](https://github.com/AgnesAI-Labs/agnes-harness) | Agent host / 智能体宿主 | [Apache-2.0](https://github.com/AgnesAI-Labs/agnes-harness/blob/main/LICENSE); used as an external host, not bundled here / 外部宿主，不随本仓库打包 |
| [Blender](https://www.blender.org/about/license/) | Modeling, rendering, Python API / 建模、渲染、Python API | GPL; see Blender's own license and API guidance / 具体版本与 API 使用说明以上游为准；本仓库不分发 Blender 二进制 |
| [Python](https://docs.python.org/3/license.html) | Standalone CLI helpers / 独立 CLI | PSF License; separate installation / 独立安装 |
| [PyYAML](https://github.com/yaml/pyyaml/blob/main/LICENSE) | YAML/frontmatter validation / YAML 校验 | MIT |
| [Pillow](https://github.com/python-pillow/Pillow/blob/main/LICENSE) | Image utilities / 图像辅助 | HPND and applicable component notices / HPND 及组件声明 |

The optional plugin retains its [local MIT license](integrations/agnes-visual-guard/LICENSE). Installing dependencies does not replace their licenses with SciRender's MIT license.

可选插件保留[目录内 MIT 许可证](integrations/agnes-visual-guard/LICENSE)。依赖的许可证不因安装本项目而改变。

## Research sources / 科研来源

These articles identify source evidence for illustrative reconstructions. Their authors do not endorse or validate SciRender's reconstructions. Figure-level credit lines and supplementary-material terms take precedence where applicable. License links below were checked against publisher article pages on **2026-10-28**.

以下论文是示意重建的来源依据，不表示原作者认可或验证研境成果。具体图版信用行与补充材料的许可说明适用时优先。下列许可已于 **2026-10-28** 对照出版方文章页核查。

| Source / 来源 | Project use / 本项目使用 | Publisher license / 出版方许可 |
| --- | --- | --- |
| Yan et al., *Magneto-active elastic shells with tunable buckling strength* (2021), [DOI: 10.1038/s41467-021-22776-y](https://www.nature.com/articles/s41467-021-22776-y) | Fig. 1a photograph cropped/resized in the demo; magnetic-shell illustration / 视频中的 Fig. 1a 实拍裁图与磁性壳体示意 | [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/) |
| Wareing et al., *Microscopy with microfluidics in microgravity using FlightScope* (2025), [DOI: 10.1038/s41526-025-00470-3](https://www.nature.com/articles/s41526-025-00470-3) | Fig. 3C and detail crops in the demo; microfluidic scene evidence / 视频中 Fig. 3C 及局部裁图、微流控场景依据 | [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/) |
| Aygül et al., *A framework for soft mechanism driven robots* (2025), [DOI: 10.1038/s41467-025-56025-3](https://www.nature.com/articles/s41467-025-56025-3) | Source for published gripping scenes / 已发布夹持场景的来源；本轮未新增该论文原图 | [CC BY-NC-ND 4.0](https://creativecommons.org/licenses/by-nc-nd/4.0/); outside the MIT grant / 不纳入 MIT 授权 |
| Gao et al., *Polymer-inspired mechanical metamaterials* (2026), [DOI: 10.1038/s41467-026-77199-4](https://www.nature.com/articles/s41467-026-77199-4) | Earlier mechanical scene shown in the demo; methods and supplementary-figure context / 视频中早期力学场景的方法及补充图依据 | [CC BY-NC-ND 4.0](https://creativecommons.org/licenses/by-nc-nd/4.0/); outside the MIT grant / 不纳入 MIT 授权 |

The demo's research figures are cropped/resized and placed beside project-generated reconstructions. Reconstructions include illustrative geometry, layout and material choices; they are not original experimental images. The third example is a structure-description demonstration informed by an existing case and supplementary figures, not a verified text-only generation experiment.

视频中的来源图经过裁剪、缩放，并与项目生成场景并排展示。重建包含示意几何、布局和材质选择，不是原始实验图像。第三类演示结合已有案例和补充图，不应称为经过验证的纯文字生成实验。

## Audio and software recordings / 音频与软件录屏

Music: 'Reverie' by Scott Buckley - released under CC-BY 4.0. www.scottbuckley.com.au

[Track source / 曲目来源](https://www.scottbuckley.com.au/library/reverie/) · [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/)

The production record notes excerpts, volume adjustment, speech ducking, fades and a repeated passage with a crossfade. Agnes and Blender UI recordings remain attributable to their respective projects. / 制作记录注明音乐经过截取、音量调整、旁白避让、淡入淡出和片段交叉淡化循环；Agnes 与 Blender 界面录屏归各自项目。

## Historical archive / 历史档案

Earlier tracked directories include research PDFs, source crops, comparison canvases and case records. This documentation update does not certify every historical asset's redistribution rights and does not rewrite Git history. Consult the [source ledger](public-validation-11-20/SOURCE_LEDGER.md), [later source index](validation-next/2026-10-14/SOURCES.md) and per-case records. Missing asset-level permissions remain unresolved; the root MIT grant must not be applied to them. Obtain the applicable permission or exclude the material before redistributing an archive.

较早的受版本管理目录包含论文 PDF、来源裁图、对照画布和案例记录。本轮文档完善不表示历史素材的逐项转载权均已核清，也不重写 Git 历史。请查阅[来源台账](public-validation-11-20/SOURCE_LEDGER.md)、[后续来源索引](validation-next/2026-10-14/SOURCES.md)和案例记录。缺少素材级授权的项目仍为待核，不得套用根目录 MIT；再分发档案前应取得适用许可或排除相关素材。
