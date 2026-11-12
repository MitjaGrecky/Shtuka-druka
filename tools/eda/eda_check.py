#!/usr/bin/env python3
"""Check an EasyEDA Pro project against hardware/for-routing/<ID>/netlist.net, read-only, one command.

Usage:
  eda_check.py ID [--project NAME] [--netlist PATH] [--md OUT.md] [--keep DIR]

Needs: EasyEDA Pro with the run-api-gateway extension (Allow External Interaction ticked) and the
bridge from github.com/easyeda/easyeda-api-skill. If no bridge answers on 127.0.0.1:49620-49629,
the script starts `node <bridge>/scripts/bridge-server.mjs` (bridge folder: $EASYEDA_BRIDGE,
default ~/easyeda-api-skill) and waits for EasyEDA to connect.
Open the project in EasyEDA first. The script picks the newest extension connection that sees the
project's schematic and PCB tabs (old connections keep an old view and are skipped); if none does,
it opens both documents and asks you to press API Gateway -> Reconnect once, then run again.
It reads PCB pad nets, builds schematic nets geometrically and compares both with the netlist.
Nothing in the project is changed or saved.
License: AGPL-3.0-or-later.
"""
import argparse
import concurrent.futures as cf
import json
import os
import subprocess
import sys
import time
import urllib.request
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
sys.path.insert(0, str(HERE))
import netcompare  # noqa: E402


def http(url, body=None, timeout=10):
    req = urllib.request.Request(url, data=None if body is None else json.dumps(body).encode(),
                                 headers={"Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return json.loads(r.read().decode("utf-8"))
    except urllib.error.HTTPError as e:             # the bridge answers errors with a JSON body
        try:
            return json.loads(e.read().decode("utf-8"))
        except ValueError:
            raise e from None


def find_bridge():
    for port in range(49620, 49630):
        try:
            if http(f"http://127.0.0.1:{port}/health", timeout=1).get("service") == "easyeda-bridge":
                return f"http://127.0.0.1:{port}"
        except OSError:
            pass
    return None


def start_bridge():
    d = Path(os.environ.get("EASYEDA_BRIDGE", Path.home() / "easyeda-api-skill"))
    script = d / "scripts" / "bridge-server.mjs"
    if not script.exists():
        sys.exit(f"bridge not running and not found at {script}; set EASYEDA_BRIDGE")
    log = open(ROOT / "logs" / "eda_bridge.log", "a", encoding="utf-8") if (ROOT / "logs").is_dir() else subprocess.DEVNULL
    flags = getattr(subprocess, "CREATE_NEW_PROCESS_GROUP", 0) | getattr(subprocess, "DETACHED_PROCESS", 0)
    subprocess.Popen(["node", str(script)], cwd=d, stdout=log, stderr=log, creationflags=flags)
    print("bridge started, waiting for EasyEDA to connect (up to 60 s)...", flush=True)
    for _ in range(60):
        time.sleep(1)
        b = find_bridge()
        if b and http(f"{b}/health").get("edaConnected"):
            return b
    sys.exit("EasyEDA did not connect: check the extension (API Gateway -> Reconnect)")


def run(bridge, win, code, timeout=120):
    r = http(f"{bridge}/execute", {"code": code, "windowId": win}, timeout=timeout)
    if not r.get("success"):
        raise RuntimeError(r.get("error"))
    return r["result"]


def states(bridge):
    """What every extension connection sees, newest first. Old connections keep an old view of the
    editor (an extension instance does not see documents opened after it started), so only a
    connection that sees this project's schematic and PCB tabs can be trusted."""
    wins = [w["windowId"] for w in http(f"{bridge}/eda-windows")["windows"] if w["connected"]]
    code = (HERE / "js" / "state.js").read_text(encoding="utf-8")

    def ask(w):
        try:
            return w, run(bridge, w, code, timeout=8)
        except Exception:  # noqa: BLE001 - dead connection
            return w, None
    with cf.ThreadPoolExecutor(len(wins) or 1) as ex:
        return [x for x in reversed(list(ex.map(ask, wins))) if x[1]]


def live_connection(bridge, want):
    st = states(bridge)
    ok = lambda s: s and (want is None or s["project"] == want)  # noqa: E731
    for w, s in st:
        if ok(s) and s["sch"] and s["pcb"]:
            return w, s
    cand = [(w, s) for w, s in st if ok(s)]
    if not cand:
        sys.exit(f"no EasyEDA connection sees project {want or '(any)'}; seen: {[s['project'] for _, s in st]}. "
                 "Open the project in EasyEDA and run again.")
    w, s = cand[0]
    print(f"opening schematic and PCB of {s['project']} ...", flush=True)
    run(bridge, w, (HERE / "js" / "open_docs.js").read_text(encoding="utf-8"))
    for _ in range(12):           # a fresh connection may appear on its own
        time.sleep(5)
        for w2, s2 in states(bridge):
            if ok(s2) and s2["sch"] and s2["pcb"]:
                return w2, s2
    sys.exit("The documents are open, but no extension connection sees them yet. "
             "In EasyEDA: menu API Gateway -> Reconnect, then run this again.")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("id", help="board ID in hardware/for-routing/, e.g. M1")
    ap.add_argument("--project", help="EasyEDA project name to require, e.g. M1_v2")
    ap.add_argument("--netlist")
    ap.add_argument("--md")
    ap.add_argument("--keep", help="folder to save the raw pin -> net dumps (JSON)")
    a = ap.parse_args()
    netlist = Path(a.netlist or ROOT / "hardware" / "for-routing" / a.id / "netlist.net")
    if not netlist.exists():
        sys.exit(f"no netlist: {netlist}")
    bridge = find_bridge() or start_bridge()
    win, info = live_connection(bridge, a.project)
    js = lambda f: (HERE / "js" / f).read_text(encoding="utf-8")  # noqa: E731
    out =[f"### EasyEDA check: {a.id}, project `{info['project']}` (board `{info['board']}`)",
           f"Netlist: `{netlist.relative_to(ROOT) if netlist.is_relative_to(ROOT) else netlist}`", ""]
    for kind, f in (("PCB", "pcb_nets.js"), ("Schematic", "sch_nets.js")):
        res = run(bridge, win, js(f).replace("__PROJECT_UUID__", info["projectUuid"]), timeout=300)
        if "error" in res:
            out.append(f"**{kind}:** {res['error']}")
            continue
        if a.keep:
            Path(a.keep).mkdir(parents=True, exist_ok=True)
            Path(a.keep, f"{info['project']}_{kind.lower()}.json").write_text(json.dumps(res), encoding="utf-8")
        out.append(netcompare.report(kind, netcompare.compare(netlist, res["comps"])))
        if kind == "Schematic":
            pf = {k: v for k, v in res.get("flags", {}).items() if "PWR_FLAG" in k}
            out.append(f"- PWR_FLAG flags: {pf or 'none'}")
        out.append("")
    text = "\n".join(out)
    print(text)
    if a.md:
        Path(a.md).write_text(text + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
