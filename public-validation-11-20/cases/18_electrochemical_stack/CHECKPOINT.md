# 18 electrochemical_stack — AGH v01 checkpoint

- Input: `../../inputs/18_electrochemical_stack.png`, sha256 `8fe9073f1d220f2e3f83bbd0e495d4c784d696cf8346f3f94cb80563014841a4`; Codex source acquisition/review, AGH not yet visual review.
- Target: Fig.6(c); DOI `10.1038/s41467-026-68436-x`; source https://www.nature.com/articles/s41467-026-68436-x/figures/6.
- Required scope: Reconstruct the ordered exploded stack and assembled four-cell stack shown in c. Consult caption for material/layer names and repeats; do not merge panels b cabinet or d tubing into the target. Exploded spacings are presentation choices, not working contact gaps.
- Stage: initialized; build/render/audit pending. No acceptance claimed.

- AGH first-stage: `build_v01.py` completed (Blender background exit 0), `scene_v01.blend` and `overview_v01.png` saved (1280×700); stdout/stderr `build_v01.log`. No source-vs-output visual acceptance asserted.

- AGH stage-2 independent re-open: first scene audit exit 2, `VERTICAL:c11` for assembled stack. Preserved `audit_scene_v01_initial.json/.log`; changed only overview camera scale/position in `build_v01.py`, rebuilt scene/PNG exit 0, independent audit now exit 3 UNVERIFIED with no recorded FAIL. Render not visually accepted.

- AGH stage-2: static validator exit 3 UNKNOWN; reopened saved-scene auditor exit 3 UNVERIFIED (0 FAIL, 15 UNVERIFIED); PNG numeric review exit 0 NUMERIC_ONLY. Logs+JSON saved. Visual output comparison NOT done by AGH; paired image generated for Codex/user.

- R1 external actual-pixel reviewer Codex 2026-10-12: `../../CODEX_FEEDBACK_R1.md` per-case 18 verdict **requires revision**. Reviewer opened `../../codex-review/pair_18_v01.png`; this is external pixel evidence, not AGH self-review/user acceptance. v01 retained. v02 pending structural correction.

- AGH R1 build_v02.py executed via Blender 5.1.2 background, exit 0, saved scene_v02.blend / overview_v02.png (1350×760), log build_v02.log. v01 preserved. Geometry/file creation only, v02 pixels not externally reviewed.

- AGH v02 QA: source-derived components 19; validator UNKNOWN exit 3, reopened scene UNVERIFIED exit 3 (FAIL 0), PNG numeric NUMERIC_ONLY exit 0. Ports/routes/supports still unbound: no whole-scope QA success. Pair image generated; output pixel review by Codex pending. See V02_CHECKPOINT.md.

- R2 external reviewer: Codex actual v02 reference/output pixel comparison requires v03. See user R2 feedback, not AGH own pixel acceptance. v01/v02 retained; v03 build and route QA pending.

- AGH R2 v03 done: Blender build/render exit 0; static UNKNOWN(3); reopened-scene UNVERIFIED(3), zero recorded failures; PNG review NUMERIC_ONLY(0). Declared routes 0 / endpoint PASS 0; zero does not mean all routes absent. See V03_CHECKPOINT.md. Output pixels pending Codex.

- R3 external actual-v03-pixel correction requires v04; scope limited to this case, v01/v02/v03 retained. Source feedback in ../../CODEX_FEEDBACK_R3.md; no user final acceptance.

- v04 initial independent center Y-ray probe exit 2: positions 12–14 FAIL relative to v03 OPEN classification because newly added contrasting panels intentionally occupy the center. Kept `mesh_audit_v04_initial.json/.log`. Do not remove intended panels for a false OPEN PASS. Need classification per v04 R3 design: perimeter aperture and contrasting central panel separately; old v03 checker is not a v04 schema.

- v04 new probe first exit 2 from checker bug: no `basic` mesh for four-bar OPEN layer returns None (no intersection evidence), wrongly compared only to False. Saved `mesh_audit_v04_probe_bug.json/.log`; condition corrected to accept no hit as empty OPEN for this one ray. Re-run exit 3 UNVERIFIED with 17/17 declared center-ray categories, NOT full geometry seal or identity verification. v03-old checker initial v04 mismatch preserved too.

- AGH v04 R3: case-local build/render exit 0, static UNKNOWN(3), reopened scene UNVERIFIED(3) FAIL 0, PNG NUMERIC_ONLY(0). Visible declared endpoint count 0/0; latest pixels pending Codex. See V04_CHECKPOINT.md.

- Codex R4 independent v04 full-pixel verdict requires revision: repeated positions12–14 inner faces obscured by preceding layers. Nine other cases frozen with limited external schematic-preview stage approval; only case18 v05 presentation repair permitted. Preserve v04 and source ambiguities.

- v05 first candidate FAILED independent camera ray sampling on actual saved exploded meshes: 12/13/14 each 0/9 sampled face-first hits, preceding layers occluded them. Retained `visibility_audit_v05_initial.json/.log`; build/renders of first candidate also kept in `build_v05_initial.*`/`overview_v05_initial.png`/`repeated_cell_detail_v05_initial.png`/`scene_v05_initial.blend` locally. Adjust presentation camera/spacing only; no tolerance inflation or false visual PASS.

- v05 second candidate X-stair display and shallower camera still FAILED saved-scene face-first sampled visibility 12/13/14 = 0/9; prior layer12/13 hit on later samples. Kept `visibility_audit_v05_stair.json`, `scene_v05_stair.blend`, `overview_v05_stair.png` and logs locally. Next: present module 12–14 in supplementary same-mesh face camera, and make overview show front face by reducing projection overlap, not asserting geometry-only success.

- v05 third display candidate wide X-stair (1.78 each) still independent face ray 0/9 all three; additionally saved-scene camera projection FAIL for positions16/17; preserved `visibility_audit_v05_widestair.json` and `audit_scene_v05_widestair.json` + binary scene locally. Investigate face ray depth/normals instead of claiming achieved visibility.

- AGH v05 final build exit0; static UNKNOWN(3), independent reopened scene audit UNVERIFIED(3) zero FAIL, numeric PNG helper NUMERIC_ONLY(0); 17/17 center layer categories and 12/13/14 face ray samples each 9/9 IN FRAME in saved scene, all probes overall UNVERIFIED(3). v05 actual pixels pending Codex. Earlier v05 initial/stair/widestair failed and audit history remains under versioned filenames, not silently overwritten. See V05_CHECKPOINT.md.

- Codex R5: v05 actual full PNGs judged locally improved 12–14 faces but whole scope regressed (1–11 occlusion, assembled projection wrong side, flat/empty overview, detail endplate). v05 not accepted; retain all intermediate/failure evidence. Next case18-only v06: restore v04 whole overview + same-geometry separate locally isolated supplementary views, no primary main-view hiding.

- R5 AGH case18-only v06: v04 full overview rendered pixel-identical RGB/RGBA; three isolated same-mesh supplements for 12/13/14, all other parts unhidden in saved main scene. First build import error preserved in log; rerun --python-exit-code1 build=0; record UNKNOWN(3), independent saved scene UNVERIFIED(3), 0 FAIL, saved 17 center-Y samples/0 hidden primary, numeric NUMERIC_ONLY(0). Actual v06 pixels pending Codex. See V06_CHECKPOINT.md.
