#!/usr/bin/env python3
"""
fetch_contributions.py
Fetches real public GitHub contribution data for a user without requiring a PAT.
Parses the contribution calendar matrix (53 weeks x 7 days) and writes to data/github/contributions.json.
Provides resilient fallback to existing cache if offline or network unavailable.
"""

import json
import os
import re
import sys
import urllib.request
import urllib.error
from datetime import datetime, timezone

USERNAME = "Prithiv04"
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(SCRIPT_DIR, "..", ".."))
DATA_DIR = os.path.join(PROJECT_ROOT, "data", "github")
CACHE_FILE = os.path.join(DATA_DIR, "contributions.json")


def fetch_contributions_html(username: str) -> str:
    """Fetch public contributions HTML from GitHub profile endpoint."""
    url = f"https://github.com/users/{username}/contributions"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    }
    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req, timeout=15) as response:
        return response.read().decode("utf-8")


def parse_contributions(html: str) -> dict:
    """Parse contribution days, dates, counts, and levels from HTML."""
    # Find all <td> day cells
    td_pattern = re.compile(
        r'<td[^>]*?id="(?P<id>[^"]+)"[^>]*?data-date="(?P<date>[^"]+)"[^>]*?data-level="(?P<level>\d+)"[^>]*?>',
        re.DOTALL
    )

    days_by_id = {}
    for match in td_pattern.finditer(html):
        day_id = match.group("id")
        date_str = match.group("date")
        level = int(match.group("level"))
        days_by_id[day_id] = {
            "id": day_id,
            "date": date_str,
            "level": level,
            "count": 0,
        }

    # Tooltips correspond to day cells via 'for="id"'
    tooltip_pattern = re.compile(
        r'<tool-tip[^>]*?for="(?P<id>[^"]+)"[^>]*?>(?P<text>[^<]+)</tool-tip>',
        re.DOTALL
    )

    for match in tooltip_pattern.finditer(html):
        day_id = match.group("id")
        text = match.group("text").strip()
        if day_id in days_by_id:
            count_match = re.search(r"(\d+|No)\s+contribution", text)
            if count_match:
                c_val = count_match.group(1)
                count = 0 if c_val.lower() == "no" else int(c_val)
                days_by_id[day_id]["count"] = count

    days_list = list(days_by_id.values())

    # Fallback pattern if tooltips/ids didn't match
    if not days_list:
        alt_pattern = re.compile(r'data-date="([^"]+)"[^>]*data-level="(\d+)"')
        for match in alt_pattern.finditer(html):
            date_str, level = match.group(1), int(match.group(2))
            days_list.append({
                "date": date_str,
                "level": level,
                "count": level,
            })

    # Sort strictly chronologically by date
    days_list.sort(key=lambda d: d["date"])

    # Calculate weekday and week_idx
    # In GitHub calendar: Sunday is row 0, Saturday is row 6
    if days_list:
        start_dt = datetime.strptime(days_list[0]["date"], "%Y-%m-%d")
        for d in days_list:
            dt = datetime.strptime(d["date"], "%Y-%m-%d")
            # Python weekday: Monday=0 ... Sunday=6
            # GitHub row: Sunday=0, Monday=1 ... Saturday=6
            github_row = (dt.weekday() + 1) % 7
            d["weekday"] = github_row
            # Days since start_date divided by 7 gives week column index
            delta_days = (dt - start_dt).days
            d["week_idx"] = delta_days // 7

    total_contributions = sum(d["count"] for d in days_list)
    total_active_days = sum(1 for d in days_list if d["count"] > 0)
    max_week_idx = max((d.get("week_idx", 0) for d in days_list), default=0)

    return {
        "username": USERNAME,
        "fetched_at": datetime.now(timezone.utc).isoformat(),
        "total_contributions": total_contributions,
        "active_days": total_active_days,
        "total_days": len(days_list),
        "start_date": days_list[0]["date"] if days_list else "",
        "end_date": days_list[-1]["date"] if days_list else "",
        "weeks_count": max_week_idx + 1,
        "days": days_list,
    }


def main():
    os.makedirs(DATA_DIR, exist_ok=True)
    print(f"Fetching contribution calendar for @{USERNAME}...")

    try:
        html = fetch_contributions_html(USERNAME)
        data = parse_contributions(html)

        if data["total_days"] > 0:
            with open(CACHE_FILE, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2)
            print(f" Successfully fetched {data['total_days']} days ({data['weeks_count']} weeks).")
            print(f" Total contributions: {data['total_contributions']} across {data['active_days']} active days.")
            print(f" Range: {data['start_date']} -> {data['end_date']}")
            print(f" Saved to {CACHE_FILE}")
            return 0
        else:
            print(" Warning: No contribution days parsed from HTML.")
    except Exception as e:
        print(f" Error fetching live contributions: {e}")

    if os.path.exists(CACHE_FILE):
        print(f" Falling back to existing cached data at {CACHE_FILE}")
        return 0

    print(" Error: Could not fetch contributions and no cache exists.")
    return 1


if __name__ == "__main__":
    sys.exit(main())
