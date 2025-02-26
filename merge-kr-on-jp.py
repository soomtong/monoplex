#!/usr/bin/env python3
"""
Font Merger - Merge Korean fonts into Japanese fonts

This script merges Korean fonts into Japanese fonts to create
composite fonts with both language support.
"""

import fontforge
import sys


def print_font_info(font, label="Font info"):
    """Print font information."""
    print(f"{label}:")
    print(f" - Font name: {font.fontname}")
    print(f" - Family name: {font.familyname}")
    print(f" - Full name: {font.fullname}")
    print(f" - Font name: {font.sfnt_names}")


def merge_font(base_font_path, korean_font_path, target_font_name,
              target_family_name, target_full_name, output_path):
    """Merge Korean font into Japanese font and set new names."""
    # Open base font
    font = fontforge.open(base_font_path)
    print_font_info(font, "Before changes")

    # Merge Korean font
    font.mergeFonts(korean_font_path)

    # Set new font names
    font.fontname = target_font_name
    font.familyname = target_family_name
    font.fullname = target_full_name

    # Set TTF name
    font.sfnt_names = tuple(name for name in font.sfnt_names
                          if name[1] != 'Family')
    font.appendSFNTName('English (US)', 'Preferred Family', target_family_name)
    # font.appendSFNTName(0x409, 16, target_family_name)

    print_font_info(font, "After changes")

    # Generate new font file
    font.generate(output_path)
    font.close()


def process_style(style, is_wide=False):
    """Process a specific font style."""
    # Set up the font family names
    if is_wide:
        family_name = "Monoplex Wide Nerd"
        safe_family_name = "MonoplexWideNerd"
        jp_base_dir = "build/PlemolJP35Console_NF"
        jp_base_prefix = "PlemolJP35ConsoleNF"
        kr_dir = "build/MonoplexKRWide"
        kr_prefix = "MonoplexKRWide"
    else:
        family_name = "Monoplex Nerd"
        safe_family_name = "MonoplexNerd"
        jp_base_dir = "build/PlemolJPConsole_NF"
        jp_base_prefix = "PlemolJPConsoleNF"
        kr_dir = "build/MonoplexKR"
        kr_prefix = "MonoplexKR"

    print(f"Merge {family_name} {style}...")

    # Define paths
    base_font_path = f"{jp_base_dir}/{jp_base_prefix}-{style}.ttf"
    korean_font_path = f"{kr_dir}/{kr_prefix}-{style}.ttf"
    output_path = f"build/{safe_family_name}-{style}.ttf"

    # Define naming
    target_font_name = f"{safe_family_name}-{style}"
    target_family_name = family_name
    target_full_name = f"{'Monoplex Wide Nerd' if is_wide else 'Monoplex Nerd'} Font {style}"

    # Merge fonts
    merge_font(
        base_font_path,
        korean_font_path,
        target_font_name,
        target_family_name,
        target_full_name,
        output_path
    )


def main():
    """Main function to merge fonts."""
    # List of all font styles
    styles = [
        "Bold", "SemiBold", "Medium", "Text", "Regular",
        "Light", "ExtraLight", "Thin",
        "BoldItalic", "SemiBoldItalic", "MediumItalic", "TextItalic",
        "Italic", "LightItalic", "ExtraLightItalic", "ThinItalic"
    ]

    # Process wide fonts
    print("Processing wide fonts...")
    for style in styles:
        process_style(style, is_wide=True)

    # Process regular fonts
    print("Processing regular fonts...")
    for style in styles:
        process_style(style, is_wide=False)

    print("All fonts processed successfully!")


if __name__ == "__main__":
    main()
