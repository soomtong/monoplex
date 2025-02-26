#!/usr/bin/env python3
import sys
import fontforge

def change_font_family_name(input_font, output_font, new_family_name):
    """
    Change the font family name of a font file.
    
    Args:
        input_font (str): Path to the input font file
        output_font (str): Path to save the modified font
        new_family_name (str): New family name for the font
    """
    try:
        # Open the font
        font = fontforge.open(input_font)
        
        # Get the current font information
        old_family_name = font.familyname
        print(f"Current font family name: {old_family_name}")
        
        # Change the family name
        font.familyname = new_family_name
        
        # Update related font names to maintain consistency
        if font.fontname:
            font.fontname = font.fontname.replace(old_family_name, new_family_name).replace(" ", "")
        
        if font.fullname:
            font.fullname = font.fullname.replace(old_family_name, new_family_name)
        
        # Update PostScript names if they exist
        for name_id in (1, 2, 3, 4, 6, 16, 17, 18, 20, 21, 22):
            try:
                if font.sfnt_names:
                    for index, (lang, string_type, string_value) in enumerate(font.sfnt_names):
                        if string_type == name_id:
                            new_value = string_value.replace(old_family_name, new_family_name)
                            font.sfnt_names = (font.sfnt_names[:index] + 
                                              ((lang, string_type, new_value),) + 
                                              font.sfnt_names[index+1:])
            except:
                pass
        
        # Save the modified font
        print(f"Saving font with new family name: {new_family_name}")
        font.generate(output_font)
        font.close()
        print(f"Font saved successfully to: {output_font}")
        
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python change_font_family.py <input_font> <output_font> <new_family_name>")
        sys.exit(1)
    
    input_font = sys.argv[1]
    output_font = sys.argv[2]
    new_family_name = sys.argv[3]
    
    change_font_family_name(input_font, output_font, new_family_name)