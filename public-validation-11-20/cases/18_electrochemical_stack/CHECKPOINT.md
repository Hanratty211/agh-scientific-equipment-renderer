# 18 electrochemical_stack — AGH v01 checkpoint

- Input: `../../inputs/18_electrochemical_stack.png`, sha256 `8fe9073f1d220f2e3f83bbd0e495d4c784d696cf8346f3f94cb80563014841a4`; Codex source acquisition/review, AGH not yet visual review.
- Target: Fig.6(c); DOI `10.1038/s41467-026-68436-x`; source https://www.nature.com/articles/s41467-026-68436-x/figures/6.
- Required scope: Reconstruct the ordered exploded stack and assembled four-cell stack shown in c. Consult caption for material/layer names and repeats; do not merge panels b cabinet or d tubing into the target. Exploded spacings are presentation choices, not working contact gaps.
- Stage: initialized; build/render/audit pending. No acceptance claimed.

- AGH first-stage: `build_v01.py` completed (Blender background exit 0), `scene_v01.blend` and `overview_v01.png` saved (1280×700); stdout/stderr `build_v01.log`. No source-vs-output visual acceptance asserted.

- AGH stage-2 independent re-open: first scene audit exit 2, `VERTICAL:c11` for assembled stack. Preserved `audit_scene_v01_initial.json/.log`; changed only overview camera scale/position in `build_v01.py`, rebuilt scene/PNG exit 0, independent audit now exit 3 UNVERIFIED with no recorded FAIL. Render not visually accepted.

- AGH stage-2: static validator exit 3 UNKNOWN; reopened saved-scene auditor exit 3 UNVERIFIED (0 FAIL, 15 UNVERIFIED); PNG numeric review exit 0 NUMERIC_ONLY. Logs+JSON saved. Visual output comparison NOT done by AGH; paired image generated for Codex/user.
