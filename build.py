"""Builds the korolevalab.com home page (GitHub Pages, static).

    python3 build.py                      writes index.html, favicon.svg, 404.html, robots.txt, sitemap.xml
    uv run --with playwright python build.py --og    also renders og.png (1200 x 630) from the page's hero

Design: the "Petrol" theme. Content is honest about what exists: formats are described, publications and tools are
marked as in preparation, nothing is listed that has not been published.
"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
URL = "https://korolevalab.com/"
EMAIL = "eva@korolevalab.com"
TITLE = "Koroleva Lab · Independent market analytics"
DESC = ("Independent analysis of market structure, systematic strategies and event risk for traders and investors, "
        "from elections and sanctions to cyber incidents. Built on public data, with the method published.")

INK, ACC, PALE, BG = "#0f2733", "#0b6e7f", "#cfe3e7", "#eef1f4"


def queen(size, color, fill=None, sw=1.6, at=(2, 3), frame=True):
    """The mark: an 8 x 8 board and the queen's eight moves from one square."""
    c = size / 8
    qx, qy = (at[0] + .5) * c, (at[1] + .5) * c
    out = f'<rect x="{sw / 2}" y="{sw / 2}" width="{size - sw}" height="{size - sw}" fill="none" stroke="{color}" stroke-width="{sw}"/>' if frame else ""
    for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (1, -1), (-1, 1), (-1, -1)]:
        tx = ((size - qx) if dx > 0 else qx) if dx else 1e9
        ty = ((size - qy) if dy > 0 else qy) if dy else 1e9
        t = min(tx, ty)
        out += f'<line x1="{qx:.2f}" y1="{qy:.2f}" x2="{qx + dx * t:.2f}" y2="{qy + dy * t:.2f}" stroke="{color}" stroke-width="{sw}"/>'
    out += f'<rect x="{qx - c * .36:.2f}" y="{qy - c * .36:.2f}" width="{c * .72:.2f}" height="{c * .72:.2f}" fill="{fill or color}"/>'
    return out


LOGO = f'<svg width="28" height="28" viewBox="0 0 28 28" aria-hidden="true">{queen(28, INK, ACC)}</svg>'
FAVICON = f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32 32"><rect width="32" height="32" fill="{BG}"/><g transform="translate(2,2)">{queen(28, INK, ACC, sw=2)}</g></svg>'
HERO = f'''<svg class="art" viewBox="0 0 560 560" role="img" aria-label="Koroleva Lab: a geometric composition with the lab's mark">
<rect x="0" y="0" width="280" height="280" fill="{PALE}"/>
<path d="M280,0 A280,280 0 0 1 560,280 L280,280 Z" fill="{ACC}"/>
<rect x="280" y="280" width="280" height="280" fill="{INK}"/>
<circle cx="140" cy="420" r="140" fill="none" stroke="{ACC}" stroke-width="2"/>
<circle cx="140" cy="420" r="92" fill="none" stroke="{ACC}" stroke-width="2"/>
<circle cx="140" cy="420" r="44" fill="{ACC}"/>
<line x1="0" y1="280" x2="560" y2="280" stroke="{INK}" stroke-width="2"/>
<line x1="280" y1="0" x2="280" y2="560" stroke="{INK}" stroke-width="2"/>
<g transform="translate(316,316)">{queen(208, "#ffffff", sw=1.8)}</g>
<rect x="40" y="40" width="200" height="200" fill="none" stroke="{INK}" stroke-width="2"/>
<line x1="40" y1="240" x2="240" y2="40" stroke="{INK}" stroke-width="2"/>
</svg>'''

COVERAGE = [
    ("Markets", [("01", "Market Structure", "Liquidity, order flow, venues and derivatives: how prices form and where they break."),
                 ("02", "Systematic Strategies", "Signals and strategies tested out of sample, with trading costs included.")]),
    ("Event Risk", [("03", "Geopolitics &amp; Policy", "Elections, sanctions and regulation, and how markets reprice around them."),
                    ("04", "Cyber &amp; Operational Risk", "Hacks, exchange failures and outages, and their effect on prices and liquidity.")]),
]
FORMATS = [("Data Note", "One chart or one finding, published while it still matters."),
           ("Outlook", "Quarterly and annual views of the event risks ahead."),
           ("Event Risk Calendar", "Scheduled events of the week, by region and asset class.")]
TOOLS = [("Monitor", "Event Risk Monitor", "Upcoming events with implied moves across asset classes."),
         ("Dashboard", "Liquidity Dashboard", "Depth and spreads across venues, updated daily."),
         ("Data", "Datasets", "The cleaned, documented data behind every publication.")]
METHOD = [("Public data", "Every figure traces to a public source."), ("Reproducible", "Methods, code and data are published with the analysis."),
          ("Versioned", "Revisions are dated and logged."), ("Disclosures", "Any related position is disclosed.")]

CSS = f"""
:root {{ --bg:{BG}; --ink:{INK}; --muted:#51646f; --faint:#7f929c; --line:#d6dee3; --acc:{ACC}; --pale:{PALE}; --card:#ffffff; }}
* {{ box-sizing: border-box; }}
html {{ scroll-behavior: smooth; }}
body {{ margin: 0; background: var(--bg); color: var(--ink); font: 16px/1.55 Manrope, system-ui, sans-serif; -webkit-font-smoothing: antialiased; }}
.wrap {{ max-width: 1240px; margin: 0 auto; padding: 0 32px; }}
a {{ color: inherit; text-decoration: none; }}
.lab {{ font: 500 11.5px "JetBrains Mono", ui-monospace, monospace; letter-spacing: .14em; text-transform: uppercase; color: var(--faint); }}
.btn {{ display: inline-flex; align-items: center; gap: 10px; padding: 14px 22px; font-weight: 600; font-size: 15px; border-radius: 2px; }}
.btn.p {{ background: var(--acc); color: #fff; }}
.btn.s {{ border: 1.5px solid var(--ink); }}
.btn:hover {{ opacity: .9; }}
header {{ display: flex; align-items: center; justify-content: space-between; height: 76px; border-bottom: 1px solid var(--line); }}
.brand {{ display: flex; align-items: center; gap: 12px; font-weight: 700; font-size: 18px; letter-spacing: -.2px; }}
nav {{ display: flex; align-items: center; gap: 28px; font-size: 14.5px; font-weight: 500; color: var(--muted); }}
nav a:not(.btn):hover {{ color: var(--ink); }}
nav .btn {{ padding: 10px 18px; font-size: 14px; color: #fff; }}
.hero {{ display: grid; grid-template-columns: 1fr minmax(0, 520px); gap: 56px; align-items: center; padding: 72px 0 84px; border-bottom: 1px solid var(--line); }}
.hero h1 {{ margin: 20px 0 26px; font: 600 clamp(42px, 5.4vw, 72px)/1.03 Manrope; letter-spacing: -.035em; }}
.hero p {{ margin: 0 0 34px; max-width: 560px; font-size: 18.5px; color: var(--muted); }}
.cta {{ display: flex; flex-wrap: wrap; gap: 12px; }}
.art {{ width: 100%; height: auto; display: block; }}
section[id] {{ scroll-margin-top: 20px; }}
.cov {{ display: grid; grid-template-columns: 1fr 1fr; border-bottom: 1px solid var(--line); }}
.pillar {{ padding: 40px 40px 46px 0; }}
.pillar + .pillar {{ padding: 40px 0 46px 40px; border-left: 1px solid var(--line); }}
.pillar > .lab {{ display: block; margin-bottom: 22px; }}
.areas {{ display: grid; grid-template-columns: 1fr 1fr; gap: 28px; }}
.area .n {{ font: 500 13px "JetBrains Mono", monospace; color: var(--acc); }}
.area h3 {{ margin: 12px 0 8px; font-size: 22px; letter-spacing: -.02em; }}
.area p {{ margin: 0; color: var(--muted); font-size: 15px; }}
.sec {{ display: flex; justify-content: space-between; align-items: end; gap: 20px; margin: 84px 0 26px; }}
.sec h2 {{ margin: 8px 0 0; font: 600 clamp(32px, 3.6vw, 44px)/1.05 Manrope; letter-spacing: -.035em; }}
.sec .note {{ color: var(--muted); font-size: 15px; max-width: 360px; text-align: right; }}
.latest {{ display: grid; grid-template-columns: 1.15fr 1fr; gap: 28px; }}
.feat {{ background: var(--card); border: 1px solid var(--line); border-radius: 2px; display: flex; flex-direction: column; }}
.feat .pic {{ height: 260px; border-bottom: 1px solid var(--line); position: relative; overflow: hidden;
  background: linear-gradient(var(--line) 1px, transparent 1px) 0 0/40px 40px, linear-gradient(90deg, var(--line) 1px, transparent 1px) 0 0/40px 40px; }}
.feat .pic i {{ position: absolute; left: 40px; right: 40px; bottom: 40px; height: 2px; background: var(--acc); }}
.feat .pic b {{ position: absolute; left: 200px; top: 80px; width: 120px; height: 120px; border: 2px solid var(--acc); }}
.feat .pic u {{ position: absolute; left: 240px; top: 40px; width: 2px; height: 180px; background: var(--ink); opacity: .5; }}
.feat .body {{ padding: 28px 30px 32px; }}
.feat h3 {{ margin: 12px 0 10px; font-size: 32px; line-height: 1.12; letter-spacing: -.03em; }}
.feat p, .item p {{ margin: 0; color: var(--muted); }}
.item {{ padding: 22px 0; border-top: 1px solid var(--line); }}
.item:last-child {{ border-bottom: 1px solid var(--line); }}
.item h4 {{ margin: 8px 0 4px; font-size: 21px; line-height: 1.25; letter-spacing: -.02em; }}
.tagf {{ color: var(--acc); }}
.cal {{ border: 1px solid var(--line); border-radius: 2px; }}
.cal .row {{ display: grid; grid-template-columns: 120px 1fr 200px 240px; gap: 12px; padding: 16px 24px; border-top: 1px solid var(--line); align-items: center; }}
.cal .row:first-child {{ border-top: 0; font: 500 11.5px "JetBrains Mono", monospace; letter-spacing: .12em; text-transform: uppercase; color: var(--faint); background: var(--card); }}
.sk {{ display: block; height: 10px; border-radius: 2px; background: var(--line); }}
.cal .msg {{ padding: 18px 24px; border-top: 1px solid var(--line); color: var(--muted); font-size: 15px; }}
.tools {{ display: grid; grid-template-columns: repeat(3, 1fr); border: 1px solid var(--line); border-radius: 2px; }}
.tool {{ padding: 30px; min-height: 210px; display: flex; flex-direction: column; justify-content: space-between; gap: 24px; }}
.tool + .tool {{ border-left: 1px solid var(--line); }}
.tool h3 {{ margin: 0 0 6px; font-size: 22px; letter-spacing: -.02em; }}
.tool p {{ margin: 0; color: var(--muted); }}
.soon {{ display: flex; justify-content: space-between; font: 12px "JetBrains Mono", monospace; color: var(--faint); }}
.soon b {{ color: var(--acc); font-weight: 500; }}
.method {{ display: grid; grid-template-columns: repeat(4, 1fr); margin-top: 84px; border-top: 2px solid var(--ink); }}
.method div {{ padding: 20px 22px 0 0; }}
.method div + div {{ padding-left: 22px; border-left: 1px solid var(--line); }}
.method b {{ display: block; margin-bottom: 6px; font-size: 17px; }}
.method span {{ color: var(--muted); font-size: 15px; }}
.news {{ margin-top: 84px; background: var(--ink); color: #fff; border-radius: 2px; padding: 56px 60px; display: grid; grid-template-columns: 1fr auto; gap: 40px; align-items: center; }}
.news h2 {{ margin: 6px 0 8px; font: 600 clamp(32px, 3.6vw, 44px)/1.05 Manrope; letter-spacing: -.035em; }}
.news p {{ margin: 0; opacity: .78; font-size: 17px; }}
.news .lab {{ color: inherit; opacity: .6; }}
.news .btn {{ background: #fff; color: var(--ink); }}
.two {{ display: grid; grid-template-columns: 1fr 1fr; margin-top: 84px; border-top: 1px solid var(--line); }}
.two > div {{ padding: 28px 40px 0 0; }}
.two > div + div {{ padding: 28px 0 0 40px; border-left: 1px solid var(--line); }}
.two h3 {{ margin: 10px 0 10px; font-size: 28px; letter-spacing: -.025em; line-height: 1.2; }}
.two p {{ margin: 0 0 22px; color: var(--muted); }}
footer {{ margin-top: 100px; border-top: 1px solid var(--line); }}
footer .wrap {{ display: grid; grid-template-columns: 1.5fr 1fr 1fr 1fr; gap: 30px; padding-top: 48px; padding-bottom: 34px; }}
footer b {{ display: block; margin-bottom: 12px; font-size: 15px; }}
footer a, footer span.t {{ display: block; margin-bottom: 7px; color: var(--muted); font-size: 14px; }}
footer .legal {{ grid-column: 1 / -1; display: flex; flex-wrap: wrap; gap: 10px; justify-content: space-between; padding-top: 22px; border-top: 1px solid var(--line); color: var(--faint); font-size: 13px; }}
@media (max-width: 1060px) {{
  .hero {{ grid-template-columns: 1fr; padding-top: 48px; }}
  .hero .art {{ max-width: 520px; }}
  .cov {{ grid-template-columns: 1fr; }}
  .pillar, .pillar + .pillar {{ padding: 34px 0; border-left: 0; }}
  .pillar + .pillar {{ border-top: 1px solid var(--line); }}
  .latest, .two {{ grid-template-columns: 1fr; }}
  .two > div, .two > div + div {{ padding: 28px 0; border-left: 0; }}
  .two > div + div {{ border-top: 1px solid var(--line); }}
  .tools {{ grid-template-columns: 1fr; }}
  .tool + .tool {{ border-left: 0; border-top: 1px solid var(--line); }}
  .method {{ grid-template-columns: 1fr 1fr; }}
  .method div, .method div + div {{ padding: 20px 16px 16px 0; border-left: 0; }}
  .news {{ grid-template-columns: 1fr; padding: 40px 32px; }}
  footer .wrap {{ grid-template-columns: 1fr 1fr; }}
}}
@media (max-width: 720px) {{
  .wrap {{ padding: 0 16px; }}
  nav a:not(.btn) {{ display: none; }}
  .areas {{ grid-template-columns: 1fr; }}
  .sec {{ display: block; margin-top: 64px; }}
  .sec .note {{ text-align: left; margin-top: 10px; }}
  .feat h3 {{ font-size: 26px; }}
  .feat .pic {{ height: 180px; }}
  .feat .pic b {{ left: 120px; top: 40px; width: 90px; height: 90px; }}
  .feat .pic u {{ left: 150px; top: 20px; height: 130px; }}
  .cal .row {{ grid-template-columns: 60px 1fr; }}
  .cal .row > :nth-child(n+3) {{ display: none; }}
  .method {{ grid-template-columns: 1fr; }}
  footer .wrap {{ grid-template-columns: 1fr; }}
}}
"""


def page():
    cov = "".join(f'<div class="pillar"><span class="lab">{p}</span><div class="areas">'
                  + "".join(f'<div class="area"><div class="n">{n}</div><h3>{h}</h3><p>{d}</p></div>' for n, h, d in areas)
                  + "</div></div>" for p, areas in COVERAGE)
    formats = "".join(f'<div class="item"><span class="lab"><span class="tagf">Format</span></span><h4>{h}</h4><p>{d}</p></div>' for h, d in FORMATS)
    sk = "".join('<div class="row" aria-hidden="true"><span class="sk" style="width:40px"></span><span class="sk" style="width:%d%%"></span>'
                 '<span class="sk" style="width:60px"></span><span class="sk" style="width:120px"></span></div>' % w for w in (62, 48, 70))
    tools = "".join(f'<div class="tool"><div class="soon"><span>{k}</span><b>In development</b></div><div><h3>{h}</h3><p>{d}</p></div></div>' for k, h, d in TOOLS)
    method = "".join(f"<div><b>{h}</b><span>{d}</span></div>" for h, d in METHOD)
    ld = ('{"@context":"https://schema.org","@type":"Organization","name":"Koroleva Lab","url":"%s",'
          '"description":"Independent market analytics for traders and investors.","email":"%s"}') % (URL, EMAIL)
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{TITLE}</title>
<meta name="description" content="{DESC}">
<link rel="canonical" href="{URL}">
<link rel="icon" href="favicon.svg" type="image/svg+xml">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Koroleva Lab">
<meta property="og:title" content="{TITLE}">
<meta property="og:description" content="{DESC}">
<meta property="og:url" content="{URL}">
<meta property="og:image" content="{URL}og.png">
<meta name="twitter:card" content="summary_large_image">
<meta name="theme-color" content="{BG}">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Manrope:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap">
<script type="application/ld+json">{ld}</script>
<style>{CSS}</style>
</head>
<body>
<div class="wrap">
  <header><a class="brand" href="{URL}">{LOGO}Koroleva Lab</a>
    <nav><a href="#coverage">Coverage</a><a href="#analysis">Analysis</a><a href="#calendar">Calendar</a><a href="#tools">Tools</a><a href="#about">About</a><a class="btn p" href="#newsletter">Subscribe</a></nav></header>

  <section class="hero">
    <div><span class="lab">Independent market analytics</span>
      <h1>Market structure and event risk, analysed.</h1>
      <p>Analysis of market structure, systematic strategies and event risk, from elections and sanctions to cyber incidents. Built on public data, with the method published.</p>
      <div class="cta"><a class="btn p" href="#coverage">Coverage →</a><a class="btn s" href="#newsletter">Weekly Brief</a></div></div>
    {HERO}
  </section>

  <section class="cov" id="coverage">{cov}</section>

  <section id="analysis">
    <div class="sec"><div><span class="lab">Analysis</span><h2>Formats</h2></div><p class="note">The first publications are in preparation.</p></div>
    <div class="latest">
      <div class="feat"><div class="pic"><i></i><u></u><b></b></div><div class="body"><span class="lab"><span class="tagf">Format</span> · Flagship</span>
        <h3>Deep Dive</h3><p>Long-form analysis of one question, with the data, the code and the method behind every figure.</p></div></div>
      <div>{formats}</div>
    </div>
  </section>

  <section id="calendar">
    <div class="sec"><div><span class="lab">Event Risk</span><h2>Event Risk Calendar</h2></div><p class="note">Scheduled events of the week by region and asset class.</p></div>
    <div class="cal"><div class="row"><span>Day</span><span>Event</span><span>Region</span><span>Asset classes</span></div>{sk}
      <div class="msg">The calendar launches with the first Weekly Brief.</div></div>
  </section>

  <section id="tools">
    <div class="sec"><div><span class="lab">Tools &amp; Data</span><h2>Instruments</h2></div></div>
    <div class="tools">{tools}</div>
  </section>

  <section class="method" id="method">{method}</section>

  <section class="news" id="newsletter"><div><span class="lab">Newsletter</span><h2>The Weekly Brief</h2><p>The Event Risk Calendar and new analysis, every Monday.</p></div>
    <a class="btn" href="mailto:{EMAIL}?subject=Weekly%20Brief">Subscribe by email</a></section>

  <section class="two" id="about">
    <div><span class="lab">About</span><h3>An independent analytics lab for traders and investors.</h3><p>Market structure, systematic strategies and event risk, analysed on public data.</p></div>
    <div><span class="lab">Bespoke analysis</span><h3>Custom analysis for funds and trading desks.</h3><p>Specific questions, answered with data and a documented method.</p><a class="btn s" href="mailto:{EMAIL}">Contact</a></div>
  </section>
</div>
<footer><div class="wrap">
  <div><b>Koroleva Lab</b><span class="t">Independent market analytics.</span></div>
  <div><b>Coverage</b><a href="#coverage">Market Structure</a><a href="#coverage">Systematic Strategies</a><a href="#coverage">Geopolitics &amp; Policy</a><a href="#coverage">Cyber &amp; Operational Risk</a></div>
  <div><b>Analysis</b><a href="#analysis">Formats</a><a href="#calendar">Event Risk Calendar</a><a href="#newsletter">Weekly Brief</a></div>
  <div><b>Lab</b><a href="#about">About</a><a href="#method">Methodology</a><a href="mailto:{EMAIL}">Contact</a></div>
  <div class="legal"><span>© 2026 Koroleva Lab</span><span>For information only. Not investment advice.</span></div>
</div></footer>
</body>
</html>
"""


def not_found():
    return (f'<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">'
            f'<title>Not found · Koroleva Lab</title><link rel="icon" href="/favicon.svg" type="image/svg+xml">'
            f'<style>body{{margin:0;background:{BG};color:{INK};font:16px/1.5 system-ui,sans-serif;display:grid;place-items:center;min-height:100vh}}'
            f'a{{color:{ACC}}}</style></head><body><div style="text-align:center"><svg width="56" height="56" viewBox="0 0 28 28">{queen(28, INK, ACC)}</svg>'
            f'<p>This page does not exist.</p><p><a href="{URL}">Koroleva Lab</a></p></div></body></html>')


def main():
    (HERE / "index.html").write_text(page())
    (HERE / "favicon.svg").write_text(FAVICON)
    (HERE / "404.html").write_text(not_found())
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
            pg.goto((HERE / "index.html").as_uri(), wait_until="networkidle")
            pg.evaluate("document.fonts.ready")
            pg.add_style_tag(content="header{display:none} .hero{padding:44px 0 0;border:0;gap:40px;grid-template-columns:1fr 470px} .hero .cta{display:none}")
            pg.wait_for_timeout(500)
            pg.screenshot(path=str(HERE / "og.png"))
            b.close()
    print("built")


if __name__ == "__main__":
    main()
