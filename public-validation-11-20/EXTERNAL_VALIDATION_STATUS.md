# Ten new public-paper validation — external latest-stage results

Reviewer: Codex, 2026-10-12 Asia/Shanghai. Sources and v01/v02/v03 were actually viewed; repaired v03 12/17/19 were re-read; latest v04 14/15/18/19 were read. Source selection, external judgments and independent probes are Codex work, not an AGH tool ledger. AGH modeling/execution checkpoints are separate.

**Result: all ten selected cases reached limited external schematic-preview stage approval after coached iterations; case18 is approved only as a whole overview plus three supplementary isolated detail views.** No user final acceptance, publication-quality similarity, CAD/manufacturing, device functionality or complete hidden routing is claimed. All automatic scene reports remain UNVERIFIED with zero declared-check FAIL. Six cases cover 43 ports / 22 declared visible connections. Four have no declared routes; those scopes do not gain interface verification from zero FAIL.

Each source has a different DOI and was not one of the earlier training cases. Publisher metadata was checked for all ten; Crossref independently matched nine, while case13 Crossref returned a network error. Details are in [source ledger](SOURCE_LEDGER.md) and `metadata_verification.json`.

| ID | Public paper / target | Latest | External result | Ports / routes | Actual PNG SHA-256 |
|---|---|---|---|---|---|
| 11 | [The primeval optical evolving matter by optical binding inside and outside the photon beam](https://www.nature.com/articles/s41467-022-33070-w) / Fig.1 main optical apparatus; exclude the upper-right nanoparticle sample inset | v03 | Limited stage approval | 20 / 10 | `a1122732071a7a30` |
| 12 | [Tip-multi-breaking in Capillary Microfluidic Devices](https://www.nature.com/articles/srep11102) / Fig.1(b) | v03 | Limited stage approval | 6 / 3 | `141b78e122231c43` |
| 13 | [Multi-objective optimization of surface finish and VOC emissions in FFF 3D printing using ANN–NSGA-II approach](https://www.nature.com/articles/s41598-025-17304-7) / Fig.1(a) | v03 | Limited stage approval | 0 / 0 | `8386351f067b88ce` |
| 14 | [Acoustic Manipulation of Droplets under Reduced Gravity](https://www.nature.com/articles/s41598-019-53281-4) / Fig.5(b) | v04 | Limited stage approval | 6 / 3 | `d9b0328d10931104` |
| 15 | [Sensing of joint and spinal bending or stretching via a retractable and wearable badge reel](https://www.nature.com/articles/s41467-021-23207-8) / Fig.1(c), main left exploded assembly | v04 | Limited stage approval | 0 / 0 | `307f788bf15f384b` |
| 16 | [Electro-spinning of highly-aligned polyacrylonitrile nano-fibres with continuous spooling](https://www.nature.com/articles/s41598-021-99890-w) / Fig.1(b) | v03 | Limited stage approval | 4 / 2 | `8f1c2cda70e5a2ce` |
| 17 | [Magneto-active elastic shells with tunable buckling strength](https://www.nature.com/articles/s41467-021-22776-y) / Fig.1(a) | v03 | Limited stage approval | 3 / 2 | `337a7707941fba4f` |
| 18 | [A self-breathing electrode enabled by interface regulation and gradient wettability engineering for industrial H2O2 electrosynthesis](https://www.nature.com/articles/s41467-026-68436-x) / Fig.6(c) | v06 + three details | Limited multi-view stage approval | 0 / 0 | `82e3e36d5751b0ca3` |
| 19 | [Integrated triboelectric nanogenerator and radiative cooler for all-weather transparent glass surfaces](https://www.nature.com/articles/s41467-024-50872-2) / Fig.2(g) | v04 | Limited stage approval | 4 / 2 | `a9b7ef07afb4f4e8` |
| 20 | [Seebeck-driven transverse thermoelectric generation](https://www.nature.com/articles/s41563-020-00884-2) / Extended Data Fig.1(a) | v03 | Limited stage approval | 0 / 0 | `79a076e1bc8507bc` |

## Known limitations / remaining differences

- **11**: Beam profiles/upper illumination path and exact supports remain simplified; real dichroic normal independently checked, optical function unknown.
- **12**: Hidden capillary topology and the actual microscope mounting/seals unknown; feeds and waste endpoint surfaces sampled.
- **13**: Commercial component outlines, controls and wiring simplified; mounting is an illustrative visible bracket, not manufacturer CAD.
- **14**: Microphone pose/readability remains approximate; visible camera/amp leads checked, sound fields/function not validated.
- **15**: Rotor cup/hub detail, resin finish and electrode counts approximate; exploded gaps intentional; real flat ribbon extent checked.
- **16**: Needle/support and enclosure display approximate; DC leads checked only to drawn boundary; internal HV route/deposition unknown.
- **17**: Pneumatic interface geometry sampled; hidden pressure paths/load-bearing and exact stage/coil sizes unverified.
- **18**: Whole overview preserves ordered layer family and separate assembled stack; internal faces12–14 are confirmed only in three supplementary isolated views. They remain obscured in the overview. Colors, patterns and cell-module detail schematic; caption identity15/16 conflicting; hidden fluid route unknown.
- **19**: Reservoir/regulator and plate interfaces illustrative; glass signal endpoints checked; electronics and measured waveform unknown.
- **20**: Sample/grease/Cu/Peltier arrangement schematic; exact thermal contacts and function unknown; thin vertical Peltier extents checked.

## Independent evidence

- `codex-review/probe_v01_stack_results.json`: wrong aperture axis and nonmanifold gasket in rejected v01.
- `codex-review/probe_v02_optics_results.json`: wrong actual mirror fold plane in rejected v02.
- `codex-review/probe_v03_results.json`: corrected real mirror reflection (error 8.43e-8), true normal-Y gasket opening with manifold bars, planar spring z span, thin vertical Peltier. These are targeted geometric observations only.
- `codex-review/independent_audit_summary.json`: all ten saved scenes independently reopened; record/scene hashes, coverage and actual audit limitations retained.
- `CODEX_FEEDBACK_R1.md` through `CODEX_FEEDBACK_R4.md`: actual external feedback. R1–R5 sent directly to AGH; the earlier lock was resolved by the user.
- AGH execution: `AGH_BATCH_CHECKPOINT.md`, per-case `CHECKPOINT.md`, versioned build/record/audit files; failed audits retained by AGH and additionally sampled by Codex.

## Final case18 review after manual unlock

The user manually unlocked the Mac; R4 and R5 were delivered directly to AGH. V05 fixed local inner-face visibility but regressed the whole target: earlier layers overlapped and the assembled stack moved left. It was rejected after actual full-resolution PNG review, despite 9/9 sampled inner-face ray checks. AGH retained the failed versions.

V06 restores the v04 whole arrangement and delivers three actual isolated module12/13/14 views from the same geometry. Codex actually opened all four v06 PNGs; the colored inner faces and dark bars are readable in the supplementary views. Independent saved-scene comparison found all173 physical objects' mesh/transform/hide_render signatures and main camera restored, with no missing/extra physical objects. Latest saved-scene audit remains UNVERIFIED with zero declared-check FAIL. This is **limited multi-view structural demonstration**, not exact source reconstruction, user final acceptance, material identification, sealing or device operation.

The ten cases were selected and iteratively coached by external feedback. These final stages are not a blind benchmark, a first-attempt success rate, or evidence of universal Skill generalization. Skill update is the next authorized task; the installed runtime snapshot remains separate from local source/Git changes.

Raw publisher images, output PNGs, .blend scenes, logs and UI screenshots stay local. Only scoped lightweight scripts/JSON/MD reports are suitable for the existing private/main Git sync.
