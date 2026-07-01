#!/usr/bin/env python3
"""
build.py — the static-site generator for the LOOM OF HEAVENS wiki.

Reads article SOURCE from   data/articles/<universe>/<slug>.md
Writes static HTML to        articles/<universe>/<slug>.html
Also emits:                  index.html, articles/<universe>/index.html,
                             search-index.json

No third-party dependencies. Run it after adding or editing any article:

    python3 tools/build.py            # build everything
    python3 tools/build.py --check    # build + report dead wiki-links

See tools/write.txt for the authoring guide (frontmatter fields, markdown
subset, cross-linking rules).
"""

from __future__ import annotations

import html
import json
import re
import sys
from pathlib import Path

# --------------------------------------------------------------------------
# Paths — repo root is the parent of the tools/ directory this file lives in.
# --------------------------------------------------------------------------
ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data" / "articles"
UNIVERSES_JSON = ROOT / "data" / "universes.json"
OUT_ARTICLES = ROOT / "articles"
SITE_TITLE = "The Loom of Heavens"
RECENT_COUNT = 12


# --------------------------------------------------------------------------
# Frontmatter parsing
# --------------------------------------------------------------------------
def parse_frontmatter(text: str):
    """Split a `--- ... ---` frontmatter block from the markdown body.

    Supports scalars (key: value) and simple inline lists (key: [a, b, c]).
    Returns (meta: dict, body: str).
    """
    if not text.startswith("---"):
        return {}, text
    end = text.find("\n---", 3)
    if end == -1:
        return {}, text
    header = text[3:end].strip("\n")
    body = text[end + 4:].lstrip("\n")

    meta = {}
    for line in header.splitlines():
        line = line.rstrip()
        if not line or line.lstrip().startswith("#"):
            continue
        if ":" not in line:
            continue
        key, _, value = line.partition(":")
        key = key.strip()
        value = value.strip()
        if value.startswith("[") and value.endswith("]"):
            inner = value[1:-1].strip()
            meta[key] = [v.strip().strip("'\"") for v in inner.split(",") if v.strip()]
        else:
            meta[key] = value.strip("'\"")
    return meta, body


# --------------------------------------------------------------------------
# Minimal markdown renderer (dependency-free, wiki-flavoured)
# --------------------------------------------------------------------------
_CODE_RE = re.compile(r"`([^`]+)`")
_WIKILINK_RE = re.compile(r"\[\[([^\]]+)\]\]")
_LINK_RE = re.compile(r"\[([^\]]+)\]\(([^)]+)\)")
_BOLD_RE = re.compile(r"\*\*([^*]+)\*\*")
_ITALIC_RE = re.compile(r"(?<!\*)\*([^*]+)\*(?!\*)")


def render_inline(text: str, resolve) -> str:
    """Escape then apply inline markdown. `resolve(slug)` -> url or None."""
    out = html.escape(text, quote=False)

    # inline code first, so its contents are not further transformed
    code_spans = []

    def _stash_code(m):
        code_spans.append(m.group(1))
        return f"\x00CODE{len(code_spans) - 1}\x00"

    out = _CODE_RE.sub(_stash_code, out)

    # wiki-links: [[slug]] or [[slug|Display text]]
    def _wiki(m):
        raw = m.group(1)
        slug, _, disp = raw.partition("|")
        slug = slug.strip()
        disp = (disp.strip() or slug)
        url = resolve(slug)
        if url:
            return f'<a href="{url}">{disp}</a>'
        return f'<a class="dead-link" title="page not yet written">{disp}</a>'

    out = _WIKILINK_RE.sub(_wiki, out)

    # standard markdown links
    out = _LINK_RE.sub(r'<a href="\2">\1</a>', out)
    out = _BOLD_RE.sub(r"<strong>\1</strong>", out)
    out = _ITALIC_RE.sub(r"<em>\1</em>", out)

    for i, code in enumerate(code_spans):
        out = out.replace(f"\x00CODE{i}\x00", f"<code>{code}</code>")
    return out


def render_markdown(body: str, resolve) -> str:
    lines = body.splitlines()
    html_parts: list[str] = []
    i = 0
    n = len(lines)

    def flush_paragraph(buf):
        if buf:
            html_parts.append("<p>" + render_inline(" ".join(buf), resolve) + "</p>")

    while i < n:
        line = lines[i]
        stripped = line.strip()

        if not stripped:
            i += 1
            continue

        # horizontal rule
        if re.fullmatch(r"-{3,}", stripped):
            html_parts.append("<hr>")
            i += 1
            continue

        # heading
        m = re.match(r"(#{1,6})\s+(.*)", stripped)
        if m:
            level = len(m.group(1))
            text = render_inline(m.group(2).strip(), resolve)
            anchor = slugify(m.group(2).strip())
            html_parts.append(f'<h{level} id="{anchor}">{text}</h{level}>')
            i += 1
            continue

        # blockquote (used for flavor pull-quotes)
        if stripped.startswith(">"):
            quote = []
            while i < n and lines[i].strip().startswith(">"):
                quote.append(lines[i].strip()[1:].strip())
                i += 1
            html_parts.append(
                "<blockquote>" + render_inline(" ".join(quote), resolve) + "</blockquote>"
            )
            continue

        # unordered list
        if re.match(r"[-*]\s+", stripped):
            items = []
            while i < n and re.match(r"[-*]\s+", lines[i].strip()):
                items.append(render_inline(re.sub(r"^[-*]\s+", "", lines[i].strip()), resolve))
                i += 1
            html_parts.append("<ul>" + "".join(f"<li>{it}</li>" for it in items) + "</ul>")
            continue

        # ordered list
        if re.match(r"\d+\.\s+", stripped):
            items = []
            while i < n and re.match(r"\d+\.\s+", lines[i].strip()):
                items.append(render_inline(re.sub(r"^\d+\.\s+", "", lines[i].strip()), resolve))
                i += 1
            html_parts.append("<ol>" + "".join(f"<li>{it}</li>" for it in items) + "</ol>")
            continue

        # paragraph (consume consecutive plain lines)
        buf = []
        while i < n and lines[i].strip() and not _starts_block(lines[i].strip()):
            buf.append(lines[i].strip())
            i += 1
        flush_paragraph(buf)

    return "\n".join(html_parts)


def _starts_block(stripped: str) -> bool:
    return bool(
        re.fullmatch(r"-{3,}", stripped)
        or re.match(r"#{1,6}\s+", stripped)
        or stripped.startswith(">")
        or re.match(r"[-*]\s+", stripped)
        or re.match(r"\d+\.\s+", stripped)
    )


# --------------------------------------------------------------------------
# Helpers
# --------------------------------------------------------------------------
def slugify(text: str) -> str:
    text = text.lower().strip()
    text = re.sub(r"[^\w\s-]", "", text)
    text = re.sub(r"[\s_]+", "-", text)
    return text.strip("-")


def load_universes() -> dict:
    if UNIVERSES_JSON.exists():
        return json.loads(UNIVERSES_JSON.read_text(encoding="utf-8"))
    return {}


# --------------------------------------------------------------------------
# HTML templates
# --------------------------------------------------------------------------
THEME_INIT = (
    "<script>(function(){try{var t=localStorage.getItem('theme');"
    "if(!t){t=matchMedia('(prefers-color-scheme: dark)').matches?'dark':'light';}"
    "document.documentElement.setAttribute('data-theme',t);}catch(e){}})();</script>"
)


def page_shell(title: str, body: str, depth: int, extra_head: str = "") -> str:
    """Wrap body in the site chrome. `depth` = how many ../ to reach root."""
    up = "../" * depth
    return f"""<!doctype html>
<html lang="en" data-theme="light">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(title)} · {SITE_TITLE}</title>
{THEME_INIT}
<link rel="stylesheet" href="{up}assets/style.css">
{extra_head}
</head>
<body>
<header class="site-header">
  <a class="brand" href="{up}index.html">✦ {SITE_TITLE}</a>
  <button class="theme-toggle" type="button" aria-label="Toggle colour theme">◐</button>
</header>
<main class="content">
{body}
</main>
<footer class="site-footer">
  <span>The Loom of Heavens — an ever-expanding multiverse wiki.</span>
</footer>
<script src="{up}assets/theme.js"></script>
</body>
</html>
"""


def render_article_page(art: dict, universes: dict) -> str:
    uni = art["universe"]
    uni_meta = universes.get(uni, {})
    uni_name = uni_meta.get("name", uni.replace("-", " ").title())

    meta_bits = []
    if art.get("type"):
        meta_bits.append(f'<span class="pill">{html.escape(art["type"])}</span>')
    if art.get("tier"):
        meta_bits.append(f'<span class="pill pill-tier">{html.escape(art["tier"])}</span>')

    tags_html = ""
    if art.get("tags"):
        tags_html = '<div class="tags">' + "".join(
            f'<span class="tag">{html.escape(t)}</span>' for t in art["tags"]
        ) + "</div>"

    breadcrumb = (
        f'<nav class="breadcrumb"><a href="../../index.html">Home</a> '
        f'<span>›</span> <a href="index.html">{html.escape(uni_name)}</a> '
        f'<span>›</span> <span>{html.escape(art["title"])}</span></nav>'
    )

    body = f"""{breadcrumb}
<article>
  <h1 class="article-title">{html.escape(art["title"])}</h1>
  <div class="article-meta">{' '.join(meta_bits)}</div>
  {f'<p class="summary">{html.escape(art["summary"])}</p>' if art.get("summary") else ''}
  <hr>
  {art["html"]}
  {tags_html}
</article>
"""
    return page_shell(art["title"], body, depth=2)


def render_universe_index(uni: str, arts: list, universes: dict) -> str:
    uni_meta = universes.get(uni, {})
    uni_name = uni_meta.get("name", uni.replace("-", " ").title())
    tagline = uni_meta.get("tagline", "")
    tier = uni_meta.get("tier", "")

    cards = []
    for a in sorted(arts, key=lambda x: x["title"].lower()):
        summary = f'<p>{html.escape(a["summary"])}</p>' if a.get("summary") else ""
        cards.append(
            f'<li><a href="{a["slug"]}.html"><span class="card-title">{html.escape(a["title"])}</span>'
            f'<span class="card-type">{html.escape(a.get("type",""))}</span></a>'
            f'{summary}</li>'
        )

    body = f"""<nav class="breadcrumb"><a href="../../index.html">Home</a> <span>›</span> <span>{html.escape(uni_name)}</span></nav>
<h1 class="article-title">{html.escape(uni_name)}</h1>
{f'<div class="article-meta"><span class="pill pill-tier">{html.escape(tier)}</span></div>' if tier else ''}
{f'<p class="summary">{html.escape(tagline)}</p>' if tagline else ''}
<hr>
<ul class="card-list">
{''.join(cards)}
</ul>
"""
    return page_shell(uni_name, body, depth=2)


def render_home(articles: list, universes: dict) -> str:
    recent = sorted(articles, key=lambda a: (a.get("date", ""), a["title"]), reverse=True)[:RECENT_COUNT]

    recent_html = []
    for a in recent:
        recent_html.append(
            f'<li><a href="{a["url"]}"><span class="card-title">{html.escape(a["title"])}</span>'
            f'<span class="card-type">{html.escape(a.get("type",""))}</span></a>'
            f'<span class="card-uni">{html.escape(universes.get(a["universe"],{}).get("name", a["universe"]))}</span></li>'
        )

    # universes present in the build (with at least one article)
    present = sorted({a["universe"] for a in articles})
    uni_cards = []
    for u in present:
        meta = universes.get(u, {})
        name = meta.get("name", u.replace("-", " ").title())
        tagline = meta.get("tagline", "")
        count = sum(1 for a in articles if a["universe"] == u)
        tag = f'<span class="uni-tag">{html.escape(tagline)}</span>' if tagline else ""
        plural = "s" if count != 1 else ""
        uni_cards.append(
            f'<a class="uni-card" href="articles/{u}/index.html">'
            f'<span class="uni-name">{html.escape(name)}</span>'
            f'<span class="uni-count">{count} article{plural}</span>'
            f'{tag}</a>'
        )

    body = f"""<section class="hero">
  <h1>The Loom of Heavens</h1>
  <p class="lede">An ever-expanding encyclopedia of a single multiverse — every story a separate stitch of the weave.</p>
  <div class="search">
    <input id="search-input" type="search" placeholder="Search the wiki…" autocomplete="off" autofocus>
    <ul id="search-results" class="search-results" hidden></ul>
  </div>
</section>

<section class="home-columns">
  <div class="col">
    <h2>Recent articles</h2>
    <ul class="card-list">
      {''.join(recent_html)}
    </ul>
  </div>
  <div class="col">
    <h2>Browse universes</h2>
    <div class="uni-grid">
      {''.join(uni_cards)}
    </div>
  </div>
</section>
"""
    return page_shell("Home", body, depth=0, extra_head='<script defer src="assets/search.js"></script>')


# --------------------------------------------------------------------------
# Build
# --------------------------------------------------------------------------
def collect_articles():
    articles = []
    if not DATA.exists():
        return articles
    for md in sorted(DATA.rglob("*.md")):
        rel = md.relative_to(DATA)
        universe = rel.parts[0]
        slug = md.stem
        meta, body = parse_frontmatter(md.read_text(encoding="utf-8"))
        art = {
            "slug": slug,
            "universe": universe,
            "title": meta.get("title", slug.replace("-", " ").title()),
            "type": meta.get("type", ""),
            "tier": meta.get("tier", ""),
            "summary": meta.get("summary", ""),
            "tags": meta.get("tags", []) if isinstance(meta.get("tags", []), list) else [meta.get("tags")],
            "date": meta.get("date", ""),
            "body": body,
            "url": f"articles/{universe}/{slug}.html",
        }
        articles.append(art)
    return articles


def build(check: bool = False) -> int:
    universes = load_universes()
    articles = collect_articles()

    # wiki-links resolve by slug OR by title (both slugified), so authors may
    # write [[skolar]] or [[Skolar]] or [[The Loom of Heavens]] interchangeably.
    link_map = {}
    for a in articles:
        link_map[slugify(a["slug"])] = a["url"]
        link_map[slugify(a["title"])] = a["url"]
    dead_links = []

    def make_resolver(depth: int):
        up = "../" * depth

        def resolve(slug):
            target = link_map.get(slugify(slug))
            if not target:
                dead_links.append(slug)
                return None
            return up + target

        return resolve

    # render each article body (article pages live at depth 2)
    for a in articles:
        a["html"] = render_markdown(a["body"], make_resolver(2))

    # write article pages
    for a in articles:
        out = OUT_ARTICLES / a["universe"] / f"{a['slug']}.html"
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(render_article_page(a, universes), encoding="utf-8")

    # per-universe index pages
    by_uni: dict[str, list] = {}
    for a in articles:
        by_uni.setdefault(a["universe"], []).append(a)
    for uni, arts in by_uni.items():
        out = OUT_ARTICLES / uni / "index.html"
        out.write_text(render_universe_index(uni, arts, universes), encoding="utf-8")

    # homepage
    (ROOT / "index.html").write_text(render_home(articles, universes), encoding="utf-8")

    # search index (built with the homepage resolver depth; urls are root-relative)
    index = [
        {
            "title": a["title"],
            "universe": universes.get(a["universe"], {}).get("name", a["universe"]),
            "type": a.get("type", ""),
            "summary": a.get("summary", ""),
            "tags": a.get("tags", []),
            "url": a["url"],
        }
        for a in articles
    ]
    (ROOT / "search-index.json").write_text(
        json.dumps(index, ensure_ascii=False, indent=2), encoding="utf-8"
    )

    print(f"Built {len(articles)} article(s) across {len(by_uni)} universe(s).")
    print(f"  → index.html, search-index.json, {len(by_uni)} universe index page(s).")

    if check and dead_links:
        uniq = sorted(set(dead_links))
        print(f"\n⚠  {len(uniq)} dead wiki-link target(s) (pages not yet written):")
        for d in uniq:
            print(f"     [[{d}]]")
    return len(articles)


if __name__ == "__main__":
    build(check="--check" in sys.argv)
