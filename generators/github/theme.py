#!/usr/bin/env python3
"""
theme.py
Design tokens and color palettes for the Engineering Activity Visualizer SVG.
Follows the AI Engineering design system established in PRITHIV / IDENTITY.SYS.
"""

FONT_MONO = "ui-monospace, SFMono-Regular, 'SF Mono', Menlo, Consolas, 'Liberation Mono', monospace"
FONT_SANS = "-apple-system, BlinkMacSystemFont, 'Segoe UI', Inter, Roboto, Helvetica, Arial, sans-serif"

DARK_THEME = {
    "name": "dark",
    "bg_start": "#0d1117",
    "bg_end": "#161b22",
    "card_bg": "#161b22",
    "border": "#30363d",
    "border_subtle": "#21262d",
    "text_hero": "#f0f6fc",
    "text_body": "#c9d1d9",
    "text_secondary": "#8b949e",
    "text_muted": "#57606a",
    "accent": "#58a6ff",
    "cyan": "#39c5cf",
    "glow": "rgba(57, 197, 207, 0.4)",
    # Contribution intensity mapping (0 to 4)
    # Using technical blue/cyan gradient rather than standard green
    "levels": {
        0: {"fill": "#161b22", "stroke": "#21262d", "opacity": "0.6"},
        1: {"fill": "#1b3858", "stroke": "#234b76", "opacity": "0.85"},
        2: {"fill": "#1f568d", "stroke": "#286db3", "opacity": "0.95"},
        3: {"fill": "#2d7cd1", "stroke": "#388bfd", "opacity": "1.0"},
        4: {"fill": "#39c5cf", "stroke": "#58a6ff", "opacity": "1.0"},
    },
    "pipeline": {
        "active_bg": "#1f3a5f",
        "active_border": "#58a6ff",
        "active_text": "#58a6ff",
        "inactive_bg": "#161b22",
        "inactive_border": "#30363d",
        "inactive_text": "#8b949e",
        "arrow": "#39c5cf",
    }
}

LIGHT_THEME = {
    "name": "light",
    "bg_start": "#ffffff",
    "bg_end": "#f6f8fa",
    "card_bg": "#f6f8fa",
    "border": "#d0d7de",
    "border_subtle": "#e1e4e8",
    "text_hero": "#1f2328",
    "text_body": "#24292f",
    "text_secondary": "#57606a",
    "text_muted": "#8c959f",
    "accent": "#0969da",
    "cyan": "#0550ae",
    "glow": "rgba(9, 105, 218, 0.3)",
    "levels": {
        0: {"fill": "#ebedf0", "stroke": "#d0d7de", "opacity": "0.8"},
        1: {"fill": "#bae6fd", "stroke": "#7dd3fc", "opacity": "0.9"},
        2: {"fill": "#60a5fa", "stroke": "#3b82f6", "opacity": "0.95"},
        3: {"fill": "#2563eb", "stroke": "#1d4ed8", "opacity": "1.0"},
        4: {"fill": "#0284c7", "stroke": "#0369a1", "opacity": "1.0"},
    },
    "pipeline": {
        "active_bg": "#ddf4ff",
        "active_border": "#0969da",
        "active_text": "#0969da",
        "inactive_bg": "#f6f8fa",
        "inactive_border": "#d0d7de",
        "inactive_text": "#57606a",
        "arrow": "#0969da",
    }
}
