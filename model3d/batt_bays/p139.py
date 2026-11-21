"""P139: two Ampul 40125140 blocks 145 x 130 x 14 (z 3..17) under P2 (deck and A1 unchanged): real check (m.check) of candidate pairs.
Pairs: y 6-136 + y 138-268 at x 112 / 150 / 187 (145 wide); rotated 130 x 145 pairs along x. g3 default packs removed. Log runs/p139.log."""
import itertools, os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.join(HERE, "..", "v8"))
import g3
m, P, col, tight = g3.build(30, 0, 117.0, 20, 0)
P0 = [p for p in P if not p.name.startswith("Battery") and not p.name.startswith("Battery block")]
def test(blocks, label):
    bs = [m.box(f"Blk{i}", "rear", x, x + w, y, y + d, 3.0, 17.0, color="battery", est=True) for i, (x, y, w, d) in enumerate(blocks)]
    res = m.check(P0 + bs)
    bad = sorted([(round(g, 1), a, b) for g, a, b, _ in res if g < 0.0 and ("Blk" in a + b)])
    print(label, "->", "CLEAR" if not bad else bad[:4], flush=True)
    return not bad
for x in (112, 150, 187):
    test([(x, 6, 145, 130), (x, 138, 145, 130)], f"A pair x{x} y6-136 + y138-268 (145x130)")
test([(112, 6, 145, 130)], "single x112 y6-136")
test([(112, 138, 145, 130)], "single x112 y138-268")
test([(112, 6, 130, 145), (244, 6, 130, 145)], "rotated pair along x 112-242 + 244-374 (overreach)")
print("done", flush=True)
