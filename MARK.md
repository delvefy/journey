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

`5-ce` — 2026-05-28. Level 5 is fully populated: all nine L5 buckets
are written. The grid stays full from L4 onward.

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

## Next to generate (Level 6, beat: TBD)

The L6 beat anchor is open. Candidate beats:

- **"The first reckoning"** — the consequences of the L5 recognition
  collect: the cart leaves at the bell of four; the magistrate's
  folder closes; the band rides out of the bowl; the corporal at the
  warden-post sends a runner east. The week's accountancy becomes
  other people's accountancy.
- **"The road south"** — the choices made in L5 begin to converge
  into a single destination the player will spend the rest of the
  story arriving at. The coast, Khaboran, the bowl, the inn behind
  Bahram, or the cell at Cyrus's door.

Reachable L6 buckets from L5: **all nine**. Three nodes have notable
constraints:

- `5-ce`'s three choices all land in CE (the player is now too deep
  in evil for any reasonable swing to escape). 6-ce will need to
  absorb three different physical lead-ins from inside Behdad's
  bowl.
- `5-ne`'s three choices route only to NE / CN (rarely TN from the
  mildest start). 6-ne will likewise carry multi-parent weight.
- `5-cn`'s C choice always routes to CE; A/B mostly stay CN.

For L6, also decide where the story is heading at L7 and beyond.
The beat-anchor pattern (one per level) suggests at least three
more levels are still on the calendar before any major arc can
close.

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

## How to continue

Read [`produce.txt`](produce.txt) before writing new nodes. For each
new node, identify ALL parents at the previous level whose choices
route into your bucket, and read them all so your opening reads
naturally for any arrival.
