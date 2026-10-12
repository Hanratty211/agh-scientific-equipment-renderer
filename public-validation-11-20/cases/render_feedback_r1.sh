#!/bin/sh
# Supplementary views from SAVED final geometry; temporary cameras, no new .blend.
set -eu
cd /Users/wht/Desktop/黑客松/agh-research-figure-skill
B=/Applications/Blender.app/Contents/MacOS/Blender
H=public-validation-11-20/cases/render_hardware_details_v01.py
root=public-validation-11-20/cases
render(){ scene=$1; image=$2; shift 2; "$B" --background --python-exit-code 1 "$scene" --python "$H" -- "$image" "$@" > "${image%.png}.log" 2>&1; }
d=$root/12_capillary_microfluidics;s=$d/scene_v05.blend
render "$s" "$d/detail_both_feeds_v05.png" -1.85 0 1.45 0 -5.0 3.0 1100 680 4.9
render "$s" "$d/detail_upper_barrel_tip_v05.png" -2.73 0 2.42 -1.8 -2.5 3.0 840 640 1.25
render "$s" "$d/detail_lower_barrel_tip_v05.png" -2.73 0 .97 -1.8 -2.5 1.8 840 640 1.25
render "$s" "$d/detail_laptop_hinge_open_data_v05.png" 3.13 -.16 .54 4.1 -3.0 1.9 840 640 1.9
render "$s" "$d/detail_camera_to_laptop_path_v05.png" 1.55 .35 1.33 5.3 -6.0 3.1 1080 680 5.8
d=$root/14_acoustic_levitation;s=$d/scene_v06.blend
render "$s" "$d/detail_scope_amp_signal_v06.png" 2.83 -.09 .52 3.8 -2.8 1.52 900 650 2.2
render "$s" "$d/detail_laptop_hinge_open_data_v06.png" 4.43 -.10 .52 5.3 -2.9 1.8 840 640 1.8
render "$s" "$d/detail_mic_amp_scope_v06.png" 1.50 -.45 1.15 3.8 -5.2 3.2 1100 680 5.5
d=$root/17_magnetic_shell;s=$d/scene_v05.blend
render "$s" "$d/detail_pump_barrel_tip_v05.png" 2.56 .05 1.42 3.00 -2.5 2.23 840 640 1.5
render "$s" "$d/detail_pump_tube_fixture_v05.png" 1.43 0 1.30 3.3 -4.8 2.8 1000 640 4.2
