# 12 capillary_microfluidics — AGH v01 checkpoint

- Input: `../../inputs/12_capillary_microfluidics.png`, sha256 `3adb351624f594291c1afb820a64ae6e3f142dcc242a4dc434758c19a8185769`; Codex source acquisition/review, AGH not yet visual review.
- Target: Fig.1(b); DOI `10.1038/srep11102`; source https://www.nature.com/articles/srep11102/figures/1.
- Required scope: Reconstruct the entire b-panel experiment including the two pumps, transparent capillary sample region, microscope/camera, visible fluid tubes, waste vessel and computer. Sealed branch state follows caption; hidden fluid topology stays unknown.
- Stage: initialized; build/render/audit pending. No acceptance claimed.

- AGH first-stage: `build_v01.py` completed (Blender background exit 0), `scene_v01.blend` and `overview_v01.png` saved (1100×660); stdout/stderr `build_v01.log`. No source-vs-output visual acceptance asserted.

- AGH stage-2: static validator exit 3 UNKNOWN; reopened saved-scene auditor exit 3 UNVERIFIED (0 FAIL, 11 UNVERIFIED); PNG numeric review exit 0 NUMERIC_ONLY. Logs+JSON saved. Visual output comparison NOT done by AGH; paired image generated for Codex/user.

- R1 external actual-pixel reviewer Codex 2026-10-12: `../../CODEX_FEEDBACK_R1.md` per-case 12 verdict **requires revision**. Reviewer opened `../../codex-review/pair_12_v01.png`; this is external pixel evidence, not AGH self-review/user acceptance. v01 retained. v02 pending structural correction.

- AGH R1 build_v02.py executed via Blender 5.1.2 background, exit 0, saved scene_v02.blend / overview_v02.png (1120×690), log build_v02.log. v01 preserved. Geometry/file creation only, v02 pixels not externally reviewed.

- AGH v02 QA: source-derived components 10; validator UNKNOWN exit 3, reopened scene UNVERIFIED exit 3 (FAIL 0), PNG numeric NUMERIC_ONLY exit 0. Ports/routes/supports still unbound: no whole-scope QA success. Pair image generated; output pixel review by Codex pending. See V02_CHECKPOINT.md.
