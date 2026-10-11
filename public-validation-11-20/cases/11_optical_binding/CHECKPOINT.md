# 11 optical_binding — AGH v01 checkpoint

- Input: `../../inputs/11_optical_binding.png`, sha256 `ee50331c2fb26e4d7593f6dec095a3455ee759c857400b482b131f8e96ee4d24`; Codex source acquisition/review, AGH not yet visual review.
- Target: Fig.1 main optical apparatus; exclude the upper-right nanoparticle sample inset; DOI `10.1038/s41467-022-33070-w`; source https://www.nature.com/articles/s41467-022-33070-w/figures/1.
- Required scope: Reconstruct the main optical apparatus, its visible beam paths and component directions. The micro-scale sample inset is context, not additional macro hardware.
- Stage: initialized; build/render/audit pending. No acceptance claimed.

- AGH: initial Blender 5.1.2 attempt failed before scene save: generated material code assumed node name `Principled BSDF`, actual node lookup None; log preserved at `build_v01.log` (later successful run overwrote first log; failure evidence recorded here). Switched node type lookup; rerun saved blend and PNG. No visual inspection or QA yet.

- AGH first-stage: `build_v01.py` completed (Blender background exit 0), `scene_v01.blend` and `overview_v01.png` saved (960×690); stdout/stderr `build_v01.log`. No source-vs-output visual acceptance asserted.

- AGH stage-2: static validator exit 3 UNKNOWN; reopened saved-scene auditor exit 3 UNVERIFIED (0 FAIL, 11 UNVERIFIED); PNG numeric review exit 0 NUMERIC_ONLY. Logs+JSON saved. Visual output comparison NOT done by AGH; paired image generated for Codex/user.

- R1 external actual-pixel reviewer Codex 2026-10-12: `../../CODEX_FEEDBACK_R1.md` per-case 11 verdict **requires revision**. Reviewer opened `../../codex-review/pair_11_v01.png`; this is external pixel evidence, not AGH self-review/user acceptance. v01 retained. v02 pending structural correction.

- AGH R1 build_v02.py executed via Blender 5.1.2 background, exit 0, saved scene_v02.blend / overview_v02.png (950×800), log build_v02.log. v01 preserved. Geometry/file creation only, v02 pixels not externally reviewed.

- AGH v02 QA: source-derived components 14; validator UNKNOWN exit 3, reopened scene UNVERIFIED exit 3 (FAIL 0), PNG numeric NUMERIC_ONLY exit 0. Ports/routes/supports still unbound: no whole-scope QA success. Pair image generated; output pixel review by Codex pending. See V02_CHECKPOINT.md.
