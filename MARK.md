# MARK — story generation progress

Updated by Claude after each generation pass. Read this first when continuing the story.

## Structural overhaul: 2026-05-28

The story has been restructured from a branching-by-plot tree to an
**alignment-keyed grid**. Every level past level 1 has up to nine
nodes — one per D&D alignment — and routing is computed automatically
from choice deltas by [`assets/story.js`](assets/story.js). The old
letter-suffixed nodes (`1-a`, `1-b`, `2-a..2-f`, `3-a..3-i`) were
deleted; their prose was salvaged into the new alignment nodes.

See [`produce.txt`](produce.txt) for the rules and
[`nodes-map.txt`](nodes-map.txt) for the graph and reachability.

## Last node added

`2-ne` — 2026-05-28. Level 2 is partially populated: only the three
buckets reachable from L1 are written.

## Nodes that exist

- [`index.html`](index.html) — title page, links into `nodes/0-a.html`
- [`nodes/0-a.html`](nodes/0-a.html) — waking, name, gender (single node)
- [`nodes/1-m.html`](nodes/1-m.html) — male body, the man in the ditch
- [`nodes/1-f.html`](nodes/1-f.html) — female body, the man in the ditch
- [`nodes/2-lg.html`](nodes/2-lg.html) — Lawful Good: the kinsman lie, warden-house at noon
- [`nodes/2-cn.html`](nodes/2-cn.html) — Chaotic Neutral: the reeds, wardens' questions
- [`nodes/2-ne.html`](nodes/2-ne.html) — Neutral Evil: the silver in pocket, the open road

## L2 reachability

The L1 choice deltas land the player in exactly three of nine L2 buckets:

| L1 choice          | delta (law / good) | post-state   | bucket | L2 node |
| ------------------ | ------------------ | ------------ | ------ | ------- |
| help               | +2 / +2            | (2, 2)       | LG     | 2-lg    |
| hide               | -2 / +1            | (-2, 1)      | CN     | 2-cn    |
| rob                | -1 / -3            | (-1, -3)     | NE     | 2-ne    |

The other six L2 alignments (ng, cg, ln, tn, le, ce) are not
first-pass reachable. They are not yet written; they could be authored
later if a re-entry mechanism is added.

## Next to generate (Level 3, beat: "The stranger who reads you")

The L3 beat anchor: a single NPC in or near Sadaiziche encounters the
player and reads who they've become. Each alignment-node should
dramatise that beat through its grain.

### Reachability from L2

| L2 node | Choice A → bucket | Choice B → bucket | Choice C → bucket |
| ------- | ----------------- | ----------------- | ----------------- |
| 2-lg    | LG (+1/+1)        | NG (-3/+1)        | LE (0/-4)         |
| 2-cn    | TN (+3/-1)        | CG (-1/+2)        | CE (0/-3)         |
| 2-ne    | CE (-1/-1)        | TN (+2/+3)        | LE (+3/+1)        |

Reachable L3 buckets: **LG, NG, CG, TN, LE, CE** (6 of 9).
Vacant L3 buckets: **LN, CN, NE**.

### Suggested NPCs by alignment (for L3)

- `3-lg` — a road-warden's clerk at the south gate, by the book
- `3-ng` — a temple-nurse at a wayside infirmary, no questions asked
- `3-cg` — a Mardesran outrider, fugitive recognising fugitive
- `3-tn` — a wandering bard or pedlar, indifferent to your colour
- `3-le` — a slaver-broker outside the gate, business is business
- `3-ce` — a hangman or torture-priest, "you have come to the right person"

### Notes for writing L3

For each L3 node, **read every L2 node whose choices route into your
bucket**. Inbound edges:

- `3-lg`: 2-lg (A) — wounded man alive, you walking him to Sadaiziche
- `3-ng`: 2-lg (B) — wounded man alive, off-road south together
- `3-cg`: 2-cn (B) — wounded man hidden, wardens sent west on a false trail
- `3-tn`: 2-cn (A) — wounded man hauled out by wardens; OR 2-ne (B) — wounded man left dying in ditch, you off-road. Two very different physical states. Frame the opening so the alignment, not the physical detail, is the through-line.
- `3-le`: 2-lg (C) — recanted to wardens for reward; OR 2-ne (C) — pressed on to Sadaiziche to sell silver. Both end with you walking into the south-gate area as a transactor.
- `3-ce`: 2-cn (C) — fight on the road, knife at the youngest's throat; OR 2-ne (A) — turned back and killed the man with a stone. Both leave blood on your hands.

Pay particular attention to `3-tn`, `3-le`, `3-ce`: each has two
parents with very different physical lead-ins. The alignment is the
universal — write the scene so the player's moral state is the
through-line and the physical particulars settle into a single shared
present.

## Open setting notes

- World: **Coulesia** (Azgaar map under `map/`). Story is set in the
  **Khvordemian Empire** (state 3, Persian culture).
- Time of year: late autumn, year of the Black Sun.
- Geography: imperial road between **Rabad** (a small town, pop. ~6)
  and **Sadaiziche** (a larger town, pop. ~13.5). The player wakes
  ~½ farsang east of Rabad. Sadaiziche has a south gate (warden-house
  is there) and a west wall along a river with dye-houses.
- Religion: **Persian Church** (state-favoured monotheism, wardens
  ride under its writ — white shoulder-cord), **Old Vabumism** (folk
  polytheism, tolerated — Vabum the Cup-Bearer's roadside shrine),
  **Mardesran Schism** (heresy, persecuted — silver fish-eating-tail
  charm).
- The wardens: three. Leader is older, narrow-faced, "slow eyes." The
  third rider is silent, observant ("fine boots for a ditch"). The
  youngest is on his first body; his shaken composure is a recurring
  lever in the L2 nodes.
- The wounded man: a **Mardesran**. Calls the player *baraadar* /
  *khahar* (brother / sister). Uses **Khoda** for the god of the road
  — a deliberately old, pre-church word. In his exchanges he
  references a network: "they have fed us before," a shepherd above
  the second vineyard called Asha.
- The player's pre-amnesia identity: callused/working body; good
  Persian boots that "fit a little too well today and a little too
  loosely yesterday"; hidden wrist scar; foreign blood on a knuckle.
  Muscle memory revealed so far: a folded knife in the coat lining; a
  "cold practised thing" in the hands when violence offers; a steady,
  accustomed posture for warden-questioning; (female) a
  fingers-without-thought re-braiding under threat; the name
  *Daiyan* surfacing on the tongue in 2-lg's brazen lie without
  context.
- Items on the NE / rob-path: silver Mardesran fish-and-tail charm;
  wax-stoppered clay phial; folded vellum with three lines the player
  cannot read in dawn light; copper ring (no stone); whetstone; three
  additional small coins (now seven total).

## How to continue

Read [`produce.txt`](produce.txt) before writing new nodes. For each
new node, identify ALL parents at the previous level whose choices
route into your bucket, and read them all so your opening reads
naturally for any arrival.
