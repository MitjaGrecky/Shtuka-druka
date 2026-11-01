#!/usr/bin/env python3
"""Build a Blender scene of the enclosure and everything inside it from fit_model.py,
mark the collisions in red and render preview pictures.

  python3 build_blend.py OUT_DIR [--render]

Needs the bpy module (pip install bpy==5.2.*) or run it inside Blender:
  blender -b -P build_blend.py -- OUT_DIR
Units: millimetres (scene unit scale 0.001). Collections: one per group of fit_model.py,
plus "Findings" with every part that collides or sits closer than 1 mm.
License: AGPL-3.0-or-later.
"""
import math
import os
import sys

import bpy  # noqa: I001  (bpy first: it provides bmesh)
import bmesh

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import fit_model as F  # noqa: E402

COLORS = {  # RGBA
    "shell": (0.78, 0.80, 0.84, 0.22), "pcb": (0.10, 0.42, 0.22, 1), "parts": (0.55, 0.55, 0.50, 0.35),
    "metal": (0.62, 0.64, 0.68, 1), "knob": (0.16, 0.16, 0.18, 1), "led": (1.0, 0.25, 0.85, 1),
    "chip": (0.05, 0.05, 0.06, 1), "plastic": (0.92, 0.92, 0.90, 1), "glass": (0.55, 0.75, 0.95, 0.30),
    "lcd": (0.03, 0.04, 0.06, 1), "battery": (0.15, 0.35, 0.80, 1), "grey": (0.5, 0.5, 0.5, 1),
    "issue": (0.95, 0.10, 0.08, 1), "tight": (1.0, 0.65, 0.0, 1),
}
GROUP_NAMES = {"shell": "Shell", "top": "Knobs on top", "panel": "Panel boards", "m1": "M1 screen knobs",
               "m1led": "M1 LEDs", "itx": "Mini-ITX", "front": "Front jacks", "screen": "Screen",
               "slope": "Slope boards", "rear": "Under the slope and rear wall"}


def material(key):
    name = "fit_" + key
    if name in bpy.data.materials:
        return bpy.data.materials[name]
    m = bpy.data.materials.new(name)
    rgba = COLORS[key]
    m.diffuse_color = rgba                     # viewport (Solid mode) colour
    try:
        m.use_nodes = True
    except AttributeError:
        pass
    bsdf = m.node_tree.nodes.get("Principled BSDF")
    if bsdf:
        bsdf.inputs["Base Color"].default_value = rgba
        bsdf.inputs["Alpha"].default_value = rgba[3]
        bsdf.inputs["Roughness"].default_value = 0.35 if key in ("metal", "glass") else 0.6
        if key == "metal":
            bsdf.inputs["Metallic"].default_value = 0.9
    if rgba[3] < 1:
        for attr, val in (("surface_render_method", "BLENDED"), ("blend_method", "BLEND")):
            try:
                setattr(m, attr, val)
                break
            except (AttributeError, TypeError):
                continue
    return m


def collection(name, parent=None):
    if name in bpy.data.collections:
        return bpy.data.collections[name]
    c = bpy.data.collections.new(name)
    (parent or bpy.context.scene.collection).children.link(c)
    return c


def make_mesh(name, shape):
    me = bpy.data.meshes.new(name)
    bm = bmesh.new()
    if shape == "cyl":
        bmesh.ops.create_cone(bm, cap_ends=True, segments=40, radius1=0.5, radius2=0.5, depth=1.0)
    else:
        bmesh.ops.create_cube(bm, size=1.0)
    bm.to_mesh(me)
    bm.free()
    return me


def profile_mesh(name, x0, x1):
    """Side wall in the true profile of the body (the collision check uses a box)."""
    pts = [(0, 0), (F.D, 0), (F.D, F.BACK_Z), (F.SHELF_Y, F.BACK_Z), (F.FOLD_Y, F.FOLD_Z), (0, F.TOP_Z)]
    me = bpy.data.meshes.new(name)
    bm = bmesh.new()
    vs0 = [bm.verts.new((x0, y, z)) for y, z in pts]
    vs1 = [bm.verts.new((x1, y, z)) for y, z in pts]
    bm.faces.new(vs0[::-1])
    bm.faces.new(vs1)
    n = len(pts)
    for i in range(n):
        bm.faces.new((vs0[i], vs0[(i + 1) % n], vs1[(i + 1) % n], vs1[i]))
    bm.to_mesh(me)
    bm.free()
    return me


def add_part(p, coll, mat_key=None):
    if p.name.startswith("Side "):
        x0 = 0 if "left" in p.name else F.W - F.SKIN
        ob = bpy.data.objects.new(p.name, profile_mesh(p.name, x0, x0 + F.SKIN))
        ob.data.materials.append(material(mat_key or p.color))
        coll.objects.link(ob)
        return ob
    ob = bpy.data.objects.new(p.name, make_mesh(p.name, p.shape))
    ob.location = p.c
    ob.scale = tuple(2 * v for v in p.h)
    ob.rotation_euler = (math.radians(p.rx), 0, 0)
    ob.data.materials.append(material(mat_key or p.color))
    ob["group"] = p.group
    ob["estimate"] = bool(p.est)
    if p.note:
        ob["note"] = p.note
    coll.objects.link(ob)
    return ob


def build(out_dir, render=False):
    bpy.ops.wm.read_factory_settings(use_empty=True)
    sc = bpy.context.scene
    sc.unit_settings.system = "METRIC"
    sc.unit_settings.scale_length = 0.001
    sc.unit_settings.length_unit = "MILLIMETERS"

    parts = F.parts()
    res = F.check(parts)
    bad = {}
    for g, a, b, est in res:
        for n in (a, b):
            if n not in bad or g < bad[n]:
                bad[n] = g
    root = collection("Shtuka Druka fit")
    objs = {}
    for p in parts:
        coll = collection(GROUP_NAMES.get(p.group, p.group), root)
        key = None
        if p.name in bad and p.group != "shell":
            key = "issue" if bad[p.name] < -0.05 else "tight"
        objs[p.name] = add_part(p, coll, key)
    fc = collection("Findings", root)
    for n in bad:
        if n in objs and objs[n].name not in fc.objects:
            fc.objects.link(objs[n])

    # report as a text block inside the .blend and next to it
    rep = F.report(parts, res)
    t = bpy.data.texts.new("fit_report.md")
    t.write(rep)
    open(os.path.join(out_dir, "fit_report.md"), "w").write(rep + "\n")

    # light and cameras
    sun = bpy.data.objects.new("Sun", bpy.data.lights.new("Sun", "SUN"))
    sun.data.energy = 3.0
    sun.rotation_euler = (math.radians(50), math.radians(10), math.radians(-35))
    root.objects.link(sun)
    cams = {}
    from mathutils import Vector
    target = Vector((F.W / 2, F.D / 2 - 10, 55))
    for name, loc, ortho in (("Cam iso", (-180, -380, 560), None), ("Cam side", (1200, F.D / 2, 75), 540),
                             ("Cam top", (F.W / 2, F.D / 2, 1500), 640)):
        cam = bpy.data.objects.new(name, bpy.data.cameras.new(name))
        cam.location = loc
        tgt = Vector((F.W / 2, F.D / 2, 75)) if ortho else target
        cam.rotation_euler = (tgt - Vector(loc)).to_track_quat("-Z", "Y").to_euler()
        cam.data.clip_end = 5000
        if ortho:
            cam.data.type = "ORTHO"
            cam.data.ortho_scale = ortho
        else:
            cam.data.lens = 32
        root.objects.link(cam)
        cams[name] = cam
    sc.camera = cams["Cam iso"]
    world = bpy.data.worlds.new("World")
    world.color = (0.93, 0.93, 0.92)
    sc.world = world
    path = os.path.join(out_dir, "shtuka_fit.blend")
    bpy.ops.wm.save_as_mainfile(filepath=path, compress=True)
    print("saved", path)
    print(rep)

    if render:
        sc.render.engine = "CYCLES"
        sc.cycles.device = "CPU"
        sc.cycles.samples = 24
        sc.render.resolution_x, sc.render.resolution_y = 1600, 1000
        sc.render.film_transparent = False
        try:
            sc.world.use_nodes = True
            bg = sc.world.node_tree.nodes.get("Background")
            bg.inputs[0].default_value = (0.93, 0.93, 0.92, 1)
            bg.inputs[1].default_value = 0.9
        except Exception:
            pass
        top = {o.name for o in bpy.data.collections[GROUP_NAMES["top"]].objects}
        skins = {"Top skin", "Slope skin", "Shelf", "Side left"}
        shots = (("fit_iso.png", "Cam iso", set()),
                 ("fit_iso_open.png", "Cam iso", skins | top),
                 ("fit_side_section.png", "Cam side", {"Side right"}))
        for fn, cam, hide in shots:
            for ob in bpy.data.objects:
                ob.hide_render = ob.name in hide
            sc.camera = cams[cam]
            sc.render.filepath = os.path.join(out_dir, fn)
            bpy.ops.render.render(write_still=True)
            print("rendered", fn)


if __name__ == "__main__":
    argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else sys.argv[1:]
    out = [a for a in argv if not a.startswith("--")]
    out_dir = os.path.abspath(out[0] if out else HERE)
    os.makedirs(out_dir, exist_ok=True)
    build(out_dir, render="--render" in argv)
