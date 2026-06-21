# tools/hoard.py — Riddle-Hoard authoring tool

One small, dependency-free script (stdlib only) for writing rooms. Its whole
reason to exist is to stay **neighbour-local**: it never scans the full grid, so
it costs the same whether the hoard has 90 rooms or 90,000. Do not `grep` every
room file to build name maps — use this instead.

Run everything from the repo root.

## The loop, one room at a time (never in batches)

Write rooms ONE AT A TIME: author a room, render it (which saves it and advances
the tracker), verify it, and ONLY THEN start the next. Saving and tracking each
room before the next is what makes the work safe to interrupt. "Write the next N
rooms" means repeat this loop N times — not author N at once. Per room:

```sh
# 1. What comes next, in writing order (closest-first, ties clockwise from N).
python3 tools/hoard.py next                # next N only PREVIEWS the order ahead

# 2. Briefing for that one room — reads ONLY its neighbours. Prints the name it
#    MUST take (what written neighbours already call it) and, per wall, the exact
#    answer to write: a written neighbour's name, an unwritten cell already fixed
#    by another room, or "NAME IT" + the quadrant for a free cell.
python3 tools/hoard.py plan                # the next room; or: plan -1:-5
python3 tools/hoard.py plan --schema       # print the render JSON schema

# 3. Author the ONE room as JSON (see schema) and render it. Writes
#    rooms/<x>/<y>.html, advances the LAST ROOM line in rooms-map.txt, and runs a
#    local crossword check. render takes ONE room and REJECTS a file with more.
python3 tools/hoard.py render room.json

# 4. Re-check that room + its neighbours (answers match neighbour names, facing
#    pairs agree both ways, answers distinct, four walls each).
python3 tools/hoard.py verify              # the frontier; or: verify -1:-5
```

Then go back to step 1 for the next room. Coords are `x:y` (e.g. `-1:-5`). The
grid is bounded -150..+150.

## Other commands

- `normalize <coords>` — re-render existing rooms in canonical form (fixes
  whitespace/entity drift). Does **not** touch the tracker. Note: hand-wrapped
  prose may re-flow; it is verified byte-identical to the hand-authored skeleton
  (title/`<meta>` use a raw `—`; prose wraps at width 98; body em-dashes are
  `&mdash;`).
- `render room.json --no-track` — re-render without moving the frontier (for
  fixing a single already-written room).

## render JSON schema

ONE room object (a one-element list is also accepted; a file with more than one
room is rejected). Hrefs, dir labels, input ids, the room skeleton, the noscript
links, em-dash encoding and prose wrapping are all computed for you — you only
supply content.

```json
{
  "x": -1, "y": -5,
  "name": "Berry",
  "desc": "one-line hook for the <meta description>.",
  "prose": "50-90 words, second person, present tense. Use - for em dashes.",
  "N": { "a": "acorn",   "lines": ["line 1", "line 2", "line 3", "line 4"] },
  "E": { "a": "sugar",   "lines": ["...", "..."] },
  "S": { "a": "honey",   "lines": ["...", "..."] },
  "W": { "a": "thistle", "lines": ["...", "..."] }
}
```

`"a"` is the neighbour's name (lowercase) = the answer that opens that wall;
`N/E/S/W` map to the top/right/bottom/left walls. A numeric `"a"` (e.g. `"7"`)
auto-sets `inputmode="numeric"`. The full doctrine (axes, difficulty bands,
the 2D-crossword rule, the corners) lives in `write.txt` (same folder).
```
