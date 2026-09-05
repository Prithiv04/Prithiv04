#!/usr/bin/env python3
"""
validate_svg.py
Validates the generated activity SVGs for XML well-formedness, correct dimensions,
and essential tags.
"""

import os
import sys
import xml.etree.ElementTree as ET

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(SCRIPT_DIR, "..", ".."))
ASSETS_DIR = os.path.join(PROJECT_ROOT, "assets", "github")

SVGS = [
    "activity.svg",
    "activity-static.svg",
    "activity-light.svg",
]


def validate_file(filename: str) -> bool:
    filepath = os.path.join(ASSETS_DIR, filename)
    if not os.path.exists(filepath):
        print(f" [FAIL] File not found: {filepath}")
        return False

    size_bytes = os.path.getsize(filepath)
    if size_bytes == 0:
        print(f" [FAIL] File is empty: {filename}")
        return False

    try:
        tree = ET.parse(filepath)
        root = tree.getroot()

        # Check tag
        if not root.tag.endswith("svg"):
            print(f" [FAIL] Root tag is not <svg>: {root.tag}")
            return False

        # Check width/height or viewBox
        viewbox = root.attrib.get("viewBox", "")
        if not viewbox and not ("width" in root.attrib and "height" in root.attrib):
            print(f" [FAIL] Missing viewBox or width/height in {filename}")
            return False

        print(f" [PASS] {filename:<25} ({size_bytes / 1024:.1f} KB) - Valid XML, viewBox='{viewbox}'")
        return True
    except ET.ParseError as e:
        print(f" [FAIL] XML parse error in {filename}: {e}")
        return False
    except Exception as e:
        print(f" [FAIL] Unexpected error in {filename}: {e}")
        return False


def main():
    print("Validating generated GitHub Activity SVGs...")
    all_pass = True
    for svg in SVGS:
        if not validate_file(svg):
            all_pass = False

    if all_pass:
        print(" All GitHub Activity SVGs are valid.")
        return 0
    else:
        print(" Some SVGs failed validation.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
