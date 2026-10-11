# 19 triboelectric_glass — AGH v01 checkpoint

- Input: `../../inputs/19_triboelectric_glass.png`, sha256 `4a209463299f7ba276257ca2044ae3b0caf1d78aaa9f385559821c0e4456fe6e`; Codex source acquisition/review, AGH not yet visual review.
- Target: Fig.2(g); DOI `10.1038/s41467-024-50872-2`; source https://www.nature.com/articles/s41467-024-50872-2/figures/2.
- Required scope: Reconstruct the g-panel tilted glass/drop delivery test and electrical readout instruments. Do not turn droplet time-series states e/f into simultaneous hardware or invent concealed electrode routes.
- Stage: initialized; build/render/audit pending. No acceptance claimed.

- AGH first-stage: `build_v01.py` completed (Blender background exit 0), `scene_v01.blend` and `overview_v01.png` saved (990×690); stdout/stderr `build_v01.log`. No source-vs-output visual acceptance asserted.

- AGH stage-2: static validator exit 3 UNKNOWN; reopened saved-scene auditor exit 3 UNVERIFIED (0 FAIL, 9 UNVERIFIED); PNG numeric review exit 0 NUMERIC_ONLY. Logs+JSON saved. Visual output comparison NOT done by AGH; paired image generated for Codex/user.

- R1 external actual-pixel reviewer Codex 2026-10-12: `../../CODEX_FEEDBACK_R1.md` per-case 19 verdict **requires revision**. Reviewer opened `../../codex-review/pair_19_v01.png`; this is external pixel evidence, not AGH self-review/user acceptance. v01 retained. v02 pending structural correction.

- AGH R1 build_v02.py executed via Blender 5.1.2 background, exit 0, saved scene_v02.blend / overview_v02.png (1070×800), log build_v02.log. v01 preserved. Geometry/file creation only, v02 pixels not externally reviewed.

- AGH v02 QA: source-derived components 7; validator UNKNOWN exit 3, reopened scene UNVERIFIED exit 3 (FAIL 0), PNG numeric NUMERIC_ONLY exit 0. Ports/routes/supports still unbound: no whole-scope QA success. Pair image generated; output pixel review by Codex pending. See V02_CHECKPOINT.md.

- R2 external reviewer: Codex actual v02 reference/output pixel comparison requires v03. See user R2 feedback, not AGH own pixel acceptance. v01/v02 retained; v03 build and route QA pending.

- AGH R2 v03 done: Blender build/render exit 0; static UNKNOWN(3); reopened-scene UNVERIFIED(3), zero recorded failures; PNG review NUMERIC_ONLY(0). Declared routes 2 / endpoint PASS 2; zero does not mean all routes absent. See V03_CHECKPOINT.md. Output pixels pending Codex.

- R3 external actual-v03-pixel correction requires v04; scope limited to this case, v01/v02/v03 retained. Source feedback in ../../CODEX_FEEDBACK_R3.md; no user final acceptance.

- AGH v04 first independent audit exit 2: four QA-only mesh anchors deliberately `hide_render=True`; current v0.6 auditor regards hidden port anchors as `PORT_RENDER FAIL` though their parent route/film is visible. Initial JSON/log retained as `audit_scene_v04_initial.*`. Do NOT show arbitrary gold blocks or widen tolerance merely for auditor. Rework QA anchor visibility via physically small black indicators / explicit limitation, re-audit saved scene.

- AGH v04 R3: case-local build/render exit 0, static UNKNOWN(3), reopened scene UNVERIFIED(3) FAIL 0, PNG NUMERIC_ONLY(0). Visible declared endpoint count 2/2; latest pixels pending Codex. See V04_CHECKPOINT.md.
