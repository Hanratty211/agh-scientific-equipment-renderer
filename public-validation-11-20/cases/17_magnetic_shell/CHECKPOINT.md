# 17 magnetic_shell — AGH v01 checkpoint

- Input: `../../inputs/17_magnetic_shell.png`, sha256 `4b39a5df39dad8ebd9a4a690bb7664e52c86dabc88a67e728972444b0e2cde8d`; Codex source acquisition/review, AGH not yet visual review.
- Target: Fig.1(a); DOI `10.1038/s41467-021-22776-y`; source https://www.nature.com/articles/s41467-021-22776-y/figures/1.
- Required scope: Reconstruct the visible whole a-panel apparatus: paired coils/frame, centered shell/sample, syringe pump, pressure sensor, supply and visible tubes/supports. Do not substitute field plots or a generic two-ring cartoon for the photograph.
- Stage: initialized; build/render/audit pending. No acceptance claimed.

- AGH first-stage: `build_v01.py` completed (Blender background exit 0), `scene_v01.blend` and `overview_v01.png` saved (1100×700); stdout/stderr `build_v01.log`. No source-vs-output visual acceptance asserted.

- AGH stage-2: static validator exit 3 UNKNOWN; reopened saved-scene auditor exit 3 UNVERIFIED (0 FAIL, 10 UNVERIFIED); PNG numeric review exit 0 NUMERIC_ONLY. Logs+JSON saved. Visual output comparison NOT done by AGH; paired image generated for Codex/user.

- R1 external actual-pixel reviewer Codex 2026-10-12: `../../CODEX_FEEDBACK_R1.md` per-case 17 verdict **requires revision**. Reviewer opened `../../codex-review/pair_17_v01.png`; this is external pixel evidence, not AGH self-review/user acceptance. v01 retained. v02 pending structural correction.

- AGH R1 build_v02.py executed via Blender 5.1.2 background, exit 0, saved scene_v02.blend / overview_v02.png (1100×800), log build_v02.log. v01 preserved. Geometry/file creation only, v02 pixels not externally reviewed.

- AGH v02 QA: source-derived components 8; validator UNKNOWN exit 3, reopened scene UNVERIFIED exit 3 (FAIL 0), PNG numeric NUMERIC_ONLY exit 0. Ports/routes/supports still unbound: no whole-scope QA success. Pair image generated; output pixel review by Codex pending. See V02_CHECKPOINT.md.
