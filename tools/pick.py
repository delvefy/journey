#!/usr/bin/env python3
# Helper: given a target cell and candidate words, report which are >=15 (D_MIN)
# from every same-name WRITTEN room and every same-name COMMIT. Reloads names.json
# each run so it tracks the live grid. Usage: pick.py X Y word1 word2 ...
import json, math, sys
d = json.load(open('tools/names.json'))
rooms, commits = d['rooms'], d['commits']
lex = set()
for ln in open('tools/approach-words.txt'):
    ln = ln.strip()
    if ln and not ln.startswith('#'): lex.add(ln)
tx, ty = int(sys.argv[1]), int(sys.argv[2])
cands = sys.argv[3:]
# name -> list of (x,y, kind)
locs = {}
for c, info in rooms.items():
    x, y = map(int, c.split(':')); locs.setdefault(info['name'], []).append((x, y, 'room'))
for c, info in commits.items():
    x, y = map(int, c.split(':')); locs.setdefault(info['name'], []).append((x, y, 'commit'))
for w in cands:
    near = []
    for (x, y, k) in locs.get(w, []):
        dist = math.hypot(x - tx, y - ty)
        if dist < 15: near.append(f"{k}@{x}:{y}={dist:.1f}")
    inlex = 'lex' if w in lex else 'NOT-IN-LEX'
    if near:
        print(f"  {w:12s} BLOCKED  ({inlex})  {', '.join(sorted(near))}")
    else:
        print(f"  {w:12s} SAFE     ({inlex})")
