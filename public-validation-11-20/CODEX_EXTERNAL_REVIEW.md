# External review of ten new public-paper cases (11–20)

## Role and evidence separation

Codex selected/downloaded the ten source figures, inspected original pixels and the prepared target contact sheet, and sent `AGH_BATCH_PROMPT.md` to the existing AGH session on 2026-10-12 (Asia/Shanghai). AGH is responsible for its modeling, tool calls and execution checkpoints. This file records Codex's independent review; it is not an AGH execution ledger or user acceptance.

The selected DOIs are unique and differ from previous cases. Publisher titles, dates and captions are recorded in `targets.json`. Crossref independently matched nine DOIs; the printer DOI request failed with a network error, so its metadata is publisher-verified only. Raw articles/figures and output images stay local.

## Input review completed

Actual original and cropped image inspection was completed. Crops 13, 14 and 19 were tightened after the first target contact sheet exposed adjacent-panel fragments. The whole Fig.1 remains the optical input because the apparatus spans its edges; the upper-right microscale inset is explicitly excluded from reconstruction. Figure 1(c) in case 15 is an exploded state, as is Figure 6(c) in case 18.

**Source ambiguity:** the case-18 publisher caption assigns item 16 both to the silicone-gasket list and to the anode current collector; the visible figure also includes an item 15 that is not resolved by this caption. Record the conflicting numbering instead of confidently inventing identities. The figure itself is usable for layer order and assembled-stack appearance.

## External review method

For each delivered version, inspect reference and rendered pixels, then independently read the saved scene/record and relevant audits. Prioritize:

- Complete target scope and relative layout; distinguish diagram arrows/insets from physical hardware.
- Whole equipment appearance, orientation, proportion and real open holes/cavities/layers.
- Visible paths at genuine interfaces and the owner of each connection; do not infer concealed functional routing.
- Exploded vs assembled state; intentional layer separation does not require fabricated supports.
- Transparent layers and visible interior, lighting, framing, margins and local detail when necessary.
- Whether helpers report their actual coverage and limitations instead of claiming general correctness from PASS counts.

Per-case verdicts use **requires revision / limited external stage approval / not yet reviewed**. Approval concerns a schematic preview only; it is not user final acceptance, exact engineering geometry or proof that a device works. Repeated flaws and false QA claims are fed back to AGH with concrete observations. Failed versions are preserved.

## Output review

### R1 completed — all ten v01 references/output PNGs actually reviewed

The ten complete pairs were opened and inspected, not inferred from the contact-sheet existence. All ten require revision. Main failures: generic optical line instead of branched apparatus (11), missing readable fluid interfaces (12), missing photo-specific printer displays/gantry/cabling (13), wrong array/reflector relative placement (14), uniform toroids instead of patterned sensor internals (15), missing defining Vee shield/top dispenser (16), wrong coil axis and sphere instead of supported hemisphere (17), incorrect plate apertures/layer ordering and stack fasteners (18), missing reservoir/U tube/second instrument (19), changed thermal fixture geometry plus unsupported meter housings (20).

R1 feedback was sent directly to AGH; complete observations are in `CODEX_FEEDBACK_R1.md`. This is an external-model verdict, not user acceptance.

### Independent saved-scene probe

Blender independently reopened case 18 `scene_v01.blend`. The selected silicone-gasket mesh had world extents approximately (1.5, 0.7, 1.5), although the script supplied 0.06 as its intended thin y dimension. A center ray along y hit solid mesh while a center ray along z passed through: the aperture was oriented through the wrong axis. 192 of 384 mesh edges were nonmanifold. Raw measured result is `codex-review/probe_v01_stack_results.json`, produced by a Codex-authored read-only probe. This does not establish manufacturing validity or collision freedom.

All ten v01 AGH records declared zero ports/connections/supports; their UNKNOWN/UNVERIFIED reports correctly did not claim complete verification. They nevertheless did not exercise route/interface helpers on real visible connections. Subsequent iterations must address both visual flaws and meaningful supported route coverage.

### Git / subsequent iterations

AGH's first stage commit was `ea9b271c9d688488dd9c98e75b6efe9838aea9db`. Script/text/report artifacts were committed; source bitmaps/HTML and scenes stayed local. Ten v02 revisions are in progress; new outputs still await inspection.

### R2 completed — all ten v02 pixels reviewed

Opened the ten v02 pairs individually. V02 improves the apparatus silhouettes and main orientations, but none is externally closed yet. Targeted v03 feedback was sent directly to AGH from `CODEX_FEEDBACK_R2.md`. Repeated issues include the optical dichroic folding in the wrong plane, pump/waste or signal lines ending away from actual interfaces, floating printer displays/probes, a helix substituted for a flat spiral ribbon, and an unsupported horizontal Peltier base.

Independent Blender reopened the v02 optical scene. Its real dichroic face normal was approximately (0.7071, -0.7071, 0); reflecting incident (-1,0,0) produces approximately (0,-1,0), whereas this view requires (0,0,1). Direction error was 1.4142. Raw independent result is `codex-review/probe_v02_optics_results.json`. This is a geometry check, not proof of optical operation.

AGH v02's static/audit results remain UNKNOWN/UNVERIFIED, with no per-endpoint route bindings. Next iteration explicitly requests coverage of supported visible routes, separate from unknown hidden routes and exploded-state intentional gaps. V02 stage commit reported by AGH: `0096efacc15283e43044ae694466183868fb24ed`; independently comparing final Git state will follow the batch.

### R3 / R4 external follow-up

All ten v03 pairs were read. The three versions regenerated after endpoint repairs (12/17/19) were read again. Four v04 pairs were read individually, plus case18 full-resolution PNG. Latest mixed-version hashes are `codex-review/images_latest_hashes.json`.

Nine cases now receive **limited external schematic-preview stage approval**: 11/12/13/16/17/20 v03; 14/15/19 v04. This is not exact manufacturer appearance, complete hidden topology, user final acceptance or publication-grade replication. Case18 v04 still requires revision: repeated framed-module internals exist but are visually obscured by preceding layers. Targeted presentation repair requested in R4, not another whole-batch rebuild.

Independent rerun of all ten saved-scene audits had zero declared-check FAIL and overall UNVERIFIED for all ten. Six cases declared 43 ports and 22 connections in total; remaining four had zero routes, with photo/exploded/contact scopes and incomplete support coverage explicitly not covered. This result is not complete scientific validation. Raw independent reports, hashes and limits are in `codex-review/independent_audit_summary.json`.

### R5 / final v06 case18 actual review

V05 overview and detail were actually read. Its inner faces became visible (independent rays9/9 hit actual inner-panel/pattern geometry), but whole scope regressed: preceding layers overlapped and assembly moved to the left. V05 was rejected. The first independent probe had a MeshVertex.y API error, corrected to MeshVertex.co.y and explicitly rerun with --python-exit-code1; that failed attempt is not a PASS.

AGH then produced v06 by retaining the v04 complete overview and three separately isolated module12/13/14 closeups. Codex actually viewed all four final PNGs. These reach limited **multi-view** stage approval: internal faces readable only in supplemental views, not the whole overview. Independent mesh/transform/hide_render comparison matched173 physical objects and restored main camera; no missing/extra objects. Raw result is `codex-review/case18_restore_v06_results.json`. Final independent saved-scene audits still overall UNVERIFIED for all ten with zero declared-check FAIL.

All ten now have finite external schematic-preview stage judgments and known limitations. This coached selected-case validation is not a blind benchmark, user final acceptance, exact manufacturer CAD, measured physics, full route/support verification or universal generalization.
