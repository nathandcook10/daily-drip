#!/usr/bin/env python3
import os
import math
from PIL import Image, ImageChops, ImageFilter, ImageOps

flats_dir = "/Users/nathan/Daily Drip/public/assets/flats"
output_dir = "/Users/nathan/Daily Drip/Core Art/extracted"
os.makedirs(output_dir, exist_ok=True)

def key_out_dark_fabric(img, threshold_low=45, threshold_high=80):
    """
    Keys out dark fabric (black/charcoal/olive) from an image, making it transparent.
    Keeps bright colors and white/green/red print elements.
    """
    img = img.convert("RGBA")
    data = img.getdata()
    new_data = []
    
    for item in data:
        r, g, b, a = item
        # Calculate maximum color channel value
        max_val = max(r, g, b)
        
        if max_val < threshold_low:
            # Completely dark fabric -> transparent
            new_data.append((0, 0, 0, 0))
        elif max_val > threshold_high:
            # Bright print -> fully opaque
            new_data.append(item)
        else:
            # Smooth transition for anti-aliasing
            ratio = (max_val - threshold_low) / (threshold_high - threshold_low)
            alpha = int(255 * ratio)
            new_data.append((r, g, b, alpha))
            
    img.putdata(new_data)
    return img

def key_out_light_fabric(img, threshold_low=180, threshold_high=220):
    """
    Keys out light fabric (white/cream) from an image, making it transparent.
    Keeps dark text and typography.
    """
    img = img.convert("RGBA")
    data = img.getdata()
    new_data = []
    
    for item in data:
        r, g, b, a = item
        # Calculate minimum color channel value (low min_val means dark print, high means light background)
        min_val = min(r, g, b)
        
        if min_val > threshold_high:
            # Pure white/cream background -> transparent
            new_data.append((0, 0, 0, 0))
        elif min_val < threshold_low:
            # Dark print text -> fully opaque
            new_data.append(item)
        else:
            # Smooth transition for anti-aliasing
            ratio = (threshold_high - min_val) / (threshold_high - threshold_low)
            alpha = int(255 * ratio)
            new_data.append((r, g, b, alpha))
            
    img.putdata(new_data)
    return img

def extract_monkey_front(img_path, out_path):
    """
    Punch the Monkey front is a photo print block. We crop it precisely.
    """
    img = Image.open(img_path)
    w, h = img.size
    crop_box = (int(w * 0.25), int(h * 0.22), int(w * 0.75), int(h * 0.65))
    cropped = img.crop(crop_box)
    
    # Mild edge cleanup
    cropped = cropped.convert("RGBA")
    data = cropped.getdata()
    new_data = []
    for item in data:
        r, g, b, a = item
        # Key out near-black borders from photo block
        if r < 18 and g < 18 and b < 18:
            new_data.append((0, 0, 0, 0))
        else:
            new_data.append(item)
    cropped.putdata(new_data)
    cropped.save(out_path, "PNG")
    print(f"✅ Extracted Monkey Front -> {out_path}")

def extract_peace_front(img_path, out_path):
    """
    Peace Sign front is white hand-drawn artwork on a black T-shirt.
    We isolate ONLY the white drawing and discard all black fabric and white background.
    """
    img = Image.open(img_path)
    w, h = img.size
    # Tighter crop box centered on the peace sign to avoid any outer white background
    crop_box = (int(w * 0.28), int(h * 0.20), int(w * 0.72), int(h * 0.64))
    cropped = img.crop(crop_box).convert("RGBA")
    
    data = cropped.getdata()
    new_data = []
    for item in data:
        r, g, b, a = item
        brightness = sum((r, g, b)) // 3
        
        if brightness < 55:
            # Black T-shirt fabric -> fully transparent
            new_data.append((0, 0, 0, 0))
        elif brightness > 160:
            # White peace sign print -> pure white opaque
            new_data.append((255, 255, 255, 255))
        else:
            # Soft anti-aliased edge blending
            ratio = (brightness - 55) / 105
            alpha = int(255 * ratio)
            new_data.append((255, 255, 255, alpha))
            
    cropped.putdata(new_data)
    cropped.save(out_path, "PNG")
    print(f"✅ Extracted Peace Front -> {out_path}")

def extract_robot_front(img_path, out_path):
    """
    Outperformed by a Robot has green, white, and red graphic elements on a black T-shirt.
    We isolate ONLY the print, keying out the black fabric.
    """
    img = Image.open(img_path)
    w, h = img.size
    crop_box = (int(w * 0.23), int(h * 0.18), int(w * 0.77), int(h * 0.62))
    cropped = img.crop(crop_box)
    
    # Key out black fabric, keeping colors and whites
    cleaned = key_out_dark_fabric(cropped, threshold_low=48, threshold_high=85)
    cleaned.save(out_path, "PNG")
    print(f"✅ Extracted Robot Front -> {out_path}")

def extract_sage_front(img_path, out_path):
    """
    Sage Archives is dark-green/black minimal typography on a cream T-shirt.
    We key out the cream fabric.
    """
    img = Image.open(img_path)
    w, h = img.size
    crop_box = (int(w * 0.25), int(h * 0.20), int(w * 0.75), int(h * 0.70))
    cropped = img.crop(crop_box)
    
    cleaned = key_out_light_fabric(cropped, threshold_low=170, threshold_high=215)
    cleaned.save(out_path, "PNG")
    print(f"✅ Extracted Sage Front -> {out_path}")

def extract_binary_front(img_path, out_path):
    """
    Binary Genesis is green matrix code on a black T-shirt.
    Key out the black fabric.
    """
    img = Image.open(img_path)
    w, h = img.size
    crop_box = (int(w * 0.22), int(h * 0.18), int(w * 0.78), int(h * 0.72))
    cropped = img.crop(crop_box)
    
    cleaned = key_out_dark_fabric(cropped, threshold_low=40, threshold_high=75)
    cleaned.save(out_path, "PNG")
    print(f"✅ Extracted Binary Front -> {out_path}")

def extract_vapor_front(img_path, out_path):
    """
    Vaporwave Paradox is bright pink/cyan graphics on a charcoal T-shirt.
    Key out the charcoal fabric.
    """
    img = Image.open(img_path)
    w, h = img.size
    crop_box = (int(w * 0.22), int(h * 0.20), int(w * 0.78), int(h * 0.70))
    cropped = img.crop(crop_box)
    
    cleaned = key_out_dark_fabric(cropped, threshold_low=52, threshold_high=95)
    cleaned.save(out_path, "PNG")
    print(f"✅ Extracted Vapor Front -> {out_path}")

def extract_neural_front(img_path, out_path):
    """
    Neural Echoes is white synapse wireframe on a dark-olive T-shirt.
    Key out the dark olive.
    """
    img = Image.open(img_path)
    w, h = img.size
    crop_box = (int(w * 0.25), int(h * 0.20), int(w * 0.75), int(h * 0.68))
    cropped = img.crop(crop_box)
    
    # Olive fabric is around (60,60,45), so we key out dark and keep white lineart
    cleaned = key_out_dark_fabric(cropped, threshold_low=75, threshold_high=130)
    cleaned.save(out_path, "PNG")
    print(f"✅ Extracted Neural Front -> {out_path}")

def extract_pixel_front(img_path, out_path):
    """
    Pixelated Soul is a colorful portrait on a white T-shirt.
    Key out the white fabric.
    """
    img = Image.open(img_path)
    w, h = img.size
    crop_box = (int(w * 0.22), int(h * 0.16), int(w * 0.78), int(h * 0.68))
    cropped = img.crop(crop_box)
    
    cleaned = key_out_light_fabric(cropped, threshold_low=180, threshold_high=220)
    cleaned.save(out_path, "PNG")
    print(f"✅ Extracted Pixel Front -> {out_path}")

def extract_clean_back(img_path, out_path, shirt_color):
    """
    Isolates back neckline logos/typography based on shirt base color.
    """
    img = Image.open(img_path)
    w, h = img.size
    crop_box = (int(w * 0.30), int(h * 0.12), int(w * 0.70), int(h * 0.35))
    cropped = img.crop(crop_box)
    
    if shirt_color in ["black", "charcoal", "olive"]:
        cleaned = key_out_dark_fabric(cropped, threshold_low=45, threshold_high=85)
    else:  # white/cream
        cleaned = key_out_light_fabric(cropped, threshold_low=170, threshold_high=215)
        
    cleaned.save(out_path, "PNG")
    print(f"✅ Extracted Back Graphic -> {out_path}")

def main():
    print("🚀 Running Flat-lay Print Extraction...")
    
    # Front extractions
    extract_monkey_front(os.path.join(flats_dir, "flat_monkey_front.png"), os.path.join(output_dir, "monkey_front.png"))
    extract_peace_front(os.path.join(flats_dir, "flat_peace_front.png"), os.path.join(output_dir, "peace_front.png"))
    extract_robot_front(os.path.join(flats_dir, "flat_robot_front.png"), os.path.join(output_dir, "robot_front.png"))
    extract_sage_front(os.path.join(flats_dir, "flat_sage_front.png"), os.path.join(output_dir, "sage_front.png"))
    extract_binary_front(os.path.join(flats_dir, "flat_binary_front.png"), os.path.join(output_dir, "binary_front.png"))
    extract_vapor_front(os.path.join(flats_dir, "flat_vapor_front.png"), os.path.join(output_dir, "vapor_front.png"))
    extract_neural_front(os.path.join(flats_dir, "flat_neural_front.png"), os.path.join(output_dir, "neural_front.png"))
    extract_pixel_front(os.path.join(flats_dir, "flat_pixel_front.png"), os.path.join(output_dir, "pixel_front.png"))
    
    # Back extractions
    extract_clean_back(os.path.join(flats_dir, "flat_robot_back.png"), os.path.join(output_dir, "robot_back.png"), "black")
    extract_clean_back(os.path.join(flats_dir, "flat_monkey_back.png"), os.path.join(output_dir, "monkey_back.png"), "black")
    extract_clean_back(os.path.join(flats_dir, "flat_peace_back.png"), os.path.join(output_dir, "peace_back.png"), "black")
    extract_clean_back(os.path.join(flats_dir, "flat_sage_back.png"), os.path.join(output_dir, "sage_back.png"), "cream")
    extract_clean_back(os.path.join(flats_dir, "flat_binary_back.png"), os.path.join(output_dir, "binary_back.png"), "black")
    extract_clean_back(os.path.join(flats_dir, "flat_vapor_back.png"), os.path.join(output_dir, "vapor_back.png"), "charcoal")
    extract_clean_back(os.path.join(flats_dir, "flat_neural_back.png"), os.path.join(output_dir, "neural_back.png"), "olive")
    extract_clean_back(os.path.join(flats_dir, "flat_pixel_back.png"), os.path.join(output_dir, "pixel_back.png"), "white")
    
    print("🎉 All 16 graphic elements extracted with pristine transparency!")

if __name__ == "__main__":
    main()
