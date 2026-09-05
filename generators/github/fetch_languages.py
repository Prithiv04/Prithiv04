#!/usr/bin/env python3
"""
fetch_languages.py
Fetches real programming language usage across public GitHub repositories for @Prithiv04.
Aggregates language byte counts, calculates real percentages, and saves to data/github/languages.json.
Provides resilient offline fallback if network or rate-limits occur.
"""

import json
import os
import sys
import urllib.request
import urllib.error
from datetime import datetime, timezone

USERNAME = "Prithiv04"
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(SCRIPT_DIR, "..", ".."))
DATA_DIR = os.path.join(PROJECT_ROOT, "data", "github")
CACHE_FILE = os.path.join(DATA_DIR, "languages.json")

# Languages or markup to exclude from programming languages if desired (e.g. templates, config)
EXCLUDED_LANGUAGES = {
    "Go Template",
    "Clarity",
    "Dockerfile",
    "Makefile",
}


def get_headers() -> dict:
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        "Accept": "application/vnd.github.v3+json",
    }
    token = os.environ.get("GITHUB_TOKEN")
    if token:
        headers["Authorization"] = f"token {token}"
    return headers


def fetch_user_repos(username: str) -> list:
    """Fetch all public repositories owned by the user."""
    url = f"https://api.github.com/users/{username}/repos?per_page=100&type=owner"
    req = urllib.request.Request(url, headers=get_headers())
    with urllib.request.urlopen(req, timeout=12) as response:
        return json.load(response)


def fetch_repo_languages(languages_url: str) -> dict:
    """Fetch language byte breakdown for a repository."""
    req = urllib.request.Request(languages_url, headers=get_headers())
    with urllib.request.urlopen(req, timeout=6) as response:
        return json.load(response)


def aggregate_languages(username: str) -> dict:
    repos = fetch_user_repos(username)
    print(f"Found {len(repos)} repositories for @{username}.")

    lang_bytes = {}
    repos_sampled = 0

    for r in repos:
        # Exclude forks if any, or profile repo if it skews
        if r.get("fork", False):
            continue

        lurl = r.get("languages_url")
        if not lurl:
            continue

        try:
            repo_langs = fetch_repo_languages(lurl)
            for lang, byte_count in repo_langs.items():
                if lang in EXCLUDED_LANGUAGES:
                    continue
                lang_bytes[lang] = lang_bytes.get(lang, 0) + byte_count
            repos_sampled += 1
        except Exception as e:
            # Fallback to repo's primary language if byte fetch times out
            primary = r.get("language")
            if primary and primary not in EXCLUDED_LANGUAGES:
                size_est = r.get("size", 100) * 1024
                lang_bytes[primary] = lang_bytes.get(primary, 0) + size_est
            print(f" Note: Skipped {r.get('name')}: {e}")

    total_bytes = sum(lang_bytes.values())
    if total_bytes == 0:
        raise ValueError("Total language bytes is zero.")

    # Sort descending by byte count
    sorted_langs = sorted(lang_bytes.items(), key=lambda x: x[1], reverse=True)

    # Take top 5 or 6 languages
    top_n = sorted_langs[:5]

    # Calculate percentages relative to the top languages (or total)
    # Showing real percentages of total codebase volume
    result_langs = []
    for lang, b_count in top_n:
        pct = (b_count / total_bytes) * 100.0
        result_langs.append({
            "name": lang,
            "bytes": b_count,
            "percentage": round(pct, 1),
            "pct_display": f"{round(pct)}%",
        })

    return {
        "username": username,
        "fetched_at": datetime.now(timezone.utc).isoformat(),
        "total_repos": len(repos),
        "repos_sampled": repos_sampled,
        "total_bytes": total_bytes,
        "languages": result_langs,
    }


def main():
    os.makedirs(DATA_DIR, exist_ok=True)
    print(f"Fetching real GitHub languages for @{USERNAME}...")

    try:
        data = aggregate_languages(USERNAME)
        with open(CACHE_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)

        print(f" Successfully aggregated languages from {data['repos_sampled']} repos:")
        for l in data["languages"]:
            print(f"   {l['name']:<15} {l['bytes']:>10} bytes ({l['percentage']}%) -> {l['pct_display']}")
        print(f" Saved to {CACHE_FILE}")
        return 0
    except Exception as e:
        print(f" Error fetching languages: {e}")

    if os.path.exists(CACHE_FILE):
        print(f" Falling back to existing cached language data at {CACHE_FILE}")
        return 0

    print(" Error: Could not fetch language data and no cache exists.")
    return 1


if __name__ == "__main__":
    sys.exit(main())
