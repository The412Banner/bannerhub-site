# BannerHub website

**🌐 Live site: <https://the412banner.github.io/bannerhub-site/>**

The official landing &amp; documentation site for the three BannerHub products — a static, dependency-free multi-page site served by GitHub Pages (from `main` / root).

## The three products

| Product | Repo | Base | Latest |
| --- | --- | --- | --- |
| **BannerHub Lite** | [Bannerhub-Lite](https://github.com/The412Banner/Bannerhub-Lite) | GameHub Lite 5.1.4 | `v1.0.2` |
| **BannerHub** | [BannerHub](https://github.com/The412Banner/BannerHub) | GameHub 5.3.5 (ReVanced) | `v3.7.5` |
| **BannerHub v6** | [bannerhub-revanced](https://github.com/The412Banner/bannerhub-revanced) | XiaoJi GameHub 6.0.8 | `v1.0.0-608` |

The three are **separate projects** with their own package names, keystores, and component/Steam backends — they don't update over one another. The site exists to explain the differences and document each one.

## Pages

| Page | File | What it covers |
| --- | --- | --- |
| Home | `index.html` | Hero, the three product cards, the why-BannerHub teaser |
| Why BannerHub | `why.html` | The case for BannerHub over stock GameHub (and what it deliberately doesn't change) |
| Compare | `compare.html` | Three-way feature comparison matrix + GameHub lineage |
| BannerHub Lite | `lite.html` | Features, "inherited from base," per-release changelog |
| BannerHub | `bannerhub.html` | Features, "inherited from base," per-release changelog |
| BannerHub v6 | `v6.html` | Features, "inherited from base," per-release changelog |
| Privacy | `v6-privacy.html` | v6 telemetry kill/leave table with commit links |
| APIs | `apis.html` | The three backends explained (GameHub API, EmuReady API, BannerHub API) |
| Configs | `configs.html` | Community Game Configs (the `bannerhub-game-configs` library) |
| FAQ | `faq.html` | Frequently asked questions |
| Credits | `credits.html` | Full contributor / upstream credits + per-project docs &amp; reports |

**Navigation:** Why BannerHub · Compare · BannerHub Lite · BannerHub · BannerHub v6 · Privacy · **Resources ▾** (APIs · Configs · Config Library ↗) · FAQ · Credits · GitHub. The "Config Library ↗" item links out to the separate [config browser](https://the412banner.github.io/bannerhub-game-configs/), which carries a matching nav bar back to this site.

## How content stays current

Content has two tiers — **auto for data, human for judgment:**

- **Auto (version numbers):** every live version string is tagged `<span data-auto="ver:lite|full|v6">…</span>` (13 spots). [`scripts/update_releases.py`](scripts/update_releases.py) rewrites only those from each repo's latest **stable** release and refreshes [`data/releases.json`](data/releases.json). Driven by [`.github/workflows/update-site.yml`](.github/workflows/update-site.yml) (daily cron + manual + `repository_dispatch: project-release`). For instant updates, each product repo can carry [`automation/notify-site.example.yml`](automation/notify-site.example.yml) (needs a `SITE_DISPATCH_TOKEN` secret).
- **Human (changelogs, comparison matrix, prose):** never auto-guessed. The updater compares each repo's latest tag against [`data/curated.json`](data/curated.json) and, if a product has advanced past the curated content, opens a "content" staleness issue instead of editing.

### Updating the site for a new release

1. Add the new release's changelog entry to the product page (`v6.html` / `bannerhub.html` / `lite.html`) — newest first; move the `latest` class to it.
2. Update any base-version prose (base version, versionCode, build branch) and the comparison matrix if features changed.
3. Bump that product's value in `data/curated.json` to the new tag — this clears the staleness flag.
4. Commit + push. The version badges (`data-auto` spans) + `data/releases.json` are handled automatically by the updater on its next run, but you can run `python3 scripts/update_releases.py` locally to bake them immediately.

## Repo layout

```
*.html              the 11 pages (above)
assets/css/style.css   single stylesheet (dark theme)
assets/js/main.js      progressive-enhancement JS (nav, FAQ accordions, fade-in, Resources dropdown)
data/releases.json     latest stable tag/date/url per product (auto-written)
data/curated.json      tag each product's curated content currently reflects (human-bumped)
scripts/update_releases.py   the version sync + staleness check
automation/            notify workflow template + setup notes for the product repos
_data/                 release-note dumps (reference only; .gitignored, not served)
.nojekyll              serve files as-is (no Jekyll processing)
```

## Tech

Plain HTML + one CSS file + one JS file. No build step, no framework, no tracking, no third-party requests. GitHub Pages serves `main` / root directly.

## Local preview

```sh
python3 -m http.server 8080   # then open http://localhost:8080
```
