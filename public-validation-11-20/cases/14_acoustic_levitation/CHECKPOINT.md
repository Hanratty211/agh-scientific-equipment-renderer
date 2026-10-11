# 14 acoustic_levitation — AGH v01 checkpoint

- Input: `../../inputs/14_acoustic_levitation.png`, sha256 `0e12d2a8b3f27a55bbe917d22493dda65487aeaaa4c3b86013696989ec931ae8`; Codex source acquisition/review, AGH not yet visual review.
- Target: Fig.5(b); DOI `10.1038/s41598-019-53281-4`; source https://www.nature.com/articles/s41598-019-53281-4/figures/5.
- Required scope: Reconstruct the b-panel apparatus with opposed array and reflector, probe, camera/light and readout instruments. Draw sound/wavefront arrows only as explanatory layers if needed, not as physical rods.
- Stage: initialized; build/render/audit pending. No acceptance claimed.

- AGH first-stage: `build_v01.py` completed (Blender background exit 0), `scene_v01.blend` and `overview_v01.png` saved (1020×750); stdout/stderr `build_v01.log`. No source-vs-output visual acceptance asserted.

- AGH stage-2: static validator exit 3 UNKNOWN; reopened saved-scene auditor exit 3 UNVERIFIED (0 FAIL, 12 UNVERIFIED); PNG numeric review exit 0 NUMERIC_ONLY. Logs+JSON saved. Visual output comparison NOT done by AGH; paired image generated for Codex/user.

- R1 external actual-pixel reviewer Codex 2026-10-12: `../../CODEX_FEEDBACK_R1.md` per-case 14 verdict **requires revision**. Reviewer opened `../../codex-review/pair_14_v01.png`; this is external pixel evidence, not AGH self-review/user acceptance. v01 retained. v02 pending structural correction.

- AGH R1 build_v02.py executed via Blender 5.1.2 background, exit 0, saved scene_v02.blend / overview_v02.png (1120×800), log build_v02.log. v01 preserved. Geometry/file creation only, v02 pixels not externally reviewed.

- AGH v02 QA: source-derived components 9; validator UNKNOWN exit 3, reopened scene UNVERIFIED exit 3 (FAIL 0), PNG numeric NUMERIC_ONLY exit 0. Ports/routes/supports still unbound: no whole-scope QA success. Pair image generated; output pixel review by Codex pending. See V02_CHECKPOINT.md.
