"""Builds the korolevalab.com placeholder page (GitHub Pages, static).

    python3 build.py                                  writes index.html, 404.html, favicon.svg, robots.txt, sitemap.xml
    uv run --with playwright python build.py --og    also renders og.png (1200 x 630) from the page

Design: the "Board" placeholder in the Petrol theme. An 8 x 8 board fills the screen; the squares the queen attacks are
tinted and her eight rays run to the edges. The full site lives on the local branch content-draft.
"""
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
URL = "https://korolevalab.com/"
EMAIL = "launch@korolevalab.com"
TITLE = "Koroleva Lab · Modern AI market analytics"
DESC = "Koroleva Lab: modern AI market analytics. Market structure, systematic strategies and event risk."

INK, ACC, PALE, BG, MUTED, FAINT, LINE = "#0f2733", "#0b6e7f", "#cfe3e7", "#eef1f4", "#51646f", "#7f929c", "#d6dee3"

FONT_FACES = "".join(
    f"@font-face {{ font-family: '{fam}'; font-style: normal; font-weight: {w}; font-display: swap; "
    f"src: url(/fonts/{file}.woff2) format('woff2'); unicode-range: {rng}; }}\n"
    for fam, w, file, rng in [
        ("Manrope", "400 700", "manrope-latin", "U+0000-00FF, U+0131, U+0152-0153, U+02BB-02BC, U+02C6, U+02DA, U+02DC, U+0304, U+0308, U+0329, U+2000-206F, U+20AC, U+2122, U+2191, U+2193, U+2212, U+2215, U+FEFF, U+FFFD"),
        ("Manrope", "400 700", "manrope-latin-ext", "U+0100-02BA, U+02BD-02C5, U+02C7-02CC, U+02CE-02D7, U+02DD-02FF, U+0304, U+0308, U+0329, U+1D00-1DBF, U+1E00-1E9F, U+1EF2-1EFF, U+2020, U+20A0-20AB, U+20AD-20C4, U+2113, U+2C60-2C7F, U+A720-A7FF"),
        ("JetBrains Mono", "400 500", "jetbrains-mono-latin", "U+0000-00FF, U+0131, U+0152-0153, U+02BB-02BC, U+02C6, U+02DA, U+02DC, U+0304, U+0308, U+0329, U+2000-206F, U+20AC, U+2122, U+2191, U+2193, U+2212, U+2215, U+FEFF, U+FFFD"),
    ])


def queen(size, color, fill=None, sw=1.6, at=(2, 3)):
    """The mark: an 8 x 8 board and the queen's eight moves from one square."""
    c = size / 8
    qx, qy = (at[0] + .5) * c, (at[1] + .5) * c
    out = f'<rect x="{sw / 2}" y="{sw / 2}" width="{size - sw}" height="{size - sw}" fill="none" stroke="{color}" stroke-width="{sw}"/>'
    for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (1, -1), (-1, 1), (-1, -1)]:
        tx = ((size - qx) if dx > 0 else qx) if dx else 1e9
        ty = ((size - qy) if dy > 0 else qy) if dy else 1e9
        t = min(tx, ty)
        out += f'<line x1="{qx:.2f}" y1="{qy:.2f}" x2="{qx + dx * t:.2f}" y2="{qy + dy * t:.2f}" stroke="{color}" stroke-width="{sw}"/>'
    out += f'<rect x="{qx - c * .36:.2f}" y="{qy - c * .36:.2f}" width="{c * .72:.2f}" height="{c * .72:.2f}" fill="{fill or color}"/>'
    return out


LOGO = f'<svg width="26" height="26" viewBox="0 0 28 28" aria-hidden="true">{queen(28, INK, ACC)}</svg>'
FAVICON = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32 32"><rect width="32" height="32" fill="{BG}"/>'
           f'<g transform="translate(2,2)">{queen(28, INK, ACC, sw=2)}</g></svg>')


def board(qc=5, qr=2):
    """Full-screen board: attacked squares tinted, rays drawn to the edges."""
    out = ['<svg class="board" viewBox="0 0 800 800" preserveAspectRatio="xMidYMid slice" aria-hidden="true">']
    for r in range(8):
        for c in range(8):
            if (c, r) != (qc, qr) and (c == qc or r == qr or abs(c - qc) == abs(r - qr)):
                delay = .6 + .05 * max(abs(c - qc), abs(r - qr))
                out.append(f'<rect class="hit" style="animation-delay:{delay:.2f}s" x="{c * 100}" y="{r * 100}" width="100" height="100" fill="{PALE}"/>')
    for i in range(1, 8):
        out.append(f'<line x1="{i * 100}" y1="0" x2="{i * 100}" y2="800" stroke="{LINE}" stroke-width="1" vector-effect="non-scaling-stroke"/>')
        out.append(f'<line x1="0" y1="{i * 100}" x2="800" y2="{i * 100}" stroke="{LINE}" stroke-width="1" vector-effect="non-scaling-stroke"/>')
    cx, cy = qc * 100 + 50, qr * 100 + 50
    for i, (dx, dy) in enumerate([(1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (1, -1), (-1, 1), (-1, -1)]):
        tx = ((800 - cx) if dx > 0 else cx) if dx else 1e9
        ty = ((800 - cy) if dy > 0 else cy) if dy else 1e9
        t = min(tx, ty)
        length = t * (2 ** .5 if dx and dy else 1)
        out.append(f'<line class="ray" style="stroke-dasharray:{length:.0f};stroke-dashoffset:{length:.0f};animation-delay:{.1 + i * .07:.2f}s" '
                   f'x1="{cx}" y1="{cy}" x2="{cx + dx * t}" y2="{cy + dy * t}" stroke="{ACC}" stroke-width="1.3"/>')
    out.append(f'<rect class="sq" x="{qc * 100 + 18}" y="{qr * 100 + 18}" width="64" height="64" fill="{ACC}"/></svg>')
    return "".join(out)


CSS = f"""{FONT_FACES}
*{{box-sizing:border-box}} html,body{{margin:0;height:100%}}
body{{background:#fff;color:{INK};font:16px/1.55 Manrope,system-ui,sans-serif;-webkit-font-smoothing:antialiased}}
a{{color:inherit;text-decoration:none}}
.lab{{font:500 11.5px "JetBrains Mono",ui-monospace,monospace;letter-spacing:.14em;text-transform:uppercase;color:{FAINT}}}
@keyframes draw{{to{{stroke-dashoffset:0}}}} @keyframes fade{{from{{opacity:0}}to{{opacity:1}}}}
.board{{position:fixed;inset:0;width:100vw;height:100vh}}
.ray{{animation:draw 1.1s cubic-bezier(.6,0,.2,1) forwards}} .sq{{opacity:0;animation:fade .5s .2s forwards}} .hit{{opacity:0;animation:fade .6s forwards}}
.card{{position:fixed;z-index:1;left:6vw;bottom:8vh;max-width:540px;margin:0;background:#fff;border:1px solid {LINE};padding:36px 38px 34px}}
.brand{{display:flex;align-items:center;gap:12px;font-weight:700;font-size:17px;margin-bottom:26px}}
h1{{margin:10px 0 14px;font:600 clamp(32px,3.6vw,46px)/1.08 Manrope;letter-spacing:-.03em;text-wrap:balance}}
.card p{{margin:0 0 26px;padding-bottom:24px;border-bottom:2px solid {INK};color:{MUTED};font-size:16.5px}}
.row{{display:flex;justify-content:space-between;align-items:center;gap:16px;flex-wrap:wrap}}
.status{{font:500 11.5px "JetBrains Mono",monospace;letter-spacing:.12em;text-transform:uppercase;color:{MUTED}}}
.mail{{font-weight:600;color:{ACC};border-bottom:1.5px solid {ACC}}}
@media (max-width:640px){{.card{{left:16px;right:16px;bottom:16px;padding:26px 22px}}}}
@media (prefers-reduced-motion: reduce){{.ray{{animation:none;stroke-dashoffset:0}} .sq,.hit{{animation:none;opacity:1}}}}
"""


PERSON = "https://blog.korolevalab.com/#person"
ORG = URL + "#organization"
# Structured data for search engines, not shown on the page: the lab, its founder (the same Person the blog describes,
# by the same @id, so search engines can join the two sites) and the website.
LD_GRAPH = {
    "@context": "https://schema.org",
    "@graph": [
        {"@type": "Organization", "@id": ORG, "name": "Koroleva Lab", "alternateName": "Koroleva Research", "url": URL,
         "logo": {"@type": "ImageObject", "url": URL + "logo.png", "width": 512, "height": 512}, "image": URL + "og.png",
         "email": EMAIL, "description": "Modern AI market analytics: market structure, systematic strategies and event risk.",
         "founder": {"@id": PERSON},
         "sameAs": ["https://github.com/korolevalab", "https://www.crunchbase.com/organization/koroleva-research"]},
        {"@type": "Person", "@id": PERSON, "name": "Eva Koroleva", "url": "https://blog.korolevalab.com/about/",
         "image": "https://blog.korolevalab.com/assets/img/eva_koroleva.jpg", "worksFor": {"@id": ORG},
         "sameAs": ["https://blog.korolevalab.com/", "https://orcid.org/0009-0005-4637-4176",
                    "https://scholar.google.com/citations?user=q9sm0sgAAAAJ", "https://github.com/xmarva",
                    "https://www.linkedin.com/in/e-koroleva", "https://twitter.com/crazyruskaya",
                    "https://www.wikidata.org/wiki/Q142104051", "https://www.crunchbase.com/person/eva-koroleva",
                    "https://huggingface.co/xmarva", "https://www.kaggle.com/qmarva"]},
        {"@type": "WebSite", "@id": URL + "#website", "name": "Koroleva Lab", "url": URL, "inLanguage": "en",
         "publisher": {"@id": ORG}},
    ],
}
LD = '<script type="application/ld+json">' + json.dumps(LD_GRAPH, ensure_ascii=False, separators=(",", ":")) + "</script>"


def head(title, desc, canonical=True):
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
{f'<link rel="canonical" href="{URL}">' if canonical else '<meta name="robots" content="noindex">'}
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Koroleva Lab">
<meta property="og:title" content="{TITLE}">
<meta property="og:description" content="{DESC}">
<meta property="og:url" content="{URL}">
<meta property="og:image" content="{URL}og.png">
<meta name="twitter:card" content="summary_large_image">
<meta name="theme-color" content="#ffffff">
<link rel="preload" href="/fonts/manrope-latin.woff2" as="font" type="font/woff2" crossorigin>
{LD if canonical else ""}
<style>{CSS}</style>
</head>
"""


def page():
    return head(TITLE, DESC) + f"""<body>
{board()}
<main class="card"><span class="brand">{LOGO}Koroleva Lab</span>
<span class="lab">Modern AI market analytics</span>
<h1>Every move on the board</h1>
<p>Market structure, systematic strategies and event risk</p>
<div class="row"><span class="status">In service · Coming back soon · 2026</span><a class="mail" href="mailto:{EMAIL}">{EMAIL}</a></div>
</main>
</body>
</html>
"""


def not_found():
    return head("Not found · Koroleva Lab", "Page not found.", canonical=False) + f"""<body>
{board(4, 3)}
<main class="card"><span class="brand">{LOGO}Koroleva Lab</span>
<span class="lab">404</span>
<h1>This square is empty</h1>
<p>The page does not exist.</p>
<div class="row"><a class="mail" href="/">korolevalab.com</a></div>
</main>
</body>
</html>
"""


def logo_png():
    """The mark as a 512 px PNG: search engines want a raster logo of at least 112 px for the organisation."""
    from playwright.sync_api import sync_playwright
    chrome = str(next(Path.home().glob("Library/Caches/ms-playwright/chromium_headless_shell-1248/*/chrome-headless-shell")))
    with sync_playwright() as p:
        b = p.chromium.launch(executable_path=chrome)
        pg = b.new_page(viewport={"width": 512, "height": 512}, device_scale_factor=1)
        size, pad = 416, 48
        mark = queen(size, INK, ACC, sw=9).replace("<rect x=", "<rect class=f x=", 1)
        svg = (f'<svg xmlns="http://www.w3.org/2000/svg" width="512" height="512" viewBox="0 0 512 512"><rect width="512" height="512" fill="{BG}"/>'
               f'<defs><clipPath id="c"><rect width="{size}" height="{size}"/></clipPath></defs>'
               f'<g transform="translate({pad},{pad})" clip-path="url(#c)">{mark}</g>'
               f'<rect x="{pad + 6}" y="{pad + 6}" width="{size - 12}" height="{size - 12}" fill="none" stroke="{INK}" stroke-width="12"/></svg>')
        pg.set_content(f'<html><body style="margin:0">{svg}</body></html>')
        pg.screenshot(path=str(HERE / "logo.png"))
        b.close()


def main():
    (HERE / "index.html").write_text(page())
    (HERE / "404.html").write_text(not_found())
    (HERE / "favicon.svg").write_text(FAVICON)
    if "--og" in sys.argv or not (HERE / "logo.png").exists():
        logo_png()
    (HERE / "robots.txt").write_text(f"User-agent: *\nAllow: /\n\nSitemap: {URL}sitemap.xml\n")
    (HERE / "sitemap.xml").write_text(f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'
                                      f"<url><loc>{URL}</loc></url></urlset>\n")
    (HERE / "CNAME").write_text("korolevalab.com\n")
    (HERE / ".nojekyll").write_text("")
    if "--og" in sys.argv:
        from playwright.sync_api import sync_playwright
        chrome = str(next(Path.home().glob("Library/Caches/ms-playwright/chromium_headless_shell-1248/*/chrome-headless-shell")))
        with sync_playwright() as p:
            b = p.chromium.launch(executable_path=chrome)
            pg = b.new_page(viewport={"width": 1200, "height": 630}, device_scale_factor=1)
            pg.goto("http://127.0.0.1:8177/", wait_until="networkidle")
            pg.evaluate("document.fonts.ready")
            pg.wait_for_timeout(2500)
            pg.screenshot(path=str(HERE / "og.png"))
            b.close()
    print("built")


if __name__ == "__main__":
    main()
