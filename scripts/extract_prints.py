import os
import math
from PIL import Image, ImageChops, ImageFilter, ImageOps

flats_dir = "/Users/nathan/Daily Drip/public/assets/flats"
output_dir = "/Users/nathan/Daily Drip/Core Art/extracted"
os.makedirs(output_dir, exist_ok=True)

def color_dist(c1, c2):
    return math.sqrt(sum((a - b) ** 2 for a, b in zip(c1[:3], c2[:3])))

def key_out_color(img, ref_color, threshold_low=30, threshold_high=70):
    """
    Keys out a specific background color from an image, making it transparent.
    """
    img = img.convert("RGBA")
    data = img.getdata()
    new_data = []
    
    for item in data:
        dist = color_dist(item, ref_color)
        if dist < threshold_low:
            new_data.append((0, 0, 0, 0))
        elif dist > threshold_high:
            new_data.append(item)
        else:
            # Interpolate alpha smoothly
            ratio = (dist - threshold_low) / (threshold_high - threshold_low)
            alpha = int(255 * ratio)
            new_data.append((item[0], item[1], item[2], alpha))
            
    img.putdata(new_data)
    return img

def extract_monkey_front(img_path, out_path):
    """
    Punch the Monkey front is a photo print block in the center of a black T-shirt.
    We crop the rectangular print block directly to preserve its shadows and details.
    """
    img = Image.open(img_path)
    w, h = img.size
    # Bounding box of the monkey photo print block
    # For a 600x600 image: center is 300, 300
    # Let's crop the rectangle exactly
    crop_box = (int(w * 0.25), int(h * 0.22), int(w * 0.75), int(h * 0.65))
    cropped = img.crop(crop_box)
    
    # We can clean the edges slightly, making pure black border transparent
    # Let's key out colors very close to black
    cleaned = key_out_color(cropped, (15, 15, 15), threshold_low=10, threshold_high=25)
    cleaned.save(out_path, "PNG")
    print(f"✅ Extracted Monkey Front -> {out_path}")

def extract_peace_front(img_path, out_path):
    """
    Peace Sign front is a white hand-drawn illustration on a black shirt.
    We use brightness-based masking: white is solid, black is transparent.
    """
    img = Image.open(img_path)
    w, h = img.size
    crop_box = (int(w * 0.22), int(h * 0.18), int(w * 0.78), int(h * 0.68))
    cropped = img.crop(crop_box).convert("RGBA")
    
    # Whiteness mask: any pixel's alpha is proportional to its brightness
    data = cropped.getdata()
    new_data = []
    for item in data:
        brightness = sum(item[:3]) // 3
        if brightness < 40:
            new_data.append((0, 0, 0, 0))
        elif brightness > 150:
            new_data.append((255, 255, 255, 255))
        else:
            ratio = (brightness - 40) / 110
            alpha = int(255 * ratio)
            new_data.append((255, 255, 255, alpha))
            
    cropped.putdata(new_data)
    cropped.save(out_path, "PNG")
    print(f"✅ Extracted Peace Front -> {out_path}")

def extract_robot_front(img_path, out_path):
    """
    Outperformed by a Robot has green text, white text, and red lights on a black shirt.
    We key out black/dark-charcoal fabric.
    """
    img = Image.open(img_path)
    w, h = img.size
    crop_box = (int(w * 0.20), int(h * 0.16), int(w * 0.80), int(h * 0.66))
    cropped = img.crop(crop_box)
    
    # Get reference background color (from top-left corner of cropped area)
    ref_color = cropped.convert("RGB").getpixel((5, 5))
    cleaned = key_out_color(cropped, ref_color, threshold_low=25, threshold_high=55)
    cleaned.save(out_path, "PNG")
    print(f"✅ Extracted Robot Front -> {out_path}")

def extract_sage_front(img_path, out_path):
    """
    Sage Archives is minimal green/black typography on a cream T-shirt.
    We key out the cream fabric color.
    """
    img = Image.open(img_path)
    w, h = img.size
    crop_box = (int(w * 0.25), int(h * 0.20), int(w * 0.75), int(h * 0.70))
    cropped = img.crop(crop_box)
    
    ref_color = cropped.convert("RGB").getpixel((5, 5))
    cleaned = key_out_color(cropped, ref_color, threshold_low=30, threshold_high=65)
    cleaned.save(out_path, "PNG")
    print(f"✅ Extracted Sage Front -> {out_path}")

def extract_binary_front(img_path, out_path):
    """
    Binary Genesis is green matrix code blocks on a black shirt.
    We key out the black background.
    """
    img = Image.open(img_path)
    w, h = img.size
    crop_box = (int(w * 0.22), int(h * 0.18), int(w * 0.78), int(h * 0.72))
    cropped = img.crop(crop_box)
    
    ref_color = cropped.convert("RGB").getpixel((5, 5))
    cleaned = key_out_color(cropped, ref_color, threshold_low=20, threshold_high=50)
    cleaned.save(out_path, "PNG")
    print(f"✅ Extracted Binary Front -> {out_path}")

def extract_vapor_front(img_path, out_path):
    """
    Vaporwave Paradox is a colorful pink/cyan retro element on a charcoal shirt.
    We key out charcoal.
    """
    img = Image.open(img_path)
    w, h = img.size
    crop_box = (int(w * 0.22), int(h * 0.20), int(w * 0.78), int(h * 0.70))
    cropped = img.crop(crop_box)
    
    ref_color = cropped.convert("RGB").getpixel((5, 5))
    cleaned = key_out_color(cropped, ref_color, threshold_low=22, threshold_high=55)
    cleaned.save(out_path, "PNG")
    print(f"✅ Extracted Vapor Front -> {out_path}")

def extract_neural_front(img_path, out_path):
    """
    Neural Echoes is abstract thin synapse line-work on a dark-olive T-shirt.
    We key out dark olive.
    """
    img = Image.open(img_path)
    w, h = img.size
    crop_box = (int(w * 0.25), int(h * 0.20), int(w * 0.75), int(h * 0.68))
    cropped = img.crop(crop_box)
    
    ref_color = cropped.convert("RGB").getpixel((5, 5))
    cleaned = key_out_color(cropped, ref_color, threshold_low=25, threshold_high=55)
    cleaned.save(out_path, "PNG")
    print(f"✅ Extracted Neural Front -> {out_path}")

def extract_pixel_front(img_path, out_path):
    """
    Pixelated Soul is a deconstructed color portrait on a white T-shirt.
    We key out white.
    """
    img = Image.open(img_path)
    w, h = img.size
    crop_box = (int(w * 0.22), int(h * 0.16), int(w * 0.78), int(h * 0.68))
    cropped = img.crop(crop_box)
    
    ref_color = cropped.convert("RGB").getpixel((5, 5))
    cleaned = key_out_color(cropped, ref_color, threshold_low=20, threshold_high=50)
    cleaned.save(out_path, "PNG")
    print(f"✅ Extracted Pixel Front -> {out_path}")

def extract_general_back(img_path, out_path):
    """
    Back views usually contain minimal brand text or logos in a specific region.
    We crop the upper back neck region where the graphic is located and key out shirt color.
    """
    img = Image.open(img_path)
    w, h = img.size
    # Crop the top-middle neck region of the back flat-lay
    crop_box = (int(w * 0.30), int(h * 0.12), int(w * 0.70), int(h * 0.35))
    cropped = img.crop(crop_box)
    
    ref_color = cropped.convert("RGB").getpixel((5, 5))
    cleaned = key_out_color(cropped, ref_color, threshold_low=25, threshold_high=55)
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
    extract_general_back(os.path.join(flats_dir, "flat_robot_back.png"), os.path.join(output_dir, "robot_back.png"))
    extract_general_back(os.path.join(flats_dir, "flat_monkey_back.png"), os.path.join(output_dir, "monkey_back.png"))
    extract_general_back(os.path.join(flats_dir, "flat_peace_back.png"), os.path.join(output_dir, "peace_back.png"))
    extract_general_back(os.path.join(flats_dir, "flat_sage_back.png"), os.path.join(output_dir, "sage_back.png"))
    extract_general_back(os.path.join(flats_dir, "flat_binary_back.png"), os.path.join(output_dir, "binary_back.png"))
    extract_general_back(os.path.join(flats_dir, "flat_vapor_back.png"), os.path.join(output_dir, "vapor_back.png"))
    extract_general_back(os.path.join(flats_dir, "flat_neural_back.png"), os.path.join(output_dir, "neural_back.png"))
    extract_general_back(os.path.join(flats_dir, "flat_pixel_back.png"), os.path.join(output_dir, "pixel_back.png"))
    
    print("🎉 All 16 graphic elements extracted and saved!")

if __name__ == "__main__":
    main()
