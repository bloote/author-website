#!/usr/bin/env python3
"""
Generates every SVG asset used by the AuthorWings "Author Websites" page.

Everything is vector, self-contained and dependency-free, so the images stay
crisp on any screen and cost a few kilobytes each. Run from the repo root:

    python3 tools/make-images.py

Rasterise afterwards with tools/rasterise.mjs if you need WebP/PNG for the
WordPress media library.
"""

import os
import textwrap

OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "assets", "img")
os.makedirs(OUT, exist_ok=True)

# --------------------------------------------------------------------------
# Brand palette (sampled from the AuthorWings design)
# --------------------------------------------------------------------------
CREAM = "#FFFDF9"
BEIGE = "#EFE7D9"
BEIGE_2 = "#E7DDCC"
PINE = "#0F2F2E"
PINE_2 = "#193837"
TERRA = "#C25937"
TERRA_L = "#C96C4D"
INK = "#22201C"
BODY = "#5A5346"


def esc(s):
    return (s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
             .replace('"', "&quot;").replace("'", "&#39;"))


def write(name, svg):
    path = os.path.join(OUT, name)
    with open(path, "w", encoding="utf-8") as f:
        f.write(svg.strip() + "\n")
    print(f"  {name:44s} {os.path.getsize(path):>6,} bytes")


# --------------------------------------------------------------------------
# Shared pieces
# --------------------------------------------------------------------------

def browser_chrome(w, url, bar=54, radius=18, chrome="#EDE7DC", dot="#CFC5B4",
                   pill="#FBF7F0", pill_text="#9E9484"):
    """Top bar of a browser window: traffic lights + an address pill."""
    pill_w = min(420, w * 0.42)
    pill_x = (w - pill_w) / 2
    return f"""
  <path d="M0 {radius}a{radius} {radius} 0 0 1 {radius}-{radius}h{w - 2 * radius}a{radius} {radius} 0 0 1 {radius} {radius}v{bar - radius}H0Z" fill="{chrome}"/>
  <circle cx="26" cy="{bar / 2:.0f}" r="5.5" fill="{dot}"/>
  <circle cx="46" cy="{bar / 2:.0f}" r="5.5" fill="{dot}"/>
  <circle cx="66" cy="{bar / 2:.0f}" r="5.5" fill="{dot}"/>
  <rect x="{pill_x:.0f}" y="{bar / 2 - 12:.0f}" width="{pill_w:.0f}" height="24" rx="12" fill="{pill}"/>
  <text x="{w / 2:.0f}" y="{bar / 2 + 4:.0f}" font-family="Inter,system-ui,sans-serif" font-size="12"
        fill="{pill_text}" text-anchor="middle">{esc(url)}</text>
"""


def book_cover(x, y, w, h, bg, fg, band, title, author, serif=True, spine=True):
    """A small stylised book cover with a title block and a spine highlight."""
    fam = "Lora,Georgia,serif" if serif else "Inter,system-ui,sans-serif"
    ts = max(9, min(w * 0.125, 30))
    parts = [
        f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="3" fill="{bg}"/>',
    ]
    if spine:
        parts.append(f'<rect x="{x}" y="{y}" width="{max(3, w * 0.055):.1f}" height="{h}" fill="{band}" opacity=".85"/>')
    parts.append(
        f'<rect x="{x + w * 0.16:.1f}" y="{y + h * 0.60:.1f}" width="{w * 0.5:.1f}" height="2" fill="{band}"/>')
    # Title, wrapped to the cover width.
    lines = textwrap.wrap(title, width=max(7, int((w * 0.70) / (ts * 0.52))))[:3]
    ty = y + h * 0.26
    for ln in lines:
        parts.append(
            f'<text x="{x + w * 0.16:.1f}" y="{ty:.1f}" font-family="{fam}" font-size="{ts:.1f}" '
            f'font-weight="600" fill="{fg}">{esc(ln)}</text>')
        ty += ts * 1.18
    parts.append(
        f'<text x="{x + w * 0.16:.1f}" y="{y + h * 0.76:.1f}" font-family="Inter,system-ui,sans-serif" '
        f'font-size="{max(6, ts * 0.52):.1f}" letter-spacing="1.2" fill="{fg}" opacity=".7">{esc(author.upper())}</text>')
    return "".join(parts)


def text_lines(x, y, widths, gap=13, h=7, fill="#CFC7BA", opacity="1", rx=3.5):
    """Placeholder body copy — a stack of rounded bars."""
    out = []
    for i, w in enumerate(widths):
        out.append(f'<rect x="{x}" y="{y + i * gap}" width="{w}" height="{h}" rx="{rx}" '
                   f'fill="{fill}" opacity="{opacity}"/>')
    return "".join(out)


# --------------------------------------------------------------------------
# Sample-site mockups
# --------------------------------------------------------------------------

GENRES = [
    dict(
        slug="literary-fiction",
        url="claraveldenbooks.com",
        name="Clara Velden", nav=["Books", "Essays", "About", "Journal"],
        headline=["The quiet between", "two winters"],
        sub="A novel about the year my mother stopped speaking, and the year she started again.",
        cta="Read an excerpt",
        page="#FBF7EE", ink="#2A2B26", body="#6A6A5F", accent="#5F7A6B",
        soft="#DCE5DE", chrome_tone="#EDE7DC",
        cover=dict(bg="#5F7A6B", fg="#F4F1E7", band="#B8D3C1", title="The Quiet Between Two Winters", author="Clara Velden"),
        shelf=[("#3E4834", "#EDE8DC", "Salt Hours"), ("#A99B82", "#2A2B26", "Essays"), ("#B8D3C1", "#2A2B26", "Small Fires")],
        strip="Two novels + essays",
    ),
    dict(
        slug="romance-series",
        url="nadiaburkeauthor.com",
        name="Nadia Burke", nav=["The Series", "Reading Order", "Extras", "Newsletter"],
        headline=["Eleven books.", "One harbour town."],
        sub="Start with Harbour Lights — then work your way down the coast with the Blackwater Bay series.",
        cta="Start book one",
        page="#FFF6F3", ink="#4A2630", body="#7A5A60", accent="#C2566B",
        soft="#F3D9DD", chrome_tone="#F0E3E0",
        cover=dict(bg="#C2566B", fg="#FFF4F1", band="#F3D9DD", title="Harbour Lights", author="Nadia Burke"),
        shelf=[("#8E3B52", "#FFF4F1", "Tidewater"), ("#E08A8A", "#4A2630", "Saltlines"), ("#F3D9DD", "#4A2630", "Low Season")],
        strip="11-book backlist",
    ),
    dict(
        slug="thriller",
        url="marcusokorothrillers.com",
        name="Marcus Okoro", nav=["Books", "The Vane Files", "Press", "Contact"],
        headline=["Everyone lied.", "She kept the tapes."],
        sub="The seventh Detective Vane thriller. Out now in hardback, ebook, and audio.",
        cta="Buy the new one",
        page="#14181F", ink="#F2F2F0", body="#A7ADB6", accent="#C8442E",
        soft="#242B36", chrome_tone="#2A313C",
        chrome_dark=True,
        cover=dict(bg="#1B222C", fg="#F2F2F0", band="#C8442E", title="The Tapes She Kept", author="Marcus Okoro"),
        shelf=[("#C8442E", "#14181F", "Cold Room"), ("#2A313C", "#F2F2F0", "Nightshift"), ("#3E4756", "#F2F2F0", "Blackout")],
        strip="Traditionally published",
    ),
    dict(
        slug="non-fiction-speaker",
        url="drhelenashaw.com",
        name="Dr Helena Shaw", nav=["Book", "Speaking", "Workshops", "Media kit"],
        headline=["The attention", "we can still afford"],
        sub="A book, a keynote, and a two-day workshop on doing deep work in a fractured decade.",
        cta="Book a keynote",
        page="#F7FAFA", ink="#1E3438", body="#5F7379", accent="#3E6B73",
        soft="#CEE0E2", chrome_tone="#E4EDED",
        cover=dict(bg="#3E6B73", fg="#F4FAFA", band="#A6CDD2", title="The Attention We Can Still Afford", author="Helena Shaw"),
        shelf=[("#1E3438", "#F4FAFA", "Deep Hours"), ("#A6CDD2", "#1E3438", "Workbook"), ("#CEE0E2", "#1E3438", "Talks")],
        strip="Speaking + workshops",
    ),
    dict(
        slug="childrens",
        url="pipandthemoonbooks.com",
        name="Rosie Wren", nav=["Books", "For teachers", "School visits", "Hello"],
        headline=["Pip is not", "sleepy. Not yet."],
        sub="Picture books for the last twenty minutes of the day. Plus free classroom packs for teachers.",
        cta="Meet Pip",
        page="#FFFBEF", ink="#3B2E1E", body="#7A6A52", accent="#E08A2B",
        soft="#FCE6BC", chrome_tone="#F5EAD4",
        cover=dict(bg="#F2B441", fg="#3B2E1E", band="#E08A2B", title="Pip Is Not Sleepy", author="Rosie Wren", serif=False),
        shelf=[("#7EA9C9", "#FFFBEF", "Pip Swims"), ("#E08A2B", "#FFFBEF", "Pip Counts"), ("#9FC08A", "#3B2E1E", "Pip Digs")],
        strip="Picture books + school visits",
        playful=True,
    ),
    dict(
        slug="epic-fantasy",
        url="thorncrownsaga.com",
        name="A. K. Marsh", nav=["The Saga", "The World", "Store", "Map"],
        headline=["Six kingdoms.", "One borrowed crown."],
        sub="The Thorncrown Saga, direct from the author — signed hardbacks, ebooks, and the audio boxset.",
        cta="Visit the store",
        page="#191428", ink="#F3EEE2", body="#A79BC0", accent="#C9A227",
        soft="#2A2140", chrome_tone="#2E2545",
        chrome_dark=True,
        cover=dict(bg="#2A2140", fg="#F3EEE2", band="#C9A227", title="The Borrowed Crown", author="A. K. Marsh"),
        shelf=[("#C9A227", "#191428", "Thornfall"), ("#4A3B6E", "#F3EEE2", "Ashroot"), ("#2A2140", "#C9A227", "Boxset")],
        strip="Direct-sales store",
    ),
]


def sample_site(g, w=1280, h=920):
    """One genre mockup: browser window wrapped around a designed author homepage."""
    bar = 50
    dark = g.get("chrome_dark")
    chrome_kw = dict(chrome=g["chrome_tone"])
    if dark:
        chrome_kw.update(dot="#59616E", pill="#1B2129", pill_text="#8A93A0")
    else:
        chrome_kw.update(dot="#CFC5B4", pill="#FBF7F0", pill_text="#9E9484")

    ink, body, accent, page, soft = g["ink"], g["body"], g["accent"], g["page"], g["soft"]
    pad = 64
    inner_w = w - pad * 2

    s = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" '
         f'role="img" aria-label="{esc(g["name"])} author website — {esc(g["strip"])}">',
         '<defs>',
         f'<clipPath id="clip-{g["slug"]}"><rect x="0" y="0" width="{w}" height="{h}" rx="18"/></clipPath>',
         f'<linearGradient id="glow-{g["slug"]}" x1="0" y1="0" x2="0" y2="1">'
         f'<stop offset="0" stop-color="{accent}" stop-opacity=".18"/>'
         f'<stop offset="1" stop-color="{accent}" stop-opacity="0"/></linearGradient>',
         '</defs>',
         f'<g clip-path="url(#clip-{g["slug"]})">',
         f'<rect width="{w}" height="{h}" fill="{page}"/>',
         browser_chrome(w, g["url"], bar=bar, **chrome_kw),
         f'<rect x="0" y="{bar}" width="{w}" height="{h - bar}" fill="{page}"/>',
         f'<rect x="0" y="{bar}" width="{w}" height="360" fill="url(#glow-{g["slug"]})"/>']

    # ---- site header ----
    hy = bar + 52
    s.append(f'<text x="{pad}" y="{hy}" font-family="Lora,Georgia,serif" font-size="26" font-weight="600" '
             f'fill="{ink}" letter-spacing=".5">{esc(g["name"])}</text>')
    nx = w - pad
    for label in reversed(g["nav"]):
        nx -= len(label) * 8 + 34
    for label in g["nav"]:
        s.append(f'<text x="{nx}" y="{hy - 6}" font-family="Inter,system-ui,sans-serif" font-size="14" '
                 f'fill="{body}">{esc(label)}</text>')
        nx += len(label) * 8 + 34
    s.append(f'<rect x="{pad}" y="{hy + 30}" width="{inner_w}" height="1" fill="{ink}" opacity=".12"/>')

    # ---- hero ----
    ty = hy + 118
    s.append(f'<text x="{pad}" y="{ty - 46}" font-family="Inter,system-ui,sans-serif" font-size="12" '
             f'font-weight="700" letter-spacing="3" fill="{accent}">{esc(g["strip"].upper())}</text>')
    for i, line in enumerate(g["headline"]):
        s.append(f'<text x="{pad}" y="{ty + i * 62}" font-family="Lora,Georgia,serif" font-size="54" '
                 f'font-weight="600" fill="{ink}">{esc(line)}</text>')
    sy = ty + len(g["headline"]) * 62 + 12
    for i, line in enumerate(textwrap.wrap(g["sub"], 46)):
        s.append(f'<text x="{pad}" y="{sy + i * 28}" font-family="Inter,system-ui,sans-serif" font-size="17" '
                 f'fill="{body}">{esc(line)}</text>')
    by = sy + len(textwrap.wrap(g["sub"], 46)) * 28 + 26
    cta_w = len(g["cta"]) * 9.5 + 60
    s.append(f'<rect x="{pad}" y="{by}" width="{cta_w:.0f}" height="52" rx="10" fill="{accent}"/>')
    s.append(f'<text x="{pad + cta_w / 2:.0f}" y="{by + 32}" font-family="Inter,system-ui,sans-serif" font-size="16" '
             f'font-weight="600" fill="{page}" text-anchor="middle">{esc(g["cta"])}</text>')
    s.append(f'<rect x="{pad + cta_w + 14:.0f}" y="{by}" width="150" height="52" rx="10" fill="none" '
             f'stroke="{ink}" stroke-opacity=".22"/>')
    s.append(f'<text x="{pad + cta_w + 89:.0f}" y="{by + 32}" font-family="Inter,system-ui,sans-serif" font-size="16" '
             f'fill="{body}" text-anchor="middle">All retailers</text>')

    # ---- hero cover ----
    cw, ch = 300, 450
    cx, cy = w - pad - cw - 20, bar + 96
    s.append(f'<rect x="{cx + 16}" y="{cy + 22}" width="{cw}" height="{ch}" rx="6" fill="{ink}" opacity=".16"/>')
    s.append(book_cover(cx, cy, cw, ch, **g["cover"]))

    # ---- shelf strip ----
    shy = h - 210
    s.append(f'<rect x="0" y="{shy - 54}" width="{w}" height="{h - shy + 54}" fill="{soft}" opacity=".55"/>')
    s.append(f'<text x="{pad}" y="{shy - 16}" font-family="Lora,Georgia,serif" font-size="22" font-weight="600" '
             f'fill="{ink}">More books</text>')
    s.append(f'<text x="{w - pad}" y="{shy - 16}" font-family="Inter,system-ui,sans-serif" font-size="14" '
             f'fill="{accent}" text-anchor="end">See all books →</text>')
    bx = pad
    for bg, fg, title in g["shelf"]:
        s.append(book_cover(bx, shy + 8, 118, 172, bg=bg, fg=fg, band=accent, title=title, author=g["name"].split()[-1]))
        bx += 146
    # newsletter capture block on the right of the shelf
    nlx = pad + 3 * 146 + 40
    nlw = w - pad - nlx
    if nlw > 240:
        s.append(f'<rect x="{nlx}" y="{shy + 8}" width="{nlw}" height="172" rx="12" fill="{page}" '
                 f'stroke="{ink}" stroke-opacity=".10"/>')
        s.append(f'<text x="{nlx + 24}" y="{shy + 46}" font-family="Lora,Georgia,serif" font-size="19" '
                 f'font-weight="600" fill="{ink}">Get the free first chapter</text>')
        s.append(f'<text x="{nlx + 24}" y="{shy + 72}" font-family="Inter,system-ui,sans-serif" font-size="13" '
                 f'fill="{body}">One email when there is a new book. Nothing else.</text>')
        s.append(f'<rect x="{nlx + 24}" y="{shy + 92}" width="{nlw - 150}" height="42" rx="8" fill="{soft}" opacity=".7"/>')
        s.append(f'<text x="{nlx + 40}" y="{shy + 119}" font-family="Inter,system-ui,sans-serif" font-size="13" '
                 f'fill="{body}" opacity=".8">you@email.com</text>')
        s.append(f'<rect x="{nlx + nlw - 118}" y="{shy + 92}" width="94" height="42" rx="8" fill="{accent}"/>')
        s.append(f'<text x="{nlx + nlw - 71}" y="{shy + 119}" font-family="Inter,system-ui,sans-serif" font-size="13" '
                 f'font-weight="600" fill="{page}" text-anchor="middle">Send it</text>')

    s.append('</g>')
    s.append(f'<rect x=".5" y=".5" width="{w - 1}" height="{h - 1}" rx="18" fill="none" stroke="{ink}" stroke-opacity=".12"/>')
    s.append('</svg>')
    return "\n".join(s)


# --------------------------------------------------------------------------
# Hero: a desktop author site with a phone beside it
# --------------------------------------------------------------------------

def hero(w=1330, h=930):
    g = GENRES[0]
    dw, dh = 1000, 700
    dx, dy = 30, 46
    bar = 46
    ink, body, accent, page, soft = g["ink"], g["body"], g["accent"], g["page"], g["soft"]

    s = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" '
         'role="img" aria-label="An AuthorWings author website shown on a laptop and a phone">',
         '<defs>',
         f'<clipPath id="hero-desk"><rect x="{dx}" y="{dy}" width="{dw}" height="{dh}" rx="16"/></clipPath>',
         '<clipPath id="hero-phone"><rect x="940" y="258" width="330" height="600" rx="38"/></clipPath>',
         '<linearGradient id="hero-glow" x1="0" y1="0" x2="0" y2="1">'
         f'<stop offset="0" stop-color="{accent}" stop-opacity=".20"/>'
         f'<stop offset="1" stop-color="{accent}" stop-opacity="0"/></linearGradient>',
         '<filter id="hero-shadow" x="-20%" y="-20%" width="140%" height="140%">'
         '<feDropShadow dx="0" dy="26" stdDeviation="30" flood-color="#2B3124" flood-opacity=".20"/></filter>',
         '<filter id="phone-shadow" x="-30%" y="-20%" width="160%" height="140%">'
         '<feDropShadow dx="-8" dy="20" stdDeviation="24" flood-color="#2B3124" flood-opacity=".26"/></filter>',
         '</defs>']

    # ---- desktop ----
    s.append('<g filter="url(#hero-shadow)">')
    s.append(f'<rect x="{dx}" y="{dy}" width="{dw}" height="{dh}" rx="16" fill="{page}"/>')
    s.append('<g clip-path="url(#hero-desk)">')
    s.append(f'<g transform="translate({dx},{dy})">')
    s.append(browser_chrome(dw, g["url"], bar=bar, radius=16))
    s.append(f'<rect x="0" y="{bar}" width="{dw}" height="{dh - bar}" fill="{page}"/>')
    s.append(f'<rect x="0" y="{bar}" width="{dw}" height="320" fill="url(#hero-glow)"/>')

    pad = 52
    hy = bar + 46
    s.append(f'<text x="{pad}" y="{hy}" font-family="Lora,Georgia,serif" font-size="24" font-weight="600" '
             f'fill="{ink}">{esc(g["name"])}</text>')
    nx = dw - pad - 300
    for label in g["nav"]:
        s.append(f'<text x="{nx}" y="{hy - 6}" font-family="Inter,system-ui,sans-serif" font-size="13" '
                 f'fill="{body}">{esc(label)}</text>')
        nx += len(label) * 7.6 + 26
    s.append(f'<rect x="{pad}" y="{hy + 26}" width="{dw - pad * 2}" height="1" fill="{ink}" opacity=".12"/>')

    ty = hy + 116
    s.append(f'<text x="{pad}" y="{ty - 42}" font-family="Inter,system-ui,sans-serif" font-size="11" '
             f'font-weight="700" letter-spacing="3" fill="{accent}">NEW NOVEL — OUT NOW</text>')
    for i, line in enumerate(g["headline"]):
        s.append(f'<text x="{pad}" y="{ty + i * 54}" font-family="Lora,Georgia,serif" font-size="46" '
                 f'font-weight="600" fill="{ink}">{esc(line)}</text>')
    sy = ty + len(g["headline"]) * 54 + 8
    for i, line in enumerate(textwrap.wrap(g["sub"], 40)):
        s.append(f'<text x="{pad}" y="{sy + i * 25}" font-family="Inter,system-ui,sans-serif" font-size="15" '
                 f'fill="{body}">{esc(line)}</text>')
    by = sy + len(textwrap.wrap(g["sub"], 40)) * 25 + 22
    s.append(f'<rect x="{pad}" y="{by}" width="180" height="48" rx="9" fill="{accent}"/>')
    s.append(f'<text x="{pad + 90}" y="{by + 30}" font-family="Inter,system-ui,sans-serif" font-size="15" '
             f'font-weight="600" fill="{page}" text-anchor="middle">Read an excerpt</text>')
    s.append(f'<rect x="{pad + 194}" y="{by}" width="150" height="48" rx="9" fill="none" stroke="{ink}" stroke-opacity=".22"/>')
    s.append(f'<text x="{pad + 269}" y="{by + 30}" font-family="Inter,system-ui,sans-serif" font-size="15" '
             f'fill="{body}" text-anchor="middle">All retailers</text>')

    s.append(f'<rect x="{dw - 350}" y="{bar + 74}" width="264" height="396" rx="6" fill="{ink}" opacity=".16" '
             f'transform="translate(14,20)"/>')
    s.append(book_cover(dw - 350, bar + 74, 264, 396, **g["cover"]))

    shy = dh - 150
    s.append(f'<rect x="0" y="{shy - 40}" width="{dw}" height="{dh - shy + 40}" fill="{soft}" opacity=".5"/>')
    s.append(f'<text x="{pad}" y="{shy - 10}" font-family="Lora,Georgia,serif" font-size="19" font-weight="600" '
             f'fill="{ink}">The backlist</text>')
    bx = pad
    for bgc, fgc, title in g["shelf"]:
        s.append(book_cover(bx, shy + 4, 92, 134, bg=bgc, fg=fgc, band=accent, title=title, author="Velden"))
        bx += 116
    s.append(f'<rect x="{bx + 20}" y="{shy + 4}" width="300" height="134" rx="10" fill="{page}" stroke="{ink}" stroke-opacity=".10"/>')
    s.append(f'<text x="{bx + 44}" y="{shy + 40}" font-family="Lora,Georgia,serif" font-size="16" font-weight="600" '
             f'fill="{ink}">Free first chapter</text>')
    s.append(f'<rect x="{bx + 44}" y="{shy + 56}" width="180" height="34" rx="7" fill="{soft}" opacity=".8"/>')
    s.append(f'<rect x="{bx + 232}" y="{shy + 56}" width="46" height="34" rx="7" fill="{accent}"/>')
    s.append(f'<text x="{bx + 58}" y="{shy + 78}" font-family="Inter,system-ui,sans-serif" font-size="12" '
             f'fill="{body}" opacity=".8">you@email.com</text>')
    s.append('</g></g>')
    s.append(f'<rect x="{dx + .5}" y="{dy + .5}" width="{dw - 1}" height="{dh - 1}" rx="16" fill="none" '
             f'stroke="{ink}" stroke-opacity=".14"/>')
    s.append('</g>')

    # ---- phone ----
    px, py, pw, ph = 940, 258, 330, 600
    s.append('<g filter="url(#phone-shadow)">')
    s.append(f'<rect x="{px - 10}" y="{py - 10}" width="{pw + 20}" height="{ph + 20}" rx="46" fill="#2A2E28"/>')
    s.append(f'<rect x="{px}" y="{py}" width="{pw}" height="{ph}" rx="38" fill="{page}"/>')
    s.append('<g clip-path="url(#hero-phone)">')
    s.append(f'<rect x="{px}" y="{py}" width="{pw}" height="200" fill="url(#hero-glow)"/>')
    s.append(f'<rect x="{px + pw / 2 - 40:.0f}" y="{py + 14}" width="80" height="7" rx="3.5" fill="#2A2E28" opacity=".5"/>')
    s.append(f'<text x="{px + 26}" y="{py + 66}" font-family="Lora,Georgia,serif" font-size="19" font-weight="600" '
             f'fill="{ink}">{esc(g["name"])}</text>')
    for i in range(3):
        s.append(f'<rect x="{px + pw - 50}" y="{py + 52 + i * 7}" width="24" height="2.5" rx="1.25" fill="{body}"/>')
    s.append(f'<rect x="{px + 26}" y="{py + 86}" width="{pw - 52}" height="1" fill="{ink}" opacity=".12"/>')
    s.append(f'<text x="{px + 26}" y="{py + 122}" font-family="Inter,system-ui,sans-serif" font-size="10" '
             f'font-weight="700" letter-spacing="2.4" fill="{accent}">OUT NOW</text>')
    s.append(f'<text x="{px + 26}" y="{py + 156}" font-family="Lora,Georgia,serif" font-size="27" font-weight="600" '
             f'fill="{ink}">The quiet</text>')
    s.append(f'<text x="{px + 26}" y="{py + 187}" font-family="Lora,Georgia,serif" font-size="27" font-weight="600" '
             f'fill="{ink}">between</text>')
    s.append(text_lines(px + 26, py + 208, [pw - 60, pw - 76, pw - 110], gap=15, h=7, fill=body, opacity=".28"))
    s.append(f'<rect x="{px + 26}" y="{py + 268}" width="150" height="42" rx="8" fill="{accent}"/>')
    s.append(f'<text x="{px + 101}" y="{py + 295}" font-family="Inter,system-ui,sans-serif" font-size="13" '
             f'font-weight="600" fill="{page}" text-anchor="middle">Read an excerpt</text>')
    s.append(book_cover(px + 26, py + 334, 122, 182, **g["cover"]))
    s.append(f'<rect x="{px + 164}" y="{py + 334}" width="{pw - 190}" height="182" rx="10" fill="{soft}" opacity=".5"/>')
    s.append(f'<text x="{px + 182}" y="{py + 366}" font-family="Lora,Georgia,serif" font-size="14" font-weight="600" '
             f'fill="{ink}">Free chapter</text>')
    s.append(text_lines(px + 182, py + 380, [96, 76], gap=13, h=6, fill=body, opacity=".3"))
    s.append(f'<rect x="{px + 182}" y="{py + 416}" width="{pw - 226}" height="34" rx="7" fill="{page}"/>')
    s.append(f'<rect x="{px + 182}" y="{py + 458}" width="{pw - 226}" height="34" rx="7" fill="{accent}"/>')
    s.append(f'<text x="{px + 182 + (pw - 226) / 2:.0f}" y="{py + 480}" font-family="Inter,system-ui,sans-serif" '
             f'font-size="12" font-weight="600" fill="{page}" text-anchor="middle">Send it</text>')
    s.append(f'<rect x="{px}" y="{py + ph - 56}" width="{pw}" height="56" fill="{soft}" opacity=".55"/>')
    for i, lab in enumerate(["Books", "About", "List"]):
        s.append(f'<text x="{px + 56 + i * 106}" y="{py + ph - 22}" font-family="Inter,system-ui,sans-serif" '
                 f'font-size="12" fill="{body}" text-anchor="middle">{lab}</text>')
    s.append('</g>')
    s.append(f'<rect x="{px}" y="{py}" width="{pw}" height="{ph}" rx="38" fill="none" stroke="#2A2E28" stroke-opacity=".35"/>')
    s.append('</g>')
    s.append('</svg>')
    return "\n".join(s)


# --------------------------------------------------------------------------
# Dashboard preview for the "one dashboard, thirteen panels" band
# --------------------------------------------------------------------------

PANELS = ["Overview", "Books & projects", "Leads", "Subscribers", "Contact form", "Email delivery",
          "Marketing & tracking", "AI & SEO", "Site assistant", "Chat logs", "Popups & bar",
          "Redirects", "Login & access"]


def dashboard(w=1180, h=760):
    bar = 46
    side = 258
    ink = "#EDE7DA"
    muted = "#8FA3A0"
    s = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" '
         'role="img" aria-label="The AuthorWings dashboard — thirteen panels in one place">',
         '<defs>',
         f'<clipPath id="dash-clip"><rect width="{w}" height="{h}" rx="16"/></clipPath>',
         '</defs>',
         '<g clip-path="url(#dash-clip)">',
         f'<rect width="{w}" height="{h}" fill="{PINE_2}"/>',
         browser_chrome(w, "yourbooks.com/wp-admin", bar=bar, radius=16, chrome="#0B2423",
                        dot="#3E5A57", pill="#0F2F2E", pill_text="#7E9694"),
         f'<rect x="0" y="{bar}" width="{side}" height="{h - bar}" fill="{PINE}"/>']

    s.append(f'<text x="26" y="{bar + 44}" font-family="Lora,Georgia,serif" font-size="17" font-weight="600" '
             f'fill="{ink}">AuthorWings</text>')
    s.append(f'<rect x="26" y="{bar + 60}" width="{side - 52}" height="1" fill="#FFFFFF" opacity=".12"/>')
    y = bar + 92
    for i, p in enumerate(PANELS):
        active = i == 2
        if active:
            s.append(f'<rect x="14" y="{y - 20}" width="{side - 28}" height="34" rx="8" fill="{TERRA}" opacity=".92"/>')
        s.append(f'<rect x="30" y="{y - 11}" width="14" height="14" rx="3" fill="{"#FFFDF9" if active else muted}" '
                 f'opacity="{".9" if active else ".55"}"/>')
        s.append(f'<text x="56" y="{y}" font-family="Inter,system-ui,sans-serif" font-size="13.5" '
                 f'fill="{"#FFFDF9" if active else muted}" font-weight="{"600" if active else "400"}">{esc(p)}</text>')
        y += 42

    # main pane — leads inbox
    mx = side + 30
    mw = w - mx - 30
    s.append(f'<text x="{mx}" y="{bar + 50}" font-family="Lora,Georgia,serif" font-size="24" font-weight="600" '
             f'fill="{ink}">Leads</text>')
    s.append(f'<rect x="{mx + mw - 132}" y="{bar + 26}" width="132" height="36" rx="8" fill="{TERRA}"/>')
    s.append(f'<text x="{mx + mw - 66}" y="{bar + 50}" font-family="Inter,system-ui,sans-serif" font-size="13" '
             f'font-weight="600" fill="#FFFDF9" text-anchor="middle">Export CSV</text>')

    stats = [("142", "leads this month"), ("1,308", "subscribers"), ("96", "assistant chats"), ("0", "lost to bounces")]
    sw = (mw - 3 * 16) / 4
    for i, (n, lab) in enumerate(stats):
        x = mx + i * (sw + 16)
        s.append(f'<rect x="{x:.0f}" y="{bar + 78}" width="{sw:.0f}" height="92" rx="12" fill="#FFFFFF" opacity=".05"/>')
        s.append(f'<rect x="{x:.0f}" y="{bar + 78}" width="{sw:.0f}" height="92" rx="12" fill="none" stroke="#FFFFFF" stroke-opacity=".10"/>')
        s.append(f'<text x="{x + 20:.0f}" y="{bar + 124}" font-family="Lora,Georgia,serif" font-size="30" '
                 f'font-weight="600" fill="{ink}">{n}</text>')
        s.append(f'<text x="{x + 20:.0f}" y="{bar + 148}" font-family="Inter,system-ui,sans-serif" font-size="12" '
                 f'fill="{muted}">{esc(lab)}</text>')

    ty = bar + 196
    s.append(f'<rect x="{mx}" y="{ty}" width="{mw}" height="{h - ty - 34}" rx="12" fill="#FFFFFF" opacity=".05"/>')
    s.append(f'<rect x="{mx}" y="{ty}" width="{mw}" height="{h - ty - 34}" rx="12" fill="none" stroke="#FFFFFF" stroke-opacity=".10"/>')
    cols = [("Name", 0.06), ("Email", 0.30), ("Source", 0.60), ("When", 0.82)]
    for lab, f in cols:
        s.append(f'<text x="{mx + mw * f:.0f}" y="{ty + 34}" font-family="Inter,system-ui,sans-serif" font-size="11" '
                 f'font-weight="700" letter-spacing="1.4" fill="{muted}">{lab.upper()}</text>')
    s.append(f'<rect x="{mx + 1}" y="{ty + 48}" width="{mw - 2}" height="1" fill="#FFFFFF" opacity=".10"/>')
    rows = [("Rebecca Hall", "r.hall@…", "Free chapter popup", "4 min ago"),
            ("Tomás Ferrer", "tomas@…", "Site assistant", "1 hr ago"),
            ("Priya Nandakumar", "priya@…", "Contact form", "3 hrs ago"),
            ("Book club, Leeds", "leeds@…", "Events page", "Yesterday"),
            ("Ade Balogun", "ade@…", "Footer signup", "Yesterday"),
            ("Marta Kowalczyk", "marta@…", "Manuscript upload", "2 days ago")]
    ry = ty + 80
    for i, r in enumerate(rows):
        if i == 0:
            s.append(f'<rect x="{mx + 1}" y="{ry - 22}" width="{mw - 2}" height="38" fill="{TERRA}" opacity=".10"/>')
            s.append(f'<circle cx="{mx + mw - 26}" cy="{ry - 4}" r="4" fill="{TERRA_L}"/>')
        for (lab, f), val in zip(cols, r):
            s.append(f'<text x="{mx + mw * f:.0f}" y="{ry}" font-family="Inter,system-ui,sans-serif" font-size="13" '
                     f'fill="{ink if f < 0.3 else muted}">{esc(val)}</text>')
        ry += 44
    s.append('</g>')
    s.append(f'<rect x=".5" y=".5" width="{w - 1}" height="{h - 1}" rx="16" fill="none" stroke="#FFFFFF" stroke-opacity=".14"/>')
    s.append('</svg>')
    return "\n".join(s)


# --------------------------------------------------------------------------
# Testimonial avatars — monogram discs
# --------------------------------------------------------------------------

def avatar(initials, bg, fg, size=120):
    return f"""
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {size} {size}" width="{size}" height="{size}" role="img" aria-label="Author portrait placeholder">
  <circle cx="{size/2}" cy="{size/2}" r="{size/2}" fill="{bg}"/>
  <text x="{size/2}" y="{size/2 + size*0.135:.1f}" font-family="Lora,Georgia,serif" font-size="{size*0.38:.0f}"
        font-weight="600" fill="{fg}" text-anchor="middle">{esc(initials)}</text>
</svg>
"""


# --------------------------------------------------------------------------
# Open Graph / social card
# --------------------------------------------------------------------------

def og_image(w=1200, h=630):
    return f"""
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" role="img" aria-label="AuthorWings — author websites">
  <defs>
    <linearGradient id="og-bg" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0" stop-color="{PINE}"/><stop offset="1" stop-color="#0A2322"/>
    </linearGradient>
  </defs>
  <rect width="{w}" height="{h}" fill="url(#og-bg)"/>
  <circle cx="{w - 120}" cy="{h - 90}" r="260" fill="{TERRA}" opacity=".14"/>
  <text x="80" y="120" font-family="Inter,system-ui,sans-serif" font-size="18" font-weight="700"
        letter-spacing="4" fill="{TERRA_L}">AUTHORWINGS — AUTHOR WEBSITES</text>
  <text x="80" y="250" font-family="Lora,Georgia,serif" font-size="72" font-weight="600" fill="{CREAM}">A home for your books</text>
  <text x="80" y="335" font-family="Lora,Georgia,serif" font-size="72" font-weight="600" fill="{CREAM}">that works while you write.</text>
  <text x="80" y="410" font-family="Inter,system-ui,sans-serif" font-size="24" fill="#B9C9C4">Designed, built, and launched in 3–4 weeks. You own everything.</text>
  <rect x="80" y="470" width="230" height="62" rx="10" fill="{TERRA}"/>
  <text x="195" y="509" font-family="Inter,system-ui,sans-serif" font-size="19" font-weight="600"
        fill="{CREAM}" text-anchor="middle">Book a free consult</text>
  <text x="340" y="509" font-family="Inter,system-ui,sans-serif" font-size="17" fill="#8FA3A0">authorwings.com/author-websites</text>
</svg>
"""


# --------------------------------------------------------------------------

if __name__ == "__main__":
    print("Writing SVG assets to assets/img/ …")
    write("hero-author-website.svg", hero())
    write("dashboard-panels.svg", dashboard())
    for g in GENRES:
        write(f"sample-{g['slug']}.svg", sample_site(g))
    for initials, bg, fg, slug in [("CV", "#3E4834", CREAM, "clara"),
                                   ("NB", "#8E3B52", "#FFF4F1", "nadia"),
                                   ("HS", "#3E6B73", "#F4FAFA", "helena")]:
        write(f"avatar-{slug}.svg", avatar(initials, bg, fg))
    write("og-author-websites.svg", og_image())
    print("Done.")
