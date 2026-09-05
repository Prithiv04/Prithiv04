#!/usr/bin/env python3
"""
generate_connect_badges.py
Generates polished, minimal, self-contained SVG connect badge pills for:
  - PORTFOLIO (primary)
  - GITHUB (primary)
  - LINKEDIN (primary)
  - EMAIL (primary)
  - LEETCODE (secondary)
  - X / Twitter (secondary)
Produces both dark mode and light mode variants in assets/icons/.
"""

import os
import sys
import xml.etree.ElementTree as ET

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(SCRIPT_DIR, "..", ".."))
ICONS_DIR = os.path.join(PROJECT_ROOT, "assets", "icons")

FONT_MONO = "ui-monospace, SFMono-Regular, 'SF Mono', Menlo, Consolas, 'Liberation Mono', monospace"

ICONS_DATA = {
    "portfolio": {
        "label": "PORTFOLIO",
        "primary": True,
        "width": 138,
        "height": 30,
        "accent": "#39c5cf",
        "accent_glow": "rgba(57, 197, 207, 0.4)",
        "light_accent": "#008694",
        "icon_path": """<circle cx="8" cy="8" r="6.5" fill="none" stroke="currentColor" stroke-width="1.3"/>
<line x1="1.5" y1="8" x2="14.5" y2="8" stroke="currentColor" stroke-width="1.2"/>
<path d="M8 1.5 C5.5 4 4.5 6 4.5 8 C4.5 10 5.5 12 8 14.5 C10.5 12 11.5 10 11.5 8 C11.5 6 10.5 4 8 1.5 Z" fill="none" stroke="currentColor" stroke-width="1.2"/>""",
    },
    "github": {
        "label": "GITHUB",
        "primary": True,
        "width": 116,
        "height": 30,
        "accent": "#f0f6fc",
        "accent_glow": "rgba(240, 246, 252, 0.3)",
        "light_accent": "#1f2328",
        "icon_path": """<path fill="currentColor" fill-rule="evenodd" clip-rule="evenodd" d="M8 0C3.58 0 0 3.58 0 8c0 3.54 2.29 6.53 5.47 7.59.4.07.55-.17.55-.38 0-.19-.01-.82-.01-1.49-2.01.37-2.53-.49-2.69-.94-.09-.23-.48-.94-.82-1.13-.28-.15-.68-.52-.01-.53.63-.01 1.08.58 1.23.82.72 1.21 1.87.87 2.33.66.07-.52.28-.87.51-1.07-1.78-.2-3.64-.89-3.64-3.95 0-.87.31-1.59.82-2.15-.08-.2-.36-1.02.08-2.12 0 0 .67-.21 2.2.82.64-.18 1.32-.27 2-.27.68 0 1.36.09 2 .27 1.53-1.04 2.2-.82 2.2-.82.44 1.1.16 1.92.08 2.12.51.56.82 1.27.82 2.15 0 3.07-1.87 3.75-3.65 3.95.29.25.54.73.54 1.48 0 1.07-.01 1.93-.01 2.2 0 .21.15.46.55.38A8.013 8.013 0 0016 8c0-4.42-3.58-8-8-8z"/>""",
    },
    "linkedin": {
        "label": "LINKEDIN",
        "primary": True,
        "width": 124,
        "height": 30,
        "accent": "#0a66c2",
        "accent_glow": "rgba(10, 102, 194, 0.4)",
        "light_accent": "#0a66c2",
        "icon_path": """<path fill="currentColor" d="M14.25 14.25h-2.5v-3.91c0-.93-.02-2.13-1.3-2.13-1.3 0-1.5 1.02-1.5 2.07v3.97H6.45V6.75h2.4v1.02h.03c.33-.63 1.15-1.3 2.36-1.3 2.53 0 3 1.66 3 3.82v3.96zM3.75 5.63a1.44 1.44 0 1 1 0-2.88 1.44 1.44 0 0 1 0 2.88zM5 14.25H2.5V6.75H5v7.5z"/>""",
    },
    "email": {
        "label": "EMAIL",
        "primary": True,
        "width": 108,
        "height": 30,
        "accent": "#ea4335",
        "accent_glow": "rgba(234, 67, 53, 0.4)",
        "light_accent": "#d93025",
        "icon_path": """<rect x="1.5" y="3" width="13" height="10" rx="1.5" fill="none" stroke="currentColor" stroke-width="1.3"/>
<path d="M2.5 4.5 L8 8.5 L13.5 4.5" fill="none" stroke="currentColor" stroke-width="1.3" stroke-linecap="round" stroke-linejoin="round"/>""",
    },
    "leetcode": {
        "label": "LEETCODE",
        "primary": False,
        "width": 110,
        "height": 24,
        "accent": "#ffa116",
        "accent_glow": "rgba(255, 161, 22, 0.4)",
        "light_accent": "#b26a00",
        "icon_path": """<path fill="currentColor" d="M10.73 11.95L8.93 13.69c-.31.31-.74.44-1.22.44s-.9-.13-1.22-.44l-2.89-2.91c-.31-.31-.47-.77-.47-1.24s.16-.9.47-1.22l2.88-2.92c.31-.31.75-.43 1.22-.43s.9.13 1.22.44l1.8 1.74c.34.34.91.33 1.27-.03.36-.36.37-.92.03-1.27l-1.74-1.76a3.38 3.38 0 0 0-2.57-.97c-.98 0-1.9.39-2.59 1.08L2.03 7.82c-.69.69-1.08 1.61-1.08 2.59s.39 1.9 1.08 2.59l2.89 2.91c.69.69 1.61 1.08 2.59 1.08s1.9-.39 2.59-1.08l1.74-1.76c.34-.34.33-.91-.03-1.27-.36-.35-.92-.37-1.27-.03z M9.19 8.58H5.51c-.49 0-.88.4-.88.88s.4.88.88.88h3.68c.49 0 .88-.4.88-.88s-.39-.88-.88-.88z"/>""",
    },
    "x": {
        "label": "X",
        "primary": False,
        "width": 68,
        "height": 24,
        "accent": "#e7e9ea",
        "accent_glow": "rgba(231, 233, 234, 0.3)",
        "light_accent": "#0f1419",
        "icon_path": """<path fill="currentColor" d="M12.16 1.5h2.2l-4.82 5.51 5.67 7.49h-4.44L7.3 9.96l-3.98 4.54H1.12l5.15-5.89L.83 1.5h4.55l3.14 4.15zm-.77 11.68h1.22L4.72 2.75H3.41z"/>""",
    },
}


def build_badge_svg(key: str, item: dict, light_mode: bool = False) -> str:
    w = item["width"]
    h = item["height"]
    is_primary = item["primary"]
    accent = item["light_accent"] if light_mode else item["accent"]
    glow = item["accent_glow"]

    # Colors
    if light_mode:
        bg_fill = "#f6f8fa"
        border_color = "#d0d7de"
        text_fill = "#1f2328"
        hover_bg = "#ffffff"
        rx = 5 if is_primary else 4
        font_size = 10 if is_primary else 8.5
        arrow_fill = "#57606a"
    else:
        bg_fill = "#161b22"
        border_color = "#30363d"
        text_fill = "#f0f6fc"
        hover_bg = "#1f242c"
        rx = 6 if is_primary else 4.5
        font_size = 10.5 if is_primary else 9
        arrow_fill = "#8b949e"

    icon_size = 16 if is_primary else 13
    icon_x = 10 if is_primary else 8
    icon_y = (h - icon_size) / 2.0

    text_x = icon_x + icon_size + (8 if is_primary else 6)
    text_y = (h / 2.0) + (3.5 if is_primary else 3.0)

    arrow_x = w - (12 if is_primary else 10)
    arrow_y = text_y

    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" role="img" aria-label="{item['label']}">
  <title>{item['label']} ↗</title>
  <defs>
    <style>
      .pill-box {{
        fill: {bg_fill};
        stroke: {border_color};
        stroke-width: 1;
        transition: all 0.2s ease-in-out;
      }}
      .pill-text {{
        font-family: {FONT_MONO};
        font-size: {font_size}px;
        font-weight: 700;
        fill: {text_fill};
        letter-spacing: 0.8px;
        transition: fill 0.2s ease-in-out;
      }}
      .pill-arrow {{
        font-family: {FONT_MONO};
        font-size: {font_size}px;
        font-weight: 700;
        fill: {arrow_fill};
        transition: fill 0.2s ease-in-out;
      }}
      .pill-icon {{
        color: {accent};
        transition: transform 0.2s ease-in-out, filter 0.2s ease-in-out;
      }}
      svg:hover .pill-box {{
        fill: {hover_bg};
        stroke: {accent};
        stroke-width: 1.2;
      }}
      svg:hover .pill-text {{
        fill: {accent};
      }}
      svg:hover .pill-arrow {{
        fill: {accent};
      }}
      svg:hover .pill-icon {{
        filter: drop-shadow(0 0 3px {glow});
      }}
    </style>
  </defs>

  <!-- Background Pill Track -->
  <rect class="pill-box" x="0.5" y="0.5" width="{w - 1}" height="{h - 1}" rx="{rx}"/>

  <!-- Platform Icon -->
  <g class="pill-icon" transform="translate({icon_x:.1f}, {icon_y:.1f})">
    <svg width="{icon_size}" height="{icon_size}" viewBox="0 0 16 16" fill="none">
      {item['icon_path']}
    </svg>
  </g>

  <!-- Platform Label -->
  <text class="pill-text" x="{text_x:.1f}" y="{text_y:.1f}">{item['label']}</text>

  <!-- External Arrow Indicator -->
  <text class="pill-arrow" x="{arrow_x:.1f}" y="{arrow_y:.1f}" text-anchor="end">↗</text>
</svg>"""

    return svg


def main():
    os.makedirs(ICONS_DIR, exist_ok=True)
    print("Generating refined connect badge SVGs...")

    for key, item in ICONS_DATA.items():
        # Dark
        dark_path = os.path.join(ICONS_DIR, f"connect-{key}.svg")
        dark_svg = build_badge_svg(key, item, light_mode=False)
        with open(dark_path, "w", encoding="utf-8") as f:
            f.write(dark_svg)

        # Light
        light_path = os.path.join(ICONS_DIR, f"connect-{key}-light.svg")
        light_svg = build_badge_svg(key, item, light_mode=True)
        with open(light_path, "w", encoding="utf-8") as f:
            f.write(light_svg)

        # Validate XML
        ET.fromstring(dark_svg)
        ET.fromstring(light_svg)
        print(f"  [PASS] {key:<10} -> {dark_path} & -light.svg")

    print("All connect badge SVGs generated and validated.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
