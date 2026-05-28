# MARK — story generation progress

Updated by Claude after each generation pass. Read this first when continuing the story.

## Last node added

`3-i` — 2026-05-28. (Level 3 completed in a single pass: 3-a through 3-i. Level 3 is the first heavily-converged tier — gender pairs from level 2 collapse into a shared trio per branch.)

## Nodes that exist

- [`index.html`](index.html) — title page, links into `nodes/0-a.html`
- [`nodes/0-a.html`](nodes/0-a.html) — waking, name entry, gender select; branches to `1-a` or `1-b`
- [`nodes/1-a.html`](nodes/1-a.html) — male, man in the ditch; → `2-a` / `2-b` / `2-c`
- [`nodes/1-b.html`](nodes/1-b.html) — female, man in the ditch; → `2-d` / `2-e` / `2-f`
- [`nodes/2-a.html`](nodes/2-a.html) — male, help; the climb; → `3-a` / `3-b` / `3-c`
- [`nodes/2-b.html`](nodes/2-b.html) — male, hide; the reeds; → `3-d` / `3-e` / `3-f`
- [`nodes/2-c.html`](nodes/2-c.html) — male, rob; pockets; → `3-g` / `3-h` / `3-i`
- [`nodes/2-d.html`](nodes/2-d.html) — female, help; the climb; → `3-a` / `3-b` / `3-c`
- [`nodes/2-e.html`](nodes/2-e.html) — female, hide; the reeds; → `3-d` / `3-e` / `3-f`
- [`nodes/2-f.html`](nodes/2-f.html) — female, rob; pockets; → `3-g` / `3-h` / `3-i`
- [`nodes/3-a.html`](nodes/3-a.html) — *Kinsman*: help+lie, leader files the lie; → `4-a` / `4-d` / `4-b`
- [`nodes/3-b.html`](nodes/3-b.html) — *Vine and Oak*: help+off-road, man fading on the slope; → `4-b` / `4-i` / `4-e`
- [`nodes/3-c.html`](nodes/3-c.html) — *The Cup-Bearer's Step*: help+handoff to shrine, riders return; → `4-a` / `4-d` / `4-f`
- [`nodes/3-d.html`](nodes/3-d.html) — *The Third Milestone*: hide+false trail works, man rises from reeds; → `4-i` / `4-c` / `4-b`
- [`nodes/3-e.html`](nodes/3-e.html) — *The Search*: hide+silent, youngest rider finds him; → `4-a` / `4-f` / `4-c`
- [`nodes/3-f.html`](nodes/3-f.html) — *The Stone*: hide+spook, knife at the youngest's throat; → `4-c` / `4-e` / `4-d`
- [`nodes/3-g.html`](nodes/3-g.html) — *Mercy*: rob+return to silence him with a stone; → `4-e` / `4-f` / `4-h`
- [`nodes/3-h.html`](nodes/3-h.html) — *The Stripped Rows*: rob+off-road, hooves pass overhead; → `4-b` / `4-g` / `4-e`
- [`nodes/3-i.html`](nodes/3-i.html) — *The Open Road*: rob+to Sadaiziche, leader files the boots; → `4-a` / `4-h` / `4-g`

## Convergence note

Level 3 → Level 4 is **heavy** convergence: 27 outgoing edges land on 9 level-4 nodes. Each level-4 node receives between 2 and 4 inbound edges, often from very different upstream paths. Writing each level-4 node requires reading **all** of its parents in order to keep the opening lines compatible with every arrival context.

Inbound edges per level-4 node:
- `4-a` (Sadaiziche warden-house, noon bell): 3-a/A, 3-c/A, 3-e/A, 3-i/A — 4 parents
- `4-b` (Asha's shepherd-fire in the oak scrub): 3-a/C, 3-b/A, 3-d/C, 3-h/A — 4 parents
- `4-c` (combat on the imperial road): 3-d/B, 3-e/C, 3-f/A — 3 parents
- `4-d` (riding/walking under warden escort): 3-a/B, 3-c/B, 3-f/C — 3 parents
- `4-e` (alone east on the road with a death behind): 3-b/C, 3-f/B, 3-g/A, 3-h/C — 4 parents
- `4-f` (the shrine of Vabum revisited): 3-c/C, 3-e/B, 3-g/B — 3 parents
- `4-g` (the vellum unfolded, three lines read): 3-h/B, 3-i/C — 2 parents
- `4-h` (river-path / dye-houses, Sadaiziche back-way): 3-g/C, 3-i/B — 2 parents
- `4-i` (the wounded man speaks, sheltered): 3-b/B, 3-d/A — 2 parents

`4-j` is held in reserve for an act-III collapse.

When writing `4-c` (combat) the prose must work whether the player initiated violence (3-f), is interrupted in their silence (3-e), or has the wardens charging back at them (3-d). When writing `4-e` the wounded man is variously: abandoned alive in the scrub (3-b), abandoned on the road during a fight (3-f), killed by the player (3-g), or never met again after a clean off-road escape (3-h). Open `4-e` on a beat of solitude and let the prior choice be remembered in the player's gut, not narrated.

## Next to generate (level 4)

Nine children pointed at, none yet written:

| node | summary | parents |
| ---- | ------- | ------- |
| 4-a | Sadaiziche, south gate to warden-house, noon bell. Lie under examination. | 3-a, 3-c, 3-e, 3-i |
| 4-b | Asha's shepherd-fire on the oak slope. Hospitality and questions. | 3-a, 3-b, 3-d, 3-h |
| 4-c | Combat on the imperial road. 2-3 wardens, mud, the wounded man as factor or stake. | 3-d, 3-e, 3-f |
| 4-d | Under warden escort. The slow ride to wherever the empire decides to take you. | 3-a, 3-c, 3-f |
| 4-e | Alone east on the road, a death behind you. The country indifferent. | 3-b, 3-f, 3-g, 3-h |
| 4-f | The shrine of Vabum revisited. What the wardens do at a folk-god's pillar. | 3-c, 3-e, 3-g |
| 4-g | The vellum unfolded. Three lines you cannot read at first — and then you can. | 3-h, 3-i |
| 4-h | Sadaiziche from the west — the river-path, the dye-houses, the back-way in. | 3-g, 3-i |
| 4-i | The wounded man speaks: a name, a destination, a debt. | 3-b, 3-d |

When writing each level-4 node, **read all parents in its inbound set** and ensure no opening detail conflicts with any of them. Pay particular attention to who is alive (the wounded man), what the player is carrying (silver / phial / vellum present only on rob-paths), and whether the player is gendered-distinct (level 3 is already gender-agnostic, so this is mostly settled).

## Open setting notes

- World: **Coulesia** (Azgaar map under `map/`). Story is set in the **Khvordemian Empire** (state 3, Persian culture).
- Time of year: late autumn, year of the Black Sun.
- Geography: imperial road between **Rabad** (a small town, pop. ~6) and **Sadaiziche** (a larger town, pop. ~13.5). The player wakes ~½ farsang east of Rabad. Sadaiziche has a south gate (the warden-house is by it) and a west wall along a river with dye-houses.
- Religion: **Persian Church** (organized monotheism, state-favored, the wardens ride under its writ), **Old Vabumism** (folk polytheism, tolerated — Vabum the Cup-Bearer's roadside shrine), **Mardesran Schism** (heresy, persecuted — the silver fish-eating-its-own-tail charm).
- The wardens: three. Leader is older, narrow-faced, "slow eyes." Third rider is silent, observant ("fine boots for a ditch"). Youngest is inexperienced — this is the first body he has had to find for the work; his shaken composure is a recurring lever in level 3 (especially in 3-e and 3-f). All three wear the **white shoulder-cord** of church writ.
- The wounded man: a **Mardesran**. Calls the player *baraadar* / *khahar* (brother / sister). Uses **Khoda** for the god of the road — a deliberately old, pre-church word. In 3-b he references **a shepherd called Asha** above the second vineyard, "who has fed us before" — collective *us* — implying a Mardesran network in the hills. In 3-g he dies whispering *Bismi Khoda* and turns his head to give a clean angle, suggesting prior familiarity with execution.
- The player's pre-amnesia identity: callused/working body; good Persian boots that fit "a little too well today and a little too loosely yesterday" (3-i — fits the "boots possibly too large" hint from earlier); hidden wrist scar; foreign blood on a knuckle. **Muscle-memory revealed in level 3**: a folded knife in the coat lining (used in 3-g to cut the charm, and in 3-f to hold the youngest); a "cold practised thing" in the hands when violence offers; a steady, accustomed posture for warden-questioning; (female 2-e) a fingers-without-thought re-braiding under threat; a name *Daiyan* that surfaces on the tongue in 3-a without context.
- Items on the rob-path: silver Mardesran fish-and-tail charm; wax-stoppered clay phial; folded vellum with three lines the player cannot read in dawn light; copper ring (no stone); whetstone; three additional small coins (now seven total).

## How to continue

Read [`produce.txt`](produce.txt) before writing the next nodes. For each level-4 node, read **all** parents in its inbound set (see table above) and the relevant ALIGNMENT/map files.
