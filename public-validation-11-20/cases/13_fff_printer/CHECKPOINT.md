# 13 fff_printer — AGH v01 checkpoint

- Input: `../../inputs/13_fff_printer.png`, sha256 `da2332cc9fae68ab58c2ce89a3710460bb4290c4e2697530b17565019a594a4e`; Codex source acquisition/review, AGH not yet visual review.
- Target: Fig.1(a); DOI `10.1038/s41598-025-17304-7`; source https://www.nature.com/articles/s41598-025-17304-7/figures/1.
- Required scope: Reconstruct the visible printer frame, gantry/head, bed, display/sensors and adjacent laptop. Scope is the photo a, not the printed channel in b. Hidden electronics and emission flow paths stay unknown.
- Stage: initialized; build/render/audit pending. No acceptance claimed.

- AGH first-stage: `build_v01.py` completed (Blender background exit 0), `scene_v01.blend` and `overview_v01.png` saved (1120×660); stdout/stderr `build_v01.log`. No source-vs-output visual acceptance asserted.

- AGH stage-2: static validator exit 3 UNKNOWN; reopened saved-scene auditor exit 3 UNVERIFIED (0 FAIL, 11 UNVERIFIED); PNG numeric review exit 0 NUMERIC_ONLY. Logs+JSON saved. Visual output comparison NOT done by AGH; paired image generated for Codex/user.

- R1 external actual-pixel reviewer Codex 2026-10-12: `../../CODEX_FEEDBACK_R1.md` per-case 13 verdict **requires revision**. Reviewer opened `../../codex-review/pair_13_v01.png`; this is external pixel evidence, not AGH self-review/user acceptance. v01 retained. v02 pending structural correction.

- AGH R1 build_v02.py executed via Blender 5.1.2 background, exit 0, saved scene_v02.blend / overview_v02.png (1130×690), log build_v02.log. v01 preserved. Geometry/file creation only, v02 pixels not externally reviewed.

- AGH v02 QA: source-derived components 7; validator UNKNOWN exit 3, reopened scene UNVERIFIED exit 3 (FAIL 0), PNG numeric NUMERIC_ONLY exit 0. Ports/routes/supports still unbound: no whole-scope QA success. Pair image generated; output pixel review by Codex pending. See V02_CHECKPOINT.md.

- R2 external reviewer: Codex actual v02 reference/output pixel comparison requires v03. See user R2 feedback, not AGH own pixel acceptance. v01/v02 retained; v03 build and route QA pending.

- AGH R2 v03 done: Blender build/render exit 0; static UNKNOWN(3); reopened-scene UNVERIFIED(3), zero recorded failures; PNG review NUMERIC_ONLY(0). Declared routes 0 / endpoint PASS 0; zero does not mean all routes absent. See V03_CHECKPOINT.md. Output pixels pending Codex.
