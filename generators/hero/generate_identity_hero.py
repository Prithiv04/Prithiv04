"""
generate_identity_hero.py
-------------------------
Generates the Signature AI Engineering Identity Hero SVGs:
  - assets/hero/identity-hero.svg        (animated, dark mode)
  - assets/hero/identity-hero-static.svg (static, dark mode)
  - assets/hero/identity-hero-light.svg  (static, light mode)

Complies with all specifications in topprofile.md:
  - Exact text:
      PRITHIV
      AI/ML ENGINEER | FULL-STACK DEVELOPER
      Autonomous Intelligent Systems · Enterprise Software Architecture · Chennai, India
  - Dimensions: 900 x 240 px (matching downstream AI console width)
  - Precision terminal/system header styling with hairline borders, corner reticles,
    system micro-labels, and live status indicator.
  - 100% static-first fallback with valid XML and no external dependencies.
"""

import os
import html
import xml.etree.ElementTree as ET

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT  = os.path.abspath(os.path.join(SCRIPT_DIR, "..", ".."))
HERO_DIR   = os.path.join(REPO_ROOT, "assets", "hero")
os.makedirs(HERO_DIR, exist_ok=True)

SVG_W = 900.0
SVG_H = 240.0

DARK_THEME = {
    "bg_start":   "#111722",
    "bg_end":     "#0d1117",
    "border":     "#30363d",
    "reticle":    "#58a6ff",
    "text_hero":  "#f0f6fc",
    "text_role":  "#c9d1d9",
    "text_dim":   "#8b949e",
    "text_muted": "#57606a",
    "accent":     "#58a6ff",
    "cyan":       "#39c5cf",
    "green":      "#3fb950",
    "grid":       "#ffffff",
}

LIGHT_THEME = {
    "bg_start":   "#ffffff",
    "bg_end":     "#f6f8fa",
    "border":     "#d0d7de",
    "reticle":    "#0969da",
    "text_hero":  "#0969da",
    "text_role":  "#24292f",
    "text_dim":   "#57606a",
    "text_muted": "#8c959f",
    "accent":     "#0969da",
    "cyan":       "#0550ae",
    "green":      "#1a7f37",
    "grid":       "#000000",
}

FONT_STACK = "ui-monospace, SFMono-Regular, Menlo, Consolas, 'Liberation Mono', monospace"


def build_identity_hero_svg(theme: dict, animated: bool = True) -> str:
    """
    Constructs the Identity Hero SVG.
    """
    # Animation snippets
    def anim(attr, from_val, to_val, begin_s, dur_s):
        if not animated:
            return ""
        return f'<animate attributeName="{attr}" from="{from_val}" to="{to_val}" begin="{begin_s:.2f}s" dur="{dur_s:.2f}s" fill="freeze"/>'

    # Animated elements
    status_dot_anim = f'<circle cx="862" cy="20" r="4.5" fill="{theme["green"]}"/>'
    hero_clip = ""
    hero_clip_ref = ""
    accent_bar_anim = ""
    sub_reveal = ""

    if animated:
        status_dot_anim = (
            f'<circle cx="862" cy="20" r="4.5" fill="{theme["green"]}">'
            f'<animate attributeName="opacity" values="0.3;1;0.3" dur="2.4s" repeatCount="indefinite"/>'
            f'</circle>'
        )

        hero_clip = (
            '    <clipPath id="heroClip">\n'
            '      <rect x="150" y="44" width="600" height="60">\n'
            '        <animate attributeName="y" from="104" to="44" begin="0.30s" dur="0.45s" fill="freeze"/>\n'
            '        <animate attributeName="height" from="0" to="60" begin="0.30s" dur="0.45s" fill="freeze"/>\n'
            '      </rect>\n'
            '    </clipPath>'
        )
        hero_clip_ref = 'clip-path="url(#heroClip)"'

        accent_bar_anim = (
            f'<line x1="330" y1="112" x2="570" y2="112" stroke="{theme["accent"]}" stroke-width="1.5">\n'
            f'    <animate attributeName="x1" from="450" to="330" begin="0.45s" dur="0.35s" fill="freeze"/>\n'
            f'    <animate attributeName="x2" from="450" to="570" begin="0.45s" dur="0.35s" fill="freeze"/>\n'
            f'  </line>'
        )

        sub_reveal = (
            f'<animate attributeName="opacity" from="0" to="1" begin="0.55s" dur="0.40s" fill="freeze"/>'
        )
    else:
        accent_bar_anim = f'<line x1="330" y1="112" x2="570" y2="112" stroke="{theme["accent"]}" stroke-width="1.5"/>'

    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" width="{SVG_W:.0f}" height="{SVG_H:.0f}" viewBox="0 0 {SVG_W:.0f} {SVG_H:.0f}" font-family="{FONT_STACK}" role="img" aria-label="PRITHIV // AI Engineering System">
  <title>PRITHIV // AI Engineering System</title>
  <desc>Signature Identity Hero for Prithiv — AI/ML Engineer &amp; Full-Stack Developer</desc>

  <defs>
    <linearGradient id="heroBg" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="{theme['bg_start']}"/>
      <stop offset="100%" stop-color="{theme['bg_end']}"/>
    </linearGradient>

    <!-- Subtle Dot Grid Pattern -->
    <pattern id="dotGrid" x="0" y="0" width="20" height="20" patternUnits="userSpaceOnUse">
      <circle cx="2" cy="2" r="0.8" fill="{theme['grid']}" opacity="0.04"/>
    </pattern>
{hero_clip}
  </defs>

  <!-- Frame Background & Grid -->
  <rect width="{SVG_W:.0f}" height="{SVG_H:.0f}" rx="10" fill="url(#heroBg)"/>
  <rect width="{SVG_W:.0f}" height="{SVG_H:.0f}" rx="10" fill="url(#dotGrid)"/>
  <rect x="0.5" y="0.5" width="{SVG_W - 1:.1f}" height="{SVG_H - 1:.1f}" rx="9.5" fill="none" stroke="{theme['border']}" stroke-width="1"/>

  <!-- Corner Reticles (+) -->
  <path d="M 12 18 L 12 12 L 18 12 M 882 12 L 888 12 L 888 18 M 12 222 L 12 228 L 18 228 M 882 228 L 888 228 L 888 222"
    fill="none" stroke="{theme['reticle']}" stroke-width="1.2" opacity="0.75"/>

  <!-- Top Rail Separator -->
  <line x1="0" y1="38" x2="{SVG_W:.0f}" y2="38" stroke="{theme['border']}" stroke-width="1"/>

  <!-- Top Left: System Signature -->
  <text x="32" y="24" fill="{theme['text_dim']}" font-size="10.5" letter-spacing="1.5">
    SYS // <tspan fill="{theme['accent']}">PRITHIV.OS</tspan> [v2.4.0-PROD]
  </text>

  <!-- Top Right: System Status -->
  <text x="850" y="24" fill="{theme['green']}" font-size="10.5" font-weight="600" text-anchor="end" letter-spacing="1">
    SYSTEM STATUS: ONLINE
  </text>
  {status_dot_anim}

  <!-- Center Identity Anchor: PRITHIV -->
  <g {hero_clip_ref}>
    <text x="{SVG_W / 2.0:.1f}" y="98" fill="{theme['text_hero']}" font-size="44" font-weight="800"
      text-anchor="middle" letter-spacing="8">PRITHIV</text>
  </g>

  <!-- Center Accent Rule -->
  {accent_bar_anim}
  <circle cx="{SVG_W / 2.0:.1f}" cy="112" r="3" fill="{theme['reticle']}"/>

  <!-- Center Subtitle: Role -->
  <g>
    {sub_reveal}
    <text x="{SVG_W / 2.0:.1f}" y="142" fill="{theme['text_role']}" font-size="13.5" font-weight="700"
      text-anchor="middle" letter-spacing="2.5">AI/ML ENGINEER  |  FULL-STACK DEVELOPER</text>

    <!-- Center Supporting Line -->
    <text x="{SVG_W / 2.0:.1f}" y="166" fill="{theme['text_dim']}" font-size="11"
      text-anchor="middle" letter-spacing="1">Autonomous Intelligent Systems · Enterprise Software Architecture · Chennai, India</text>
  </g>

  <!-- Bottom Rail Separator -->
  <line x1="0" y1="198" x2="{SVG_W:.0f}" y2="198" stroke="{theme['border']}" stroke-width="1"/>

  <!-- Bottom Rail: System Channel Index -->
  <g font-size="10" letter-spacing="1.2">
    <!-- Channel 01 -->
    <text x="85" y="222" text-anchor="middle">
      <tspan fill="{theme['accent']}">01:</tspan> <tspan fill="{theme['text_dim']}">AI / ML</tspan>
    </text>
    <circle cx="175" cy="219" r="1.5" fill="{theme['border']}"/>

    <!-- Channel 02 -->
    <text x="265" y="222" text-anchor="middle">
      <tspan fill="{theme['accent']}">02:</tspan> <tspan fill="{theme['text_dim']}">AI AGENTS</tspan>
    </text>
    <circle cx="355" cy="219" r="1.5" fill="{theme['border']}"/>

    <!-- Channel 03 -->
    <text x="450" y="222" text-anchor="middle">
      <tspan fill="{theme['accent']}">03:</tspan> <tspan fill="{theme['text_dim']}">LLMs &amp; RAG</tspan>
    </text>
    <circle cx="545" cy="219" r="1.5" fill="{theme['border']}"/>

    <!-- Channel 04 -->
    <text x="635" y="222" text-anchor="middle">
      <tspan fill="{theme['accent']}">04:</tspan> <tspan fill="{theme['text_dim']}">FULL-STACK</tspan>
    </text>
    <circle cx="725" cy="219" r="1.5" fill="{theme['border']}"/>

    <!-- Channel 05 -->
    <text x="815" y="222" text-anchor="middle">
      <tspan fill="{theme['accent']}">05:</tspan> <tspan fill="{theme['text_dim']}">DEPLOYMENT</tspan>
    </text>
  </g>
</svg>"""

    return svg


def main():
    out_animated = os.path.join(HERO_DIR, "identity-hero.svg")
    out_static   = os.path.join(HERO_DIR, "identity-hero-static.svg")
    out_light    = os.path.join(HERO_DIR, "identity-hero-light.svg")

    print("Generating identity-hero.svg (dark, animated)...")
    svg_anim = build_identity_hero_svg(DARK_THEME, animated=True)
    with open(out_animated, "w", encoding="utf-8") as f:
        f.write(svg_anim)
    print(f"  -> {out_animated} ({os.path.getsize(out_animated)/1024:.1f} KB)")

    print("Generating identity-hero-static.svg (dark, static)...")
    svg_static = build_identity_hero_svg(DARK_THEME, animated=False)
    with open(out_static, "w", encoding="utf-8") as f:
        f.write(svg_static)
    print(f"  -> {out_static} ({os.path.getsize(out_static)/1024:.1f} KB)")

    print("Generating identity-hero-light.svg (light, static)...")
    svg_light = build_identity_hero_svg(LIGHT_THEME, animated=False)
    with open(out_light, "w", encoding="utf-8") as f:
        f.write(svg_light)
    print(f"  -> {out_light} ({os.path.getsize(out_light)/1024:.1f} KB)")

    for p in [out_animated, out_static, out_light]:
        ET.parse(p)
        print(f"  [PASS] Valid XML: {os.path.basename(p)}")

    print("\nAll Identity Hero SVGs created and validated successfully.")


if __name__ == "__main__":
    main()
