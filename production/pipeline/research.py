#!/usr/bin/env python3
"""
research.py — Structured research helper (RESEARCH-BEFORE-ANSWER LAW).

When the owner asks "what's the best X" or anything time-sensitive, DON'T guess
from training data. Use this to do actual research.

Usage:
  research.py github-trending <language> [--since daily|weekly|monthly]
  research.py github-search <query> [--stars-min N] [--pushed-after DATE]
  research.py hn-search <query>
  research.py compare <topic>   # runs all sources, outputs ranked summary

All output goes to stdout as Markdown. Save it to a research doc.
"""
import json
import subprocess
import sys
import urllib.request
import urllib.parse
from datetime import datetime, timezone


def fetch(url, headers=None, timeout=30):
    req = urllib.request.Request(url, headers=headers or {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) research-tool/1.0",
        "Accept": "application/vnd.github.v3+json",
    })
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return json.loads(r.read().decode())


def github_trending(language="", since="weekly"):
    """Scrape GitHub trending (no API key needed)."""
    # Use the unofficial trending API mirror
    lang = f"/{language}" if language else ""
    url = f"https://github-trending-api.de.a9t.org/repositories?language={language}&since={since}"
    try:
        repos = fetch(url)
        out = [f"## GitHub Trending ({language or 'all'}, {since})", ""]
        for r in repos[:15]:
            out.append(f"- **[{r['name']}]({r['url']})** — ⭐ {r.get('stars', '?')} "
                       f"(+{r.get('currentPeriodStars', '?')} this period)")
            if r.get("description"):
                out.append(f"  {r['description'][:120]}")
        return "\n".join(out)
    except Exception as e:
        return f"## GitHub Trending\n\nFailed: {e}"


def github_search(query, stars_min=100, pushed_after="2025-01-01"):
    """Search GitHub repos by query, filtered by stars and recency."""
    q = f"{query} stars:>={stars_min} pushed:>={pushed_after}"
    url = ("https://api.github.com/search/repositories?"
           f"q={urllib.parse.quote(q)}&sort=stars&order=desc&per_page=15")
    try:
        data = fetch(url)
        out = [f"## GitHub Search: '{query}' (⭐≥{stars_min}, pushed after {pushed_after})", ""]
        for r in data.get("items", []):
            out.append(f"- **[{r['full_name']}]({r['html_url']})** — ⭐ {r['stargazers_count']}")
            out.append(f"  {r.get('description', 'no description')[:120]}")
            out.append(f"  Updated: {r['pushed_at'][:10]} | License: {(r.get('license') or {}).get('spdx_id', '?')}")
        return "\n".join(out)
    except Exception as e:
        return f"## GitHub Search\n\nFailed: {e}"


def hn_search(query):
    """Search Hacker News via Algolia API (free, no key)."""
    url = (f"https://hn.algolia.com/api/v1/search?"
           f"query={urllib.parse.quote(query)}&tags=story&hitsPerPage=10")
    try:
        data = fetch(url)
        out = [f"## Hacker News: '{query}'", ""]
        for h in data.get("hits", []):
            out.append(f"- [{h['title']}]({h.get('url', '#')}) "
                       f"({h.get('points', 0)} pts, {h.get('num_comments', 0)} comments)")
        return "\n".join(out)
    except Exception as e:
        return f"## Hacker News\n\nFailed: {e}"


def compare(topic):
    """Run all research sources for a topic. The full research pass."""
    ts = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    parts = [f"# Research: {topic}", f"_Generated {ts} — do not use training data, this is live._", ""]
    parts.append(github_trending("", "monthly"))
    parts.append("")
    parts.append(github_search(topic))
    parts.append("")
    parts.append(hn_search(topic))
    parts.append("")
    parts.append("---")
    parts.append("**Next step:** Pick the top 3-5 candidates above, check their licenses "
                 "(must allow commercial use), then pull the winners.")
    return "\n".join(parts)


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)
    cmd = sys.argv[1]
    if cmd == "github-trending":
        print(github_trending(sys.argv[2] if len(sys.argv) > 2 else "",
                              sys.argv[3] if len(sys.argv) > 3 else "weekly"))
    elif cmd == "github-search":
        print(github_search(" ".join(sys.argv[2:])))
    elif cmd == "hn-search":
        print(hn_search(" ".join(sys.argv[2:])))
    elif cmd == "compare":
        print(compare(" ".join(sys.argv[2:])))
    else:
        print(f"Unknown command: {cmd}")
        print(__doc__)
        sys.exit(1)


if __name__ == "__main__":
    main()
