# 20 thermoelectric_measurement — AGH v01 checkpoint

- Input: `../../inputs/20_thermoelectric_measurement.png`, sha256 `5df5525c7046e6fd1a19f347a8565bf5a504df01d8009f5e872b4ca317363d90`; Codex source acquisition/review, AGH not yet visual review.
- Target: Extended Data Fig.1(a); DOI `10.1038/s41563-020-00884-2`; source https://www.nature.com/articles/s41563-020-00884-2/figures/5.
- Required scope: Reconstruct the a-panel two copper blocks, grease contacts, bridging sample and electrodes, Peltier module and visible measurement wiring. Field/temperature arrows are annotations, not extra physical rods. Hidden power/measurement topology stays unknown.
- Stage: initialized; build/render/audit pending. No acceptance claimed.

- AGH first-stage: `build_v01.py` completed (Blender background exit 0), `scene_v01.blend` and `overview_v01.png` saved (1000×700); stdout/stderr `build_v01.log`. No source-vs-output visual acceptance asserted.

- AGH stage-2: static validator exit 3 UNKNOWN; reopened saved-scene auditor exit 3 UNVERIFIED (0 FAIL, 12 UNVERIFIED); PNG numeric review exit 0 NUMERIC_ONLY. Logs+JSON saved. Visual output comparison NOT done by AGH; paired image generated for Codex/user.

- R1 external actual-pixel reviewer Codex 2026-10-12: `../../CODEX_FEEDBACK_R1.md` per-case 20 verdict **requires revision**. Reviewer opened `../../codex-review/pair_20_v01.png`; this is external pixel evidence, not AGH self-review/user acceptance. v01 retained. v02 pending structural correction.

- AGH R1 build_v02.py executed via Blender 5.1.2 background, exit 0, saved scene_v02.blend / overview_v02.png (1020×720), log build_v02.log. v01 preserved. Geometry/file creation only, v02 pixels not externally reviewed.

- AGH v02 QA: source-derived components 7; validator UNKNOWN exit 3, reopened scene UNVERIFIED exit 3 (FAIL 0), PNG numeric NUMERIC_ONLY exit 0. Ports/routes/supports still unbound: no whole-scope QA success. Pair image generated; output pixel review by Codex pending. See V02_CHECKPOINT.md.

- R2 external reviewer: Codex actual v02 reference/output pixel comparison requires v03. See user R2 feedback, not AGH own pixel acceptance. v01/v02 retained; v03 build and route QA pending.

- AGH R2 v03 done: Blender build/render exit 0; static UNKNOWN(3); reopened-scene UNVERIFIED(3), zero recorded failures; PNG review NUMERIC_ONLY(0). Declared routes 0 / endpoint PASS 0; zero does not mean all routes absent. See V03_CHECKPOINT.md. Output pixels pending Codex.
