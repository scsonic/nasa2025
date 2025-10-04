#!/usr/bin/env python3
"""
Image Size Helper
Checks and resizes images in static/img directory:
- space.png, moon.png, mars.png, ship.png -> 1184x864
- item{X}.png -> 200x200
"""

import os
from PIL import Image
from pathlib import Path


def resize_image(image_path, target_size, description):
    """Resize an image to target size if needed."""
    try:
        with Image.open(image_path) as img:
            current_size = img.size
            
            if current_size == target_size:
                print(f"✓ {image_path.name} is already {target_size[0]}x{target_size[1]}")
                return False
            
            print(f"⚠ {image_path.name} is {current_size[0]}x{current_size[1]}, resizing to {target_size[0]}x{target_size[1]}...")
            
            # Resize image (using LANCZOS for high quality)
            resized_img = img.resize(target_size, Image.Resampling.LANCZOS)
            
            # Save the resized image
            resized_img.save(image_path)
            print(f"✓ {image_path.name} resized successfully!")
            return True
            
    except FileNotFoundError:
        print(f"✗ {image_path.name} not found, skipping...")
        return False
    except Exception as e:
        print(f"✗ Error processing {image_path.name}: {e}")
        return False


def main():
    """Main function to check and resize all images."""
    # Get the script directory and construct path to static/img
    script_dir = Path(__file__).parent
    img_dir = script_dir / "static" / "img"
    
    if not img_dir.exists():
        print(f"✗ Directory {img_dir} does not exist!")
        return
    
    print(f"Checking images in: {img_dir}\n")
    
    # Check and resize starter images (1184x864)
    print("=" * 60)
    print("Checking starter images (should be 1184x864):")
    print("=" * 60)
    
    starter_images = ["space.png", "moon.png", "mars.png", "ship.png"]
    target_size_starter = (1184, 864)
    
    resized_count = 0
    for img_name in starter_images:
        img_path = img_dir / img_name
        if resize_image(img_path, target_size_starter, "starter"):
            resized_count += 1
    
    print(f"\nStarter images: {resized_count} resized\n")
    
    # Check and resize item images (200x200)
    print("=" * 60)
    print("Checking item images (should be 200x200):")
    print("=" * 60)
    
    target_size_item = (200, 200)
    resized_count = 0
    found_count = 0
    
    # Check for item1.png to item20.png (or more if they exist)
    for i in range(1, 100):  # Check up to item99.png
        img_name = f"item{i}.png"
        img_path = img_dir / img_name
        
        if not img_path.exists():
            # Stop when we don't find consecutive items
            if i > 20:  # At least check first 20
                break
            continue
        
        found_count += 1
        if resize_image(img_path, target_size_item, "item"):
            resized_count += 1
    
    print(f"\nItem images: {found_count} found, {resized_count} resized\n")
    
    # Summary
    print("=" * 60)
    print("Summary:")
    print("=" * 60)
    print("✓ All images checked and resized as needed!")


if __name__ == "__main__":
    main()
