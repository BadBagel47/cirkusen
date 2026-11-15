#!/usr/bin/env python3
"""Manage the poster archive.

Every poster lives in public/<slug>/index.html and is listed in public/assets/posters.json
(oldest first). The newest poster is also published at "/" as a generated copy.

  tools/posters.py new <slug> "<title>"   start a new poster as a copy of the newest one
  tools/posters.py image [<slug>]         render the share image of a poster (default: the newest)
  tools/posters.py sync                   regenerate public/index.html from the newest poster
  tools/posters.py check                  verify the archive (also used before publishing)

Use --public <dir> to work on another copy of the public folder (for testing).
"""
import argparse
import json
import os
import re
import subprocess
import sys
from pathlib import Path

SITE = "https://cirkusen.trythis.one/"
SLUG = re.compile(r"^\d{4}-\d{2}-\d{2}(-[a-z0-9]+)?$")


def load(public):
    return json.loads((public / "assets" / "posters.json").read_text(encoding="utf-8"))


def save(public, posters):
    posters.sort(key=lambda p: p["slug"])
    (public / "assets" / "posters.json").write_text(
        json.dumps(posters, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def swap_url(html, old, new):
    """Replace the page address in the canonical link and og:url only."""
    for pattern in (f'<link rel="canonical" href="{{}}">', f'<meta property="og:url" content="{{}}">'):
        a, b = pattern.format(old), pattern.format(new)
        if a not in html:
            sys.exit(f"error: could not find {a}")
        html = html.replace(a, b)
    return html


def root_html(public, posters):
    last = posters[-1]["slug"]
    page = (public / last / "index.html").read_text(encoding="utf-8")
    return swap_url(page, f"{SITE}{last}/", SITE)


def cmd_sync(public):
    posters = load(public)
    (public / "index.html").write_text(root_html(public, posters), encoding="utf-8")
    print(f"public/index.html now shows {posters[-1]['slug']}")


def problems(public):
    out = []
    posters = load(public)
    slugs = [p["slug"] for p in posters]
    if slugs != sorted(slugs) or len(set(slugs)) != len(slugs):
        out.append("posters.json must be sorted by slug with no duplicates")
    for p in posters:
        if not SLUG.match(p["slug"]) or not p["date"].startswith(p["slug"][:10]):
            out.append(f"bad slug or date: {p['slug']}")
        page = public / p["slug"] / "index.html"
        if not page.exists():
            out.append(f"missing page: {page}")
            continue
        html = page.read_text(encoding="utf-8")
        if f'data-poster="{p["slug"]}"' not in html:
            out.append(f"{p['slug']}: body data-poster does not match")
        if f'href="{SITE}{p["slug"]}/"' not in html:
            out.append(f"{p['slug']}: canonical address does not match")
        image = OG_IMAGE.search(html)
        if not image or not image.group(1).startswith(SITE):
            out.append(f"{p['slug']}: og:image missing or not on this site")
        elif not (public / image.group(1)[len(SITE):]).exists():
            out.append(f"{p['slug']}: share image file is missing ({image.group(1)})")
    listed = set(slugs)
    for d in public.iterdir():
        if d.is_dir() and SLUG.match(d.name) and d.name not in listed:
            out.append(f"{d.name}: page exists but is not listed in posters.json")
    root = public / "index.html"
    if not posters:
        out.append("no posters listed")
    elif not root.exists() or root.read_text(encoding="utf-8") != root_html(public, posters):
        out.append("public/index.html is not a copy of the newest poster (run: tools/posters.py sync)")
    return out


OG_IMAGE = re.compile(r'<meta property="og:image" content="([^"]*)">')


def render_image(public, slug):
    """Render public/<slug>/og-image.jpg with Playwright and point the page's og:image at it."""
    env = dict(os.environ)
    if "NODE_PATH" not in env:
        found = subprocess.run(["npm", "root", "-g"], capture_output=True, text=True)
        if found.returncode == 0:
            env["NODE_PATH"] = found.stdout.strip()
    out = public / slug / "og-image.jpg"
    script = Path(__file__).resolve().parent / "og-image.cjs"
    result = subprocess.run(["node", str(script), str(public), slug, str(out)], env=env)
    if result.returncode != 0:
        sys.exit(f"error: could not render the share image for {slug} (needs Node and Playwright)")
    page = public / slug / "index.html"
    html = page.read_text(encoding="utf-8")
    if not OG_IMAGE.search(html):
        sys.exit("error: could not find the og:image tag")
    html = OG_IMAGE.sub(f'<meta property="og:image" content="{SITE}{slug}/og-image.jpg">', html, count=1)
    page.write_text(html, encoding="utf-8")


def cmd_image(public, slug):
    posters = load(public)
    slug = slug or posters[-1]["slug"]
    if slug not in {p["slug"] for p in posters}:
        sys.exit(f"error: {slug} is not listed in posters.json")
    render_image(public, slug)
    print(f"rendered public/{slug}/og-image.jpg")
    cmd_sync(public)


def cmd_check(public):
    found = problems(public)
    for line in found:
        print("problem:", line)
    if found:
        sys.exit(1)
    print(f"ok: {len(load(public))} poster(s)")


def cmd_new(public, slug, title):
    if not SLUG.match(slug):
        sys.exit("error: slug must look like 2026-12-01 (or 2026-12-01-b for a second one that day)")
    posters = load(public)
    if slug in {p["slug"] for p in posters}:
        sys.exit(f"error: {slug} already exists")
    if slug < posters[-1]["slug"]:
        sys.exit("error: the new poster must be newer than the newest one")
    old = posters[-1]["slug"]
    html = (public / old / "index.html").read_text(encoding="utf-8")
    html = swap_url(html, f"{SITE}{old}/", f"{SITE}{slug}/")
    html = html.replace(f'data-poster="{old}"', f'data-poster="{slug}"')
    (public / slug).mkdir()
    (public / slug / "index.html").write_text(html, encoding="utf-8")
    posters.append({"slug": slug, "date": slug[:10], "title": title})
    save(public, posters)
    cmd_sync(public)
    print(f"created public/{slug}/index.html as a copy of {old}.")
    render_image(public, slug)
    cmd_sync(public)
    print(f"Edit the poster, then run: tools/posters.py image {slug}  and  tools/posters.py check")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--public", type=Path, default=Path(__file__).resolve().parent.parent / "public")
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("sync")
    sub.add_parser("image").add_argument("slug", nargs="?")
    sub.add_parser("check")
    n = sub.add_parser("new")
    n.add_argument("slug")
    n.add_argument("title")
    a = ap.parse_args()
    if a.cmd == "sync":
        cmd_sync(a.public)
    elif a.cmd == "image":
        cmd_image(a.public, a.slug)
    elif a.cmd == "check":
        cmd_check(a.public)
    else:
        cmd_new(a.public, a.slug, a.title)


if __name__ == "__main__":
    main()
