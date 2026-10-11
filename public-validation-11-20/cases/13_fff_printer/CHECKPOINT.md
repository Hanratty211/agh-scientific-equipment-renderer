# 13 fff_printer — AGH v01 checkpoint

- Input: `../../inputs/13_fff_printer.png`, sha256 `da2332cc9fae68ab58c2ce89a3710460bb4290c4e2697530b17565019a594a4e`; Codex source acquisition/review, AGH not yet visual review.
- Target: Fig.1(a); DOI `10.1038/s41598-025-17304-7`; source https://www.nature.com/articles/s41598-025-17304-7/figures/1.
- Required scope: Reconstruct the visible printer frame, gantry/head, bed, display/sensors and adjacent laptop. Scope is the photo a, not the printed channel in b. Hidden electronics and emission flow paths stay unknown.
- Stage: initialized; build/render/audit pending. No acceptance claimed.

- AGH first-stage: `build_v01.py` completed (Blender background exit 0), `scene_v01.blend` and `overview_v01.png` saved (1120×660); stdout/stderr `build_v01.log`. No source-vs-output visual acceptance asserted.

- AGH stage-2: static validator exit 3 UNKNOWN; reopened saved-scene auditor exit 3 UNVERIFIED (0 FAIL, 11 UNVERIFIED); PNG numeric review exit 0 NUMERIC_ONLY. Logs+JSON saved. Visual output comparison NOT done by AGH; paired image generated for Codex/user.
