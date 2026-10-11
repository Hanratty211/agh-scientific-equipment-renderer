# 20 thermoelectric_measurement — AGH v01 checkpoint

- Input: `../../inputs/20_thermoelectric_measurement.png`, sha256 `5df5525c7046e6fd1a19f347a8565bf5a504df01d8009f5e872b4ca317363d90`; Codex source acquisition/review, AGH not yet visual review.
- Target: Extended Data Fig.1(a); DOI `10.1038/s41563-020-00884-2`; source https://www.nature.com/articles/s41563-020-00884-2/figures/5.
- Required scope: Reconstruct the a-panel two copper blocks, grease contacts, bridging sample and electrodes, Peltier module and visible measurement wiring. Field/temperature arrows are annotations, not extra physical rods. Hidden power/measurement topology stays unknown.
- Stage: initialized; build/render/audit pending. No acceptance claimed.

- AGH first-stage: `build_v01.py` completed (Blender background exit 0), `scene_v01.blend` and `overview_v01.png` saved (1000×700); stdout/stderr `build_v01.log`. No source-vs-output visual acceptance asserted.

- AGH stage-2: static validator exit 3 UNKNOWN; reopened saved-scene auditor exit 3 UNVERIFIED (0 FAIL, 12 UNVERIFIED); PNG numeric review exit 0 NUMERIC_ONLY. Logs+JSON saved. Visual output comparison NOT done by AGH; paired image generated for Codex/user.
