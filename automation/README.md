# Keeping the site up to date

The site auto-tracks each project's **latest stable GitHub release** for everything
mechanical, and flags a human only for the judgment calls. Here's exactly what is and
isn't automatic.

## What updates 100% automatically

Pulled straight from the GitHub Releases API (stable releases only — pre-releases and
drafts are ignored), so it can't drift:

- **Current-version badges** (home cards, compare table, matrix headers)
- **Hero "Latest: …" pills** and **"Download …" button labels**
- **`data/releases.json`** (version + date + link per project)
- Download buttons already point at `/releases/latest`, so their target is always correct.

These live in the HTML as `<span data-auto="ver:lite|full|v6">…</span>` markers that
[`scripts/update_releases.py`](../scripts/update_releases.py) rewrites. The rewrite is
surgical — it only touches those marked spans, never the historical changelog entries.

## What needs a human (with a safety net so it can't go stale)

The **curated changelog highlights**, the **comparison matrix** ✓/~/✕ cells, prose,
and **credits** can't be auto-decided (a new release might add a feature that needs a
new matrix row). So instead of guessing, the updater compares the live latest stable
tag against [`data/curated.json`](../data/curated.json) and, when a project has moved
ahead, **opens a `content` issue** listing what to do. The site is never silently wrong.

When you ship a new stable release and address the issue:
1. Add the release's curated highlight entry on the product page.
2. Eyeball `compare.html` for new features / changed cells.
3. Update `credits.html` if a new PR/contributor was integrated.
4. Bump that project's value in `data/curated.json` → the alert clears.

## How it runs

[`.github/workflows/update-site.yml`](../.github/workflows/update-site.yml) runs:
- **on a daily cron** (backstop),
- **manually** via *Run workflow*, and
- **instantly** when a project repo fires a `repository_dispatch` of type `project-release`.

It commits any version changes (as `The412Banner`) and opens the staleness issue.

## One-time setup (per project repo)

To get the instant (~30s) updates, add **`notify-site.example.yml`** to each of the three
project repos as `.github/workflows/notify-site.yml`, and create a repo secret
**`SITE_DISPATCH_TOKEN`** (a PAT allowed to send a `repository_dispatch` to
`The412Banner/bannerhub-site`). Without this you still get the daily cron update.

## Test it

```sh
python3 scripts/update_releases.py     # safe to run anytime; no-op if already current
```
