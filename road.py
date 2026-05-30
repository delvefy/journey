#!/usr/bin/env python3
"""road.py — JSON bookkeeping helper for the "All the roads lead to" project.

This script owns ONLY the mechanical mutations of the JSON files described in
produce.txt. It does NOT do any historical reasoning: choosing the article
text, the neighbour shortlist, the fame ranking, and the next CANDIDATE are
all still yours. You pass the decisions in; the script applies them atomically
and prints a confirmation so you can verify each step.

Files are written exactly as the project expects: 2-space indent,
ensure_ascii=False (raw UTF-8, e.g. "Pedro Álvares Cabral"), trailing newline.

Commands
--------
  status [--seed SLUG]
      Re-read state.json (procedure step 1). Show the current seed, its next
      target, whether that target's article file already exists, the road's
      length and how far it is from the 1000 cap, and the current top counts.

  advance [--seed SLUG] --next "Name" slug [--incr slug ...] [--dry-run]
      Do procedure steps 2, 4, 8 and 9 in one atomic move, AFTER you have
      written the target's article file:
        * cap check: if the road already has 1000 entries, do NOT append;
          mark the seed complete, clear current_seed, and stop.
        * append the CURRENT target (state.seeds[seed].next_*) to counter.json
          with count=1, order=max(order)+1  (skipped if already present).
        * increment count by 1 for each --incr slug (must already be in MEM).
        * point state.seeds[seed].next_* at the new CANDIDATE (--next).
      Refuses to run unless articles/<seed>/<target-slug>.html exists, so you
      can never advance past an article you forgot to write.
      --dry-run prints what it would do and writes nothing.

  start-seed --name "Name" --slug slug
      The STARTING A NEW SEED flow: add to seeds.json, create the road folder
      and empty counter.json, set current_seed, seed the state entry.

  finish [--seed SLUG]
      Manually mark a road complete and clear current_seed (advance does this
      automatically at the 1000 cap; this is the manual escape hatch).
"""

import argparse
import json
import os
import sys

REPO = os.path.dirname(os.path.abspath(__file__))
STATE = os.path.join(REPO, "state.json")
SEEDS = os.path.join(REPO, "seeds.json")
ARTICLES = os.path.join(REPO, "articles")
CAP = 1000


def die(msg):
    print("ERROR: " + msg, file=sys.stderr)
    sys.exit(1)


def load_json(path):
    if not os.path.exists(path):
        die(f"missing file: {path}")
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def save_json(path, data):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
        f.write("\n")


def counter_path(seed):
    return os.path.join(ARTICLES, seed, "counter.json")


def article_path(seed, slug):
    return os.path.join(ARTICLES, seed, slug + ".html")


def resolve_seed(state, seed_arg):
    seed = seed_arg or state.get("current_seed")
    if not seed:
        die("no current_seed set; start a road with 'start-seed' first")
    if seed not in state.get("seeds", {}):
        die(f"seed '{seed}' not found in state.seeds")
    return seed


def cmd_status(args):
    state = load_json(STATE)
    cur = state.get("current_seed")
    print(f"current_seed: {cur}")
    seed = args.seed or cur
    if not seed:
        print("(no road in progress — pick a new seed)")
        return
    info = state["seeds"][seed]
    counter = load_json(counter_path(seed)) if os.path.exists(counter_path(seed)) else []
    nxt_name, nxt_slug = info.get("next_name"), info.get("next_slug")
    art = article_path(seed, nxt_slug) if nxt_slug else None
    print(f"\nroad: {seed}")
    print(f"  complete:   {info.get('complete')}")
    print(f"  length:     {len(counter)} / {CAP}  ({CAP - len(counter)} remaining)")
    print(f"  next target: {nxt_name}  [{nxt_slug}]")
    print(f"  article exists: {os.path.exists(art) if art else False}  ({art})")
    top = sorted(counter, key=lambda e: (-e.get("count", 0), e.get("order", 0)))[:8]
    if top:
        print("  top by count:")
        for e in top:
            print(f"    x{e.get('count'):>2}  #{e.get('order'):<4} {e.get('name')}")


def cmd_advance(args):
    state = load_json(STATE)
    seed = resolve_seed(state, args.seed)
    info = state["seeds"][seed]
    if info.get("complete"):
        die(f"road '{seed}' is already complete")

    cpath = counter_path(seed)
    counter = load_json(cpath)

    # --- cap check (procedure step 2) -------------------------------------
    if len(counter) >= CAP:
        print(f"road '{seed}' has reached the {CAP} cap — not appending.")
        if not args.dry_run:
            info["complete"] = True
            state["current_seed"] = None
            save_json(STATE, state)
            print("marked complete and cleared current_seed. Pick a new seed.")
        else:
            print("(dry-run) would mark complete and clear current_seed.")
        return

    target_name, target_slug = info["next_name"], info["next_slug"]
    cand_name, cand_slug = args.next

    # --- ordering guard: the article must already be written --------------
    art = article_path(seed, target_slug)
    if not os.path.exists(art):
        die(f"target article not found: {art}\n"
            f"       write {target_slug}.html before advancing.")

    by_slug = {e["slug"]: e for e in counter}

    # --- append target (procedure step 4) ---------------------------------
    appended = None
    if target_slug in by_slug:
        print(f"note: target '{target_slug}' already in counter — not appending.")
    else:
        order = max((e.get("order", 0) for e in counter), default=0) + 1
        entry = {"name": target_name, "slug": target_slug, "count": 1, "order": order}
        counter.append(entry)
        by_slug[target_slug] = entry
        appended = entry

    # --- increment in-MEM neighbours (procedure step 6) -------------------
    incr = args.incr or []
    if len(set(incr)) != len(incr):
        die(f"duplicate slug in --incr: {incr}")
    bumps = []
    for s in incr:
        if s == target_slug:
            die(f"cannot increment the target itself ('{s}')")
        if s not in by_slug:
            die(f"--incr slug '{s}' is not in MEM (counter.json) for road '{seed}'")
        before = by_slug[s]["count"]
        by_slug[s]["count"] = before + 1
        bumps.append((by_slug[s]["name"], s, before, before + 1))

    # --- candidate sanity -------------------------------------------------
    if cand_slug in by_slug:
        print(f"WARNING: candidate '{cand_slug}' is already in MEM — step 6 should "
              f"pick the first NOT-in-MEM neighbour. Double-check your ranking.")

    # --- report -----------------------------------------------------------
    print(f"\nroad '{seed}'  ({len(counter)} entries after this step)")
    if appended:
        print(f"  appended: #{appended['order']}  {appended['name']}  [{target_slug}]  count=1")
    if bumps:
        print("  incremented:")
        for name, s, b, a in bumps:
            print(f"    {b} -> {a}   {name}  [{s}]")
    else:
        print("  incremented: (none — suspicious in a dense cluster; re-check step 5/6)")
    print(f"  next target -> {cand_name}  [{cand_slug}]")

    if args.dry_run:
        print("\n(dry-run) nothing written.")
        return

    save_json(cpath, counter)
    info["next_name"], info["next_slug"] = cand_name, cand_slug
    save_json(STATE, state)
    print("\nwrote counter.json and state.json.")


def cmd_start_seed(args):
    name, slug = args.name, args.slug
    seeds = load_json(SEEDS)
    if not any(s.get("slug") == slug for s in seeds):
        seeds.append({"name": name, "slug": slug})
        save_json(SEEDS, seeds)
        print(f"added seed to seeds.json: {name} [{slug}]")
    else:
        print(f"seed '{slug}' already in seeds.json")

    folder = os.path.join(ARTICLES, slug)
    os.makedirs(folder, exist_ok=True)
    cpath = counter_path(slug)
    if not os.path.exists(cpath):
        save_json(cpath, [])
        print(f"created empty {cpath}")

    state = load_json(STATE)
    state["current_seed"] = slug
    state.setdefault("seeds", {})[slug] = {
        "next_name": name,
        "next_slug": slug,
        "complete": False,
    }
    save_json(STATE, state)
    print(f"current_seed -> {slug}; first target is the seed person ({name}).")


def cmd_finish(args):
    state = load_json(STATE)
    seed = resolve_seed(state, args.seed)
    state["seeds"][seed]["complete"] = True
    if state.get("current_seed") == seed:
        state["current_seed"] = None
    save_json(STATE, state)
    print(f"road '{seed}' marked complete; current_seed cleared.")


def main():
    p = argparse.ArgumentParser(description="JSON bookkeeping for the roads project.")
    sub = p.add_subparsers(dest="cmd", required=True)

    s = sub.add_parser("status", help="re-read state and report road progress")
    s.add_argument("--seed")
    s.set_defaults(func=cmd_status)

    a = sub.add_parser("advance", help="append target, increment neighbours, advance pointer")
    a.add_argument("--seed")
    a.add_argument("--next", nargs=2, metavar=("NAME", "SLUG"), required=True,
                   help="the new CANDIDATE the road moves to")
    a.add_argument("--incr", nargs="*", default=[], metavar="SLUG",
                   help="in-MEM neighbour slugs to increment (ranked above the candidate)")
    a.add_argument("--dry-run", action="store_true")
    a.set_defaults(func=cmd_advance)

    ns = sub.add_parser("start-seed", help="begin a new road")
    ns.add_argument("--name", required=True)
    ns.add_argument("--slug", required=True)
    ns.set_defaults(func=cmd_start_seed)

    f = sub.add_parser("finish", help="manually mark a road complete")
    f.add_argument("--seed")
    f.set_defaults(func=cmd_finish)

    args = p.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
