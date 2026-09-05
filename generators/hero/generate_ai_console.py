"""
generate_ai_console.py
----------------------
Generates the Visual AI Systems Monitor SVGs:
  - assets/hero/ai-console.svg        (animated, dark mode)
  - assets/hero/ai-console-static.svg (static, dark mode)
  - assets/hero/ai-console-light.svg  (static, light mode)

Design specifications:
  - Dimensions: 900 x 420 px (retains exact console frame and surrounding layout).
  - Inside: A unique, mesmerizing visual AI systems monitor.
  - Core pipeline: INPUT -> REASON -> VALIDATE -> EXECUTE -> OBSERVE.
  - Live indicators: REASONING, VALIDATION, AUTOMATION, DEPLOYMENT.
  - Real-time token / signal waveform telemetry visualization.
  - Animated signal/data particles moving through node connections.
  - Closed-loop adaptive feedback bus (OBSERVE -> INPUT).
  - Subtle cyan/white/blue palette matching the identity hero.
  - 100% self-contained vector SVG, zero external dependencies, valid XML.
"""

import os
import xml.etree.ElementTree as ET

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT  = os.path.abspath(os.path.join(SCRIPT_DIR, "..", ".."))
HERO_DIR   = os.path.join(REPO_ROOT, "assets", "hero")
os.makedirs(HERO_DIR, exist_ok=True)

SVG_W = 900.0
SVG_H = 420.0

DARK_THEME = {
    "bg_start":     "#10141d",
    "bg_end":       "#0a0d14",
    "border":       "#262c36",
    "card_bg":      "#131822",
    "card_border":  "#1f2633",
    "node_bg":      "#161c28",
    "node_ring":    "#303a4d",
    "text_bright":  "#f0f6fc",
    "text_main":    "#c9d1d9",
    "text_dim":     "#8b949e",
    "text_muted":   "#57606a",
    "accent_blue":  "#58a6ff",
    "accent_cyan":  "#39c5cf",
    "accent_green": "#3fb950",
    "accent_purple":"#bc8cff",
    "glow_color":   "#39c5cf",
    "bus_line":     "#283345",
    "grid_dot":     "#ffffff",
}

LIGHT_THEME = {
    "bg_start":     "#ffffff",
    "bg_end":       "#f6f8fa",
    "border":       "#d0d7de",
    "card_bg":      "#f6f8fa",
    "card_border":  "#d8dee4",
    "node_bg":      "#ffffff",
    "node_ring":    "#afb8c1",
    "text_bright":  "#0969da",
    "text_main":    "#24292f",
    "text_dim":     "#57606a",
    "text_muted":   "#8c959f",
    "accent_blue":  "#0969da",
    "accent_cyan":  "#0550ae",
    "accent_green": "#1a7f37",
    "accent_purple":"#8250df",
    "glow_color":   "#0969da",
    "bus_line":     "#d0d7de",
    "grid_dot":     "#000000",
}

FONT_STACK = "ui-monospace, SFMono-Regular, Menlo, Consolas, 'Liberation Mono', monospace"


def build_ai_console_svg(theme: dict, animated: bool = True) -> str:
    """
    Constructs the AI Systems Monitor SVG.
    """
    # ── Pipeline Nodes Configuration ──
    nodes = [
        {"x": 110, "label": "INPUT",    "sub": "CONTEXT // EMBED", "tag": "01", "color": theme["accent_blue"]},
        {"x": 280, "label": "REASON",   "sub": "AGENT // INFER",   "tag": "02", "color": theme["accent_cyan"]},
        {"x": 450, "label": "VALIDATE", "sub": "GROUND // AUDIT",  "tag": "03", "color": theme["accent_green"]},
        {"x": 620, "label": "EXECUTE",  "sub": "DISPATCH // TOOL", "tag": "04", "color": theme["accent_purple"]},
        {"x": 790, "label": "OBSERVE",  "sub": "TELEMETRY // EVAL","tag": "05", "color": theme["accent_blue"]},
    ]
    node_y = 205.0
    node_r_outer = 34.0
    node_r_inner = 25.0

    # ── Connection Bus Lines & Animated Signal Particles ──
    bus_elements = []
    particle_elements = []

    for i in range(len(nodes) - 1):
        x_start = nodes[i]["x"] + node_r_outer
        x_end   = nodes[i + 1]["x"] - node_r_outer
        color   = nodes[i]["color"]

        # Background connection track
        bus_elements.append(
            f'  <line x1="{x_start:.1f}" y1="{node_y:.1f}" x2="{x_end:.1f}" y2="{node_y:.1f}" '
            f'stroke="{theme["bus_line"]}" stroke-width="2"/>'
        )
        # Directional tick in center of track
        mid_x = (x_start + x_end) / 2.0
        bus_elements.append(
            f'  <path d="M {mid_x - 3:.1f} {node_y - 4:.1f} L {mid_x + 3:.1f} {node_y:.1f} L {mid_x - 3:.1f} {node_y + 4:.1f}" '
            f'fill="none" stroke="{color}" stroke-width="1.2" opacity="0.6"/>'
        )

        if animated:
            # 2 staggered data particles moving forward along connection
            dur1 = 1.6
            dur2 = 1.6
            delay1 = i * 0.32
            delay2 = delay1 + 0.80

            particle_elements.append(
                f'  <circle cy="{node_y:.1f}" r="3" fill="{color}">\n'
                f'    <animate attributeName="cx" from="{x_start:.1f}" to="{x_end:.1f}" '
                f'begin="{delay1:.2f}s" dur="{dur1:.2f}s" repeatCount="indefinite"/>\n'
                f'    <animate attributeName="opacity" values="0;1;1;0" keyTimes="0;0.1;0.9;1" '
                f'begin="{delay1:.2f}s" dur="{dur1:.2f}s" repeatCount="indefinite"/>\n'
                f'  </circle>'
            )
            particle_elements.append(
                f'  <circle cy="{node_y:.1f}" r="2" fill="{theme["accent_cyan"]}">\n'
                f'    <animate attributeName="cx" from="{x_start:.1f}" to="{x_end:.1f}" '
                f'begin="{delay2:.2f}s" dur="{dur2:.2f}s" repeatCount="indefinite"/>\n'
                f'    <animate attributeName="opacity" values="0;0.8;0.8;0" keyTimes="0;0.1;0.9;1" '
                f'begin="{delay2:.2f}s" dur="{dur2:.2f}s" repeatCount="indefinite"/>\n'
                f'  </circle>'
            )
        else:
            # Static data packet in transit
            particle_elements.append(
                f'  <circle cx="{x_start + (x_end - x_start) * 0.45:.1f}" cy="{node_y:.1f}" r="2.5" fill="{color}"/>'
            )

    # ── Feedback Loop (OBSERVE -> INPUT) ──
    feedback_path = f"M 790 {node_y + node_r_outer:.1f} C 790 300, 110 300, 110 {node_y + node_r_outer:.1f}"
    feedback_bus = (
        f'  <!-- Closed-Loop Feedback Bus -->\n'
        f'  <path d="{feedback_path}" fill="none" stroke="{theme["bus_line"]}" stroke-width="1.5" stroke-dasharray="4 4"/>'
    )
    feedback_particle = ""
    if animated:
        feedback_particle = (
            f'  <circle r="3" fill="{theme["accent_cyan"]}">\n'
            f'    <animateMotion path="{feedback_path}" dur="4.2s" repeatCount="indefinite"/>\n'
            f'    <animate attributeName="opacity" values="0;1;1;0" keyTimes="0;0.05;0.95;1" dur="4.2s" repeatCount="indefinite"/>\n'
            f'  </circle>'
        )
    else:
        feedback_particle = f'  <circle cx="450" cy="300" r="2.5" fill="{theme["accent_cyan"]}"/>'

    # ── Node Graphics ──
    node_elements = []
    for node in nodes:
        nx = node["x"]
        col = node["color"]
        pulse = ""
        if animated:
            pulse = (
                f'<animate attributeName="r" values="32;36;32" dur="3.0s" repeatCount="indefinite"/>\n'
                f'<animate attributeName="stroke-opacity" values="0.8;0.2;0.8" dur="3.0s" repeatCount="indefinite"/>'
            )

        node_elements.append(f"""  <!-- Node {node['label']} -->
  <g id="node-{node['tag']}">
    <!-- Outer Glow Ring -->
    <circle cx="{nx}" cy="{node_y:.1f}" r="34" fill="none" stroke="{col}" stroke-width="1" stroke-opacity="0.3">
      {pulse}
    </circle>
    <!-- Node Body -->
    <circle cx="{nx}" cy="{node_y:.1f}" r="{node_r_inner:.1f}" fill="{theme['node_bg']}" stroke="{col}" stroke-width="1.6"/>
    <!-- Node Channel Tag -->
    <text x="{nx}" y="{node_y - 7:.1f}" fill="{col}" font-size="9" font-weight="700" text-anchor="middle" letter-spacing="1.5">{node['label']}</text>
    <text x="{nx}" y="{node_y + 8:.1f}" fill="{theme['text_dim']}" font-size="7.5" text-anchor="middle" letter-spacing="1">[{node['tag']}]</text>
    <!-- Sub-label underneath -->
    <text x="{nx}" y="{node_y + 48:.1f}" fill="{theme['text_dim']}" font-size="9" text-anchor="middle" letter-spacing="1.2">{node['sub']}</text>
  </g>""")

    # ── Signal Waveform Telemetry (Bottom Left) ──
    wave_path = (
        "M 50 376 "
        "L 80 376 L 90 368 L 100 384 L 110 364 L 120 388 L 130 360 L 140 376 "
        "L 170 376 L 180 366 L 190 386 L 200 362 L 210 376 "
        "L 250 376 L 260 370 L 270 382 L 280 376 "
        "L 320 376"
    )
    wave_anim = ""
    if animated:
        wave_anim = '<animate attributeName="stroke-dashoffset" from="270" to="0" dur="2.8s" repeatCount="indefinite"/>'

    # Top Status Indicators
    indicators = [
        {"name": "REASONING",  "state": "ACTIVE",      "color": theme["accent_cyan"]},
        {"name": "VALIDATION", "state": "DETERMINISTIC","color": theme["accent_green"]},
        {"name": "AUTOMATION", "state": "AGENT LOOP",  "color": theme["accent_purple"]},
        {"name": "DEPLOYMENT", "state": "PRODUCTION",  "color": theme["accent_blue"]},
    ]

    indicator_cards = []
    card_w = 196.0
    card_h = 36.0
    card_y = 52.0
    start_x = 44.0
    spacing = 205.0

    for idx, ind in enumerate(indicators):
        cx = start_x + (idx * spacing)
        dot_anim = ""
        if animated:
            dot_anim = f'<animate attributeName="opacity" values="1;0.3;1" dur="2.2s" repeatCount="indefinite"/>'

        indicator_cards.append(f"""    <!-- Indicator {ind['name']} -->
    <rect x="{cx:.1f}" y="{card_y:.1f}" width="{card_w:.1f}" height="{card_h:.1f}" rx="6" fill="{theme['card_bg']}" stroke="{theme['card_border']}" stroke-width="1"/>
    <circle cx="{cx + 14:.1f}" cy="{card_y + 18:.1f}" r="4" fill="{ind['color']}">
      {dot_anim}
    </circle>
    <text x="{cx + 26:.1f}" y="{card_y + 16:.1f}" fill="{theme['text_dim']}" font-size="8.5" letter-spacing="1">{ind['name']}</text>
    <text x="{cx + 26:.1f}" y="{card_y + 27:.1f}" fill="{ind['color']}" font-size="9" font-weight="700" letter-spacing="1">{ind['state']}</text>""")

    indicators_markup = "\n".join(indicator_cards)
    bus_markup = "\n".join(bus_elements)
    particles_markup = "\n".join(particle_elements)
    nodes_markup = "\n".join(node_elements)

    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {SVG_W:.0f} {SVG_H:.0f}" width="{SVG_W:.0f}" height="{SVG_H:.0f}" font-family="{FONT_STACK}" role="img" aria-label="PRITHIV // Visual AI Systems Monitor">
  <title>PRITHIV // Visual AI Systems Monitor</title>
  <desc>Real-time pipeline monitoring and dynamic feedback loop for intelligent systems engineering</desc>

  <defs>
    <!-- Background Gradient -->
    <linearGradient id="consoleBg" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="{theme['bg_start']}"/>
      <stop offset="100%" stop-color="{theme['bg_end']}"/>
    </linearGradient>

    <!-- Subtle Technical Grid Pattern -->
    <pattern id="consoleGrid" x="0" y="0" width="24" height="24" patternUnits="userSpaceOnUse">
      <circle cx="2" cy="2" r="0.75" fill="{theme['grid_dot']}" opacity="0.035"/>
    </pattern>
  </defs>

  <!-- Frame Background & Pattern -->
  <rect width="{SVG_W:.0f}" height="{SVG_H:.0f}" rx="10" fill="url(#consoleBg)"/>
  <rect width="{SVG_W:.0f}" height="{SVG_H:.0f}" rx="10" fill="url(#consoleGrid)"/>
  <rect x="0.5" y="0.5" width="{SVG_W - 1:.1f}" height="{SVG_H - 1:.1f}" rx="9.5" fill="none" stroke="{theme['border']}" stroke-width="1"/>

  <!-- Terminal Top Bar -->
  <rect x="0" y="0" width="{SVG_W:.0f}" height="38" rx="10" fill="{theme['card_bg']}"/>
  <rect x="0" y="28" width="{SVG_W:.0f}" height="10" fill="{theme['card_bg']}"/>
  <line x1="0" y1="38" x2="{SVG_W:.0f}" y2="38" stroke="{theme['border']}" stroke-width="1"/>

  <!-- Window Controls -->
  <circle cx="22" cy="19" r="5" fill="#ff5f56"/>
  <circle cx="38" cy="19" r="5" fill="#ffbd2e"/>
  <circle cx="54" cy="19" r="5" fill="#3fb950"/>

  <!-- Title & Adaptive Loop Label -->
  <text x="{SVG_W / 2.0:.1f}" y="23" fill="{theme['text_dim']}" font-size="11" text-anchor="middle" letter-spacing="2.5">PRITHIV // AI SYSTEMS MONITOR</text>
  <text x="{SVG_W - 24:.1f}" y="23" fill="{theme['accent_cyan']}" font-size="10.5" font-weight="600" text-anchor="end" letter-spacing="1.5">SYSTEM LOOP // ADAPTIVE</text>

  <!-- 1. Top Telemetry Indicators -->
  <g id="indicators">
{indicators_markup}
  </g>

  <!-- Sub-bar Divider -->
  <line x1="36" y1="102" x2="{SVG_W - 36:.1f}" y2="102" stroke="{theme['border']}" stroke-width="1" stroke-dasharray="3 3"/>

  <!-- Pipeline Label -->
  <text x="44" y="126" fill="{theme['accent_blue']}" font-size="10" letter-spacing="2" font-weight="700">▶ AUTONOMOUS EXECUTION PIPELINE</text>
  <text x="{SVG_W - 44:.1f}" y="126" fill="{theme['text_dim']}" font-size="9.5" text-anchor="end" letter-spacing="1">STATE: CONVERGED · CYCLE: 12ms</text>

  <!-- 2. Network Bus Tracks & Connections -->
{bus_markup}

  <!-- Feedback Bus Loop -->
{feedback_bus}
  <text x="{SVG_W / 2.0:.1f}" y="318" fill="{theme['text_dim']}" font-size="8.5" text-anchor="middle" letter-spacing="2">ADAPTIVE FEEDBACK BUS // CONTINUOUS LEARNING</text>

  <!-- 3. Animated Signal Particles -->
{particles_markup}
{feedback_particle}

  <!-- 4. Pipeline Nodes -->
{nodes_markup}

  <!-- Lower Monitor Divider -->
  <line x1="0" y1="352" x2="{SVG_W:.0f}" y2="352" stroke="{theme['border']}" stroke-width="1"/>

  <!-- 5. Bottom Signal Waveform & Diagnostics -->
  <g id="waveform-telemetry">
    <!-- Waveform Track -->
    <text x="44" y="379" fill="{theme['accent_cyan']}" font-size="9.5" font-weight="600" letter-spacing="1">SIGNAL // TOKEN FLUX:</text>
    <path d="{wave_path}" fill="none" stroke="{theme['bus_line']}" stroke-width="1.5"/>
    <path d="{wave_path}" fill="none" stroke="{theme['accent_cyan']}" stroke-width="1.5" stroke-dasharray="60 210">
      {wave_anim}
    </path>

    <!-- Center Diagnostics -->
    <text x="{SVG_W / 2.0:.1f}" y="380" fill="{theme['text_dim']}" font-size="9.5" text-anchor="middle" letter-spacing="1.2">
      INFERENCE: <tspan fill="{theme['accent_green']}">STEADY</tspan> &#160;·&#160; LATENCY: <tspan fill="{theme['accent_cyan']}">14ms</tspan> &#160;·&#160; GUARDRAILS: <tspan fill="{theme['text_bright']}">ENFORCED</tspan>
    </text>

    <!-- Right Telemetry State -->
    <circle cx="{SVG_W - 170:.1f}" cy="376" r="3.5" fill="{theme['accent_green']}"/>
    <text x="{SVG_W - 24:.1f}" y="380" fill="{theme['text_dim']}" font-size="9.5" text-anchor="end" letter-spacing="1">
      MONITOR: <tspan fill="{theme['accent_green']}">ONLINE</tspan>
    </text>
  </g>
</svg>"""

    return svg


def main():
    out_animated = os.path.join(HERO_DIR, "ai-console.svg")
    out_static   = os.path.join(HERO_DIR, "ai-console-static.svg")
    out_light    = os.path.join(HERO_DIR, "ai-console-light.svg")

    print("Generating ai-console.svg (dark, animated visual monitor)...")
    svg_anim = build_ai_console_svg(DARK_THEME, animated=True)
    with open(out_animated, "w", encoding="utf-8") as f:
        f.write(svg_anim)
    print(f"  -> {out_animated} ({os.path.getsize(out_animated)/1024:.1f} KB)")

    print("Generating ai-console-static.svg (dark, static)...")
    svg_static = build_ai_console_svg(DARK_THEME, animated=False)
    with open(out_static, "w", encoding="utf-8") as f:
        f.write(svg_static)
    print(f"  -> {out_static} ({os.path.getsize(out_static)/1024:.1f} KB)")

    print("Generating ai-console-light.svg (light, static)...")
    svg_light = build_ai_console_svg(LIGHT_THEME, animated=False)
    with open(out_light, "w", encoding="utf-8") as f:
        f.write(svg_light)
    print(f"  -> {out_light} ({os.path.getsize(out_light)/1024:.1f} KB)")

    for p in [out_animated, out_static, out_light]:
        ET.parse(p)
        print(f"  [PASS] Valid XML: {os.path.basename(p)}")

    print("\nVisual AI Systems Monitor SVGs created and validated successfully.")


if __name__ == "__main__":
    main()
