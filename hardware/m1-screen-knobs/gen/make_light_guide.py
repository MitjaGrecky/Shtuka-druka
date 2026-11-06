#!/usr/bin/env python3
"""Light guide for the M1 rings (R126): a black spacer between the board and the panel skin
with a hole over every LED, so each dot stays a dot. Print in black PETG or PLA, 0.2 mm layers.

  python3 make_light_guide.py OUT_DIR [--render]     (needs bpy: pip install bpy==5.2.*)

Writes m1_light_guide.stl (millimetres) and, with --render, a preview picture.
Sizes: the board top is 6.5 mm under the skin (encoder body height), the spacer is 6.4 mm.
License: CERN-OHL-S-2.0 (the part), AGPL-3.0-or-later (this script).
"""
import math
import os
import sys

import bpy  # noqa: I001  (bpy first: it provides bmesh)
import bmesh

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import design as D  # noqa: E402

T = 6.4             # thickness
LED_HOLE = 2.4      # diameter; LED 1.6 x 1.5, diagonal 2.2
ENC_CUT = (13.0, 14.2)   # encoder body 12 x 11.6 plus mounting tabs (+-6.6), with clearance
HOLE_M2 = 2.4
J1_POCKET = (11.5, 4.0, 2.0)   # header pins sticking out of the top side, pocket from below


def cube(bm, cx, cy, cz, sx, sy, sz):
    r = bmesh.ops.create_cube(bm, size=1.0)
    bmesh.ops.scale(bm, vec=(sx, sy, sz), verts=r["verts"])
    bmesh.ops.translate(bm, vec=(cx, cy, cz), verts=r["verts"])


def cyl(bm, cx, cy, d, h, z0=-1.0):
    r = bmesh.ops.create_cone(bm, cap_ends=True, segments=24, radius1=d / 2, radius2=d / 2, depth=h)
    bmesh.ops.translate(bm, vec=(cx, cy, z0 + h / 2), verts=r["verts"])


def obj(name, bm):
    me = bpy.data.meshes.new(name)
    bm.to_mesh(me)
    bm.free()
    ob = bpy.data.objects.new(name, me)
    bpy.context.scene.collection.objects.link(ob)
    return ob


def build(out_dir, render=False):
    bpy.ops.wm.read_factory_settings(use_empty=True)
    # board coordinates: x right, y down -> Blender y = -y
    bm = bmesh.new()
    cube(bm, D.W / 2, -D.H / 2, T / 2, D.W, D.H, T)
    plate = obj("M1 light guide", bm)

    bm = bmesh.new()
    for k in range(8):
        x, y = D.knob_xy(k)
        cube(bm, x, -y, T / 2, ENC_CUT[0], ENC_CUT[1], T + 2)
        for i in range(D.RING_N):
            lx, ly, _ = D.led_xy(k, i)
            cyl(bm, lx, -ly, LED_HOLE, T + 2)
    pl = D.placement()
    for h in range(len(D.HOLES)):
        x, y = pl[f"H{h + 1}"][:2]
        cyl(bm, x, -y, HOLE_M2, T + 2)
    x, y = pl["J1"][:2]
    cube(bm, x, -y, J1_POCKET[2] / 2 - 0.5, J1_POCKET[0], J1_POCKET[1], J1_POCKET[2] + 1)
    cutter = obj("cutter", bm)

    mod = plate.modifiers.new("cut", "BOOLEAN")
    mod.operation, mod.object, mod.solver = "DIFFERENCE", cutter, "EXACT"
    mod.use_self = True                 # cutter pieces overlap (J1 pocket and an LED hole)
    cutter.hide_set(True)
    bpy.context.view_layer.objects.active = plate
    plate.select_set(True)
    bpy.ops.object.modifier_apply(modifier=mod.name)
    me = plate.data
    bpy.data.objects.remove(cutter)

    stl = os.path.join(out_dir, "m1_light_guide.stl")
    plate.select_set(True)
    bpy.ops.wm.stl_export(filepath=stl, export_selected_objects=True, global_scale=1.0, apply_modifiers=True)
    print("ok", stl, len(me.polygons), "faces")

    if render:
        m = bpy.data.materials.new("black")
        m.diffuse_color = (0.04, 0.04, 0.045, 1)
        bsdf = m.node_tree.nodes.get("Principled BSDF")
        bsdf.inputs["Base Color"].default_value = (0.05, 0.05, 0.055, 1)
        bsdf.inputs["Roughness"].default_value = 0.7
        plate.data.materials.append(m)
        from mathutils import Vector
        cam = bpy.data.objects.new("cam", bpy.data.cameras.new("cam"))
        cam.location = (40, -95, 90)
        cam.rotation_euler = (Vector((95, -14, 0)) - cam.location).to_track_quat("-Z", "Y").to_euler()
        cam.data.lens = 40
        bpy.context.scene.collection.objects.link(cam)
        sun = bpy.data.objects.new("sun", bpy.data.lights.new("sun", "SUN"))
        sun.data.energy = 4
        sun.rotation_euler = (math.radians(40), 0, math.radians(30))
        bpy.context.scene.collection.objects.link(sun)
        sc = bpy.context.scene
        sc.camera = cam
        sc.world = bpy.data.worlds.new("w")
        sc.world.color = (0.9, 0.9, 0.88)
        sc.render.engine = "CYCLES"
        sc.cycles.samples = 24
        sc.render.resolution_x, sc.render.resolution_y = 1600, 800
        sc.render.filepath = os.path.join(out_dir, "m1_light_guide.png")
        bpy.ops.render.render(write_still=True)


if __name__ == "__main__":
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    out = os.path.abspath(args[0] if args else ".")
    os.makedirs(out, exist_ok=True)
    build(out, "--render" in sys.argv)
