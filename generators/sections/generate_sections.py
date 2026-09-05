"""
generate_sections.py
--------------------
Generates the 11/10 visual quality SVGs for:
  1. SELECTED RECOGNITION (Horizontal Career Milestone Timeline)
  2. CURRENTLY ENGINEERING (Directional Engineering Focus Map & Center Statement)

Complies with all specifications:
  - Exact verified content with zero fabricated claims.
  - Recognition timeline: Large 01/02/03 numbering, strong titles, smaller metadata,
    continuous hairline timeline with subtle signal particle.
  - Engineering focus map: Structured progression BUILD -> ENGINEER -> SYSTEMIZE -> EXPLORE -> COLLABORATE,
    directional flow connectors, and distinctive center statement.
  - Dark/light mode theme support.
  - 100% valid XML, lightweight (< 15 KB), zero external dependencies.
"""

import os
import xml.etree.ElementTree as ET

SCRIPT_DIR   = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT    = os.path.abspath(os.path.join(SCRIPT_DIR, "..", ".."))
SECTIONS_DIR = os.path.join(REPO_ROOT, "assets", "sections")
os.makedirs(SECTIONS_DIR, exist_ok=True)

DARK_THEME = {
    "bg_start":     "#111722",
    "bg_end":       "#0d1117",
    "border":       "#30363d",
    "timeline_line":"#21262d",
    "big_num":      "#1e2530",
    "text_hero":    "#f0f6fc",
    "text_body":    "#c9d1d9",
    "text_dim":     "#8b949e",
    "text_muted":   "#57606a",
    "accent":       "#58a6ff",
    "cyan":         "#39c5cf",
    "green":        "#3fb950",
    "purple":       "#bc8cff",
    "label_bg":     "#161b22",
    "label_border": "#30363d",
}

LIGHT_THEME = {
    "bg_start":     "#ffffff",
    "bg_end":       "#f6f8fa",
    "border":       "#d0d7de",
    "timeline_line":"#d8dee4",
    "big_num":      "#e6edf3",
    "text_hero":    "#1f2328",
    "text_body":    "#24292f",
    "text_dim":     "#57606a",
    "text_muted":   "#8c959f",
    "accent":       "#0969da",
    "cyan":         "#0550ae",
    "green":        "#1a7f37",
    "purple":       "#8250df",
    "label_bg":     "#f6f8fa",
    "label_border": "#d0d7de",
}

FONT_SANS = "-apple-system, BlinkMacSystemFont, 'Segoe UI', Inter, Roboto, Helvetica, Arial, sans-serif"
FONT_MONO = "ui-monospace, SFMono-Regular, Menlo, Consolas, 'Liberation Mono', monospace"


# ═══════════════════════════════════════════════════════════════════════════════
# 1. SELECTED RECOGNITION (Horizontal Career Milestone Timeline)
# ═══════════════════════════════════════════════════════════════════════════════
def build_recognition_svg(theme: dict, animated: bool = True) -> str:
    w = 900.0
    h = 200.0

    timeline_y = 66.0
    milestones = [
        {
            "x": 160.0, "num": "01",
            "title": "WEB3 CONFERENCE HACKATHON",
            "result": "WINNER", "res_col": theme["green"],
            "meta": "DELHI · 2024"
        },
        {
            "x": 450.0, "num": "02",
            "title": "CARDANO HACKATHON ASIA",
            "result": "TOP 5", "res_col": theme["cyan"],
            "meta": "ASIA REGION"
        },
        {
            "x": 740.0, "num": "03",
            "title": "NASA SPACE APPS CHALLENGE",
            "result": "FINALIST", "res_col": theme["purple"],
            "meta": "GLOBAL NOMINEE"
        }
    ]

    particle = ""
    if animated:
        particle = (
            f'  <!-- Subtle Signal Particle on Timeline -->\n'
            f'  <circle cy="{timeline_y}" r="3" fill="{theme["cyan"]}">\n'
            f'    <animate attributeName="cx" from="80" to="820" dur="3.6s" repeatCount="indefinite"/>\n'
            f'    <animate attributeName="opacity" values="0;1;1;0" keyTimes="0;0.05;0.95;1" dur="3.6s" repeatCount="indefinite"/>\n'
            f'  </circle>'
        )

    nodes_markup = []
    for m in milestones:
        mx = m["x"]
        pulse = ""
        if animated:
            pulse = f'<animate attributeName="r" values="6;8;6" dur="2.8s" repeatCount="indefinite"/>'

        meta_line = f'<tspan fill="{m["res_col"]}" font-weight="700">{m["result"]}</tspan> &#160;&#183;&#160; {m["meta"]}' if m["meta"] else f'<tspan fill="{m["res_col"]}" font-weight="700">{m["result"]}</tspan>'

        nodes_markup.append(f"""    <!-- Milestone {m['num']} -->
    <g id="ms-{m['num']}">
      <!-- Large Watermark Numeral -->
      <text x="{mx}" y="56" font-family="{FONT_MONO}" font-size="42" font-weight="800"
        fill="{theme['big_num']}" text-anchor="middle" letter-spacing="-1">{m['num']}</text>

      <!-- Node Outer Ring & Inner Dot -->
      <circle cx="{mx}" cy="{timeline_y}" r="6" fill="{theme['bg_end']}" stroke="{m['res_col']}" stroke-width="1.8">
        {pulse}
      </circle>
      <circle cx="{mx}" cy="{timeline_y}" r="2.5" fill="{m['res_col']}"/>

      <!-- Milestone Title -->
      <text x="{mx}" y="112" font-family="{FONT_SANS}" font-size="12.5" font-weight="700"
        fill="{theme['text_hero']}" text-anchor="middle" letter-spacing="0.5">{m['title']}</text>

      <!-- Result & Location Metadata -->
      <text x="{mx}" y="136" font-family="{FONT_MONO}" font-size="10.5"
        fill="{theme['text_dim']}" text-anchor="middle" letter-spacing="1">
        {meta_line}
      </text>
    </g>""")

    milestones_str = "\n".join(nodes_markup)

    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w:.0f} {h:.0f}" width="{w:.0f}" height="{h:.0f}" role="img" aria-label="Selected Recognition Milestones">
  <title>Selected Recognition Milestones</title>
  <desc>Career milestones: Web3 Conference Hackathon Winner, Cardano Hackathon Asia Top 5, NASA Space Apps Challenge Finalist</desc>

  <defs>
    <linearGradient id="recogBg" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="{theme['bg_start']}"/>
      <stop offset="100%" stop-color="{theme['bg_end']}"/>
    </linearGradient>
  </defs>

  <!-- Frame Background & Hairline Border -->
  <rect width="{w:.0f}" height="{h:.0f}" rx="10" fill="url(#recogBg)"/>
  <rect x="0.5" y="0.5" width="{w - 1:.1f}" height="{h - 1:.1f}" rx="9.5" fill="none" stroke="{theme['border']}" stroke-width="1"/>

  <!-- Top Technical Header Line -->
  <line x1="0" y1="30" x2="{w:.0f}" y2="30" stroke="{theme['border']}" stroke-width="1"/>
  <text x="36" y="20" font-family="{FONT_MONO}" font-size="9.5" fill="{theme['text_muted']}" letter-spacing="1.5">CAREER MILESTONES // VERIFIED RECOGNITION</text>
  <text x="{w - 36:.1f}" y="20" font-family="{FONT_MONO}" font-size="9.5" fill="{theme['accent']}" text-anchor="end" letter-spacing="1">CHRONOLOGY: 2024</text>

  <!-- Continuous Horizontal Timeline Connection -->
  <line x1="80" y1="{timeline_y}" x2="820" y2="{timeline_y}" stroke="{theme['timeline_line']}" stroke-width="1.6"/>
  <circle cx="80" cy="{timeline_y}" r="2" fill="{theme['accent']}"/>
  <circle cx="820" cy="{timeline_y}" r="2" fill="{theme['accent']}"/>

{particle}

  <!-- Milestones -->
{milestones_str}

  <!-- Subtle Bottom Bar -->
  <line x1="36" y1="168" x2="{w - 36:.1f}" y2="168" stroke="{theme['border']}" stroke-width="1" stroke-dasharray="3 3"/>
  <text x="{w / 2.0:.1f}" y="184" font-family="{FONT_MONO}" font-size="9" fill="{theme['text_muted']}" text-anchor="middle" letter-spacing="1.8">
    PROVEN CAPABILITIES IN AUTONOMOUS AGENTS, DISTRIBUTED SYSTEMS &amp; REMOTE SENSING
  </text>
</svg>"""

    return svg


# ═══════════════════════════════════════════════════════════════════════════════
# 2. CURRENTLY ENGINEERING (Directional Engineering Focus Map & Center Statement)
# ═══════════════════════════════════════════════════════════════════════════════
def build_currently_engineering_svg(theme: dict, animated: bool = True) -> str:
    w = 900.0
    h = 330.0

    stages = [
        {
            "label": "BUILDING", "prog": "BUILD", "col": theme["accent"],
            "concepts": [("AI AGENTS", True), ("MULTI-AGENT SYSTEMS", True), ("LLM APPLICATIONS", True)]
        },
        {
            "label": "ENGINEERING", "prog": "ENGINEER", "col": theme["cyan"],
            "concepts": [("RAG", True), ("VECTOR SEARCH", True), ("TOOL CALLING", True), ("MODEL EVALUATION", True)]
        },
        {
            "label": "SYSTEMS", "prog": "SYSTEMIZE", "col": theme["accent"],
            "concepts": [("CLOUD DEPLOYMENT", True), ("REST APIs", True), ("BACKEND ARCHITECTURE", True), ("DATA PIPELINES", True)]
        },
        {
            "label": "EXPLORING", "prog": "EXPLORE", "col": theme["purple"],
            "concepts": [("ADAPTIVE ML", False), ("REAL-TIME INFERENCE", False), ("EDGE AI", False)]
        },
        {
            "label": "OPEN TO", "prog": "COLLABORATE", "col": theme["green"],
            "concepts": [("AI/ML INTERNSHIPS", True), ("RESEARCH", True), ("OPEN-SOURCE COLLABORATION", True)]
        }
    ]

    row_y_start = 74.0
    row_gap = 36.0

    rows_markup = []
    for idx, st in enumerate(stages):
        ry = row_y_start + (idx * row_gap)
        color = st["col"]

        # Build concept spans
        c_parts = []
        for c_text, is_bold in st["concepts"]:
            if is_bold:
                c_parts.append(f'<tspan font-weight="700" fill="{theme["text_hero"]}">{c_text}</tspan>')
            else:
                c_parts.append(f'<tspan font-weight="500" fill="{theme["text_body"]}">{c_text}</tspan>')
        concepts_str = " &#160;&#183;&#160; ".join(c_parts)

        # Directional chevron / line
        chevron = f'<path d="M 178 {ry - 4:.1f} L 184 {ry:.1f} L 178 {ry + 4:.1f}" fill="none" stroke="{color}" stroke-width="1.4"/>'

        rows_markup.append(f"""    <!-- Stage {idx+1}: {st['label']} -->
    <g id="stage-{idx+1}">
      <!-- Compact Technical Label Badge -->
      <rect x="42" y="{ry - 12:.1f}" width="124" height="24" rx="4" fill="{theme['label_bg']}" stroke="{color}" stroke-width="1" stroke-opacity="0.8"/>
      <circle cx="54" cy="{ry:.1f}" r="2.5" fill="{color}"/>
      <text x="110" y="{ry + 3.5:.1f}" font-family="{FONT_MONO}" font-size="9" font-weight="700"
        fill="{color}" text-anchor="middle" letter-spacing="1.2">{st['label']}</text>

      <!-- Directional Connector Line & Chevron -->
      <line x1="166" y1="{ry:.1f}" x2="182" y2="{ry:.1f}" stroke="{theme['border']}" stroke-width="1.2"/>
      {chevron}

      <!-- Actual Technical Concepts (The Visual Focus) -->
      <text x="200" y="{ry + 4:.1f}" font-family="{FONT_SANS}" font-size="12" letter-spacing="0.2">
        {concepts_str}
      </text>
    </g>""")

    stages_str = "\n".join(rows_markup)

    # Progression ribbon
    prog_ribbon = " &#160;──►&#160; ".join([f'<tspan fill="{st["col"]}" font-weight="700">{st["prog"]}</tspan>' for st in stages])

    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w:.0f} {h:.0f}" width="{w:.0f}" height="{h:.0f}" role="img" aria-label="Currently Engineering Focus Map">
  <title>Currently Engineering Focus Map</title>
  <desc>Structured engineering progression: BUILD -> ENGINEER -> SYSTEMIZE -> EXPLORE -> COLLABORATE</desc>

  <defs>
    <linearGradient id="focusBg" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="{theme['bg_start']}"/>
      <stop offset="100%" stop-color="{theme['bg_end']}"/>
    </linearGradient>
  </defs>

  <!-- Frame Background & Hairline Border -->
  <rect width="{w:.0f}" height="{h:.0f}" rx="10" fill="url(#focusBg)"/>
  <rect x="0.5" y="0.5" width="{w - 1:.1f}" height="{h - 1:.1f}" rx="9.5" fill="none" stroke="{theme['border']}" stroke-width="1"/>

  <!-- Top Progression Ribbon -->
  <rect x="0" y="0" width="{w:.0f}" height="36" rx="10" fill="{theme['label_bg']}"/>
  <rect x="0" y="26" width="{w:.0f}" height="10" fill="{theme['label_bg']}"/>
  <line x1="0" y1="36" x2="{w:.0f}" y2="36" stroke="{theme['border']}" stroke-width="1"/>

  <!-- Progression Label -->
  <text x="36" y="23" font-family="{FONT_MONO}" font-size="9" fill="{theme['text_muted']}" letter-spacing="1.5">TRAJECTORY:</text>
  <text x="130" y="23" font-family="{FONT_MONO}" font-size="9" letter-spacing="1.5">
    {prog_ribbon}
  </text>
  <text x="{w - 36:.1f}" y="23" font-family="{FONT_MONO}" font-size="9" fill="{theme['green']}" text-anchor="end" letter-spacing="1">STATUS: ACTIVE</text>

  <!-- Vertical Timeline Guide Line on Left -->
  <line x1="104" y1="74" x2="104" y2="218" stroke="{theme['border']}" stroke-width="1" stroke-dasharray="2 3" opacity="0.5"/>

  <!-- 5 Engineering Focus Stages -->
{stages_str}

  <!-- Divider Above Center Statement -->
  <line x1="36" y1="262" x2="{w - 36:.1f}" y2="262" stroke="{theme['border']}" stroke-width="1"/>
  <circle cx="{w / 2.0:.1f}" cy="262" r="2.5" fill="{theme['accent']}"/>

  <!-- Distinctive Center Statement -->
  <text x="{w / 2.0:.1f}" y="286" font-family="{FONT_MONO}" font-size="11" font-weight="700"
    fill="{theme['accent']}" text-anchor="middle" letter-spacing="2.5">
    MODELS &#160;→&#160; AGENTS &#160;→&#160; DATA &#160;→&#160; SYSTEMS &#160;→&#160; DEPLOYMENT
  </text>

  <text x="{w / 2.0:.1f}" y="308" font-family="{FONT_SANS}" font-size="11.5" font-style="italic"
    fill="{theme['text_dim']}" text-anchor="middle" letter-spacing="0.2">
    Building intelligent software that can reason, use tools, process evidence, and operate as reliable systems.
  </text>
</svg>"""

    return svg


def main():
    # 1. Selected Recognition
    recog_anim   = os.path.join(SECTIONS_DIR, "selected-recognition.svg")
    recog_static = os.path.join(SECTIONS_DIR, "selected-recognition-static.svg")
    recog_light  = os.path.join(SECTIONS_DIR, "selected-recognition-light.svg")

    print("Generating selected-recognition SVGs...")
    with open(recog_anim, "w", encoding="utf-8") as f:
        f.write(build_recognition_svg(DARK_THEME, animated=True))
    with open(recog_static, "w", encoding="utf-8") as f:
        f.write(build_recognition_svg(DARK_THEME, animated=False))
    with open(recog_light, "w", encoding="utf-8") as f:
        f.write(build_recognition_svg(LIGHT_THEME, animated=False))

    # 2. Currently Engineering
    curr_anim   = os.path.join(SECTIONS_DIR, "currently-engineering.svg")
    curr_static = os.path.join(SECTIONS_DIR, "currently-engineering-static.svg")
    curr_light  = os.path.join(SECTIONS_DIR, "currently-engineering-light.svg")

    print("Generating currently-engineering SVGs...")
    with open(curr_anim, "w", encoding="utf-8") as f:
        f.write(build_currently_engineering_svg(DARK_THEME, animated=True))
    with open(curr_static, "w", encoding="utf-8") as f:
        f.write(build_currently_engineering_svg(DARK_THEME, animated=False))
    with open(curr_light, "w", encoding="utf-8") as f:
        f.write(build_currently_engineering_svg(LIGHT_THEME, animated=False))

    # Validate XML
    all_files = [recog_anim, recog_static, recog_light, curr_anim, curr_static, curr_light]
    for p in all_files:
        ET.parse(p)
        print(f"  [PASS] Valid XML: {os.path.basename(p)} ({os.path.getsize(p)/1024:.1f} KB)")

    print("\nAll recognition and engineering focus map SVGs generated successfully.")


if __name__ == "__main__":
    main()
