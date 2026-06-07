# BannerHub website

The official landing &amp; documentation site for the three BannerHub products — a static, dependency-free multi-page site built for GitHub Pages.

**Live site:** _(enable GitHub Pages on this repo → Settings → Pages → Deploy from branch `main` / root)_

## Pages

| Page | File | What it covers |
| --- | --- | --- |
| Home | `index.html` | Hero, the three product cards, why-BannerHub teaser |
| Why BannerHub | `why.html` | The case for BannerHub over stock GameHub (and what it doesn't change) |
| Compare | `compare.html` | Three-way feature comparison matrix |
| BannerHub Lite | `lite.html` | Features + per-release changelog |
| BannerHub | `bannerhub.html` | Features + per-release changelog |
| BannerHub v6 | `v6.html` | Features + per-release changelog |
| Privacy | `v6-privacy.html` | v6 telemetry kill/leave table |
| FAQ | `faq.html` | Frequently asked questions |

## The three products

- **BannerHub Lite** — https://github.com/The412Banner/Bannerhub-Lite (base: GameHub Lite 5.1.4)
- **BannerHub** — https://github.com/The412Banner/BannerHub (base: GameHub 5.3.5 ReVanced)
- **BannerHub v6** — https://github.com/The412Banner/bannerhub-revanced (base: XiaoJi GameHub 6.0.7)

## Tech

Plain HTML + one CSS file (`assets/css/style.css`) + one progressive-enhancement JS file (`assets/js/main.js`). No build step, no framework, no tracking. `.nojekyll` is present so GitHub Pages serves files as-is.

Content (feature lists, changelogs, the privacy table) is sourced from each repo's GitHub release notes and `PRIVACY.md`. Live version numbers auto-update from the latest stable releases — see [`automation/README.md`](automation/README.md).

## Local preview

```sh
python3 -m http.server 8080   # then open http://localhost:8080
```
