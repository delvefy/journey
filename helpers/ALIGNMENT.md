# Alignment system

Two axes, each tracked as a signed integer in `localStorage` under `coulesia.story.v1`:

- **law** — positive is Lawful, negative is Chaotic
- **good** — positive is Good, negative is Evil

A choice button declares its alignment nudge via `data-law` and `data-good` attributes. Typical deltas are ±1 to ±3 per choice. Avoid deltas larger than 3 except for the final beat of a major moral commitment.

## Bucketing

In `assets/story.js`, `alignmentLabel(state)` buckets each axis using threshold `T = 2`:

| value          | bucket   |
| -------------- | -------- |
| `≥ +T`         | Lawful / Good   |
| `> -T and < T` | Neutral         |
| `≤ -T`         | Chaotic / Evil  |

The combined label is one of the nine D&D-style alignments below. (`Neutral × Neutral` collapses to **True Neutral**.)

## The nine alignments

| Label | Compass description | Archetype |
| ----- | ------------------- | --------- |
| **Lawful Good**     | Honor, truth, helping within laws/codes. | Superman, classic Paladin |
| **Neutral Good**    | Helping others directly, not bound by rules. | Spider-Man, Robin Hood |
| **Chaotic Good**    | Own moral compass; right action regardless of law. | Han Solo |
| **Lawful Neutral**  | Order and code above outcome. | Judge Dredd |
| **True Neutral**    | Balance, self-interest, distance from cosmic battles. | Treebeard |
| **Chaotic Neutral** | Personal freedom; rejects authority on whim. | Deadpool |
| **Lawful Evil**     | Structures, hierarchies, and rules used to oppress. | Darth Vader |
| **Neutral Evil**    | Pure self-interest and greed; no grand creed. | Jafar |
| **Chaotic Evil**    | Malice and disregard for all laws and lives. | The Joker |

## How to write choices

For each node, the three choices should — in aggregate — sample at least three different parts of the alignment grid. Don't write three "good" choices with only mild differences. Examples of healthy three-way splits:

- **Lawful Good / Chaotic Good / Neutral Evil** — help within the rules; help against the rules; rob and walk on.
- **Lawful Neutral / Chaotic Good / Lawful Evil** — follow the order; defy for mercy; follow the order for profit.
- **True Neutral / Chaotic Neutral / Neutral Good** — keep walking; cause a scene; help quietly.

Each choice's `data-law` and `data-good` should reflect the *flavor* of that choice, not the consequences (which are paid out in the destination node). A character who helps a heretic gets a `good +2` whether or not it turns out badly later.

## Sample deltas

| Choice flavor | law | good |
| ------------- | --- | ---- |
| Help within the laws of the empire           | +2 | +2 |
| Help against the laws of the empire          | -2 | +2 |
| Help quietly, no public position             |  0 | +2 |
| Stand by, indifferent                        |  0 | -1 |
| Inform on a heretic to imperial authority    | +2 | -1 |
| Rob a dying man and flee                     | -1 | -3 |
| Murder for gain                              | -1 | -4 |
| Honor an oath even at personal cost          | +3 |  0 |
| Break a sworn promise on a whim              | -3 |  0 |

Tune deltas to the weight of the moment. Early-game nudges are smaller (±1 to ±2). Mid-game commitments may be ±3. Reserve ±4 for truly definitive moments.
