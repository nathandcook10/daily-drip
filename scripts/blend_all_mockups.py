#!/usr/bin/env python3
"""
💧 [The Daily Drip] Batch Mockup Compositing Engine
--------------------------------------------------
This script automates the compositing of isolated print graphics (front/back)
onto the high-fidelity model blank images generated for the 5 option styles.
It places them at precise coordinates with proper blending modes to achieve
photorealistic visual parity.
"""

import os
import sys
from PIL import Image, ImageEnhance, ImageOps, ImageChops

# Paths
BASE_DIR = "/Users/nathan/Daily Drip"
GRAPHICS_DIR = os.path.join(BASE_DIR, "Core Art/extracted")
MODELS_DIR = os.path.join(BASE_DIR, "public/assets/models")
BRAIN_DIR = "/Users/nathan/.gemini/antigravity/brain/affe4f09-1adf-4c4a-8e08-54786009d8b9"

# Model Blanks Mapping in the Brain Dir
BLANKS = {
    "curator_2_blank": "curator_2_blank_1779480139744.png",
    "curator_5_blank": "curator_5_blank_1779480167607.png",
    "modernist_7_blank": "modernist_7_blank_1779480187588.png",
    "modernist_8_blank": "modernist_8_blank_1779480206195.png",
    "modernist_9_blank": "modernist_9_blank_1779480227440.png",
    "modernist_10_blank": "modernist_10_blank_1779480246349.png",
    "rebel_3_blank": "rebel_3_blank_black_1779511533466.png",
    "rebel_6_blank": "rebel_6_blank_black_1779511552985.png",
    "cyber_1_blank": "cyber_1_blank_1779480311849.png",
    "cyber_4_blank": "cyber_4_blank_1779480332086.png",
    "cyber_7_blank": "cyber_7_blank_1779480354156.png",
    "cyber_8_blank": "cyber_8_blank_1779480527019.png",
    "retro_7_blank": "retro_7_blank_1779480577798.png",
    "retro_8_blank": "retro_8_blank_1779480595612.png",
    "retro_9_blank": "retro_9_blank_1779480639022.png",
    "retro_10_blank": "retro_10_blank_1779480681126.png"
}

# The 16 Compositing Tasks
# Format: (model_blank_key, graphic_filename, relative_dest_path, x, y, width, blend_mode, shadow_intensity)
COMPOSITING_TASKS = [
    # --- Option 1: Curator (Punch the Monkey) ---
    ("curator_2_blank", "monkey_front.png", "option1/curator_2.png", 370, 360, 280, "multiply", 1.2),
    ("curator_5_blank", "monkey_front.png", "option1/curator_5.png", 390, 380, 240, "multiply", 1.2),
    
    # --- Option 2: Modernist (Sage Archives & Neural Echoes) ---
    # Sage Archives
    ("modernist_7_blank", "sage_front.png", "option2/modernist_7_sage.png", 360, 350, 300, "overlay", 1.1),
    ("modernist_8_blank", "sage_front.png", "option2/modernist_8_sage_layer.png", 380, 370, 260, "overlay", 1.1),
    # Neural Echoes
    ("modernist_9_blank", "neural_front.png", "option2/modernist_9_neural.png", 360, 350, 300, "multiply", 1.1),
    ("modernist_10_blank", "neural_front.png", "option2/modernist_10_neural_layer.png", 385, 370, 250, "multiply", 1.1),
    
    # --- Option 3: Rebel (Peace Sign) ---
    ("rebel_3_blank", "peace_front.png", "option3/rebel_3.png", 365, 340, 290, "normal", 1.2),
    ("rebel_6_blank", "peace_front.png", "option3/rebel_6.png", 385, 360, 250, "normal", 1.2),
    
    # --- Option 4: Cyber (Robot & Binary Genesis) ---
    # Outperformed by Robot
    ("cyber_1_blank", "robot_front.png", "option4/cyber_1.png", 365, 340, 290, "normal", 1.0),
    ("cyber_4_blank", "robot_back.png", "option4/cyber_4.png", 380, 320, 260, "normal", 1.0),
    # Binary Genesis
    ("cyber_7_blank", "binary_front.png", "option4/cyber_7_binary.png", 365, 345, 290, "normal", 1.0),
    ("cyber_8_blank", "binary_back.png", "option4/cyber_8_binary_back.png", 385, 310, 250, "normal", 1.0),
    
    # --- Option 5: Retro (Vaporwave Paradox & Pixelated Soul) ---
    # Vaporwave Paradox
    ("retro_7_blank", "vapor_front.png", "option5/retro_7_vapor.png", 360, 340, 300, "normal", 1.0),
    ("retro_8_blank", "vapor_front.png", "option5/retro_8_vapor_layer.png", 385, 350, 250, "normal", 1.0),
    # Pixelated Soul
    ("retro_9_blank", "pixel_front.png", "option5/retro_9_pixel.png", 360, 340, 300, "multiply", 1.1),
    ("retro_10_blank", "pixel_front.png", "option5/retro_10_pixel_layer.png", 385, 350, 250, "multiply", 1.1)
]

def create_mockup(model_blank_path, graphic_path, output_path, x_offset, y_offset, target_width, blend_mode="multiply", shadow_intensity=1.0):
    """
    Composites transparent graphic onto model blank with fabric wrinkles and shadows.
    """
    if not os.path.exists(model_blank_path):
        print(f"❌ Error: Model blank file not found at '{model_blank_path}'")
        return False
    if not os.path.exists(graphic_path):
        print(f"❌ Error: Graphic artwork not found at '{graphic_path}'")
        return False

    model_img = Image.open(model_blank_path).convert("RGBA")
    graphic_img = Image.open(graphic_path).convert("RGBA")
    
    # Calculate height to maintain original aspect ratio
    aspect_ratio = graphic_img.height / graphic_img.width
    target_height = int(target_width * aspect_ratio)
    
    resized_graphic = graphic_img.resize((target_width, target_height), Image.Resampling.LANCZOS)
    
    # Create an empty canvas matching the model image size to position the graphic
    graphic_canvas = Image.new("RGBA", model_img.size, (0, 0, 0, 0))
    graphic_canvas.paste(resized_graphic, (x_offset, y_offset))
    
    r, g, b, alpha = graphic_canvas.split()
    rgb_graphic = Image.merge("RGB", (r, g, b))
    
    # Crop the exact region on the blank shirt where the graphic will go to extract crease/shadow profile
    crop_box = (x_offset, y_offset, x_offset + target_width, y_offset + target_height)
    shirt_region = model_img.crop(crop_box).convert("RGBA")
    
    # Extract the brightness/lighting profile from the blank shirt
    l_mask = shirt_region.convert("L")
    
    # Enhance the contrast of the lighting profile to make folds/creases pop
    enhancer = ImageEnhance.Contrast(l_mask)
    crease_map = enhancer.enhance(1.4 * shadow_intensity)
    
    # Resize the crease map back to full canvas size
    full_crease_canvas = Image.new("L", model_img.size, 128)  # 128 = Neutral Gray
    full_crease_canvas.paste(crease_map, (x_offset, y_offset))
    
    if blend_mode == "multiply":
        # Best for white/light shirts
        blended_rgb = ImageChops.multiply(rgb_graphic, Image.merge("RGB", (full_crease_canvas, full_crease_canvas, full_crease_canvas)))
        final_graphic = Image.merge("RGBA", (blended_rgb.split()[0], blended_rgb.split()[1], blended_rgb.split()[2], alpha))
        
    elif blend_mode == "overlay":
        # Best for colored/mid-tone shirts
        overlay_canvas = Image.new("RGB", model_img.size, (128, 128, 128))
        overlay_canvas.paste(crease_map.convert("RGB"), (x_offset, y_offset))
        blended_rgb = ImageChops.overlay(rgb_graphic, overlay_canvas)
        final_graphic = Image.merge("RGBA", (blended_rgb.split()[0], blended_rgb.split()[1], blended_rgb.split()[2], alpha))
        
    else:  # "normal"
        # Standard transparent overlay with crease-preserving multiplier mask
        # To make "normal" blends look realistic (especially on dark/black shirts), we extract a crease map,
        # invert it, and use it to slightly darken the graphic's alpha channel where shadows/folds are,
        # or multiply the graphic's RGB with a subtle shadow mask.
        
        # Build crease map shadow mask
        shadow_mask = ImageOps.invert(crease_map)
        shadow_mask_enhanced = ImageEnhance.Contrast(shadow_mask).enhance(0.5) # Soften
        
        # Apply shadow mask overlay
        shadow_canvas = Image.new("L", model_img.size, 255)
        shadow_canvas.paste(shadow_mask_enhanced, (x_offset, y_offset))
        
        # Blend graphic with shadow canvas to embed shirt folds
        blended_rgb = ImageChops.multiply(rgb_graphic, Image.merge("RGB", (shadow_canvas, shadow_canvas, shadow_canvas)))
        final_graphic = Image.merge("RGBA", (blended_rgb.split()[0], blended_rgb.split()[1], blended_rgb.split()[2], alpha))

    # Composite the blended graphic on top of the original model blank
    composite_img = Image.alpha_composite(model_img, final_graphic)
    
    # Save the output image
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    composite_img.convert("RGB").save(output_path, "PNG")
    print(f"✅ Blended successfully -> {os.path.basename(output_path)}")
    return True

def main():
    print("🚀 Drip Compositing Engine Starting...")
    print(f"📂 Graphics Source: {GRAPHICS_DIR}")
    print(f"📂 Models Output: {MODELS_DIR}")
    print(f"📂 Blanks Source: {BRAIN_DIR}")
    print("--------------------------------------------------")
    
    success_count = 0
    for blank_key, graphic_file, rel_dest, x, y, width, blend, shadows in COMPOSITING_TASKS:
        blank_file = BLANKS.get(blank_key)
        if not blank_file:
            print(f"⚠️ Warning: No blank mapped for '{blank_key}'")
            continue
            
        model_blank_path = os.path.join(BRAIN_DIR, blank_file)
        graphic_path = os.path.join(GRAPHICS_DIR, graphic_file)
        output_path = os.path.join(MODELS_DIR, rel_dest)
        
        print(f"🎨 Compositing {graphic_file} onto {blank_key} ({blend} mode)...")
        success = create_mockup(
            model_blank_path=model_blank_path,
            graphic_path=graphic_path,
            output_path=output_path,
            x_offset=x,
            y_offset=y,
            target_width=width,
            blend_mode=blend,
            shadow_intensity=shadows
        )
        if success:
            success_count += 1
            
    print("--------------------------------------------------")
    print(f"🎉 Batch Compositing Complete! {success_count}/{len(COMPOSITING_TASKS)} mockups blended successfully.")

if __name__ == "__main__":
    main()
