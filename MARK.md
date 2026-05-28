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

`9-ce` — 2026-05-29. Level 9 is fully populated: all nine L9 buckets
are written. The grid stays full from L4 onward. Beat anchor for L9
is **What the room costs** — the morning (or evening) after the L8
threshold, the price of the L8 conversation arrives in a concrete
shape. A new fifth voice — drawn from the current generation rather
than from before the morning of the man in the ditch — comes to the
door with the first specific instance of that price. The player
makes the first act from the new authority, or refuses to act from
it. Across the nine nodes the price takes nine forms: Maziar at a
cell, Bahram at an inner door, a Mardesran forge with morning news
of the bishop's riding, the captain's map-table at dawn, a wayside
country bench, an unmarked country widow at her cistern, the iron
at the brazier of Bagh-e-Sang, the morning's first inland delivery
at Bardas's gate, the bowl's saddlebags on the eve of a new moon's
ride.

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
- [`nodes/4-lg.html`](nodes/4-lg.html) — Lawful Good: Father Asad waylaid at a wagon-stop east of Sadaiziche
- [`nodes/4-ng.html`](nodes/4-ng.html) — Neutral Good: a beaten bond-boy in a derelict stone byre
- [`nodes/4-cg.html`](nodes/4-cg.html) — Chaotic Good: a Mardesran courier and a list of six names
- [`nodes/4-ln.html`](nodes/4-ln.html) — Lawful Neutral: the brass-pin writ and Hamza of the river-quay
- [`nodes/4-tn.html`](nodes/4-tn.html) — True Neutral: a thrown trooper at the foot of a poplar
- [`nodes/4-cn.html`](nodes/4-cn.html) — Chaotic Neutral: a chained debt-convoy at a culvert
- [`nodes/4-le.html`](nodes/4-le.html) — Lawful Evil: Mehrdad's brick-floor post and a man on the table
- [`nodes/4-ne.html`](nodes/4-ne.html) — Neutral Evil: a stroke-felled traveller alone in long light
- [`nodes/4-ce.html`](nodes/4-ce.html) — Chaotic Evil: a burning farmstead and three bandits on the next ridge
- [`nodes/5-lg.html`](nodes/5-lg.html) — Lawful Good: Magistrate-Father Hossein reads your name at a bright table
- [`nodes/5-ng.html`](nodes/5-ng.html) — Neutral Good: Bahram the cooper at a wayside long table
- [`nodes/5-cg.html`](nodes/5-cg.html) — Chaotic Good: Maziar, a turned field-man, at the cold spring
- [`nodes/5-ln.html`](nodes/5-ln.html) — Lawful Neutral: Captain Faramarz arrives at the post with a folder
- [`nodes/5-tn.html`](nodes/5-tn.html) — True Neutral: Parvin the wash-woman speaks the name to a linen
- [`nodes/5-cn.html`](nodes/5-cn.html) — Chaotic Neutral: Roshanak at a country market behind a cloth-stall
- [`nodes/5-le.html`](nodes/5-le.html) — Lawful Evil: Father Karim's strong-box and the four-year column
- [`nodes/5-ne.html`](nodes/5-ne.html) — Neutral Evil: Cyrus at the fence's door with the brand at his temple
- [`nodes/5-ce.html`](nodes/5-ce.html) — Chaotic Evil: Behdad on the leader's stone in the hide-fire bowl
- [`nodes/6-lg.html`](nodes/6-lg.html) — Lawful Good: Sahar at the post door; a writ for the brick-floor post at Bagh-e-Sang
- [`nodes/6-ng.html`](nodes/6-ng.html) — Neutral Good: a struck boy in the verge-grass under poplars; a soldier's grey mare bridle-down
- [`nodes/6-cg.html`](nodes/6-cg.html) — Chaotic Good: a switchback path down to a network boat; a man with the same knife-fold on the path behind
- [`nodes/6-ln.html`](nodes/6-ln.html) — Lawful Neutral: the warden-post's six writs; the empty column at the head of the daybook
- [`nodes/6-tn.html`](nodes/6-tn.html) — True Neutral: Hassan of Behbahan on the bench opposite at a brown-river ferry
- [`nodes/6-cn.html`](nodes/6-cn.html) — Chaotic Neutral: a Mira's runner at a propped rooflight; three at the front of the dyer's shop
- [`nodes/6-le.html`](nodes/6-le.html) — Lawful Evil: Behshad on the table at Bagh-e-Sang; the iron, the case-file, the third name
- [`nodes/6-ne.html`](nodes/6-ne.html) — Neutral Evil: a fence's man at Karkand reading your cuff; Bardas's runner two bells west
- [`nodes/6-ce.html`](nodes/6-ce.html) — Chaotic Evil: eight riders on a spur above Farzad's almond-orchards; the leader asks you to speak
- [`nodes/7-lg.html`](nodes/7-lg.html) — Lawful Good: Hossein on the doorstep at sundown with a Khaboran red-cord packet of three writs
- [`nodes/7-ng.html`](nodes/7-ng.html) — Neutral Good: Manuchehr of Sayyaf at the country house gate, the grey mare at the rein
- [`nodes/7-cg.html`](nodes/7-cg.html) — Chaotic Good: a coast-warden's cutter in the lee of the next headland, eight crew, the brass piece at the bow
- [`nodes/7-ln.html`](nodes/7-ln.html) — Lawful Neutral: a Khaboran post-runner at sundown with the order's wax at the centre of the desk
- [`nodes/7-tn.html`](nodes/7-tn.html) — True Neutral: a Khaboran circuit-clerk at the walnut inn's chimney-table with a description-sheet
- [`nodes/7-cn.html`](nodes/7-cn.html) — Chaotic Neutral: a country wash-woman at the stream-bend with talk of two horsemen and three offices
- [`nodes/7-le.html`](nodes/7-le.html) — Lawful Evil: the Sadaiziche bishop's green-linen folder on the brick-floor post's morning table
- [`nodes/7-ne.html`](nodes/7-ne.html) — Neutral Evil: an ox-cart at the salt-line with the Karkand fence's man canvas-wrapped in the back
- [`nodes/7-ce.html`](nodes/7-ce.html) — Chaotic Evil: an imperial riding of twenty, Khaboran red cord at the lead, on the coast-track at the third hour
- [`nodes/8-lg.html`](nodes/8-lg.html) — Lawful Good: the matron of the year of the second snow at the south-stair parlour at Khaboran's seminary
- [`nodes/8-ng.html`](nodes/8-ng.html) — Neutral Good: Banu Mahin (Khorshid's half-aunt, Bahram's mother) at the doorstep of the fourth house at Behesht
- [`nodes/8-cg.html`](nodes/8-cg.html) — Chaotic Good: the Reader of Behesht at the cold spring beyond the southern spur, with the mother's mother's book on his knee
- [`nodes/8-ln.html`](nodes/8-ln.html) — Lawful Neutral: Captain Faramarz at a senior post's back desk with the brown-leather red-cord folder open
- [`nodes/8-tn.html`](nodes/8-tn.html) — True Neutral: Master Yazdan on the ferry-yard bench at a junction crossing of a small brown river
- [`nodes/8-cn.html`](nodes/8-cn.html) — Chaotic Neutral: Asha at the slope's last step of a herder's shelter east of the dyer's town
- [`nodes/8-le.html`](nodes/8-le.html) — Lawful Evil: Banu Mahin (the cooper's mother) at the doorstep at Behesht, the morning's ride at the bishop's green linen
- [`nodes/8-ne.html`](nodes/8-ne.html) — Neutral Evil: Bardas at the inner counter of an inland fence's back room half a day west of Karkand
- [`nodes/8-ce.html`](nodes/8-ce.html) — Chaotic Evil: Cyrus's letter at the bothy's doorway, brought up by Asha's runner to the cold-spring winter-station
- [`nodes/9-lg.html`](nodes/9-lg.html) — Lawful Good: Marziyeh the seminary scribe at the south-stair writing-room; Maziar Karimi at the senior post's cell
- [`nodes/9-ng.html`](nodes/9-ng.html) — Neutral Good: Bahram at the cooper's mother's inner door at Behesht; the cooper's wife at the loaf; news of the bishop's morning hand from the next valley
- [`nodes/9-cg.html`](nodes/9-cg.html) — Chaotic Good: an old country forge-keeper at the second pruning-shed; Anahid the young runner with the morning's news of the bishop's dust-blue at Behesht
- [`nodes/9-ln.html`](nodes/9-ln.html) — Lawful Neutral: Lieutenant Hosrov of Khaboran's second tower at the senior post's map-table with bishop's dispatch and order's packet at the corners
- [`nodes/9-tn.html`](nodes/9-tn.html) — True Neutral: Father Marvan, a country priest at no parish, at a wayside fountain three farsang past the ferry
- [`nodes/9-cn.html`](nodes/9-cn.html) — Chaotic Neutral: Tahmineh, a country widow at an unmarked holding a half-day west of the herder's shelter
- [`nodes/9-le.html`](nodes/9-le.html) — Lawful Evil: Father Vali, the bishop's deacon-of-the-south, at the brick-floor post's back room; the iron at the second hook; the cooper at the cell
- [`nodes/9-ne.html`](nodes/9-ne.html) — Neutral Evil: Daryush the narrow man with the morning's first inland consignment at Bardas's inner yard; a thin chained boy at the cart's tail
- [`nodes/9-ce.html`](nodes/9-ce.html) — Chaotic Evil: Reza, son of the second orchard's widow, at the bowl's leader-stone's right shoulder on the eve of the new moon's ride

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

## L4 reachability

The L3 choice deltas land the player in all nine L4 buckets:

| L3 node | A → bucket | B → bucket | C → bucket |
| ------- | ---------- | ---------- | ---------- |
| 3-lg    | LG (+1/+1) | NG (-3/+1) | LN (0/-4)  |
| 3-ng    | LG (+3/0)  | CG (-1/+2) | CN (-2/-3) |
| 3-cg    | CG (-1/+1) | NG (+2/+1) | TN (+3/-3) |
| 3-tn    | LN (+2/+1) | NG (-2/+2) | NE (-1/-3) |
| 3-le    | LE (+2/-1) | TN (-1/+3) | NE (-1/-3) |
| 3-ce    | NE (+3/0)  | CN (-1/+3) | CE (0/-3)  |

Reachable L4 buckets: **LG, NG, CG, LN, TN, CN, LE, NE, CE** (9 of 9).
The grid is finally full at L4.

### L4 multi-parent nodes (convergence framing)

Several L4 nodes have multiple parents with markedly different physical
lead-ins. As with the L3 multi-parent nodes, each opening uses moral
state as the through-line and resolves physical particulars into a
single shared present:

- `4-lg` ← 3-lg (A) holds the kinsman lie at registry; OR 3-ng (A)
  paid Mira and signed. Both arrive: formally identified, paper in
  coat, walking east on the imperial road.
- `4-ng` ← 3-lg (B) bolted through dye-yard; OR 3-cg (B) parted at
  the goat-track; OR 3-tn (B) spoke morning to Razin. Convergence:
  late-afternoon, off-road, looking for a roof.
- `4-cg` ← 3-ng (B) stayed at Mira's; OR 3-cg (A) went with Behnam.
  Convergence: a stage further along the Mardesran network at
  Soraya's high fold.
- `4-ln` ← 3-lg (C) recanted at the desk; OR 3-tn (A) bought news
  cleanly. Convergence: clean hands at the south-gate post, given a
  brass pin for a half-day's writ work.
- `4-tn` ← 3-cg (C) took the cover and the horse; OR 3-le (B)
  refused Yusef's three doors. Convergence: alone on a wagon-track
  south of Sadaiziche, no obligations.
- `4-cn` ← 3-ng (C) robbed Mira; OR 3-ce (B) refused Mehrdad and
  warned the farmhouse. Convergence: off the empire's grid in
  unnamed country, crouched in dry broom at a road-bend.
- `4-ne` ← 3-tn (C) robbed Razin; OR 3-le (C) walked the child to
  the ship; OR 3-ce (A) apprenticed to Mehrdad. Convergence: alone
  at evening on a high road, a stroke-felled stranger at the verge.
- `4-le` (single parent, 3-le A) and `4-ce` (single parent, 3-ce C)
  are direct continuations of their parent's deepening commitment.

## L5 reachability

The L4 choice deltas land the player in all nine L5 buckets. The grid
stays full.

| L4 node | A → bucket    | B → bucket    | C → bucket |
| ------- | ------------- | ------------- | ---------- |
| 4-lg    | LG (+2/+2)    | NG (-3/+2)    | LN (+1/-3) |
| 4-ng    | LG (+3/0)     | CG (-2/+2)    | TN (+1/-3) |
| 4-cg    | CG (-1/+2)    | NG (+3/+1)    | CN (0/-4)  |
| 4-ln    | LN/LG (+2/+1) | TN/NG (-2/+2) | LE (+2/-3) |
| 4-tn    | NG/LG (+1/+2) | TN (0/-1)     | NE (-1/-3) |
| 4-cn    | CG/CN (-2/+2) | CN/CE (-3/-1) | NE (+3/-3) |
| 4-le    | LE (+2/-3)    | LN (+1/+2)    | TN (-3/+3) |
| 4-ne    | NE (0/-3)     | LE/LN (+2/+1) | TN/NE (-1/+2) |
| 4-ce    | CN/CE (-1/+4) | CE (0/-3)     | CE (-2/-4) |

### The player's pre-amnesia identity (revealed at L5)

The player is **Khorshid Daiyani**. Born in the eastern province to a
Mardesran mother (died young) and a Khvordemian functionary at
Khaboran. Taken into the Church's question-order seminary at Khaboran
at thirteen; trained partway as a question-priest (the same office
Mehrdad now holds at Sadaiziche); left the seminary at nineteen to
work as a field-informer, mapping Mardesran cells along the coast and
the southern circuit. Has not reported in four years. The order has
kept his column half-paid in Father Karim's paybook ever since,
under the marginal note *presumed living, location unknown*. Recent
operation: embedded in the Sadaiziche-coastal route under the cover
name *Daiyan*. Struck down on the imperial road east of Rabad at
first light of the day the story opens — by whom is not yet decided
in-text (Mardesran retaliation, Church loose-end, or a third party
all options).

Identifying body markers consistent with this identity, seeded
through L1–L4: callused/working body; Persian boots that "fit a
little too well today and a little too loosely yesterday" (the
order's standard field-boots); a hidden wrist scar (from a manacle
taken once and let go); foreign blood on a knuckle; the folded
knife in the coat lining set with the **Khaboran fold** at the
third button; the cold practised thing in the hands when violence
offers; the steady accustomed posture for warden-questioning; the
names *Daiyan* (cover) and *Khorshid* (real) surfacing on the
tongue under lies.

### L5 multi-parent nodes (convergence framing)

- `5-lg` ← 4-lg (A); 4-ng (A); 4-ln (A from clean start); 4-tn (A
  from clean start). Convergence: at a Church post, mid-afternoon
  of a later day, the magistrate-father Hossein is on circuit.
- `5-ng` ← 4-lg (B); 4-cg (B); 4-ln (B); 4-tn (A). Convergence: at
  a wayside inn in country off the chart, evening, Bahram the
  half-brother cooper is the seventh man at the long pine table.
- `5-cg` ← 4-ng (B); 4-cg (A); 4-cn (A). Convergence: at a small
  fire by a cold spring on the southern spur, second night out,
  Maziar — a former order field-man who turned four years ago.
- `5-ln` ← 4-lg (C); 4-ln (A); 4-le (B); 4-ne (B). Convergence: at
  a warden-post the morning after, Captain Faramarz arrives ahead
  of the bell with a leather folder from Khaboran.
- `5-tn` ← 4-ng (C); 4-tn (B); 4-le (C); 4-ln (B); 4-ne (C).
  Convergence: at a wayside inn-yard at the bare hour after noon,
  the wash-woman Parvin at the inn's trough wringing seminary-grey
  linens — she knew the boy Khorshid at thirteen.
- `5-cn` ← 4-cg (C); 4-cn (B); 4-cn (A); 4-ce (A). Convergence: at
  a small country market on a Thursday, between the cloth-stalls,
  Roshanak — a former lover from the river-bend at Sayedabad.
- `5-le` ← 4-ln (C); 4-le (A); 4-ne (B). Convergence: at a back
  room of a warden-post, Father Karim of the question-order's
  southern circuit at a desk with his strong-box and paybook.
- `5-ne` ← 4-tn (C); 4-cn (C); 4-ne (A); 4-ne (C). Convergence: at
  the back-alley door of a Sadaiziche fence after dark, Cyrus — a
  Mardesran the empire took once and let go to sit at the door.
- `5-ce` ← 4-cn (B); 4-ce (A); 4-ce (B); 4-ce (C). Convergence: at
  a hide-fire in a stone bowl above the coast-track, Behdad —
  Cyrus's brother, who took the brand at fifteen and built a band.

## L6 reachability

The L5 choice deltas land the player in all nine L6 buckets. The grid
stays full. Beat anchor for L6: **The first reckoning** — the bell
after the recognition. By the next morning, the recognition has begun
to do its own work on the player: a runner, a writ, a stranger
already on the path, a leader on a spur. Every L6 node frames a first
concrete act-as-Khorshid (or first explicit act-not-as-Khorshid).

| L5 node | A → bucket             | B → bucket             | C → bucket          |
| ------- | ---------------------- | ---------------------- | ------------------- |
| 5-lg    | LG (+2/+2)             | NG (-3/+1) / LG        | LN (+2/-3) / LG     |
| 5-ng    | NG/CG (-2/+3)          | LG/CG (+1/+2)          | LN/NG (+2/-3)       |
| 5-cg    | CG (-1/+2)             | NG/CG (+2/+2)          | CN (0/-4)           |
| 5-ln    | LN (+2/+1)             | LG/TN (-2/+2)          | LE (+2/-3)          |
| 5-tn    | NG/TN/LG (+1/+2)       | TN/NE (0/-1)           | NE/CE (-1/-3)       |
| 5-cn    | CN/CG (-2/+1)          | CN/CE (-3/-1)          | CE (-1/-4)          |
| 5-le    | LE (+2/-3)             | LN (+3/+2)             | LN/TN (-1/+2)       |
| 5-ne    | NE (0/-4)              | NE/LE (+1/-2)          | NE/CN (-1/+3)       |
| 5-ce    | CE (-2/-4)             | CE (+1/-3)             | CE (-2/+3)          |

### L6 multi-parent nodes (convergence framing)

- `6-lg` ← 5-lg (A) at Hossein's table; 5-ng (B) the long-table cup
  finished with Bahram; 5-tn (A) Parvin at the kitchen door. Convergence:
  first bell of the next morning, a small post-priest's outer room
  somewhere on the road south, where a runner has come ahead of the
  bell with a writ to be signed.
- `6-ng` ← 5-lg (B) walked out of Hossein's room into the road;
  5-ng (A) walked out at first light with Bahram; 5-tn (A from a
  clean start). Convergence: a wagon-road in country off the chart
  two farsang from the way-house, a struck boy at the verge, a
  soldier's grey mare bridle-down ten paces on.
- `6-cg` ← 5-cg (A) walked out with Maziar to the coast; 5-cg (B)
  put the question back to Maziar; 5-cn (A from a cg-leaning start);
  5-ng (A from a cg-leaning start). Convergence: a switchback path
  down a low limestone cliff to a small fishing-boat at a cove, a
  Khaboran-fold man on the path three switchbacks behind.
- `6-ln` ← 5-lg (C); 5-ng (C); 5-ln (A); 5-le (B) closed clean with
  Karim; 5-le (C from a low start). Convergence: a warden-post's
  main room at the bell of the third hour, the day's six writs in
  the desk-clerk's hand, an empty column at the head of the daybook
  with the player's name.
- `6-tn` ← 5-ln (B from a low start); 5-tn (A,B); 5-le (C from a
  low start). Convergence: a flat-bottomed ferry on a brown river,
  a second passenger at the opposite bench who reads the Khaboran
  fold at the right hand.
- `6-cn` ← 5-cg (C) the knife at the cold spring; 5-cn (A,B);
  5-tn (C from very low); 5-ce (?) — convergence: an attic above
  a dyer's loft in an unmarked country town, a propped rooflight,
  Mira's network runner at the willow, three men two roofs over.
- `6-le` ← 5-ln (C) take the writ further; 5-le (A) reopen the
  column; 5-ne (B) report at the next post (from a low-good start).
  Convergence: the brick-floor post at Bagh-e-Sang in the early
  afternoon, the iron at the brazier, Behshad on the table, the
  post-priest at the door.
- `6-ne` ← 5-tn (B,C from very low); 5-ne (A,B) at Cyrus's door;
  5-cn (B from middle). Convergence: the back room of a Karkand
  wine-seller a day west of Sadaiziche, the fence's man at the
  inner counter reading the Khaboran fold, Bardas's runner two
  bells west on the river-road.
- `6-ce` ← 5-cn (C) at the gap behind the cloth-stall; 5-tn (C);
  5-ce (A,B,C); 5-ne (C from very low). Convergence: a spur of
  the coast-ridge above Farzad's almond-orchards at the fourth
  hour, eight riders strung along the spur, the leader's hand
  lifting at the third bend.

## L7 reachability

The L6 choice deltas land the player in all nine L7 buckets. The grid
stays full. Beat anchor for L7: **The road answers** — by the bell
of evening (or the next morning), the country has had its half-bell
to react to the L6 act, and the response has come up to the player.
The L6 act is no longer in the player's hand alone; a second party
has arrived (Hossein, Manuchehr, the cutter, the sealed letter, the
circuit-clerk, the wash-woman, the bishop's folder, the cart at the
salt, the imperial riding).

| L6 node | A → bucket            | B → bucket            | C → bucket           |
| ------- | --------------------- | --------------------- | -------------------- |
| 6-lg    | LG (+2/+2)            | NG/LG (-3/+2)         | LN/LG (+1/-3)        |
| 6-ng    | NG (-2/+3)            | LG (+2/+2)            | TN/LG (0/-3)         |
| 6-cg    | CG (-1/+2)            | TN/CG (+3/-3)         | CG (-3/+2)           |
| 6-ln    | LN/LG (+2/+1)         | TN/LG (-2/+2)         | LE/LN (+2/-3)        |
| 6-tn    | TN/NG/LG (+1/+2)      | TN (0/-1)             | NE/TN (-1/-3)        |
| 6-cn    | CN/CG (-2/+2)         | CN/CE (-3/-1)         | CE/CN (-1/-4)        |
| 6-le    | LE (+2/-3)            | LN/LE (+3/0)          | LE (+1/-4)           |
| 6-ne    | NE (0/-4)             | NE/LE (+1/-2)         | NE/CN (-1/+3)        |
| 6-ce    | CE (-2/-4)            | CE (+1/-3)            | CE (-2/+3)           |

### L7 multi-parent nodes (convergence framing)

- `7-lg` ← 6-lg (A) the writ at the third line; 6-lg (B from high
  state); 6-ng (B) waited at the verge; 6-ln (A from high state).
  Convergence: a wayside post at the bell of sundown of the same
  long day, the day's signed writs piled at the desk, the magistrate-
  father's grey at the rail.
- `7-ng` ← 6-ng (A) took the boy; 6-lg (B mixed); 6-cg (B mixed).
  Convergence: a country house at mid-afternoon, the boy on a folded
  blanket in the inner room, the mare's man at the gate having
  ridden the long way round.
- `7-cg` ← 6-cg (A) tied the man on the path; 6-cg (B mixed) talked
  him down; 6-cg (C) goat-track to the boat; 6-cn (A mixed) out the
  rooflight with the woman. Convergence: the fishing-boat past the
  cove's south headland, the coast-warden's cutter at the next.
- `7-ln` ← 6-ln (A) signed the daybook; 6-ln (C mixed); 6-le (B
  mixed) closed the case-file. Convergence: the warden-post at the
  seventh bell, the leader at the desk, the Khaboran post-runner
  with the wax-sealed letter at the centre of the desk.
- `7-tn` ← 6-tn (A,B,C mixed) speak with Hassan, step off, take the
  copper; 6-cg (B mixed); 6-ln (B mixed); 6-ng (C mixed).
  Convergence: a country inn at the turning of the road by the lone
  walnut, evening, a Khaboran circuit-clerk at the chimney-table
  with a description-sheet under his elbow.
- `7-cn` ← 6-cn (A,B,C); 6-ne (C mixed). Convergence: a stream-bend
  a day's walk west of the dyer's town, a country wash-woman at the
  middle washing-stone speaking to the linen.
- `7-le` ← 6-le (A,B,C); 6-ln (C mixed); 6-ne (B mixed) buy off the
  cart. Convergence: the brick-floor post's front office at the
  morning of the next day, the post-priest at the triangular table,
  the Sadaiziche bishop's green-linen folder on the dawn-cart.
- `7-ne` ← 6-ne (A,B,C); 6-tn (C mixed) the half-copper at the
  bank. Convergence: an ox-cart at the long white smear of the
  western salt-line, two country men on the cart's tail, the
  Karkand fence's man canvas-wrapped in the cart.
- `7-ce` ← 6-ce (A,B,C); 6-cn (B,C mixed). Convergence: the bowl at
  the small grey hour after Farzad's, a runner from Asha's fire
  over the lip, an imperial riding on the coast-track at the bell
  of the third hour.

## L8 reachability

The L7 choice deltas land the player in all nine L8 buckets. The grid
stays full. Beat anchor for L8: **The threshold** — by the bell of
this morning (or evening), the road has narrowed to a single line,
and the player is at the door of the Place the L1–L7 arc has been
pulling toward. A fourth voice — someone from before the morning of
the man in the ditch, never seen at any previous level — is at that
door. The choices are: cross, pause, or turn.

| L7 node | A → bucket           | B → bucket           | C → bucket           |
| ------- | -------------------- | -------------------- | -------------------- |
| 7-lg    | LG (+2/+1)           | LG/NG (-2/+3)        | LG/LN (+3/-1)        |
| 7-ng    | LG/NG (+1/+2)        | CG/LG (-3/+2)        | LG/NG (+2/-3)        |
| 7-cg    | CG (-1/+3)           | CG/NG (+2/+2)        | CG (-3/+2)           |
| 7-ln    | LG/LN (+2/+1)        | LN (+3/-1)           | LG/NG (-2/+2)        |
| 7-tn    | TN/LG (0/+1)         | TN/LG (+1/0)         | CE/TN/NE (-2/-3)     |
| 7-cn    | CN/CG (-1/+2)        | CN/CG (-3/0)         | CE/CN (-2/-3)        |
| 7-le    | LE (+2/-3)           | LE/LN (+3/0)         | LE (+1/-4)           |
| 7-ne    | NE/CE (-1/-3)        | LE/NE (+2/-2)        | CE/NE/CN (-2/+2)     |
| 7-ce    | CE (-1/-3)           | CE (+1/-4)           | CE (-3/-2)           |

### L8 multi-parent nodes (convergence framing)

- `8-lg` ← 7-lg (A from any arrival); 7-lg (B from high); 7-lg (C
  from high); 7-ng (A from mid/high); 7-ng (B from mid); 7-ng (C
  from high); 7-ln (A from high); 7-ln (C from high); 7-tn (A from
  high arrival); 7-tn (B from high arrival). Convergence: the south
  stair of the order's seminary house at Khaboran, the parlour at
  the third floor, the matron of the year of the second snow in her
  chair at the window. Three signed writs from Hossein on the side-
  table for high-arrival parents; the single letter under the wax
  for low-arrival parents. The matron reads only the boy of thirteen.
- `8-ng` ← 7-lg (B from low); 7-ng (A from low); 7-ng (C from mid);
  7-cg (B from low); 7-ln (C from low). Convergence: Behesht, the
  fourth house on the right at the lane's bend under the chestnut,
  Banu Mahin (Khorshid's half-aunt, the cooper Bahram's mother)
  folding the cooper's wife's washing on the doorstep at the bell
  of the seventh.
- `8-cg` ← 7-cg (A,B,C); 7-cn (A from high); 7-ng (B from high).
  Convergence: the cold spring at a high fold above the southern
  spur, a half-roof of brushwood and goat-hide pegged at the foot
  of a basalt slot, the Reader of Behesht at the fire with the
  mother's mother's small leather-bound book on his knee.
- `8-ln` ← 7-lg (C from high); 7-ln (A from high); 7-ln (B); 7-le
  (B mid). Convergence: a senior warden-post a day east of the L7
  warden-post; the back room set out with a long oak desk; Captain
  Faramarz at the window with the brown-leather red-cord folder
  open on the desk.
- `8-tn` ← 7-tn (A from low); 7-tn (B from low). Convergence: a
  small ferry-yard at a junction crossing of a small brown river,
  the bench under a half-roof of cane, Master Yazdan (Khorshid's
  seminary field-master at fourteen) with a piece of dry bread and
  a sleeping grey lurcher at his foot.
- `8-cn` ← 7-cn (A,B); 7-cn (C from mid); 7-ne (C from low).
  Convergence: a herder's shelter at a fold of country east of the
  dyer's town, the herder up at a higher fold with the flock, Asha
  at the slope's last step having come down from her fire at the
  morning's runner's word.
- `8-le` ← 7-le (A,B,C); 7-ne (B from high). Convergence: Behesht,
  the same fourth house on the lane as 8-ng, but the morning's hand
  has come up the lane in dust-blue and silver olives with the post-
  priest's brother-in-law and his nephew at the saddles behind. Same
  Banu Mahin at the doorstep, opposite valence.
- `8-ne` ← 7-ne (A,B); 7-ne (C from mid); 7-tn (C from low).
  Convergence: a small dust-coloured town a half-day's ride west
  of Karkand, the back room of an inland fence's house, Bardas
  himself at the inner counter with the brass scales at his elbow
  and the canvas-wrapped bundle from the salt-line cart on the long
  pine table at the back wall.
- `8-ce` ← 7-ce (A,B,C); 7-cn (C from high); 7-ne (A from mid);
  7-tn (C from very low). Convergence: the bowl's stone winter-
  bothy at the cold spring above the southern spur, the bowl's
  saddlebags at the back wall, Behdad at the leader's stone with
  the falchion across his knees, and Asha's runner at the doorway
  with Cyrus's folded letter in his hand.

## L9 reachability

The L8 choice deltas land the player in all nine L9 buckets. The grid
stays full. Beat anchor for L9: **What the room costs** — the morning
or evening after the threshold, the price of the L8 conversation
arrives in a concrete shape. A new fifth voice (current generation,
never seen before this morning) comes to the door with the first
specific instance of that price.

| L8 node | A → bucket           | B → bucket           | C → bucket           |
| ------- | -------------------- | -------------------- | -------------------- |
| 8-lg    | LG (+2/+1)           | LG (+1/+2)           | LG/NG (-3/+2)        |
| 8-ng    | LG/NG (+2/+2)        | NG/LG (0/+2)         | CG/NG (-2/+2)        |
| 8-cg    | CG (-1/+3)           | CG (-2/+2)           | CG (-3/+1)           |
| 8-ln    | LG/LN (+3/0)         | LG/LN (+2/+1)        | LG (-2/+2)           |
| 8-tn    | LG/LN (+2/+1)        | TN/LG (0/0)          | CE/TN/NE (-2/-3)     |
| 8-cn    | CG/CN (-1/+2)        | CG/CN/CE (-2/0)      | CN/CE (-2/-3)        |
| 8-le    | LE (+2/-3)           | LE (+3/-1)           | LE (+1/-4)           |
| 8-ne    | NE (0/-3)            | NE/LE (+2/-2)        | NE/CN/CE (-1/+2)     |
| 8-ce    | CE (-1/-3)           | CE (+1/-4)           | CE (-2/-4)           |

### L9 multi-parent nodes (convergence framing)

- `9-lg` ← 8-lg (A,B,C from high arrival); 8-ng (A from various); 8-ln
  (A,B,C from high state); 8-tn (A,B from high arrival). Convergence:
  an upper writing-room at the south end of the third-floor corridor
  of the order's seminary house at Khaboran, the morning after the
  matron's parlour (or Faramarz's folder, or the doorstep at Behesht
  with the morning's letter pending). Marziyeh the matron's scribe
  brings the morning's case-list. The case at the head is Maziar
  Karimi, taken at the salt-flats; the post-priest's brother-in-law
  has asked the matron's hand whether the column closes at the cell.
- `9-ng` ← 8-ng (B,C); 8-lg (C decline); 8-ln (C from mid). Convergence:
  the cooper's mother's inner kitchen the morning after the doorstep
  (or, by C of 8-lg, the back gate by the donkey-path from the
  matron's house). Bahram has walked up from his own forge at the next
  valley at the bell of the dawn at the cooper's wife's mother's
  sister's husband's word; he is at the inner door from the workshop's
  yard. The bishop's pen is moving at Sadaiziche.
- `9-cg` ← 8-cg (A,B,C); 8-ng (C from low); 8-cn (A from low).
  Convergence: a small country forge in a half-built lean-to at the
  back of the second pruning-shed three farsang east along the spur
  from the cold spring. Soraya, an old country forge-keeper, and
  Anahid (a young runner from the deeper country, two winters since
  her own brand) — Anahid has come up the lower path with the
  morning's news that the bishop's dust-blue riding has left the
  brick-floor post for Behesht.
- `9-ln` ← 8-ln (A,B); 8-tn (A from high); 8-lg (A from various).
  Convergence: the senior warden-post's morning room a half-bell after
  Faramarz has ridden east, the long map-table at the inner wall.
  Lieutenant Hosrov of the second tower at Khaboran comes up at the
  bell of the second with the bishop's first dispatch (the dust-blue
  riding for Behesht) and a sealed packet from the order's drawer at
  the same desk.
- `9-tn` ← 8-tn (B from various). Convergence: a small wayside
  fountain three farsang past the ferry's western bank where the
  country track meets a dust-coloured cart-road south to the
  salt-line. Father Marvan, an old country priest at no parish since
  the year of the first snow, on a long flat-stone bench at the
  trough's near side.
- `9-cn` ← 8-cn (A,B); 8-cg (C from low). Convergence: a small
  unmarked country holding a half-day's walk west of the herder's
  shelter, a low stone cistern at the foot of a dry-stone wall.
  Tahmineh, a country widow at an unmarked half-fold holding the
  bishop's clerk has not yet read; a small child of three at her
  knee.
- `9-le` ← 8-le (A,B,C); 8-ne (B from mid). Convergence: the
  brick-floor post at Bagh-e-Sang at the bell of the third hour of
  the morning after Behesht. The cooper at the cell, the iron at the
  second hook on the brazier, the small black leather case of the
  order's instruments open at the long pine question-table. Father
  Vali, the bishop's deacon-of-the-south, has ridden up at the bell
  of the third with the bishop's morning's rate-sheet for the half-
  fold case-list's first column.
- `9-ne` ← 8-ne (A,B); 8-tn (C from very low); 8-cn (C from low).
  Convergence: the inner yard of Bardas's inland fence's house the
  morning after the counter. Daryush — the narrow man at the inner
  counter, formerly canvas-wrapped at the salt-line cart, now reading
  the morning's first inland delivery at the cart's tail — with two
  country men, a low ox-cart of four canvas-packets, and a chained
  boy of twelve.
- `9-ce` ← 8-ce (A,B,C); 8-cn (B,C from very low); 8-ne (C from low);
  8-tn (C from very low). Convergence: the bothy's outer yard at the
  cold spring's upper fold at the bell of the dusk after Cyrus's
  letter. Fifteen country horses at the half-line, saddlebags set at
  the small stone shelf, Reza of the second orchard's widow's son at
  the leader's right shoulder, the small grey order-shirt folded
  fresh at the brother's saddle's near edge.

## Next to generate (Level 10, beat: TBD)

By L10 the morning's first act (or first refusal) at L9 has been
played; the room's first cost is paid (or deferred, or stolen). The
L10 beat anchor is open. Candidates:

- **"The first ride back"** — the answer of the next day's road to
  L9's first act. A senior officer rides up, a Mardesran cell sets
  a meeting, a fence sends a runner, a matron sends a letter, the
  bowl arrives at Bardas's door at the bell of dawn.
- **"Who comes when the door is open"** — the second party L9's act
  has now drawn in: a wife at the doorstep, a brother at the gate,
  a country priest at the lane's foot, a child of three who walks
  out from the cistern after the morning's leaving.

Notable L9 constraints to remember when writing L10:

- `9-le`'s three choices stay LE (B can drift LN at the top end);
  10-le will absorb three distinct physical lead-ins from the
  brick-floor's morning.
- `9-ce`'s three choices stay CE (the bowl's three doors of the
  new-moon's saddle).
- `9-cg`'s three choices stay CG (the forge's three onward stages).
- `9-tn`'s C choice routes drastically away (CE/NE) for an arrival
  that took the C of 8-tn — a small narrative continuity warning.

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
- The player's pre-amnesia identity: **Khorshid Daiyani**, half-
  Mardesran by mother, Khvordemian by father; raised at Khaboran;
  taken into the Church question-order seminary at thirteen; left
  at nineteen for field-informer work mapping Mardesran cells along
  the southern coast circuit. Has not reported in four years. The
  order's paybook at Khaboran has carried his column half-paid in
  Father Karim's hand under the note *presumed living, location
  unknown*. Cover name in the recent operation: *Daiyan*.
  Identifying body markers: callused/working body; standard order
  field-boots ("fit a little too well today and a little too
  loosely yesterday"); wrist scar from a manacle taken once and
  let go (no star-brand because of the order's protection);
  foreign blood on a knuckle. Muscle memory revealed: a folded
  knife in the coat lining set with the *Khaboran fold* (lining at
  the inner seam, against the third button, haft turned out); a
  cold practised thing in the hands when violence offers; the
  steady, accustomed posture for warden-questioning; the names
  *Daiyan*/*Khorshid* surfacing on the tongue under lies; the cool
  calculation that "a fast walker invites questions."
- Items on the NE / rob-path: silver Mardesran fish-and-tail charm;
  wax-stoppered clay phial; folded vellum with three lines the player
  cannot read in dawn light; copper ring (no stone); whetstone; three
  additional small coins (now seven total).
- **Khaboran**: a town east of Sadaiziche, three farsang along the
  imperial road past a third milestone. Has a Church post-priest at
  the milestone and a dean to whom the Sadaiziche bishop writes.
- **Father Asad** (4-lg): Church deacon, perhaps fifty, long careful
  hands, grey wool robe with embroidered cross at breast. Carries the
  morning's collections and a sealed letter bishop-to-dean that must
  reach Khaboran by tomorrow's first bell.
- **Soraya** (4-cg): woman of the high fold safehouse above the second
  vineyard's pruning-shed, white at the temple, star-scar. Quiet;
  speaks little. Mardesran network station-keeper.
- **Hirsi** (4-cg): the elder at the second pruning-shed, white in
  both braids. Reads the strip-marks; does not know runners' faces.
- **Davud** (4-ln): warden-corporal at the south-gate post,
  recognisable by belt-buckle. Under the leader with the slow eyes.
- **Hamid** (4-ln): warden at the south-gate post; pairs with Davud.
- **Hamza of the river-quay** (4-ln): a dyer in a dyer's apron, taken
  on a writ of question for the murder of his brother three days past.
  Hides in the culvert under the imperial road at the third milestone.
- **Tirzah** (4-ng): Sadaiziche merchant of the dye-yard street; owner
  of the brass-collar bond-boy who has fled into the country east.
- The Mardesran network's stages (so far): the road in the ditch east
  of Rabad → Mira's elder-tree hospice → Asha's fire above the second
  vineyard → Soraya's high fold → the second pruning-shed (Hirsi) →
  south through bandit-tolerant country to the coast.
- **Khaboran seminary** (the question-order's house): where Khorshid
  trained 13–19. Senior figures: the matron of the year of the second
  snow; the seminary-prefect of twenty years ago, now **Magistrate-
  Father Hossein**, who rides circuit. Wash-women included **Parvin**
  (now at a wayside inn). The Khaboran knife-fold is a master's habit
  taught to perhaps eight field-men of Khorshid's seminary years.
- **Sayedabad**: a river-bend village in the eastern province where
  Khorshid and Roshanak had a brief life and a child eight years ago.
  Roshanak now lives there with her husband and trades at the country
  Thursday-market in a small town nearby. The child was the player's;
  the player saw him born and saw him once and never again.
- **Yazdebar**: a river-house in the eastern province whose family
  Khorshid put to the question nine winters past. Three names on the
  page: the father (did not live the autumn), Behdad the elder
  brother at fifteen (gave up the third name at the second hour;
  branded and walked; now leads a bandit-bowl above the coast-track),
  and Cyrus the younger (lived the winter; now sits at Bardas's
  fence's door in Sadaiziche by the order's arrangement).
- **The order's paybook**: kept in Khaboran by **Father Karim**, the
  paymaster of the question-order's southern circuit. Khorshid's
  column has been open four years at half-pay. The strong-box and
  the paybook ride with Karim when he rides circuit.
- **Captain Faramarz**: senior officer of the imperial border force,
  Khaboran posting. Carries a brown-leather red-cord folder with
  Khorshid's name at the head of the first sheet — forwarded to his
  desk four years ago when the field-man failed to return.
- **Bahram the cooper**: Khorshid's half-brother (Mardesran mother's
  sister's son), working the small towns of the southern country.
  Has searched seven seasons.
- **Maziar Karimi**: a field-man of Khorshid's seminary cohort who
  turned four years ago — at the cold spring on the southern spur,
  running the network's southern stages now.
- **Bagh-e-Sang**: a brick-floor post a half-day's ride south of
  Sadaiziche on the imperial road. Single-storey, new bricks paid
  for in the second year of the present bishop. Post-priest unnamed
  but described as a careful man whose office has been paying small
  parish bounties for Mardesran sales to imperial-road tax-collectors.
- **Sahar / Behshad** (6-lg, 6-le): the niece (Sahar, ~15) of a small
  almond-orchard holder (Behshad, ~60) south of Vahdat by half a
  farsang. Behshad held on a Mardesran hearsay-charge by Bagh-e-Sang's
  post-priest's own brother-in-law. The case-file at Bagh-e-Sang
  carries a third name out of Khaboran whose own column the order
  has been minded to read these last four years.
- **Hassan of Behbahan** (6-tn): a year at the Khaboran seminary,
  let go for a thing the master would not write in the order's drawer.
  Has spent the week's silver at four wayside inns tracing a
  Khaboran-fold rumour. On the ferry by his own walking.
- **Karkand**: a small unmarked town a day west of Sadaiziche by
  the river-road. No Church post, no warden's stable. Four wine-sellers;
  one of them keeps a back room for the country's quieter trade.
- **Farzad** (6-ce): small landlord, three almond-orchards on a slope
  three farsang up the coast-track from Behdad's bowl. Empire's listed
  tax-collector for the country-houses between the slope and the coast
  these last four winters. Sold a Mardesran widow at his second orchard
  to Bagh-e-Sang's post-priest for the small parish bounty three days
  past. The widow's son is on the third horse along the bowl's spur.
- **Manuchehr of the second tower at Sayyaf** (7-ng): imperial border
  force, dust-blue coat with silver olive at the shoulder, light
  cavalry sabre, the grey mare of the army's pattern. Younger brother
  of the boy at the verge. Left the boy in the long grass at the
  third bend in a fight with three men in a thicket; came back the
  long way round the mill-stream four bells later.
- **Behesht** (7-le, also referenced 5-ng, 7-le head-case): a village
  in the eastern province where Khorshid's mother's people kept a
  yard. Bahram the half-brother cooper's mother's house was there
  when Khorshid was eleven. Now: a Mardesran-leaning village the
  bishop's standing case-list keeps a head-case on.
- **Bagh-e-Sang's post-priest** (6-le, 7-le): unnamed; described as
  a careful man at three years at his post; keeps the brick-floor
  drawer's parish bounties in a small locked drawer at the front
  office; pleased to share the fourth year of an orchard with a
  visiting brother of the order who works an iron at his brazier.
- **The Sadaiziche bishop's green-linen folder** (7-le): the bishop's
  standing case-list for the southern circuit. Eighteen cases in the
  folder; the three at the head are the ones the bishop's pen has
  ridden a particular morning's hand on. One of the three head-cases
  is the Behesht half-fold (Bahram).
- **Karkand fence's man** (7-ne): the narrow man at the inner counter
  with the embroidered coat over a yellow shirt, the bone-handled awl
  on a cord, the green-bronze ring at the third finger. By the salt-
  line at the bell of the noon, canvas-wrapped in a country cart's
  back. The middle finger of his right hand carries an old break at
  the second joint.
- **The Khaboran circuit-clerk's description-sheet** (7-tn, 7-cn): a
  carefully written description circulated in the southern circuit
  by the bell of the morning after L6 — *man, perhaps forty, sun-
  darkened, Persian boots of the order's pattern; the right hand
  carries the Khaboran fold at the lining at the third button; the
  gait at the right knee a small habit from a boyhood at the
  seminary's south stair.* Carried by travelling clerks; ink-stoppers
  of red glass placed at perhaps a dozen wayside inns along the
  southern circuit.
- **Asha's fire** (7-ce, referenced earlier 3-cg lore): now a
  Mardesran-network signal-station for runners between the second
  vineyard's ridge and the southern spur. Asha sends runners up to
  the bowl's lip when an imperial riding passes her ridge.
- **Khaboran circuit-captain's red cord**: imperial border force,
  Khaboran posting; the lead-rider's saddle of any imperial riding
  out of Khaboran carries the red cord. The riding south of the
  Sadaiziche-Bagh-e-Sang area at L7 is twenty horses with the red
  cord at the lead.
- **The matron of the year of the second snow** (8-lg): a woman of
  perhaps eighty at the order's seminary house at Khaboran, white
  at the temple under a pearl-grey scarf of the outer house; was
  the matron of the year Khorshid arrived at thirteen. Sits at a
  low chair by the south-stair parlour window onto the lemon-tree
  courtyard. Set the boy's right-knee gait at fourteen with a thin
  willow-switch. Has kept Khorshid's column at half-pay against her
  own recommendation these four years.
- **Banu Mahin** (8-ng, 8-le): Khorshid's mother's elder sister; the
  cooper Bahram's mother; sixty years, iron-grey hair under a country
  scarf, lives at the fourth house on the right at the bend of the
  single lane at Behesht under the old chestnut. Folds the cooper's
  wife's washing on Thursdays. Reads the boy in the man without
  comment. The same doorstep meets the player as kin (8-ng) or as
  quarry (8-le) depending on alignment.
- **The Reader of Behesht** (8-cg): a Mardesran scholar of perhaps
  seventy, white beard, no star at the temple, keeps a fire at the
  cold spring above the southern spur at the small upper fold past
  the basalt slot. Holds Khorshid's mother's mother's small leather-
  bound book — the dark red Mardesran cover — and has been at the
  fire since the year of the second snow. Can read the third page
  of the book aloud and write the small name Khorshid's mother gave
  the boy at four into the book's last page.
- **Master Yazdan** (8-tn): an old Khaboran field-master, seventh
  decade, brown country coat, no scarf, sleeping grey lurcher at
  the foot. Set the third-week field-test for the boys of fourteen
  at the south stair's small inner room every February of Khorshid's
  seminary years. Sits the bench at a small ferry-yard at a junction
  crossing of a small brown river the empire does not maintain.
- **Asha at the shelter** (8-cn): the woman shepherd referenced from
  L3 onward, now seen in person. White at both temples, man's coat,
  country felt boots. Came down from her fire at the second
  vineyard's ridge at the morning's wash-woman's runner's word. Tall;
  speaks at a small carefully roughened pitch.
- **Bardas** (8-ne): the fence at Sadaiziche referenced from L3
  onward, now seen in person at a small back-room counter at an
  inland fence's house half a day west of Karkand. Sixty, fat, long
  brown coat, wide leather belt, brass scales at the elbow, small
  careful steady eyes. Was set back a year's takings by Khorshid's
  careful hand in the autumn of the open winter; has had the small
  careful eye on the order's southern circuit at the back of his
  counter ever since.
- **Cyrus's letter** (8-ce): a piece of brown paper folded in three
  with a small dark red wax at the spine bearing Cyrus's right
  thumb-print. Written at the back of Bardas's door the night the
  bell of the midnight rang at Sadaiziche; brought up by the wash-
  woman at the river-quay to Asha's fire, then by Asha's runner to
  the bowl's bothy at the cold spring. Names Cyrus as the third
  name's house's younger brother, names the leader at the stone as
  the elder, and offers the bowl the third name's column.
- **Marziyeh** (9-lg): the first woman the order has set at the
  south-stair scribe's stool since the year of the second snow.
  Perhaps nineteen; dark-grey scarf of the order's outer house;
  dark brown braid at the back; small careful scribe-master's hand
  trained three years at the seminary's writing rooms. Brings the
  morning's case-list to the upper writing-room at the south end of
  the third-floor corridor.
- **Maziar Karimi at the salt-flats** (9-lg): the L5-cg field-man,
  taken at the salt-flats four farsang south of Karkand by the
  post-priest's brother-in-law's hand; at the cell of the senior
  warden-post a day east of Khaboran. Column at the head of the
  matron's morning's three.
- **Anahid** (9-cg): a thin young Mardesran runner of the deeper
  country, perhaps twenty; small fresh star at the temple from a
  branding two winters past; carries the network's onward satchels
  between the second pruning-shed and the deeper country's stations
  three days east. The country forge-keeper at the second pruning-
  shed (unnamed, perhaps seventy, Mardesran's long grey country
  coat, small star at the white at the left temple) is a station-
  keeper of the network's mid-eastern run.
- **Lieutenant Hosrov of the second tower at Khaboran** (9-ln):
  imperial border force, perhaps twenty-six; dust-blue coat with
  silver olive of a lieutenant of the second tower; fencing-master's
  hands at the sabre. Subordinate to Captain Faramarz. Brings the
  bishop's first dispatch (the dust-blue riding for Behesht) and a
  sealed packet from the order's drawer to the senior post's
  map-table the morning after Faramarz rides east.
- **Father Marvan** (9-tn): an old country priest of perhaps seventy,
  brown wool cassock of the country pattern, no embroidery at the
  breast, no white cord at the shoulder. Was at a parish three valleys
  south until the year of the first snow of the previous year; the
  parish has been writing itself into the country's own small drawer
  ever since. Walks between four wayside fountains on the slow road
  south, sitting each at a small careful particular hour. Carries no
  name to any drawer of the empire's or the bishop's or the order's.
- **Tahmineh** (9-cn): a country widow of perhaps thirty-five at an
  unmarked country holding a half-day's walk west of the dyer's-town
  herder's shelter. Husband taken on the bishop's standing case-list
  two winters past for a half-fold; the country at the fold did not
  read the half-fold to the bishop's clerk (Asha's word at her own
  ridge). A child of perhaps three at her knee, small carved wooden
  horse in the right hand.
- **Father Vali** (9-le): the bishop of Sadaiziche's deacon-of-the-
  south. Perhaps forty-five; clean grey robe at the small careful
  pressing of a senior clerk's at the bishop's south stair; embroidered
  cross at the breast at the bishop's particular stitch; nine years
  at the rate-book at the bishop's south stair. Rides up the imperial
  road from Sadaiziche at the bell of the third hour of the morning
  to read the half-fold case-list's first column at the brick-floor
  post at Bagh-e-Sang.
- **Daryush** (9-ne): the narrow man at Bardas's inner counter the
  day after the salt-line cart, formerly canvas-wrapped in the cart's
  back at the L7 salt-line scene. Embroidered coat over a yellow
  shirt; small bone-handled awl on a cord at the inner pocket;
  green-bronze ring at the third finger of the right hand; old break
  at the second joint of the middle finger of the right hand. Bardas's
  morning-runner for the small inland circuit.
- **Reza of the second orchard's widow's son** (9-ce): a thin rider
  of perhaps twenty-three in the bowl. Small fresh star at the temple
  (empire took him once and let him go eighteen months past). Came up
  to the spur in the company of the orchard widow Farzad had sold to
  Bagh-e-Sang's post-priest for the small parish bounty three days
  before L6-ce. Set at the bowl's leader-stone's right shoulder during
  the four hours after Cyrus's letter.

## How to continue

Read [`produce.txt`](produce.txt) before writing new nodes. For each
new node, identify ALL parents at the previous level whose choices
route into your bucket, and read them all so your opening reads
naturally for any arrival.
