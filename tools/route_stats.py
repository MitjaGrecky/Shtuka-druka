#!/usr/bin/env python3
"""Routing statistics of a KiCad board through pcbnew (no kicad-cli): copper length (mm), vias, tracks, unrouted
connections (ratsnest edges left by the connectivity engine, zones filled first).   python route_stats.py BOARD.kicad_pcb
License: AGPL-3.0-or-later."""
import sys
import pcbnew

b = pcbnew.LoadBoard(sys.argv[1])
pcbnew.ZONE_FILLER(b).Fill(b.Zones())
b.BuildConnectivity()
tr = [t for t in b.GetTracks()]
vias = [t for t in tr if t.GetClass() == "PCB_VIA"]
seg = [t for t in tr if t.GetClass() == "PCB_TRACK"]
length = sum(t.GetLength() for t in seg) / 1e6
con = b.GetConnectivity()
unrouted = con.GetUnconnectedCount(False)
print(f"tracks={len(seg)} vias={len(vias)} length_mm={length:.1f} unrouted={unrouted}")
