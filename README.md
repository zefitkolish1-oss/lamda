# Lamda website (static)

Plain HTML/CSS/JS, no framework, no build needed to deploy. Arabic (RTL) by default, full English toggle (`?lang=en` also works).

```
index.html  install.html  pay.html  privacy.html  terms.html  404.html
assets/css/style.css   assets/js/config.js   assets/js/main.js   assets/img/…
sitemap.xml  robots.txt  site.webmanifest  _headers  favicon.ico
_tools/   generator + asset scripts (not needed at runtime)   _shots/  QA screenshots
```

## Configure
- **APK link / version / sha256 / contact / socials:** `assets/js/config.js` (no rebuild needed).
- **Domain** (canonical, OG image, sitemap): `LAMDA_SITE=https://your.domain python3 _tools/build.py` (default placeholder `https://lamda.pages.dev`).
- **Text:** all copy lives in `_tools/build.py` (Arabic + English side by side) → `python3 _tools/build.py`.
- **Images:** `python3 _tools/gen_assets.py` re-renders the orb/favicons from `icon/lamda_icon.svg` and screenshots from `screens2/`.
  OG image: `google-chrome --headless=new --no-sandbox --window-size=1200,630 --screenshot=assets/img/og.png file://$PWD/_tools/og.html`.

## Deploy (all free)
- **Cloudflare Pages:** Dashboard → Workers & Pages → Create → Pages → *Upload assets* → drop this folder (or connect a Git repo; build command: none, output dir: `/`). `_headers` is honoured.
  CLI: `npx wrangler pages deploy . --project-name lamda`.
- **Netlify:** drag-and-drop the folder on app.netlify.com/drop, or `npx netlify-cli deploy --dir . --prod`. `_headers` is honoured.
- **GitHub Pages:** push the folder to a repo → Settings → Pages → Deploy from branch (root). Add an empty `.nojekyll` file so `_headers`/`_tools` are left alone (headers are ignored there).

## Download link — important
`apkUrl` currently points at the Google Drive file for 2.2.1. **The Drive file must be shared “Anyone with the link”**, otherwise visitors get “request access”. Drive also shows a preview page / virus-scan interstitial for big files; a direct host is nicer: GitHub Releases, Cloudflare R2 public bucket, or put the APK in this folder (Cloudflare Pages max file size is 25 MB, so the 40 MB APK does **not** fit there; Netlify allows it).

## QA
`python3 -m http.server 8787` then `node _tools/shots.mjs` (needs `npm i puppeteer-core`) → `_shots/`, console errors and broken internal links.
Lighthouse: `npx lighthouse http://localhost:8787/ --preset=desktop`.

## Placeholders to replace
Domain `lamda.pages.dev`, e-mail `hello@lamda.ai`, social URLs (@lamda.ai), payment buttons (“Coming soon”), Privacy/Terms (DRAFT — need legal review), ZainCash/FastPay/Qi tiles are text badges, not official logos.
