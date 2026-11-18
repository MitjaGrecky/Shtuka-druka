import g3
B = g3.B
for gap in (1.0, 5.0, 10.0, 15.0, 20.0):
    B.FAN_SPEC.update(gap=gap)
    m, P, col, tight = g3.build(30, 0, 117.0, 20, 0)
    print(f"gap H5-fan {gap}: collisions {len(col)} {col[:3]}; tight {len(tight)} {tight[:2]}", flush=True)
