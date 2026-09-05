"""
generate_whoami.py
------------------
Generates the Premium Editorial Typography SVGs for the $ whoami section:
  - assets/hero/whoami-editorial.svg        (animated / interactive dark)
  - assets/hero/whoami-editorial-static.svg (static dark)
  - assets/hero/whoami-editorial-light.svg  (static light)

Design Specifications:
  - Preserves exact wording from original profile.
  - Large, readable focal opening statement with subtle emphasis on
    "AI/ML Engineer" and "complete intelligent systems".
  - Editorial metadata grid for CAPABILITIES, FOUNDATION, and OPPORTUNITIES:
    clean monospace labels on the left, refined sans-serif prose on the right.
  - Subtle interactive hover effect on metadata rows.
  - Restrained palette (off-white, slate, cyan, blue, emerald).
  - 100% vector SVG, zero external fonts/images, fully accessible and responsive.
"""

import os
import xml.etree.ElementTree as ET

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT  = os.path.abspath(os.path.join(SCRIPT_DIR, "..", ".."))
HERO_DIR   = os.path.join(REPO_ROOT, "assets", "hero")
os.makedirs(HERO_DIR, exist_ok=True)

SVG_W = 900.0
SVG_H = 268.0

DARK_THEME = {
    "bg_start":     "#111722",
    "bg_end":       "#0d1117",
    "border":       "#30363d",
    "card_bg":      "#161b22",
    "hover_bg":     "#58a6ff",
    "text_hero":    "#f0f6fc",
    "text_body":    "#c9d1d9",
    "text_dim":     "#8b949e",
    "text_muted":   "#57606a",
    "accent":       "#58a6ff",
    "cyan":         "#39c5cf",
    "green":        "#3fb950",
    "label_bg":     "#1f242c",
    "label_border": "#30363d",
}

LIGHT_THEME = {
    "bg_start":     "#ffffff",
    "bg_end":       "#f6f8fa",
    "border":       "#d0d7de",
    "card_bg":      "#f6f8fa",
    "hover_bg":     "#0969da",
    "text_hero":    "#1f2328",
    "text_body":    "#24292f",
    "text_dim":     "#57606a",
    "text_muted":   "#8c959f",
    "accent":       "#0969da",
    "cyan":         "#0550ae",
    "green":        "#1a7f37",
    "label_bg":     "#eaeef2",
    "label_border": "#d0d7de",
}

FONT_SANS = "-apple-system, BlinkMacSystemFont, 'Segoe UI', Inter, Roboto, Helvetica, Arial, sans-serif"
FONT_MONO = "ui-monospace, SFMono-Regular, Menlo, Consolas, 'Liberation Mono', monospace"


def build_whoami_svg(theme: dict, animated: bool = True) -> str:
    """
    Constructs the Editorial WhoAmI SVG.
    """
    style_block = f"""  <style>
    .meta-row {{
      cursor: default;
    }}
    .row-bg {{
      transition: fill-opacity 0.2s ease, stroke-opacity 0.2s ease;
    }}
    .row-label {{
      transition: fill 0.2s ease;
    }}
    .meta-row:hover .row-bg {{
      fill-opacity: 0.08 !important;
      stroke-opacity: 0.8 !important;
    }}
    .meta-row:hover .row-label {{
      fill: {theme['cyan']} !important;
    }}
  </style>"""

    hover_reveal = ""
    if animated:
        hover_reveal = f"""  <animate attributeName="opacity" from="0" to="1" dur="0.5s" begin="0.1s" fill="freeze"/>"""

    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {SVG_W:.0f} {SVG_H:.0f}" width="{SVG_W:.0f}" height="{SVG_H:.0f}" role="img" aria-label="Prithiv — AI Engineering Profile">
  <title>Prithiv — AI Engineering Profile</title>
  <desc>I'm Prithiv — an AI/ML Engineer who builds complete intelligent systems</desc>

  <defs>
    <linearGradient id="editorialBg" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="{theme['bg_start']}"/>
      <stop offset="100%" stop-color="{theme['bg_end']}"/>
    </linearGradient>
  </defs>

{style_block}

  <!-- Frame Background & Hairline Border -->
  <rect width="{SVG_W:.0f}" height="{SVG_H:.0f}" rx="10" fill="url(#editorialBg)"/>
  <rect x="0.5" y="0.5" width="{SVG_W - 1:.1f}" height="{SVG_H - 1:.1f}" rx="9.5" fill="none" stroke="{theme['border']}" stroke-width="1"/>
  {hover_reveal}

  <!-- 1. Opening Focal Paragraph -->
  <g font-family="{FONT_SANS}">
    <!-- Primary Hook (Line 1) -->
    <text x="36" y="44" font-size="16.5" fill="{theme['text_body']}" letter-spacing="-0.2">
      I&#8217;m <tspan fill="{theme['text_hero']}" font-weight="700">Prithiv</tspan> &#8212; an <tspan fill="{theme['accent']}" font-weight="700">AI/ML Engineer</tspan> who builds <tspan fill="{theme['cyan']}" font-weight="700">complete intelligent systems</tspan>:
    </text>
    <!-- Scope & Infrastructure (Line 2) -->
    <text x="36" y="69" font-size="14.5" fill="{theme['text_dim']}" letter-spacing="-0.1">
      from designing models and agents to shipping production applications and cloud infrastructure.
    </text>
  </g>

  <!-- Technical Divider Line -->
  <line x1="36" y1="88" x2="{SVG_W - 36:.1f}" y2="88" stroke="{theme['border']}" stroke-width="1"/>
  <circle cx="36" cy="88" r="2" fill="{theme['accent']}"/>
  <circle cx="{SVG_W - 36:.1f}" cy="88" r="2" fill="{theme['accent']}"/>

  <!-- Section Philosophy Tagline -->
  <text x="36" y="110" font-family="{FONT_MONO}" font-size="11.5" font-weight="600" fill="{theme['text_body']}" letter-spacing="1.5">
    I THINK IN <tspan fill="{theme['cyan']}" font-weight="700">SYSTEMS</tspan>, NOT JUST MODELS.
  </text>

  <!-- 2. Metadata Grid (Row 1: CAPABILITIES) -->
  <g class="meta-row">
    <!-- Row Hitbox / Hover Background -->
    <rect x="36" y="123" width="{SVG_W - 72:.1f}" height="38" rx="6" fill="{theme['hover_bg']}" fill-opacity="0" stroke="{theme['border']}" stroke-opacity="0.35" class="row-bg"/>
    <!-- Left Monospace Badge -->
    <rect x="42" y="129" width="138" height="26" rx="4" fill="{theme['label_bg']}" stroke="{theme['label_border']}" stroke-width="1"/>
    <text x="111" y="146" font-family="{FONT_MONO}" font-size="10" font-weight="700" fill="{theme['accent']}" text-anchor="middle" letter-spacing="1.5" class="row-label">CAPABILITIES</text>
    <!-- Content String -->
    <text x="194" y="147" font-family="{FONT_SANS}" font-size="13" fill="{theme['text_body']}" letter-spacing="-0.1">
      <tspan font-weight="600" fill="{theme['text_hero']}">Machine Learning</tspan> &#160;&#183;&#160; 
      <tspan font-weight="600" fill="{theme['text_hero']}">Generative AI</tspan> &#160;&#183;&#160; 
      <tspan font-weight="600" fill="{theme['text_hero']}">LLMs</tspan> &#160;&#183;&#160; 
      <tspan font-weight="600" fill="{theme['text_hero']}">AI Agents</tspan> &#160;&#183;&#160; 
      <tspan font-weight="600" fill="{theme['text_hero']}">Computer Vision</tspan> &#160;&#183;&#160; 
      <tspan font-weight="600" fill="{theme['text_hero']}">NLP</tspan>
    </text>
  </g>

  <!-- 3. Metadata Grid (Row 2: FOUNDATION) -->
  <g class="meta-row">
    <!-- Row Hitbox / Hover Background -->
    <rect x="36" y="167" width="{SVG_W - 72:.1f}" height="38" rx="6" fill="{theme['hover_bg']}" fill-opacity="0" stroke="{theme['border']}" stroke-opacity="0.35" class="row-bg"/>
    <!-- Left Monospace Badge -->
    <rect x="42" y="173" width="138" height="26" rx="4" fill="{theme['label_bg']}" stroke="{theme['label_border']}" stroke-width="1"/>
    <text x="111" y="190" font-family="{FONT_MONO}" font-size="10" font-weight="700" fill="{theme['accent']}" text-anchor="middle" letter-spacing="1.5" class="row-label">FOUNDATION</text>
    <!-- Content String -->
    <text x="194" y="191" font-family="{FONT_SANS}" font-size="13" fill="{theme['text_body']}" letter-spacing="-0.1">
      <tspan font-style="italic" fill="{theme['text_dim']}">backed by</tspan> &#160;
      <tspan font-weight="600" fill="{theme['text_hero']}">Software Engineering</tspan> &#160;&#183;&#160; 
      <tspan font-weight="600" fill="{theme['text_hero']}">Full Stack</tspan> &#160;&#183;&#160; 
      <tspan font-weight="600" fill="{theme['text_hero']}">Cloud</tspan> &#160;&#183;&#160; 
      <tspan font-weight="600" fill="{theme['text_hero']}">Security</tspan>
    </text>
  </g>

  <!-- 4. Metadata Grid (Row 3: OPPORTUNITIES) -->
  <g class="meta-row">
    <!-- Row Hitbox / Hover Background -->
    <rect x="36" y="211" width="{SVG_W - 72:.1f}" height="38" rx="6" fill="{theme['hover_bg']}" fill-opacity="0" stroke="{theme['border']}" stroke-opacity="0.35" class="row-bg"/>
    <!-- Left Monospace Badge -->
    <rect x="42" y="217" width="138" height="26" rx="4" fill="{theme['label_bg']}" stroke="{theme['green']}" stroke-width="1" stroke-opacity="0.7"/>
    <circle cx="56" cy="230" r="3" fill="{theme['green']}"/>
    <text x="116" y="234" font-family="{FONT_MONO}" font-size="9.5" font-weight="700" fill="{theme['green']}" text-anchor="middle" letter-spacing="1.2" class="row-label">OPPORTUNITIES</text>
    <!-- Content String -->
    <text x="194" y="235" font-family="{FONT_SANS}" font-size="13" fill="{theme['text_body']}" letter-spacing="-0.1">
      Currently pursuing opportunities in <tspan font-weight="600" fill="{theme['text_hero']}">AI/ML internships</tspan>, <tspan font-weight="600" fill="{theme['text_hero']}">research roles</tspan>, and <tspan font-weight="600" fill="{theme['text_hero']}">open-source collaboration</tspan>.
    </text>
  </g>
</svg>"""

    return svg


def main():
    out_animated = os.path.join(HERO_DIR, "whoami-editorial.svg")
    out_static   = os.path.join(HERO_DIR, "whoami-editorial-static.svg")
    out_light    = os.path.join(HERO_DIR, "whoami-editorial-light.svg")

    print("Generating whoami-editorial.svg (dark)...")
    svg_anim = build_whoami_svg(DARK_THEME, animated=True)
    with open(out_animated, "w", encoding="utf-8") as f:
        f.write(svg_anim)
    print(f"  -> {out_animated} ({os.path.getsize(out_animated)/1024:.1f} KB)")

    print("Generating whoami-editorial-static.svg (dark, static)...")
    svg_static = build_whoami_svg(DARK_THEME, animated=False)
    with open(out_static, "w", encoding="utf-8") as f:
        f.write(svg_static)
    print(f"  -> {out_static} ({os.path.getsize(out_static)/1024:.1f} KB)")

    print("Generating whoami-editorial-light.svg (light, static)...")
    svg_light = build_whoami_svg(LIGHT_THEME, animated=False)
    with open(out_light, "w", encoding="utf-8") as f:
        f.write(svg_light)
    print(f"  -> {out_light} ({os.path.getsize(out_light)/1024:.1f} KB)")

    for p in [out_animated, out_static, out_light]:
        ET.parse(p)
        print(f"  [PASS] Valid XML: {os.path.basename(p)}")

    print("\nEditorial WhoAmI SVGs created and validated successfully.")


if __name__ == "__main__":
    main()
