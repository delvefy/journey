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

`3-ce` — 2026-05-28. Level 3 is fully populated for first-pass entry:
all six L3 buckets reachable from L2 are written.

## Nodes that exist

- [`index.html`](index.html) — title page, links into `nodes/0-a.html`
- [`nodes/0-a.html`](nodes/0-a.html) — waking, name, gender (single node)
- [`nodes/1-m.html`](nodes/1-m.html) — male body, the man in the ditch
- [`nodes/1-f.html`](nodes/1-f.html) — female body, the man in the ditch
- [`nodes/2-lg.html`](nodes/2-lg.html) — Lawful Good: the kinsman lie, warden-house at noon
- [`nodes/2-cn.html`](nodes/2-cn.html) — Chaotic Neutral: the reeds, wardens' questions
- [`nodes/2-ne.html`](nodes/2-ne.html) — Neutral Evil: the silver in pocket, the open road
- [`nodes/3-lg.html`](nodes/3-lg.html) — Lawful Good: the clerk's pen at the south gate
- [`nodes/3-ng.html`](nodes/3-ng.html) — Neutral Good: Mira's wayside Vabum shrine
- [`nodes/3-cg.html`](nodes/3-cg.html) — Chaotic Good: Behnam the Mardesran outrider down the ditch
- [`nodes/3-tn.html`](nodes/3-tn.html) — True Neutral: Razin the pedlar at a roadside fire
- [`nodes/3-le.html`](nodes/3-le.html) — Lawful Evil: Yusef the indenture-broker at the south gate
- [`nodes/3-ce.html`](nodes/3-ce.html) — Chaotic Evil: Mehrdad the question-priest at the crossroads

## L2 reachability

The L1 choice deltas land the player in exactly three of nine L2 buckets:

| L1 choice          | delta (law / good) | post-state   | bucket | L2 node |
| ------------------ | ------------------ | ------------ | ------ | ------- |
| help               | +2 / +2            | (2, 2)       | LG     | 2-lg    |
| hide               | -2 / +1            | (-2, 1)      | CN     | 2-cn    |
| rob                | -1 / -3            | (-1, -3)     | NE     | 2-ne    |

The other six L2 alignments (ng, cg, ln, tn, le, ce) are not
first-pass reachable.

## L3 reachability

The L2 choice deltas land the player in six of nine L3 buckets:

| L2 node | A → bucket   | B → bucket   | C → bucket   |
| ------- | ------------ | ------------ | ------------ |
| 2-lg    | LG (3-lg)    | NG (3-ng)    | LE (3-le)    |
| 2-cn    | TN (3-tn)    | CG (3-cg)    | CE (3-ce)    |
| 2-ne    | CE (3-ce)    | TN (3-tn)    | LE (3-le)    |

Reachable L3 buckets: **LG, NG, CG, TN, LE, CE** (6 of 9).
Vacant L3 buckets: **LN, CN, NE**.

Two L3 nodes have two parents:
- `3-tn` ← 2-cn (A) and 2-ne (B). Different physical lead-ins:
  cooperated-with-wardens (clean hands) vs. robbed-and-fled-south
  (carrying silver/phial/etc.). Opening kept deliberately vague — a
  drift-walk through autumn country to a wayside fire — and the
  pedlar reads ALIGNMENT, not items.
- `3-le` ← 2-lg (C) and 2-ne (C). Different physical lead-ins:
  recanted to wardens for reward (empty-handed) vs. fenced silver
  at the market (carrying contraband). Both converge at the unofficial
  market outside the south gate. The broker reads "transactor,"
  not contents of pocket.
- `3-ce` ← 2-cn (C) and 2-ne (A). Different physical lead-ins:
  killed (or fought) wardens on the road vs. went back and stoned the
  heretic. Opening converges on "off-road, blood on sleeves, walking
  through country" and arrives at a crossroads where Mehrdad waits.

## Next to generate (Level 4, beat: "The second man in the ditch")

The L4 beat anchor: a second moral test that echoes L1 — another
wounded man, another body, another road-decision — refracted through
who the player has now become. **All nine L4 buckets are first-pass
reachable** from L3, so this is the level where the grid finally
fills out.

### Reachability from L3

| L3 node | A → bucket | B → bucket | C → bucket |
| ------- | ---------- | ---------- | ---------- |
| 3-lg    | LG (+1/+1) | NG (-3/+1) | LN (0/-4)  |
| 3-ng    | LG (+3/0)  | CG (-1/+2) | CN (-2/-3) |
| 3-cg    | CG (-1/+1) | NG (+2/+1) | TN (+3/-3) |
| 3-tn    | LN (+2/+1) | NG (-2/+2) | NE (-1/-3) |
| 3-le    | LE (+2/-1) | TN (-1/+3) | NE (-1/-3) |
| 3-ce    | NE (+3/0)  | CN (-1/+3) | CE (0/-3)  |

Reachable L4 buckets: **LG, NG, CG, LN, TN, CN, LE, NE, CE** (9 of 9).

### Suggested situations by alignment (for L4)

The beat: another wounded man (or body, or trapped soul) on the road
ahead, in circumstances that test whether the player has hardened,
softened, or simply become other than they were.

- `4-lg` — a Church deacon set upon by bandits; the player can
  ride for help by the imperial road
- `4-ng` — a hidden person in need (a runaway, a beaten servant)
  who cannot be helped through any official channel
- `4-cg` — a Mardesran courier dying with a list of names that
  must reach a contact before dusk
- `4-ln` — a sworn-to-duty arrest in progress where the player is
  asked to assist by writ
- `4-tn` — a stranger on the road who is neither friend nor foe,
  and whose trouble is not the player's
- `4-cn` — a chained convoy passing on the road; whim and freedom
  pull two ways
- `4-le` — an official torture in a roadside post; the player is
  invited to participate or to walk past
- `4-ne` — a body on the verge with intact pockets and no witnesses
- `4-ce` — a dying victim of someone else's atrocity, and the
  perpetrator still on the road within reach

### Notes for writing L4

For each L4 node, **read every L3 node whose choices route into your
bucket**. Inbound edges:

- `4-lg`: 3-lg (A) — held the kinsman lie at the registry; OR 3-ng (A) — paid Mira coin and signed your name
- `4-ng`: 3-lg (B) — bolted with him through the dye-yard; OR 3-cg (B) — parted at the goat-track and walked east alone; OR 3-tn (B) — spoke the morning to Razin
- `4-cg`: 3-ng (B) — stayed and worked at the shrine; OR 3-cg (A) — went with Behnam to the coast
- `4-ln`: 3-lg (C) — recanted cleanly at the desk; OR 3-tn (A) — bought news from Razin cleanly
- `4-tn`: 3-cg (C) — took the cover and then took the horse; OR 3-le (B) — refused the broker's three doors
- `4-cn`: 3-ng (C) — robbed Mira; OR 3-ce (B) — refused Mehrdad and rode to warn the farmhouse
- `4-le`: 3-le (A) — took the Church's bounty door
- `4-ne`: 3-tn (C) — robbed the sleeping pedlar; OR 3-le (C) — took Mehri's door and walked the child to the ship; OR 3-ce (A) — apprenticed to the question
- `4-ce`: 3-ce (C) — killed Mehrdad at the crossroads

Several L4 nodes have multiple parents with markedly different
physical lead-ins. As with `3-tn` / `3-le` / `3-ce`, frame each
opening so the moral state is the through-line and the physical
particulars settle into a single shared present.

## Open setting notes

- World: **Coulesia** (Azgaar map under `map/`). Story is set in the
  **Khvordemian Empire** (state 3, Persian culture).
- Time of year: late autumn, year of the Black Sun.
- Geography: imperial road between **Rabad** (a small town, pop. ~6)
  and **Sadaiziche** (a larger town, pop. ~13.5). The player wakes
  ~½ farsang east of Rabad. Sadaiziche has a south gate (warden-house
  is there) and a west wall along a river with dye-houses. The
  unofficial market sits in a dust-strip outside the south gate.
- Religion: **Persian Church** (state-favoured monotheism, wardens
  ride under its writ — white shoulder-cord), **Old Vabumism** (folk
  polytheism, tolerated — Vabum the Cup-Bearer's roadside shrine),
  **Mardesran Schism** (heresy, persecuted — silver fish-eating-tail
  charm; the brand the empire puts on a Mardesran it has taken once
  and released is a small star-shaped scar at the temple).
- The wardens: three. Leader is older, narrow-faced, "slow eyes." The
  third rider is silent, observant ("fine boots for a ditch"). The
  youngest is on his first body.
- The wounded man: a **Mardesran**. Calls the player *baraadar* /
  *khahar* (brother / sister). Uses **Khoda** for the god of the road.
  In his exchanges he references a network: "they have fed us before,"
  a shepherd above the second vineyard called Asha.
- **Asha**: woman shepherd, white at the temple, wears a man's coat.
  Keeps a fire above the second vineyard. Sends travellers along to
  Mira's hospice at the elder-tree hollow (3-ng).
- **Mira**: old woman, keeps the Cup-Bearer's wayside shrine in the
  elder-tree hollow above the second vineyard. Folk-healer in the
  old way. Has a small grey cat and a brown mule.
- **Behnam** (3-cg): Mardesran outrider with a star-shaped brand at
  the temple. Came down from Asha's at first light to meet the
  brother who never arrived. Rides a small Persian horse with cloth-
  wrapped hooves.
- **Razin** (3-tn): old pedlar, fifteen years on the route between
  here and the coast. Carries a small two-stringed instrument in a
  leather case. Will not remember a traveller's face by morning.
- **Yusef** (3-le): indenture-broker at the south-gate market, by
  Persian Church licence. Settlements of seven years; arranges
  Church-bounty affidavits; quietly arranges Bardas's prison
  bodies and Mehri's child-to-ship contracts.
- **Mehrdad** (3-ce): Question-priest of the south-gate warden-house,
  appointed by the Church. Wears the brown-blood robe. Carries a
  small leather case of instruments and a heavier purse. Sent out
  this morning by the leader with the slow eyes. Riding next to a
  farmhouse half-farsang east of the L3 crossroads to question the
  brother's sister and child.
- The player's pre-amnesia identity: callused/working body; good
  Persian boots that "fit a little too well today and a little too
  loosely yesterday"; hidden wrist scar; foreign blood on a knuckle.
  Muscle memory revealed so far: a folded knife in the coat lining;
  a "cold practised thing" in the hands when violence offers; a
  steady, accustomed posture for warden-questioning; the names
  *Daiyan*, *Khorshid* surfacing on the tongue in the brazen lies
  without context; the cool calculation of "a fast walker invites
  questions."
- Items on the NE / rob-path: silver Mardesran fish-and-tail charm;
  wax-stoppered clay phial; folded vellum with three lines the player
  cannot read in dawn light; copper ring (no stone); whetstone; three
  additional small coins (now seven total).

## How to continue

Read [`produce.txt`](produce.txt) before writing new nodes. For each
new node, identify ALL parents at the previous level whose choices
route into your bucket, and read them all so your opening reads
naturally for any arrival.
