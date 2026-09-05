#!/usr/bin/env python3
"""
generate_languages_svg.py
Generates the Language Signal horizontal bar graph SVGs:
  - assets/github/languages.svg (animated dark mode)
  - assets/github/languages-static.svg (static dark mode / reduced-motion)
  - assets/github/languages-light.svg (light mode)
Uses real GitHub repository language data from data/github/languages.json.
"""

import json
import os
import sys

from theme import DARK_THEME, LIGHT_THEME, FONT_MONO, FONT_SANS

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(SCRIPT_DIR, "..", ".."))
DATA_FILE = os.path.join(PROJECT_ROOT, "data", "github", "languages.json")
ASSETS_DIR = os.path.join(PROJECT_ROOT, "assets", "github")


def load_languages() -> dict:
    if not os.path.exists(DATA_FILE):
        raise FileNotFoundError(f"Missing {DATA_FILE}. Run fetch_languages.py first.")
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def format_bytes(b: int) -> str:
    """Format byte count to readable MB / KB string."""
    if b >= 1024 * 1024:
        return f"{b / (1024 * 1024):.1f} MB"
    elif b >= 1024:
        return f"{b / 1024:.0f} KB"
    return f"{b} B"


def build_languages_svg(data: dict, theme: dict, animated: bool = True) -> str:
    w = 900.0
    h = 216.0

    languages = data.get("languages", [])
    total_repos = data.get("repos_sampled", data.get("total_repos", 0))

    # Layout geometry
    row_y0 = 68.0
    row_gap = 27.0

    label_x = 142.0          # Right-aligned language name
    track_x = 160.0          # Bar track start
    track_w = 560.0          # Total track width
    bar_h = 10.0             # Bar thickness
    pct_x = track_x + track_w + 18.0  # Percentage label start
    vol_x = w - 36.0         # Right-aligned volume metadata

    rows_svg = []
    for idx, lang in enumerate(languages):
        ly = row_y0 + (idx * row_gap)
        pct = lang.get("percentage", 0.0)
        pct_display = lang.get("pct_display", f"{round(pct)}%")
        name = lang.get("name", "")
        b_count = lang.get("bytes", 0)
        vol_str = format_bytes(b_count)

        # Calculate bar width proportional to percentage
        # Normalize so that 50% occupies ~65% of the bar, or pure scale:
        # Pure scale: bar_w = track_w * (pct / 100.0)
        # Using a slight perceptual curve so small percentages (7%) are clearly visible:
        bar_w = max(12.0, round(track_w * (pct / 100.0) * 1.6))
        bar_w = min(bar_w, track_w)

        # Subtle reveal animation on load
        anim_markup = ""
        initial_width = bar_w
        if animated:
            initial_width = 0
            t_delay = 0.15 + (idx * 0.10)
            anim_markup = f"""<animate attributeName="width"
              from="0" to="{bar_w:.1f}"
              dur="0.8s" begin="{t_delay:.2f}s"
              fill="freeze"
              calcMode="spline" keySplines="0.16 1 0.3 1" keyTimes="0; 1"/>"""

        rows_svg.append(f"""    <!-- Row {idx+1}: {name} -->
    <g id="lang-row-{idx+1}">
      <!-- Language Name -->
      <text x="{label_x:.1f}" y="{ly + 2:.1f}" font-family="{FONT_MONO}" font-size="10.5" font-weight="600"
        fill="{theme['text_hero']}" text-anchor="end" letter-spacing="0.5">{name}</text>

      <!-- Track Groove -->
      <rect x="{track_x:.1f}" y="{ly - 7:.1f}" width="{track_w:.1f}" height="{bar_h:.1f}" rx="2.5"
        fill="{theme['card_bg']}" stroke="{theme['border_subtle']}" stroke-width="1"/>

      <!-- Accent Bar -->
      <rect x="{track_x:.1f}" y="{ly - 7:.1f}" width="{initial_width:.1f}" height="{bar_h:.1f}" rx="2.5"
        fill="{theme['accent']}">
        {anim_markup}
      </rect>

      <!-- Percentage Display -->
      <text x="{pct_x:.1f}" y="{ly + 2:.1f}" font-family="{FONT_MONO}" font-size="10" font-weight="700"
        fill="{theme['accent']}" letter-spacing="0.5">{pct_display}</text>

      <!-- Codebase Volume Metadata -->
      <text x="{vol_x:.1f}" y="{ly + 2:.1f}" font-family="{FONT_MONO}" font-size="9"
        fill="{theme['text_muted']}" text-anchor="end" letter-spacing="0.5">{vol_str}</text>
    </g>""")

    rows_markup = "\n".join(rows_svg)

    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w:.0f} {h:.0f}" width="{w:.0f}" height="{h:.0f}" role="img" aria-label="GitHub Repository Language Signal Graph">
  <title>Programming Language Signal · @{data.get('username', 'Prithiv04')}</title>
  <desc>Codebase language distribution across {total_repos} public repositories: {', '.join([l['name'] + ' ' + l['pct_display'] for l in languages])}.</desc>

  <defs>
    <linearGradient id="langBg" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="{theme['bg_start']}"/>
      <stop offset="100%" stop-color="{theme['bg_end']}"/>
    </linearGradient>
  </defs>

  <!-- Frame Background & Hairline Border -->
  <rect width="{w:.0f}" height="{h:.0f}" rx="10" fill="url(#langBg)"/>
  <rect x="0.5" y="0.5" width="{w - 1:.1f}" height="{h - 1:.1f}" rx="9.5" fill="none" stroke="{theme['border']}" stroke-width="1"/>

  <!-- Top Header Ribbon -->
  <rect x="0" y="0" width="{w:.0f}" height="36" rx="10" fill="{theme['card_bg']}"/>
  <rect x="0" y="26" width="{w:.0f}" height="10" fill="{theme['card_bg']}"/>
  <line x1="0" y1="36" x2="{w:.0f}" y2="36" stroke="{theme['border']}" stroke-width="1"/>

  <!-- Header Labels -->
  <text x="36" y="23" font-family="{FONT_MONO}" font-size="9" font-weight="700"
    fill="{theme['accent']}" letter-spacing="1.5">GITHUB / LANGUAGE SIGNAL</text>

  <text x="{w - 36:.1f}" y="23" font-family="{FONT_MONO}" font-size="9"
    fill="{theme['text_secondary']}" text-anchor="end" letter-spacing="1">
    CODEBASE VOLUME &#160;·&#160; <tspan fill="{theme['text_hero']}" font-weight="700">{len(languages)} PRIMARY LANGUAGES</tspan> &#160;·&#160; {total_repos} PUBLIC REPOS
  </text>

  <!-- Language Horizontal Bars -->
  <g id="language-bars">
{rows_markup}
  </g>
</svg>"""

    return svg


def main():
    os.makedirs(ASSETS_DIR, exist_ok=True)
    print("Loading cached language data...")
    data = load_languages()

    print(f"Rendering Language Signal SVGs for @{data.get('username')}...")

    # 1. Dark animated
    dark_anim_path = os.path.join(ASSETS_DIR, "languages.svg")
    with open(dark_anim_path, "w", encoding="utf-8") as f:
        f.write(build_languages_svg(data, DARK_THEME, animated=True))
    print(f" Generated: {dark_anim_path}")

    # 2. Dark static (reduced-motion)
    dark_static_path = os.path.join(ASSETS_DIR, "languages-static.svg")
    with open(dark_static_path, "w", encoding="utf-8") as f:
        f.write(build_languages_svg(data, DARK_THEME, animated=False))
    print(f" Generated: {dark_static_path}")

    # 3. Light mode
    light_path = os.path.join(ASSETS_DIR, "languages-light.svg")
    with open(light_path, "w", encoding="utf-8") as f:
        f.write(build_languages_svg(data, LIGHT_THEME, animated=False))
    print(f" Generated: {light_path}")

    print("All language SVGs generated successfully.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
