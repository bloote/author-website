# AuthorWings — Author Websites page

The **Author Websites** service page for [authorwings.com](https://authorwings.com),
built from the supplied design. Plain HTML, CSS, and a little progressive-
enhancement JavaScript — no build step, no framework, no third-party runtime.

Open `index.html` to preview it. Everything it needs is in the repo, so it works
offline.

---

## What's here

```
index.html                     The page — standalone, ready to preview
favicon.svg

assets/
  css/author-websites.css      All page styling, scoped under .aw-ws
  css/fonts.css                @font-face for Lora + Inter (preview only)
  fonts/*.woff2                The same font files authorwings.com serves
  js/author-websites.js        Scroll reveal, sticky-bar state, smooth anchors
  img/*.svg                    12 generated illustrations (see below)
  img/raster/*.webp            2x raster copies for the WP media library
  img/raster/og-*.png          Social card (og:image needs a raster format)

wordpress/
  author-websites-content.html Paste-in page body, generated from index.html
  enqueue.php                  Loads the CSS/JS on that page only

tools/
  make-images.py               Regenerates every SVG in assets/img/
  rasterise.mjs                Renders those SVGs to WebP + PNG
  build-wp.py                  Rebuilds the WordPress paste-in file
```

## Design

Type and colour follow the live site rather than inventing a new system.

| Token | Value | Used for |
| --- | --- | --- |
| `--ws-cream` | `#FFFDF9` | Page background |
| `--ws-pine` | `#0F2F2E` | Dark bands, featured pricing card |
| `--ws-terra` | `#C25937` | Primary buttons, accents, closing CTA band |
| `--ws-beige` | `#EFE7D9` | Timeline band |
| `--ws-ink` / `--ws-body` | `#22201C` / `#5A5346` | Headings / body copy |

Headings are **Lora** 600, body is **Inter** — the same two families
GeneratePress already loads on authorwings.com, served from the same font
files. On the live site the theme provides them, so `assets/css/fonts.css` and
`assets/fonts/` can be dropped; they exist so the standalone preview renders
correctly with no network access.

Every class is prefixed `ws-` inside a single `.aw-ws` wrapper, so nothing can
collide with GeneratePress or GenerateBlocks.

## Sections

Hero → who it's for → what's included (6) → everything under the hood (4 panels
+ the thirteen dashboard panels) → two pieces (theme + core plugin) → sample
sites (6 genres) → packages (Debut $1,450 / Author Pro $2,650 / Signature
$4,900+) → four-week timeline → add-ons → testimonials → FAQ → closing CTA.

## Images

There are no stock photos. All twelve illustrations are generated SVG — a hero
device composition, a dashboard screen, six genre sample-site mockups, three
testimonial avatars, and a social card. They stay sharp at any size, weigh
6–10 KB each, and are regenerated from source:

```bash
python3 tools/make-images.py                              # SVG
CHROMIUM_PATH=/path/to/chromium node tools/rasterise.mjs   # WebP + PNG @2x (PNGs gitignored)
```

Edit the `GENRES` list in `tools/make-images.py` to change a sample site's
author name, palette, headline, or book titles. Replace any `.svg` with a real
screenshot when client sites are ready to show — the markup does not care.

## Putting it on authorwings.com

1. Upload `assets/img/*.svg` to `/wp-content/uploads/author-websites/`.
2. Copy `assets/css/author-websites.css` and `assets/js/author-websites.js` into
   the GeneratePress child theme under `assets/css/` and `assets/js/`.
3. Add the contents of `wordpress/enqueue.php` to the child theme's
   `functions.php`.
4. Create the page at `/author-websites/`, choose a full-width template, add one
   **Custom HTML** block, and paste `wordpress/author-websites-content.html`.
5. Copy the meta title, description, and JSON-LD from the `<head>` of
   `index.html` into the site's SEO panel.

Re-run `python3 tools/build-wp.py` after any edit to `index.html` so the paste-in
file stays in sync.

## Notes

- **Accessibility** — skip link, visible focus rings, real landmarks and heading
  order, alt text on every meaningful image, 4.5:1+ contrast throughout, and
  `prefers-reduced-motion` honoured (reveals and smooth scrolling both switch
  off).
- **No-JS** — the page is complete without `author-websites.js`. The FAQ is
  native `<details>`/`<summary>`, and reveal animations fail open rather than
  leaving content invisible.
- **SEO** — canonical, Open Graph, Twitter card, plus `Service` (with a package
  `OfferCatalog`), `FAQPage`, and `BreadcrumbList` JSON-LD.
- **Links** — CTAs point at `https://authorwings.com/contact/` and
  `mailto:hello@authorwings.com`. Repoint them if the consult booking moves to a
  scheduler.
- **Placeholder copy** — testimonials use initials and genres rather than real
  names, matching the design's "Author name" placeholders. Swap in real
  attributions before publishing.
