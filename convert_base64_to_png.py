#!/usr/bin/env python3
"""
Convert Base64 TXT files to PNG images
Converts all .txt files in the test folder that contain base64 encoded PNG data
"""

import os
import base64
from pathlib import Path


def convert_base64_to_png(txt_file_path, output_dir):
    """Convert a base64 txt file to PNG image."""
    try:
        # Read the base64 string from file
        with open(txt_file_path, 'r') as f:
            base64_string = f.read().strip()
        
        # Decode base64 to binary data
        image_data = base64.b64decode(base64_string)
        
        # Create output filename (same name but .png extension)
        txt_filename = os.path.basename(txt_file_path)
        png_filename = os.path.splitext(txt_filename)[0] + '.png'
        output_path = os.path.join(output_dir, png_filename)
        
        # Write binary data to PNG file
        with open(output_path, 'wb') as f:
            f.write(image_data)
        
        print(f"✓ Converted: {txt_filename} -> {png_filename}")
        return True
        
    except Exception as e:
        print(f"✗ Error converting {txt_file_path}: {e}")
        return False


def main():
    """Main function to convert all base64 txt files in test folder."""
    # Get script directory and test folder path
    script_dir = Path(__file__).parent
    test_dir = script_dir / "test"
    
    if not test_dir.exists():
        print(f"✗ Test directory does not exist: {test_dir}")
        return
    
    print(f"Converting base64 txt files in: {test_dir}\n")
    
    # Find all .txt files in test directory
    txt_files = list(test_dir.glob("*.txt"))
    
    if not txt_files:
        print("No .txt files found in test directory")
        return
    
    print(f"Found {len(txt_files)} txt file(s)\n")
    
    # Convert each txt file
    converted_count = 0
    for txt_file in txt_files:
        if convert_base64_to_png(txt_file, test_dir):
            converted_count += 1
    
    # Summary
    print(f"\n{'='*60}")
    print(f"Summary: {converted_count}/{len(txt_files)} files converted successfully")
    print(f"{'='*60}")


if __name__ == "__main__":
    main()
