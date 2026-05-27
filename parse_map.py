"""
Parse the Azgaar Fantasy Map Generator JSON for Coulesia into a folder
of smaller JSON files suitable for a top-down 2D web browser game.

Design goals:
  * Spatial chunking of the map (64x64 px chunks -> 23x13 = 299 chunks)
    so the game can lazy-load only the chunks near the player.
  * Per-entity files for large quest-relevant entities (burgs, states,
    notes) so they can be loaded on demand.
  * Reference files (cultures, religions, biomes, ...) loaded once at
    boot.
  * A manifest.json that tells the game what exists where and how the
    chunk grid maps to world coordinates.

The output is consumed by a separate game engine; this script is purely
a data preparation step. Re-run it whenever the source JSON changes.

Usage:
    python3 parse_map.py [source.json] [out_dir]

Defaults to "Coulesia Full 2026-05-27-22-47.json" and ./map/.
"""

from __future__ import annotations

import json
import os
import re
import shutil
import sys
from pathlib import Path
from typing import Any

CHUNK_SIZE = 64  # pixels per chunk side (source-map pixels)

REPO_ROOT = Path(__file__).resolve().parent
DEFAULT_SRC = REPO_ROOT / "Coulesia Full 2026-05-27-22-47.json"
DEFAULT_OUT = REPO_ROOT / "map"


# ---------------------------------------------------------------------------
# Generic helpers
# ---------------------------------------------------------------------------


def write_json(path: Path, data: Any, *, pretty: bool = False) -> int:
    """Write `data` to `path` as JSON and return the byte size.

    Uses ensure_ascii=True so any stray unpaired surrogates from the
    source data (Azgaar's exports sometimes contain them in note
    legends) round-trip as \\uXXXX escapes instead of crashing the
    utf-8 writer.
    """
    path.parent.mkdir(parents=True, exist_ok=True)
    if pretty:
        text = json.dumps(data, ensure_ascii=True, indent=2)
    else:
        text = json.dumps(data, ensure_ascii=True, separators=(",", ":"))
    path.write_text(text, encoding="utf-8")
    return path.stat().st_size


def slugify(value: str) -> str:
    """Filesystem-friendly id."""
    value = value.strip().lower()
    value = re.sub(r"[^a-z0-9._-]+", "-", value)
    value = re.sub(r"-{2,}", "-", value).strip("-")
    return value or "item"


def drop_keys(d: dict, keys: set[str]) -> dict:
    return {k: v for k, v in d.items() if k not in keys}


# ---------------------------------------------------------------------------
# Spatial chunking
# ---------------------------------------------------------------------------


def chunk_coords(x: float, y: float, *, chunk_size: int, chunks_x: int, chunks_y: int) -> tuple[int, int]:
    cx = min(int(x // chunk_size), chunks_x - 1)
    cy = min(int(y // chunk_size), chunks_y - 1)
    cx = max(cx, 0)
    cy = max(cy, 0)
    return cx, cy


# ---------------------------------------------------------------------------
# Main parse
# ---------------------------------------------------------------------------


def parse(src_path: Path, out_dir: Path) -> None:
    print(f"reading {src_path}")
    with src_path.open("r", encoding="utf-8") as f:
        data = json.load(f)

    if out_dir.exists():
        shutil.rmtree(out_dir)
    out_dir.mkdir(parents=True)

    info = data["info"]
    settings = data["settings"]
    coords = data["mapCoordinates"]
    pack = data["pack"]
    grid = data["grid"]
    biomes = data["biomesData"]
    notes = data["notes"]

    width = info["width"]
    height = info["height"]
    chunks_x = (width + CHUNK_SIZE - 1) // CHUNK_SIZE
    chunks_y = (height + CHUNK_SIZE - 1) // CHUNK_SIZE

    print(f"world: {width}x{height} px, chunks {chunks_x}x{chunks_y} @ {CHUNK_SIZE}px")

    sizes: dict[str, int] = {}

    # -------------------------------------------------------------------
    # World metadata
    # -------------------------------------------------------------------
    world_dir = out_dir / "world"
    sizes["world/info.json"] = write_json(
        world_dir / "info.json",
        {
            "name": info["mapName"],
            "seed": info["seed"],
            "mapId": info["mapId"],
            "version": info["version"],
            "exportedAt": info["exportedAt"],
            "width": width,
            "height": height,
            "source": "Azgaar's Fantasy Map Generator",
        },
        pretty=True,
    )

    sizes["world/settings.json"] = write_json(
        world_dir / "settings.json",
        {
            # Distance & scale settings that matter for in-game distances/weather.
            "distanceUnit": settings.get("distanceUnit"),
            "distanceScale": settings.get("distanceScale"),
            "areaUnit": settings.get("areaUnit"),
            "heightUnit": settings.get("heightUnit"),
            "heightExponent": settings.get("heightExponent"),
            "temperatureScale": settings.get("temperatureScale"),
            "populationRate": settings.get("populationRate"),
            "urbanization": settings.get("urbanization"),
            "mapSize": settings.get("mapSize"),
            "latitude": settings.get("latitude"),
            "longitude": settings.get("longitude"),
            "prec": settings.get("prec"),
        },
        pretty=True,
    )

    sizes["world/coordinates.json"] = write_json(
        world_dir / "coordinates.json", coords, pretty=True
    )

    # -------------------------------------------------------------------
    # Biomes (reference table indexed by biome id)
    # -------------------------------------------------------------------
    biome_list = []
    for i in biomes["i"]:
        biome_list.append(
            {
                "i": i,
                "name": biomes["name"][i],
                "color": biomes["color"][i],
                "habitability": biomes["habitability"][i],
                "movementCost": biomes["cost"][i],
                "iconsDensity": biomes["iconsDensity"][i],
                "icons": biomes["icons"][i],
            }
        )
    sizes["biomes.json"] = write_json(out_dir / "biomes.json", biome_list, pretty=True)

    # -------------------------------------------------------------------
    # Features (oceans / lakes / islands)
    # -------------------------------------------------------------------
    features = []
    for f in pack["features"]:
        if not isinstance(f, dict):
            continue
        features.append(
            {
                "i": f.get("i"),
                "type": f.get("type"),
                "land": f.get("land"),
                "border": f.get("border"),
                "cells": f.get("cells"),
                "firstCell": f.get("firstCell"),
                "area": f.get("area"),
                "height": f.get("height"),
                "group": f.get("group"),
                "name": f.get("name"),
            }
        )
    sizes["features.json"] = write_json(out_dir / "features.json", features, pretty=True)

    # -------------------------------------------------------------------
    # Cultures, religions
    # -------------------------------------------------------------------
    cultures = [drop_keys(c, {"shield"}) if isinstance(c, dict) else c for c in pack["cultures"]]
    sizes["cultures.json"] = write_json(out_dir / "cultures.json", cultures, pretty=True)

    religions = pack["religions"]
    sizes["religions.json"] = write_json(out_dir / "religions.json", religions, pretty=True)

    # -------------------------------------------------------------------
    # Provinces (drop heraldry COA, keep gameplay+display)
    # -------------------------------------------------------------------
    provinces_out = []
    for p in pack["provinces"]:
        if not isinstance(p, dict):
            provinces_out.append(p)
            continue
        provinces_out.append(drop_keys(p, {"coa"}))
    sizes["provinces.json"] = write_json(out_dir / "provinces.json", provinces_out, pretty=True)

    # -------------------------------------------------------------------
    # States: per-state file (diplomacy text is large) + slim index
    # -------------------------------------------------------------------
    states_dir = out_dir / "states"
    state_index = []
    for s in pack["states"]:
        if not isinstance(s, dict):
            continue
        i = s["i"]
        slim = {
            "i": i,
            "name": s.get("name"),
            "fullName": s.get("fullName"),
            "form": s.get("form"),
            "formName": s.get("formName"),
            "type": s.get("type"),
            "color": s.get("color"),
            "capital": s.get("capital"),
            "center": s.get("center"),
            "culture": s.get("culture"),
            "neighbors": s.get("neighbors"),
            "expansionism": s.get("expansionism"),
            "urban": s.get("urban"),
            "rural": s.get("rural"),
            "burgs": s.get("burgs"),
            "area": s.get("area"),
            "cells": s.get("cells"),
            "alert": s.get("alert"),
            "pole": s.get("pole"),
            "provinces": s.get("provinces"),
        }
        full = drop_keys(s, {"coa"})
        sizes[f"states/{i}.json"] = write_json(states_dir / f"{i}.json", full, pretty=True)
        state_index.append(slim)
    sizes["states/index.json"] = write_json(states_dir / "index.json", state_index, pretty=True)

    # -------------------------------------------------------------------
    # Rivers, zones
    # -------------------------------------------------------------------
    sizes["rivers.json"] = write_json(out_dir / "rivers.json", pack["rivers"], pretty=True)
    sizes["zones.json"] = write_json(out_dir / "zones.json", pack["zones"], pretty=True)

    # -------------------------------------------------------------------
    # Markers (point-of-interest icons) -- assign chunk for spatial lookup
    # -------------------------------------------------------------------
    markers_by_chunk: dict[tuple[int, int], list[int]] = {}
    markers_out = []
    for m in pack["markers"]:
        if not isinstance(m, dict):
            continue
        cx, cy = chunk_coords(m["x"], m["y"], chunk_size=CHUNK_SIZE, chunks_x=chunks_x, chunks_y=chunks_y)
        m_out = dict(m)
        m_out["chunk"] = [cx, cy]
        markers_out.append(m_out)
        markers_by_chunk.setdefault((cx, cy), []).append(m["i"])
    sizes["markers.json"] = write_json(out_dir / "markers.json", markers_out, pretty=True)

    # -------------------------------------------------------------------
    # Notes (lore) -- one file per note, indexed
    # -------------------------------------------------------------------
    notes_dir = out_dir / "notes"
    note_index = []
    for n in notes:
        nid = n.get("id") or f"note-{len(note_index)}"
        slug = slugify(nid)
        sizes[f"notes/{slug}.json"] = write_json(notes_dir / f"{slug}.json", n, pretty=True)
        note_index.append({"id": nid, "name": n.get("name"), "file": f"notes/{slug}.json"})
    sizes["notes/index.json"] = write_json(notes_dir / "index.json", note_index, pretty=True)

    # -------------------------------------------------------------------
    # Burgs -- per-burg file + slim index. Group by chunk for fast spatial
    # queries.
    # -------------------------------------------------------------------
    burgs_dir = out_dir / "burgs"
    burg_index = []
    burgs_by_chunk: dict[tuple[int, int], list[int]] = {}
    for b in pack["burgs"]:
        if not isinstance(b, dict):
            continue
        i = b["i"]
        cx, cy = chunk_coords(b["x"], b["y"], chunk_size=CHUNK_SIZE, chunks_x=chunks_x, chunks_y=chunks_y)
        b_out = drop_keys(b, {"coa"})
        b_out["chunk"] = [cx, cy]
        sizes[f"burgs/{i}.json"] = write_json(burgs_dir / f"{i}.json", b_out, pretty=True)
        burg_index.append(
            {
                "i": i,
                "name": b.get("name"),
                "cell": b.get("cell"),
                "x": b.get("x"),
                "y": b.get("y"),
                "state": b.get("state"),
                "culture": b.get("culture"),
                "capital": b.get("capital"),
                "port": b.get("port"),
                "population": b.get("population"),
                "type": b.get("type"),
                "feature": b.get("feature"),
                "group": b.get("group"),
                "chunk": [cx, cy],
            }
        )
        burgs_by_chunk.setdefault((cx, cy), []).append(i)
    sizes["burgs/index.json"] = write_json(burgs_dir / "index.json", burg_index, pretty=True)

    # -------------------------------------------------------------------
    # Routes -- keep one file, but build a chunk -> route-id index so the
    # game can ask "which roads touch my current chunk?"
    # -------------------------------------------------------------------
    routes_out = []
    routes_by_chunk: dict[tuple[int, int], set[int]] = {}
    for r in pack["routes"]:
        if not isinstance(r, dict):
            continue
        rid = r["i"]
        # Slim points: [x, y, cellId] tuples are kept as-is.
        pts = r.get("points", [])
        chunks_touched: set[tuple[int, int]] = set()
        for p in pts:
            if len(p) < 2:
                continue
            cx, cy = chunk_coords(p[0], p[1], chunk_size=CHUNK_SIZE, chunks_x=chunks_x, chunks_y=chunks_y)
            chunks_touched.add((cx, cy))
            routes_by_chunk.setdefault((cx, cy), set()).add(rid)
        routes_out.append(
            {
                "i": rid,
                "group": r.get("group"),
                "feature": r.get("feature"),
                "points": pts,
                "chunks": sorted(list(chunks_touched)),
            }
        )
    sizes["routes.json"] = write_json(out_dir / "routes.json", routes_out, pretty=True)

    # -------------------------------------------------------------------
    # Cells + vertices -- chunked spatially. This is the bulk of the data
    # the game will stream as the player walks the map.
    #
    # For each chunk we include:
    #   - cells whose centre p falls inside the chunk
    #   - the polygon vertices those cells reference, deduplicated
    #     within the chunk (vertex ids that resolve in another chunk are
    #     still emitted here so the chunk is self-rendering)
    #   - temp/prec sampled from grid cells (denormalised, so the grid
    #     can be discarded entirely)
    #   - quick lookups: burg ids, marker ids, route ids touching this
    #     chunk
    # -------------------------------------------------------------------
    chunks_dir = out_dir / "chunks"

    # Pre-index temp/prec by grid cell id so we can denormalise.
    grid_cells = grid["cells"]

    # Bucket pack cells by chunk.
    cells_by_chunk: dict[tuple[int, int], list[dict]] = {}
    cell_to_chunk: dict[int, tuple[int, int]] = {}
    for c in pack["cells"]:
        if not isinstance(c, dict):
            continue
        cx, cy = chunk_coords(
            c["p"][0],
            c["p"][1],
            chunk_size=CHUNK_SIZE,
            chunks_x=chunks_x,
            chunks_y=chunks_y,
        )
        cells_by_chunk.setdefault((cx, cy), []).append(c)
        cell_to_chunk[c["i"]] = (cx, cy)

    pack_vertices = pack["vertices"]

    chunk_index = {}
    for cy in range(chunks_y):
        for cx in range(chunks_x):
            key = (cx, cy)
            cells_in_chunk = cells_by_chunk.get(key, [])
            chunk_cells_out = []
            vertex_ids_needed: set[int] = set()
            for c in cells_in_chunk:
                gidx = c.get("g")
                g_cell = grid_cells[gidx] if gidx is not None and gidx < len(grid_cells) else None
                temp = g_cell.get("temp") if isinstance(g_cell, dict) else None
                prec = g_cell.get("prec") if isinstance(g_cell, dict) else None
                cell_out = {
                    "i": c["i"],
                    "p": c["p"],
                    "v": c.get("v", []),
                    "c": c.get("c", []),
                    "h": c.get("h"),  # elevation 0-100, >=20 is land
                    "area": c.get("area"),
                    "f": c.get("f"),  # feature id
                    "t": c.get("t"),  # coast distance (-2 deep, -1 water, 1 coast, +n inland)
                    "haven": c.get("haven") or 0,
                    "harbor": c.get("harbor") or 0,
                    "fl": c.get("fl") or 0,  # water flux
                    "r": c.get("r") or 0,  # river id
                    "conf": c.get("conf") or 0,  # confluence flux
                    "biome": c.get("biome"),
                    "s": c.get("s") or 0,  # suitability for settlement
                    "pop": c.get("pop") or 0,
                    "burg": c.get("burg") or 0,
                    "culture": c.get("culture") or 0,
                    "state": c.get("state") or 0,
                    "religion": c.get("religion") or 0,
                    "province": c.get("province") or 0,
                    "temp": temp,
                    "prec": prec,
                }
                if c.get("routes"):
                    cell_out["routes"] = c["routes"]
                chunk_cells_out.append(cell_out)
                for vid in c.get("v", []):
                    if vid >= 0:
                        vertex_ids_needed.add(vid)

            # Build a compact vertex map for this chunk. The renderer can
            # look up vertex coordinates by id when drawing a cell polygon.
            vertices_out = {}
            for vid in sorted(vertex_ids_needed):
                if 0 <= vid < len(pack_vertices):
                    v = pack_vertices[vid]
                    if isinstance(v, dict):
                        vertices_out[str(vid)] = v["p"]

            burgs_here = sorted(burgs_by_chunk.get(key, []))
            markers_here = sorted(markers_by_chunk.get(key, []))
            routes_here = sorted(list(routes_by_chunk.get(key, set())))

            chunk_doc = {
                "chunk": [cx, cy],
                "bounds": [
                    cx * CHUNK_SIZE,
                    cy * CHUNK_SIZE,
                    min((cx + 1) * CHUNK_SIZE, width),
                    min((cy + 1) * CHUNK_SIZE, height),
                ],
                "cells": chunk_cells_out,
                "vertices": vertices_out,
                "burgs": burgs_here,
                "markers": markers_here,
                "routes": routes_here,
            }
            fname = f"{cx}_{cy}.json"
            file_size = write_json(chunks_dir / fname, chunk_doc)
            sizes[f"chunks/{fname}"] = file_size
            chunk_index[f"{cx},{cy}"] = {
                "file": f"chunks/{fname}",
                "cells": len(chunk_cells_out),
                "burgs": len(burgs_here),
                "markers": len(markers_here),
                "routes": len(routes_here),
                "bytes": file_size,
            }

    # Cell-id -> chunk lookup so the game can map a cell id to a chunk file.
    cell_lookup = {str(cid): list(chunk) for cid, chunk in cell_to_chunk.items()}
    sizes["chunks/cell_lookup.json"] = write_json(
        chunks_dir / "cell_lookup.json", cell_lookup
    )
    sizes["chunks/index.json"] = write_json(
        chunks_dir / "index.json",
        {
            "chunkSize": CHUNK_SIZE,
            "chunksX": chunks_x,
            "chunksY": chunks_y,
            "width": width,
            "height": height,
            "chunks": chunk_index,
        },
        pretty=False,
    )

    # -------------------------------------------------------------------
    # Top-level manifest -- the single entrypoint a game client loads
    # first to discover everything else.
    # -------------------------------------------------------------------
    manifest = {
        "schema": 1,
        "name": info["mapName"],
        "world": {
            "width": width,
            "height": height,
            "chunkSize": CHUNK_SIZE,
            "chunksX": chunks_x,
            "chunksY": chunks_y,
        },
        "files": {
            "info": "world/info.json",
            "settings": "world/settings.json",
            "coordinates": "world/coordinates.json",
            "biomes": "biomes.json",
            "features": "features.json",
            "cultures": "cultures.json",
            "religions": "religions.json",
            "provinces": "provinces.json",
            "rivers": "rivers.json",
            "zones": "zones.json",
            "markers": "markers.json",
            "routes": "routes.json",
            "statesIndex": "states/index.json",
            "stateDir": "states/",
            "burgsIndex": "burgs/index.json",
            "burgDir": "burgs/",
            "notesIndex": "notes/index.json",
            "noteDir": "notes/",
            "chunksIndex": "chunks/index.json",
            "chunkDir": "chunks/",
            "cellLookup": "chunks/cell_lookup.json",
        },
        "counts": {
            "cells": sum(len(v) for v in cells_by_chunk.values()),
            "burgs": len(burg_index),
            "states": len(state_index),
            "provinces": sum(1 for p in provinces_out if isinstance(p, dict)),
            "religions": sum(1 for r in religions if isinstance(r, dict)),
            "cultures": sum(1 for c in cultures if isinstance(c, dict)),
            "rivers": len(pack["rivers"]),
            "routes": len(routes_out),
            "markers": len(markers_out),
            "zones": len(pack["zones"]),
            "notes": len(notes),
            "features": sum(1 for f in features if isinstance(f, dict)),
            "biomes": len(biome_list),
        },
    }
    sizes["manifest.json"] = write_json(out_dir / "manifest.json", manifest, pretty=True)

    # -------------------------------------------------------------------
    # Report
    # -------------------------------------------------------------------
    total = sum(sizes.values())
    file_count = len(sizes)
    print(f"\nwrote {file_count} files, total {total / 1024:.1f} KB ({total} bytes)")
    largest = sorted(sizes.items(), key=lambda kv: -kv[1])[:10]
    print("largest files:")
    for name, sz in largest:
        print(f"  {sz / 1024:>8.1f} KB  {name}")


def main(argv: list[str]) -> int:
    src = Path(argv[1]) if len(argv) > 1 else DEFAULT_SRC
    out = Path(argv[2]) if len(argv) > 2 else DEFAULT_OUT
    if not src.exists():
        print(f"source file not found: {src}", file=sys.stderr)
        return 1
    parse(src, out)
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
