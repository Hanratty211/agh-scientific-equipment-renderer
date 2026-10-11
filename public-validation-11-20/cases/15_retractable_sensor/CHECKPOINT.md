# 15 retractable_sensor — AGH v01 checkpoint

- Input: `../../inputs/15_retractable_sensor.png`, sha256 `cffb3896399a7f4abcf70748db6e33bb4be8d185ad50b549d1841d98fb76b57d`; Codex source acquisition/review, AGH not yet visual review.
- Target: Fig.1(c), main left exploded assembly; DOI `10.1038/s41467-021-23207-8`; source https://www.nature.com/articles/s41467-021-23207-8/figures/1.
- Required scope: Reconstruct only the main left exploded sensor assembly: lid, rotor, coil spring/rope, stator and visible electrode rings. Exploded layers are intentionally separated; do not invent supports joining them. Exclude human/application scenes, inset electrode/SEM/photos and legend graphics.
- Stage: initialized; build/render/audit pending. No acceptance claimed.

- AGH first-stage: `build_v01.py` completed (Blender background exit 0), `scene_v01.blend` and `overview_v01.png` saved (780×980); stdout/stderr `build_v01.log`. No source-vs-output visual acceptance asserted.

- AGH stage-2: static validator exit 3 UNKNOWN; reopened saved-scene auditor exit 3 UNVERIFIED (0 FAIL, 12 UNVERIFIED); PNG numeric review exit 0 NUMERIC_ONLY. Logs+JSON saved. Visual output comparison NOT done by AGH; paired image generated for Codex/user.

- R1 external actual-pixel reviewer Codex 2026-10-12: `../../CODEX_FEEDBACK_R1.md` per-case 15 verdict **requires revision**. Reviewer opened `../../codex-review/pair_15_v01.png`; this is external pixel evidence, not AGH self-review/user acceptance. v01 retained. v02 pending structural correction.

- AGH R1 build_v02.py executed via Blender 5.1.2 background, exit 0, saved scene_v02.blend / overview_v02.png (780×1050), log build_v02.log. v01 preserved. Geometry/file creation only, v02 pixels not externally reviewed.

- AGH v02 QA: source-derived components 7; validator UNKNOWN exit 3, reopened scene UNVERIFIED exit 3 (FAIL 0), PNG numeric NUMERIC_ONLY exit 0. Ports/routes/supports still unbound: no whole-scope QA success. Pair image generated; output pixel review by Codex pending. See V02_CHECKPOINT.md.
