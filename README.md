# portfolio

Personal site — [0xyuri.vercel.app](https://0xyuri.vercel.app)

Static multi-page site: plain HTML + CSS + a little vanilla JS. No framework, no build step to deploy — Vercel serves the files as-is.

- Modern dark theme (default) with a light toggle; emerald accent
- Space Grotesk + JetBrains Mono
- Full-colour technology logos (Simple Icons, CC0) + Lucide UI icons, inlined as an SVG sprite
- Home + a detail page per project (`projects/*.html`)
- Inline SVG architecture diagram for [Aegis](https://github.com/0xYurii/Aegis)
- SEO + Open Graph / Twitter meta, generated share image

## Structure

```
index.html            home (hero, work, about, skills, contact)
projects/*.html        one detail page per project
styles.css  script.js  shared styles + behaviour
cv/                    downloadable CV
img/                   covers, og image, touch icon
tools/                 build.py + sources (regenerate the HTML)
```

## Editing

The HTML pages are generated from `tools/build.py` (content, CSS in `tools/site.css`, JS in `tools/site.js`).
Edit those and run `python3 tools/build.py` to regenerate `index.html`, `projects/*.html`, and `styles.css` / `script.js`.
You can also edit the built files directly — they're plain static HTML.
