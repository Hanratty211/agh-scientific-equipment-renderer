"""Independent read-only probe of first physical pass; no geometry mutations.

Positive separation of evaluated world AABBs proves a gap; overlapping AABBs
do not prove contact. Units are illustrative scene units, not measured metres.
"""
import bpy
import json
from pathlib import Path

root = Path(__file__).resolve().parents[1]
cases = [
    ("12_capillary_microfluidics", "scene_v04.blend", [
        ("upper syringe pump mounted syringe barrel", "upper visible syringe tip"),
        ("lower syringe pump mounted syringe barrel", "lower visible syringe tip"),
    ]),
    ("17_magnetic_shell", "scene_v04.blend", [
        ("right syringe pump mounted syringe barrel", "red pump syringe interface"),
    ]),
]
results = []

def evaluated_bounds(obj):
    ev = obj.evaluated_get(bpy.context.evaluated_depsgraph_get())
    mesh = ev.to_mesh()
    try:
        pts = [ev.matrix_world @ v.co for v in mesh.vertices]
        return [[min(p[i] for p in pts), max(p[i] for p in pts)] for i in range(3)]
    finally:
        ev.to_mesh_clear()

for case, scene_name, pairs in cases:
    source = root / "cases" / case / scene_name
    bpy.ops.wm.open_mainfile(filepath=str(source))
    for barrel_name, tip_name in pairs:
        barrel = bpy.data.objects.get(barrel_name)
        tip = bpy.data.objects.get(tip_name)
        if not barrel or not tip:
            results.append({"case": case, "pair": [barrel_name, tip_name],
                            "status": "UNVERIFIED", "reason": "object missing"})
            continue
        ba, ta = evaluated_bounds(barrel), evaluated_bounds(tip)
        separation = [max(0.0, ba[i][0]-ta[i][1], ta[i][0]-ba[i][1]) for i in range(3)]
        axis_a = barrel.matrix_world.to_3x3().col[2].normalized()
        axis_b = tip.matrix_world.to_3x3().col[2].normalized()
        delta = tip.matrix_world.translation - barrel.matrix_world.translation
        lateral = (delta - axis_a * delta.dot(axis_a)).length
        results.append({"case": case, "scene": str(source), "pair": [barrel_name, tip_name],
                        "status": "GAP_PROVEN" if any(x > 1e-5 for x in separation) else "UNVERIFIED",
                        "evaluated_bounds": [ba, ta], "axis_separation_lower_bounds": separation,
                        "axis_parallel_abs_dot": abs(axis_a.dot(axis_b)),
                        "axis_lateral_offset": lateral,
                        "limits": "No physical-unit claim. AABB overlap alone never certifies connection."})

out = Path(__file__).with_name("probe_physical_syringe_chain_results.json")
out.write_text(json.dumps(results, ensure_ascii=False, indent=2) + "\n")
print(json.dumps(results, ensure_ascii=False))
