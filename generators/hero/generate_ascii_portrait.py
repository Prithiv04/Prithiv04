"""
generate_ascii_portrait.py
--------------------------
Converts hhgoa.jpeg -> ASCII art portrait -> self-contained SVGs:
  - assets/hero/ascii-portrait.svg        (animated, dark mode)
  - assets/hero/ascii-portrait-static.svg (static, dark mode)
  - assets/hero/ascii-portrait-light.svg  (static, light mode)

Complies with all specifications in ASCII.md:
  - Preserves Prithiv's facial likeness, curly hair, glasses, jawline, and silhouette.
  - Character density: dense chars for hair/dark areas, sparse for highlights, clean spaces for background.
  - Clean terminal frame matching the AI Engineering Command Center identity.
  - Smooth, professional top-to-bottom reveal with scanline and blinking cursor.
  - 100% static-first compatibility: fully visible if SMIL animation is disabled.
  - Valid XML, no external dependencies, no JS, file size < 150 KB.
"""

import os
import html
import xml.etree.ElementTree as ET
from PIL import Image, ImageEnhance
import numpy as np

# ─── File Paths ───────────────────────────────────────────────────────────────
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT  = os.path.abspath(os.path.join(SCRIPT_DIR, "..", ".."))
SRC_IMAGE  = os.path.join(REPO_ROOT, "hhgoa.jpeg")
HERO_DIR   = os.path.join(REPO_ROOT, "assets", "hero")
os.makedirs(HERO_DIR, exist_ok=True)

# ─── Grid & Geometry ──────────────────────────────────────────────────────────
COLS        = 118      # Character columns
CHAR_ASPECT = 0.50     # Monospace character aspect ratio (width / height)
SVG_W       = 768.0    # SVG viewBox width
PADDING_X   = 22.0     # Left & right padding
CONTENT_W   = SVG_W - (PADDING_X * 2.0)  # 724.0px textLength
ROW_H       = 11.5     # Height per line of text
FONT_SIZE   = 9.8      # Monospace font size
TOP_BAR_H   = 38.0     # Terminal header bar height
BOT_BAR_H   = 34.0     # Terminal footer bar height
PAD_TOP     = 16.0     # Spacing between top bar and first text line
PAD_BOT     = 14.0     # Spacing between last text line and bottom bar

# ─── Color Themes ─────────────────────────────────────────────────────────────
DARK_THEME = {
    "bg_start": "#111722",
    "bg_end":   "#0d1117",
    "border":   "#30363d",
    "header_bg": "#161b22",
    "text":     "#c9d1d9",
    "dim":      "#7d8590",
    "accent":   "#58a6ff",
    "green":    "#3fb950",
    "red":      "#ff5f56",
    "yellow":   "#ffbd2e",
}

LIGHT_THEME = {
    "bg_start": "#ffffff",
    "bg_end":   "#f6f8fa",
    "border":   "#d0d7de",
    "header_bg": "#ebeef2",
    "text":     "#24292f",
    "dim":      "#57606a",
    "accent":   "#0969da",
    "green":    "#1a7f37",
    "red":      "#cf222e",
    "yellow":   "#9a6700",
}

FONT_STACK = "ui-monospace, SFMono-Regular, Menlo, Consolas, 'Liberation Mono', monospace"

# Character ramp from sparse/light to dense/dark
# Index 0 is space ' ' for background/clean areas
RAMP = "   ..::--==++**##%%@@@@"


def generate_ascii_lines(image_path: str, cols: int) -> list[str]:
    """
    Process hhgoa.jpeg and return list of ASCII character strings.
    """
    img = Image.open(image_path).convert("RGB")
    w, h = img.size

    # Crop to head and shoulders
    crop_x1 = int(w * 0.12)
    crop_y1 = int(h * 0.02)
    crop_x2 = int(w * 0.88)
    crop_y2 = int(h * 0.84)
    crop = img.crop((crop_x1, crop_y1, crop_x2, crop_y2))
    cw, ch = crop.size

    # Compute target rows preserving aspect ratio
    rows = int(ch / (cw / cols / CHAR_ASPECT))

    # Grayscale and detail enhancement
    gray = crop.convert("L")
    enhanced = ImageEnhance.Contrast(gray).enhance(1.52)
    enhanced = ImageEnhance.Sharpness(enhanced).enhance(1.60)

    # Resize to character grid
    small = enhanced.resize((cols, rows), Image.Resampling.LANCZOS)
    arr = np.array(small, dtype=float)

    # Clean background wall reflections
    for y in range(rows):
        for x in range(cols):
            # Left studio wall suppression
            if x < cols * 0.32 and y < rows * 0.62:
                if arr[y, x] < 55:
                    arr[y, x] = 0
            # Right studio wall suppression
            elif x > cols * 0.72 and y < rows * 0.55:
                if arr[y, x] < 45:
                    arr[y, x] = 0
            elif arr[y, x] < 24:
                arr[y, x] = 0

    ramp_len = len(RAMP)
    lines = []
    for y in range(rows):
        chars = []
        for x in range(cols):
            val = min(255.0, max(0.0, arr[y, x]))
            idx = int(val / 256.0 * ramp_len)
            idx = min(ramp_len - 1, max(0, idx))
            chars.append(RAMP[idx])
        lines.append("".join(chars))

    return lines


def build_svg_document(lines: list[str], theme: dict, animated: bool = True) -> str:
    """
    Construct a clean, valid XML SVG string representing the terminal ASCII portrait.
    """
    num_rows = len(lines)
    content_h = num_rows * ROW_H
    portrait_start_y = TOP_BAR_H + PAD_TOP
    footer_y = portrait_start_y + content_h + PAD_BOT
    svg_h = footer_y + BOT_BAR_H

    # XML Defs: gradient and row reveal clip paths
    clip_defs = []
    text_elements = []

    for i, line in enumerate(lines):
        y_pos = portrait_start_y + (i * ROW_H)
        text_y = y_pos + (ROW_H * 0.78)
        escaped_text = html.escape(line)

        if animated:
            clip_id = f"r{i}"
            begin_sec = 0.15 + (i * 0.022)  # smooth staggered reveal
            clip_defs.append(
                f'    <clipPath id="{clip_id}">\n'
                f'      <rect x="{PADDING_X:.1f}" y="{y_pos:.1f}" width="{CONTENT_W:.1f}" height="{ROW_H:.1f}">\n'
                f'        <animate attributeName="width" from="0" to="{CONTENT_W:.1f}" begin="{begin_sec:.3f}s" dur="0.10s" fill="freeze"/>\n'
                f'      </rect>\n'
                f'    </clipPath>'
            )
            text_elements.append(
                f'  <g clip-path="url(#{clip_id})">\n'
                f'    <text xml:space="preserve" x="{PADDING_X:.1f}" y="{text_y:.1f}" '
                f'fill="{theme["text"]}" font-size="{FONT_SIZE:.1f}" '
                f'textLength="{CONTENT_W:.1f}" lengthAdjust="spacing">{escaped_text}</text>\n'
                f'  </g>'
            )
        else:
            text_elements.append(
                f'  <text xml:space="preserve" x="{PADDING_X:.1f}" y="{text_y:.1f}" '
                f'fill="{theme["text"]}" font-size="{FONT_SIZE:.1f}" '
                f'textLength="{CONTENT_W:.1f}" lengthAdjust="spacing">{escaped_text}</text>'
            )

    clip_defs_str = "\n".join(clip_defs)
    text_content_str = "\n".join(text_elements)

    # Optional dynamic scanline and cursor for animated mode
    scanline_str = ""
    cursor_str = ""
    status_dot_str = f'<circle cx="32" cy="{footer_y + (BOT_BAR_H / 2.0):.1f}" r="4" fill="{theme["green"]}"/>'

    if animated:
        total_anim_dur = 0.15 + (num_rows * 0.022) + 0.10
        scanline_str = (
            f'  <!-- Scanline Reveal -->\n'
            f'  <line x1="{PADDING_X:.1f}" y1="{portrait_start_y:.1f}" x2="{SVG_W - PADDING_X:.1f}" y2="{portrait_start_y:.1f}" '
            f'stroke="{theme["accent"]}" stroke-width="1.5" opacity="0">\n'
            f'    <animate attributeName="y1" from="{portrait_start_y:.1f}" to="{portrait_start_y + content_h:.1f}" '
            f'begin="0.15s" dur="{total_anim_dur:.2f}s" fill="freeze"/>\n'
            f'    <animate attributeName="y2" from="{portrait_start_y:.1f}" to="{portrait_start_y + content_h:.1f}" '
            f'begin="0.15s" dur="{total_anim_dur:.2f}s" fill="freeze"/>\n'
            f'    <animate attributeName="opacity" values="0;0.65;0.65;0" keyTimes="0;0.05;0.95;1" '
            f'begin="0.15s" dur="{total_anim_dur:.2f}s" fill="freeze"/>\n'
            f'  </line>'
        )

        cursor_begin = total_anim_dur + 0.1
        cursor_str = (
            f'  <!-- Blinking Terminal Cursor -->\n'
            f'  <rect x="238" y="{footer_y + 11:.1f}" width="6" height="11" fill="{theme["accent"]}">\n'
            f'    <animate attributeName="opacity" values="1;1;0;0;1" dur="1.1s" begin="{cursor_begin:.2f}s" repeatCount="indefinite"/>\n'
            f'  </rect>'
        )

        status_dot_str = (
            f'  <circle cx="32" cy="{footer_y + (BOT_BAR_H / 2.0):.1f}" r="4" fill="{theme["green"]}">\n'
            f'    <animate attributeName="opacity" values="1;0.4;1" dur="2.2s" begin="{cursor_begin:.2f}s" repeatCount="indefinite"/>\n'
            f'  </circle>'
        )

    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" width="{SVG_W:.0f}" height="{svg_h:.0f}" viewBox="0 0 {SVG_W:.0f} {svg_h:.0f}" font-family="{FONT_STACK}" role="img" aria-label="Prithiv — ASCII portrait and AI engineering system identity">
  <title>Prithiv — ASCII portrait and AI engineering system identity</title>
  <desc>Personal ASCII portrait of Prithiv generated from hhgoa.jpeg inside the AI Engineering System terminal frame</desc>

  <defs>
    <linearGradient id="bgGrad" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="{theme['bg_start']}"/>
      <stop offset="100%" stop-color="{theme['bg_end']}"/>
    </linearGradient>
{clip_defs_str}
  </defs>

  <!-- Frame Background & Border -->
  <rect width="{SVG_W:.0f}" height="{svg_h:.0f}" rx="10" fill="url(#bgGrad)"/>
  <rect x="0.5" y="0.5" width="{SVG_W - 1:.1f}" height="{svg_h - 1:.1f}" rx="9.5" fill="none" stroke="{theme['border']}" stroke-width="1"/>

  <!-- Terminal Title Bar -->
  <rect x="0" y="0" width="{SVG_W:.0f}" height="{TOP_BAR_H:.0f}" rx="10" fill="{theme['header_bg']}"/>
  <rect x="0" y="{TOP_BAR_H - 10:.0f}" width="{SVG_W:.0f}" height="10" fill="{theme['header_bg']}"/>
  <line x1="0" y1="{TOP_BAR_H:.0f}" x2="{SVG_W:.0f}" y2="{TOP_BAR_H:.0f}" stroke="{theme['border']}" stroke-width="1"/>

  <!-- Window Dots -->
  <circle cx="24" cy="19" r="5" fill="{theme['red']}"/>
  <circle cx="40" cy="19" r="5" fill="{theme['yellow']}"/>
  <circle cx="56" cy="19" r="5" fill="{theme['green']}"/>

  <!-- Header Labels -->
  <text x="{SVG_W / 2.0:.1f}" y="23" fill="{theme['dim']}" font-size="11" text-anchor="middle" letter-spacing="2">PRITHIV // AI ENGINEERING SYSTEM</text>
  <text x="{SVG_W - 24:.1f}" y="23" fill="{theme['accent']}" font-size="10" text-anchor="end">portrait.exe</text>

  <!-- ASCII Portrait Content -->
{text_content_str}

{scanline_str}

  <!-- Footer Status Bar -->
  <line x1="0" y1="{footer_y:.1f}" x2="{SVG_W:.0f}" y2="{footer_y:.1f}" stroke="{theme['border']}" stroke-width="1"/>

  {status_dot_str}
  <text x="44" y="{footer_y + 21:.1f}" fill="{theme['text']}" font-size="10.5" letter-spacing="1">IDENTITY: <tspan fill="{theme['green']}">PRITHIV</tspan> · AI/ML SYSTEMS</text>
  {cursor_str}

  <text x="{SVG_W - 24:.1f}" y="{footer_y + 21:.1f}" fill="{theme['dim']}" font-size="10" text-anchor="end">
    Chennai, India · STATUS: <tspan fill="{theme['green']}">ONLINE</tspan>
  </text>
</svg>"""

    return svg


def main():
    print(f"Loading source image: {SRC_IMAGE}")
    lines = generate_ascii_lines(SRC_IMAGE, COLS)
    print(f"Generated ASCII grid: {len(lines)} rows x {len(lines[0])} columns")

    # Output paths
    out_animated = os.path.join(HERO_DIR, "ascii-portrait.svg")
    out_static   = os.path.join(HERO_DIR, "ascii-portrait-static.svg")
    out_light    = os.path.join(HERO_DIR, "ascii-portrait-light.svg")

    # 1. Animated SVG (Dark Mode)
    print("Writing animated SVG...")
    svg_anim = build_svg_document(lines, DARK_THEME, animated=True)
    with open(out_animated, "w", encoding="utf-8") as f:
        f.write(svg_anim)
    size_anim_kb = os.path.getsize(out_animated) / 1024
    print(f"  -> {out_animated} ({size_anim_kb:.1f} KB)")

    # 2. Static SVG (Dark Mode)
    print("Writing static dark SVG...")
    svg_static = build_svg_document(lines, DARK_THEME, animated=False)
    with open(out_static, "w", encoding="utf-8") as f:
        f.write(svg_static)
    size_static_kb = os.path.getsize(out_static) / 1024
    print(f"  -> {out_static} ({size_static_kb:.1f} KB)")

    # 3. Static SVG (Light Mode)
    print("Writing static light SVG...")
    svg_light = build_svg_document(lines, LIGHT_THEME, animated=False)
    with open(out_light, "w", encoding="utf-8") as f:
        f.write(svg_light)
    size_light_kb = os.path.getsize(out_light) / 1024
    print(f"  -> {out_light} ({size_light_kb:.1f} KB)")

    # Validation
    for p in [out_animated, out_static, out_light]:
        ET.parse(p)
        print(f"  [PASS] Valid XML: {os.path.basename(p)}")

    print("\nAll ASCII portrait SVGs generated and validated successfully.")


if __name__ == "__main__":
    main()
