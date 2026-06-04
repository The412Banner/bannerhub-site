#!/usr/bin/env python3
"""
Auto-update the BannerHub site's live version strings from each project's
latest STABLE GitHub release, and flag when curated content has gone stale.

What it touches automatically (always safe, mechanical):
  - every `<span data-auto="ver:<proj>">…</span>` across *.html  -> latest stable tag
  - data/releases.json                                          -> {version, date, url}

What it does NOT touch (needs a human):
  - the curated changelog bullets, comparison matrix, prose.
    Instead it compares each latest stable tag against data/curated.json and,
    if a project advanced beyond what the curated content covers, marks it
    "stale" so the workflow can open an issue.

Run with no args. Honors $GITHUB_TOKEN (optional) for API rate limit.
Sets GitHub Actions outputs `changed` and `stale` when $GITHUB_OUTPUT is set.
"""
import json
import os
import re
import sys
import urllib.request
import urllib.error
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"

# project key -> GitHub repo
REPOS = {
    "lite": "The412Banner/Bannerhub-Lite",
    "full": "The412Banner/BannerHub",
    "v6":   "The412Banner/bannerhub-revanced",
}


def api(url):
    req = urllib.request.Request(url, headers={
        "Accept": "application/vnd.github+json",
        "User-Agent": "bannerhub-site-updater",
    })
    token = os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN")
    if token:
        req.add_header("Authorization", f"Bearer {token}")
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.load(r)


def latest_stable(repo):
    """Return (tag, date, url) for the latest non-prerelease, non-draft release."""
    try:
        # /releases/latest already excludes prereleases & drafts
        rel = api(f"https://api.github.com/repos/{repo}/releases/latest")
        return rel["tag_name"], rel.get("published_at", "")[:10], rel["html_url"]
    except urllib.error.HTTPError as e:
        if e.code == 404:
            # no non-prerelease release yet; fall back to scanning
            for rel in api(f"https://api.github.com/repos/{repo}/releases?per_page=20"):
                if not rel.get("prerelease") and not rel.get("draft"):
                    return rel["tag_name"], rel.get("published_at", "")[:10], rel["html_url"]
        raise


def update_html(proj, tag):
    """Set the inner text of every <span data-auto="ver:proj">…</span> to tag."""
    pat = re.compile(r'(data-auto="ver:' + re.escape(proj) + r'"\s*>)([^<]*)(</span>)')
    changed = 0
    for html in ROOT.glob("*.html"):
        text = html.read_text(encoding="utf-8")
        new, n = pat.subn(lambda m: m.group(1) + tag + m.group(3), text)
        if n and new != text:
            html.write_text(new, encoding="utf-8")
            changed += n
    return changed


def main():
    DATA.mkdir(exist_ok=True)
    curated = json.loads((DATA / "curated.json").read_text()) if (DATA / "curated.json").exists() else {}

    releases = {}
    stale = []
    html_changes = 0
    errors = []

    for proj, repo in REPOS.items():
        try:
            tag, date, url = latest_stable(repo)
        except Exception as e:  # network/API hiccup: never corrupt the site, just skip
            errors.append(f"{proj} ({repo}): {e}")
            continue
        releases[proj] = {"repo": repo, "version": tag, "date": date, "url": url}
        html_changes += update_html(proj, tag)
        if curated.get(proj) and curated[proj] != tag:
            stale.append(f"{proj} {curated[proj]} -> {tag}")

    if releases:
        (DATA / "releases.json").write_text(json.dumps(releases, indent=2) + "\n", encoding="utf-8")

    # Report
    print("== BannerHub site release sync ==")
    for proj, info in releases.items():
        flag = "  ⚠ STALE (curated content behind)" if any(s.startswith(proj + " ") for s in stale) else ""
        print(f"  {proj:5} {info['version']:14} {info['date']}{flag}")
    if errors:
        print("  errors:", "; ".join(errors))
    print(f"  html spans rewritten: {html_changes}; stale: {len(stale)}")

    # GitHub Actions outputs
    out = os.environ.get("GITHUB_OUTPUT")
    if out:
        with open(out, "a", encoding="utf-8") as f:
            f.write(f"changed={'true' if html_changes else 'false'}\n")
            f.write(f"stale={'; '.join(stale)}\n")
    summary = os.environ.get("GITHUB_STEP_SUMMARY")
    if summary:
        with open(summary, "a", encoding="utf-8") as f:
            f.write("### BannerHub site release sync\n\n")
            for proj, info in releases.items():
                f.write(f"- **{proj}** → `{info['version']}` ({info['date']})\n")
            if stale:
                f.write("\n**Curated content needs review:** " + "; ".join(stale) + "\n")

    # Never fail the build on a transient API error unless nothing resolved
    if errors and not releases:
        print("ERROR: could not resolve any release", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
