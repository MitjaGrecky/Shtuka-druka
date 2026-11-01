# Fit check of the enclosure

Every board, module and big part of Shtuka Druka as a box (sizes from docs 27-30 and from
`hardware/*/gen/design.py`), checked pair by pair for collisions and gaps under 1 mm.

```
python3 fit_model.py                       # report only, no Blender needed
python3 build_blend.py OUT_DIR --render    # shtuka_fit.blend + fit_report.md + 3 pictures (pip install bpy==5.2.*)
blender -b -P build_blend.py -- OUT_DIR    # the same inside Blender
```

In the .blend: one collection per group, collisions in red, gaps under 1 mm in orange, all of them also in the
"Findings" collection. Parts marked `estimate` are guesses to replace with datasheet sizes.
Units are millimetres; x from the left side, y from the front edge, z from the floor.

License: AGPL-3.0-or-later (code), CERN-OHL-S-2.0 (data).
