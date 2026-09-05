"""
generate_terminal_profile.py
----------------------------
Generates the right-side Terminal Profile Dossier SVGs:
  - assets/hero/terminal-profile.svg        (animated, dark mode)
  - assets/hero/terminal-profile-static.svg (static, dark mode)
  - assets/hero/terminal-profile-light.svg  (static, light mode)

Matches the exact dimensions (768 x 826), frame styling, borders, colors,
and monospace typography of assets/hero/ascii-portrait.svg to form a cohesive
twin-terminal command center.
"""

import os
import html
import xml.etree.ElementTree as ET

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT  = os.path.abspath(os.path.join(SCRIPT_DIR, "..", ".."))
HERO_DIR   = os.path.join(REPO_ROOT, "assets", "hero")
os.makedirs(HERO_DIR, exist_ok=True)

# ─── Geometry (Identical to ascii-portrait.svg) ───────────────────────────────
SVG_W      = 768.0
SVG_H      = 826.0
TOP_BAR_H  = 38.0
BOT_BAR_H  = 34.0
FOOTER_Y   = SVG_H - BOT_BAR_H  # 792.0
PAD_X      = 32.0

# ─── Color Themes ─────────────────────────────────────────────────────────────
DARK_THEME = {
    "bg_start":  "#111722",
    "bg_end":    "#0d1117",
    "border":    "#30363d",
    "header_bg": "#161b22",
    "text":      "#c9d1d9",
    "bright":    "#f0f6fc",
    "dim":       "#7d8590",
    "accent":    "#58a6ff",
    "cyan":      "#39c5cf",
    "green":     "#3fb950",
    "orange":    "#f0883e",
    "purple":    "#bc8cff",
    "red":       "#ff5f56",
    "yellow":    "#ffbd2e",
    "card_bg":   "#161b22",
    "card_border":"#21262d",
}

LIGHT_THEME = {
    "bg_start":  "#ffffff",
    "bg_end":    "#f6f8fa",
    "border":    "#d0d7de",
    "header_bg": "#ebeef2",
    "text":      "#24292f",
    "bright":    "#0969da",
    "dim":       "#57606a",
    "accent":    "#0969da",
    "cyan":      "#0550ae",
    "green":     "#1a7f37",
    "orange":    "#bc4c00",
    "purple":    "#8250df",
    "red":       "#cf222e",
    "yellow":    "#9a6700",
    "card_bg":   "#f6f8fa",
    "card_border":"#d0d7de",
}

FONT_STACK = "ui-monospace, SFMono-Regular, Menlo, Consolas, 'Liberation Mono', monospace"


def build_terminal_profile_svg(theme: dict, animated: bool = True) -> str:
    """
    Constructs the terminal profile dossier SVG with clean XML and optional SMIL reveals.
    """
    # Animation helper for groups
    def anim_reveal(delay: float, dur: float = 0.45) -> str:
        if not animated:
            return ""
        return (
            f'<animate attributeName="opacity" from="0" to="1" '
            f'begin="{delay:.2f}s" dur="{dur:.2f}s" fill="freeze"/>'
        )

    # Initial opacity is 1 if static, or animated via SMIL
    # Notice: we DO NOT set opacity="0" on parent to ensure static-first fallback
    cur_anim = ""
    status_dot_anim = f'<circle cx="32" cy="{FOOTER_Y + (BOT_BAR_H / 2.0):.1f}" r="4" fill="{theme["green"]}"/>'
    if animated:
        cur_anim = (
            f'<rect x="420" y="70" width="7" height="13" fill="{theme["accent"]}">'
            f'<animate attributeName="opacity" values="1;1;0;0;1" dur="1.0s" repeatCount="indefinite"/>'
            f'</rect>'
        )
        status_dot_anim = (
            f'<circle cx="32" cy="{FOOTER_Y + (BOT_BAR_H / 2.0):.1f}" r="4" fill="{theme["green"]}">'
            f'<animate attributeName="opacity" values="1;0.4;1" dur="2.2s" repeatCount="indefinite"/>'
            f'</circle>'
        )

    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" width="{SVG_W:.0f}" height="{SVG_H:.0f}" viewBox="0 0 {SVG_W:.0f} {SVG_H:.0f}" font-family="{FONT_STACK}" role="img" aria-label="Prithiv — Terminal Profile Dossier">
  <title>Prithiv — Terminal Profile Dossier</title>
  <desc>Personal telemetry, education, projects, achievements and operational status in a matching terminal window</desc>

  <defs>
    <linearGradient id="profileBg" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="{theme['bg_start']}"/>
      <stop offset="100%" stop-color="{theme['bg_end']}"/>
    </linearGradient>
  </defs>

  <!-- Frame Background & Border -->
  <rect width="{SVG_W:.0f}" height="{SVG_H:.0f}" rx="10" fill="url(#profileBg)"/>
  <rect x="0.5" y="0.5" width="{SVG_W - 1:.1f}" height="{SVG_H - 1:.1f}" rx="9.5" fill="none" stroke="{theme['border']}" stroke-width="1"/>

  <!-- Terminal Title Bar -->
  <rect x="0" y="0" width="{SVG_W:.0f}" height="{TOP_BAR_H:.0f}" rx="10" fill="{theme['header_bg']}"/>
  <rect x="0" y="{TOP_BAR_H - 10:.0f}" width="{SVG_W:.0f}" height="10" fill="{theme['header_bg']}"/>
  <line x1="0" y1="{TOP_BAR_H:.0f}" x2="{SVG_W:.0f}" y2="{TOP_BAR_H:.0f}" stroke="{theme['border']}" stroke-width="1"/>

  <!-- Window Control Dots -->
  <circle cx="24" cy="19" r="5" fill="{theme['red']}"/>
  <circle cx="40" cy="19" r="5" fill="{theme['yellow']}"/>
  <circle cx="56" cy="19" r="5" fill="{theme['green']}"/>

  <!-- Title Bar Labels -->
  <text x="{SVG_W / 2.0:.1f}" y="23" fill="{theme['dim']}" font-size="11" text-anchor="middle" letter-spacing="2">PRITHIV // PROFILE DOSSIER</text>
  <text x="{SVG_W - 24:.1f}" y="23" fill="{theme['accent']}" font-size="10" text-anchor="end">profile.sh</text>

  <!-- 1. Command Prompt Section -->
  <g id="sec-prompt">
    {anim_reveal(0.10)}
    <text x="{PAD_X}" y="81" fill="{theme['accent']}" font-size="12" font-weight="600">prithiv@ai-core</text>
    <text x="{PAD_X + 114}" y="81" fill="{theme['dim']}" font-size="12">:</text>
    <text x="{PAD_X + 124}" y="81" fill="{theme['cyan']}" font-size="12">~</text>
    <text x="{PAD_X + 138}" y="81" fill="{theme['text']}" font-size="12">$ ./profile.sh --verbose --node-id=01</text>
    {cur_anim}
  </g>

  <!-- Divider 1 -->
  <line x1="{PAD_X}" y1="102" x2="{SVG_W - PAD_X}" y2="102" stroke="{theme['border']}" stroke-width="1" stroke-dasharray="4 4"/>

  <!-- 2. System Identity & Core Role -->
  <g id="sec-identity">
    {anim_reveal(0.25)}
    <!-- Section Title -->
    <text x="{PAD_X}" y="126" fill="{theme['accent']}" font-size="10" letter-spacing="2" font-weight="700">▶ SYSTEM IDENTITY &amp; CORE FOCUS</text>
    
    <!-- Identity Rows -->
    <text x="{PAD_X + 12}" y="152" fill="{theme['dim']}" font-size="11">NAME</text>
    <text x="{PAD_X + 110}" y="152" fill="{theme['bright']}" font-size="12" font-weight="700" letter-spacing="1">PRITHIV</text>

    <text x="{PAD_X + 12}" y="174" fill="{theme['dim']}" font-size="11">ROLE</text>
    <text x="{PAD_X + 110}" y="174" fill="{theme['text']}" font-size="11.5">AI/ML Engineer &amp; Full-Stack Developer</text>

    <text x="{PAD_X + 12}" y="196" fill="{theme['dim']}" font-size="11">EDUCATION</text>
    <text x="{PAD_X + 110}" y="196" fill="{theme['text']}" font-size="11.5">B.Tech Information Technology</text>
    <text x="{PAD_X + 110}" y="214" fill="{theme['dim']}" font-size="10.5">Chennai Institute of Technology · CGPA: 8.5+</text>

    <text x="{PAD_X + 12}" y="238" fill="{theme['dim']}" font-size="11">DOMAINS</text>
    <text x="{PAD_X + 110}" y="238" fill="{theme['cyan']}" font-size="11">Generative AI · Multi-Agent Systems · LLMs · Computer Vision</text>
    <text x="{PAD_X + 110}" y="256" fill="{theme['dim']}" font-size="10.5">Full Stack Architecture · Cloud Deployment · Systems Security</text>
  </g>

  <!-- Divider 2 -->
  <line x1="{PAD_X}" y1="274" x2="{SVG_W - PAD_X}" y2="274" stroke="{theme['border']}" stroke-width="1" stroke-dasharray="4 4"/>

  <!-- 3. Key Deployed Systems -->
  <g id="sec-projects">
    {anim_reveal(0.40)}
    <text x="{PAD_X}" y="298" fill="{theme['cyan']}" font-size="10" letter-spacing="2" font-weight="700">▶ KEY PRODUCTION &amp; RESEARCH SYSTEMS</text>

    <!-- Project 1: SciVerify -->
    <rect x="{PAD_X}" y="312" width="{SVG_W - (PAD_X * 2)}" height="54" rx="6" fill="{theme['card_bg']}" stroke="{theme['card_border']}" stroke-width="1"/>
    <text x="{PAD_X + 14}" y="333" fill="{theme['bright']}" font-size="11.5" font-weight="700">[01] SciVerify</text>
    <text x="{PAD_X + 125}" y="333" fill="{theme['dim']}" font-size="10">· Multi-Source Research Fact-Checking</text>
    <text x="{PAD_X + 14}" y="353" fill="{theme['text']}" font-size="10.5">Automated claims verification pipeline using LLM agents &amp; cross-paper citations</text>

    <!-- Project 2: EraseXpertz -->
    <rect x="{PAD_X}" y="374" width="{SVG_W - (PAD_X * 2)}" height="54" rx="6" fill="{theme['card_bg']}" stroke="{theme['card_border']}" stroke-width="1"/>
    <text x="{PAD_X + 14}" y="395" fill="{theme['bright']}" font-size="11.5" font-weight="700">[02] EraseXpertz</text>
    <text x="{PAD_X + 140}" y="395" fill="{theme['dim']}" font-size="10">· NIST 800-88 Data Sanitization</text>
    <text x="{PAD_X + 14}" y="415" fill="{theme['text']}" font-size="10.5">Enterprise secure data wiping tool with cryptographic tamper-evident audit logs</text>

    <!-- Project 3: Kshitij -->
    <rect x="{PAD_X}" y="436" width="{SVG_W - (PAD_X * 2)}" height="54" rx="6" fill="{theme['card_bg']}" stroke="{theme['card_border']}" stroke-width="1"/>
    <text x="{PAD_X + 14}" y="457" fill="{theme['bright']}" font-size="11.5" font-weight="700">[03] Kshitij</text>
    <text x="{PAD_X + 105}" y="457" fill="{theme['dim']}" font-size="10">· Satellite Crop Health &amp; Disaster Intelligence</text>
    <text x="{PAD_X + 14}" y="477" fill="{theme['text']}" font-size="10.5">Multi-spectral earth observation analytics for predictive drought &amp; crop yields</text>

    <!-- Project 4: T-BillFlow -->
    <rect x="{PAD_X}" y="498" width="{SVG_W - (PAD_X * 2)}" height="54" rx="6" fill="{theme['card_bg']}" stroke="{theme['card_border']}" stroke-width="1"/>
    <text x="{PAD_X + 14}" y="519" fill="{theme['bright']}" font-size="11.5" font-weight="700">[04] T-BillFlow</text>
    <text x="{PAD_X + 125}" y="519" fill="{theme['dim']}" font-size="10">· Financial Settlement &amp; Auction Engine</text>
    <text x="{PAD_X + 14}" y="539" fill="{theme['text']}" font-size="10.5">High-throughput Treasury Bill auction matching engine with zero-loss audit ledger</text>
  </g>

  <!-- Divider 3 -->
  <line x1="{PAD_X}" y1="562" x2="{SVG_W - PAD_X}" y2="562" stroke="{theme['border']}" stroke-width="1" stroke-dasharray="4 4"/>

  <!-- 4. Verified Accolades & Hackathons -->
  <g id="sec-accolades">
    {anim_reveal(0.55)}
    <text x="{PAD_X}" y="586" fill="{theme['orange']}" font-size="10" letter-spacing="2" font-weight="700">▶ VERIFIED ACCOLADES &amp; COMPETITIONS</text>

    <!-- Hackathon 1 -->
    <text x="{PAD_X + 12}" y="612" fill="{theme['yellow']}" font-size="11">🏆 WINNER</text>
    <text x="{PAD_X + 130}" y="612" fill="{theme['bright']}" font-size="11" font-weight="600">Web3 Conference Hackathon</text>
    <text x="{PAD_X + 130}" y="628" fill="{theme['dim']}" font-size="10">1st Place — Decentralized identity &amp; automated verification systems</text>

    <!-- Hackathon 2 -->
    <text x="{PAD_X + 12}" y="654" fill="{theme['cyan']}" font-size="11">⚡ TOP 5</text>
    <text x="{PAD_X + 130}" y="654" fill="{theme['bright']}" font-size="11" font-weight="600">Cardano Hackathon Asia</text>
    <text x="{PAD_X + 130}" y="670" fill="{theme['dim']}" font-size="10">Regional finalist — Autonomous smart-contract agent architecture</text>

    <!-- Hackathon 3 -->
    <text x="{PAD_X + 12}" y="696" fill="{theme['purple']}" font-size="11">🛰️ FINALIST</text>
    <text x="{PAD_X + 130}" y="696" fill="{theme['bright']}" font-size="11" font-weight="600">NASA Space Apps Challenge</text>
    <text x="{PAD_X + 130}" y="712" fill="{theme['dim']}" font-size="10">Global Nominee / Finalist — Remote sensing satellite data model</text>
  </g>

  <!-- Divider 4 -->
  <line x1="{PAD_X}" y1="728" x2="{SVG_W - PAD_X}" y2="728" stroke="{theme['border']}" stroke-width="1" stroke-dasharray="4 4"/>

  <!-- 5. Operational Node Status -->
  <g id="sec-status">
    {anim_reveal(0.70)}
    <rect x="{PAD_X}" y="742" width="{SVG_W - (PAD_X * 2)}" height="38" rx="6" fill="{theme['card_bg']}" stroke="{theme['green']}" stroke-width="1" stroke-opacity="0.6"/>
    <circle cx="{PAD_X + 16}" cy="761" r="5" fill="{theme['green']}"/>
    <text x="{PAD_X + 30}" y="765" fill="{theme['green']}" font-size="11" font-weight="700" letter-spacing="1">CURRENT STATUS: OPEN TO INTERNSHIPS</text>
    <text x="{SVG_W - PAD_X - 16}" y="765" fill="{theme['dim']}" font-size="10.5" text-anchor="end">AI/ML · Research · Full-Stack</text>
  </g>

  <!-- Footer Status Bar -->
  <line x1="0" y1="{FOOTER_Y:.1f}" x2="{SVG_W:.0f}" y2="{FOOTER_Y:.1f}" stroke="{theme['border']}" stroke-width="1"/>

  {status_dot_anim}
  <text x="44" y="{FOOTER_Y + 21:.1f}" fill="{theme['text']}" font-size="10.5" letter-spacing="1">TELEMETRY: <tspan fill="{theme['cyan']}">ACTIVE</tspan> · LATENCY: &lt;12ms</text>

  <text x="{SVG_W - 24:.1f}" y="{FOOTER_Y + 21:.1f}" fill="{theme['dim']}" font-size="10" text-anchor="end">
    zsh 5.9 · UTF-8 · ENV: <tspan fill="{theme['green']}">PRODUCTION</tspan>
  </text>
</svg>"""

    return svg


def main():
    out_animated = os.path.join(HERO_DIR, "terminal-profile.svg")
    out_static   = os.path.join(HERO_DIR, "terminal-profile-static.svg")
    out_light    = os.path.join(HERO_DIR, "terminal-profile-light.svg")

    # 1. Dark Animated
    print("Writing terminal-profile.svg (dark, animated)...")
    svg_anim = build_terminal_profile_svg(DARK_THEME, animated=True)
    with open(out_animated, "w", encoding="utf-8") as f:
        f.write(svg_anim)
    print(f"  -> {out_animated} ({os.path.getsize(out_animated)/1024:.1f} KB)")

    # 2. Dark Static
    print("Writing terminal-profile-static.svg (dark, static)...")
    svg_static = build_terminal_profile_svg(DARK_THEME, animated=False)
    with open(out_static, "w", encoding="utf-8") as f:
        f.write(svg_static)
    print(f"  -> {out_static} ({os.path.getsize(out_static)/1024:.1f} KB)")

    # 3. Light Static
    print("Writing terminal-profile-light.svg (light, static)...")
    svg_light = build_terminal_profile_svg(LIGHT_THEME, animated=False)
    with open(out_light, "w", encoding="utf-8") as f:
        f.write(svg_light)
    print(f"  -> {out_light} ({os.path.getsize(out_light)/1024:.1f} KB)")

    # XML Validation
    for p in [out_animated, out_static, out_light]:
        ET.parse(p)
        print(f"  [PASS] Valid XML: {os.path.basename(p)}")

    print("\nTerminal profile dossier SVGs created and validated successfully.")


if __name__ == "__main__":
    main()
