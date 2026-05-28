#!/usr/bin/env python3
"""
💧 [The Daily Drip] Specialized Punch the Monkey Compositing Engine
------------------------------------------------------------------
This script programmatically generates all black and white garment variations
for the Punch the Monkey PDP, ensuring pixel-perfect parity between flats and fits.

It outputs:
1. curator_2_black.png (Black fit 1)
2. curator_5_black.png (Black fit 2 layered)
3. curator_2_white.png (White fit 1)
4. curator_5_white.png (White fit 2 layered)
5. flat_monkey_front_black.png
6. flat_monkey_back_black.png
7. flat_monkey_front_white.png
8. flat_monkey_back_white.png
"""

import os
from PIL import Image, ImageEnhance, ImageOps, ImageChops, ImageFilter

# Paths
BASE_DIR = "/Users/nathan/Daily Drip"
EXTRACTED_DIR = os.path.join(BASE_DIR, "Core Art/extracted")
FLATS_OUT_DIR = os.path.join(BASE_DIR, "public/assets/flats")
MODELS_OUT_DIR = os.path.join(BASE_DIR, "public/assets/models/option1")
BRAIN_DIR = "/Users/nathan/.gemini/antigravity/brain/affe4f09-1adf-4c4a-8e08-54786009d8b9"

# Source Blanks
BLANK_WHITE_1 = os.path.join(BRAIN_DIR, "curator_2_blank_1779480139744.png")
BLANK_WHITE_2 = os.path.join(BRAIN_DIR, "curator_5_blank_1779480167607.png")
BLANK_BLACK_1 = os.path.join(BRAIN_DIR, "curator_2_blank_black_1779483040653.png")
BLANK_BLACK_2 = os.path.join(BRAIN_DIR, "curator_5_blank_black_1779483059120.png")

FLAT_SAGE_FRONT = os.path.join(BRAIN_DIR, "flat_sage_front_1779478400430.png")
FLAT_SAGE_BACK = os.path.join(BRAIN_DIR, "flat_sage_back_1779478534910.png")

GRAPHIC_FRONT = os.path.join(EXTRACTED_DIR, "monkey_front.png")
GRAPHIC_BACK = os.path.join(EXTRACTED_DIR, "monkey_back.png")

os.makedirs(FLATS_OUT_DIR, exist_ok=True)
os.makedirs(MODELS_OUT_DIR, exist_ok=True)

def apply_soft_feather(img, feather_radius=3):
    """
    Applies a soft alpha feather to the edges of a transparent/alpha-masked image.
    This prevents harsh pixel cut edges and blends the print naturally into fabric.
    """
    img = img.convert("RGBA")
    r, g, b, alpha = img.split()
    
    # Blur the alpha mask to create a soft transition gradient
    blurred_alpha = alpha.filter(ImageFilter.GaussianBlur(feather_radius))
    
    # Keep the center fully opaque but soften the immediate edge pixels
    # We do this by taking the minimum of a dilated alpha and the blurred alpha
    # or simply using a subtle contrast curve on the blurred alpha.
    enhanced_alpha = ImageEnhance.Contrast(blurred_alpha).enhance(1.5)
    
    return Image.merge("RGBA", (r, g, b, enhanced_alpha))

def create_clean_flat_white_blank():
    """
    Erases the "Sage Archives" text from the cream flat-lay front by patching it
    with a clean cream fabric region, creating a pristine blank white flat lay front.
    """
    print("🧹 Creating clean white flat-lay front blank...")
    img = Image.open(FLAT_SAGE_FRONT).convert("RGBA")
    w, h = img.size
    
    # "Sage Archives" text is centered roughly between y=160 and y=400, x=150 and x=450
    # Let's copy a clean patch of fabric from the bottom-left of the shirt (e.g. y=420 to 520, x=80 to 200)
    # and use it to cover the text. Since we'll paste the monkey photo block right over it,
    # we just need a clean textured canvas.
    clean_patch = img.crop((80, 420, 200, 520))
    
    # Create a textured background fill in the center
    # We can also just smoothly interpolate the color to keep it natural
    # Let's sample a clean cream pixel
    cream_color = img.getpixel((100, 450)) # (248, 249, 246, 255)
    
    # Draw a clean box to erase the print text
    box = Image.new("RGBA", (340, 260), cream_color)
    img.paste(box, (130, 160))
    
    # Paste some clean texture on top with low opacity to preserve fabric look
    # or just let it blend. Since the monkey print is 280px wide and covers the center,
    # it will completely overlay the erased box!
    return img

def composite_flat_lay(blank_img, graphic_path, out_path, is_back=False):
    """
    Composites the graphic onto a flat-lay blank.
    """
    graphic = Image.open(graphic_path).convert("RGBA")
    w, h = blank_img.size
    
    if is_back:
        # Mini back branding, scaled and positioned near top neck
        target_w = 60
        aspect = graphic.height / graphic.width
        target_h = int(target_w * aspect)
        resized = graphic.resize((target_w, target_h), Image.Resampling.LANCZOS)
        
        canvas = Image.new("RGBA", blank_img.size, (0, 0, 0, 0))
        canvas.paste(resized, (int(w/2 - target_w/2), int(h * 0.16)))
        
        final_img = Image.alpha_composite(blank_img, canvas)
    else:
        # Front print block, centered
        target_w = 280
        aspect = graphic.height / graphic.width
        target_h = int(target_w * aspect)
        resized = graphic.resize((target_w, target_h), Image.Resampling.LANCZOS)
        
        # Feather the flat-lay print edges too!
        resized = apply_soft_feather(resized, feather_radius=2)
        
        canvas = Image.new("RGBA", blank_img.size, (0, 0, 0, 0))
        canvas.paste(resized, (int(w/2 - target_w/2), int(h * 0.20)))
        
        final_img = Image.alpha_composite(blank_img, canvas)
        
    final_img.convert("RGB").save(out_path, "PNG")
    print(f"📦 Created Flat-Lay -> {os.path.basename(out_path)}")

def composite_model_fit(blank_path, graphic_path, out_path, x, y, width, is_black_shirt=False, shadow_intensity=1.2):
    """
    Composites the graphic onto the model blank with high-end fabric creases and shadow embossing.
    """
    if not os.path.exists(blank_path):
        print(f"❌ Error: Blank not found at {blank_path}")
        return
        
    model_img = Image.open(blank_path).convert("RGBA")
    graphic = Image.open(graphic_path).convert("RGBA")
    
    # Calculate dimensions
    aspect = graphic.height / graphic.width
    height = int(width * aspect)
    
    # Resize graphic
    resized = graphic.resize((width, height), Image.Resampling.LANCZOS)
    
    # Apply soft feathering to the print borders to make it blend into the cotton
    resized = apply_soft_feather(resized, feather_radius=3)
    
    # Graphic positioning canvas
    graphic_canvas = Image.new("RGBA", model_img.size, (0, 0, 0, 0))
    graphic_canvas.paste(resized, (x, y))
    
    r, g, b, alpha = graphic_canvas.split()
    rgb_graphic = Image.merge("RGB", (r, g, b))
    
    # Extract creases/folds from the shirt region
    crop_box = (x, y, x + width, y + height)
    shirt_region = model_img.crop(crop_box).convert("RGBA")
    l_mask = shirt_region.convert("L")
    
    # Enhance creases contrast
    enhancer = ImageEnhance.Contrast(l_mask)
    crease_map = enhancer.enhance(1.4 * shadow_intensity)
    
    # Create crease canvas (neutral gray 128)
    full_crease = Image.new("L", model_img.size, 128)
    full_crease.paste(crease_map, (x, y))
    
    if is_black_shirt:
        # For black shirts, highlights and shadows are embossed.
        # We overlay the crease map directly on top of the graphic to preserve highlight reflections.
        overlay_canvas = Image.new("RGB", model_img.size, (128, 128, 128))
        overlay_canvas.paste(crease_map.convert("RGB"), (x, y))
        
        # Overlay blend graphic with shirt crease canvas
        blended_rgb = ImageChops.overlay(rgb_graphic, overlay_canvas)
        
        # Also apply a subtle shadow mask to darken valleys
        shadow_mask = ImageOps.invert(crease_map)
        shadow_mask_soft = ImageEnhance.Contrast(shadow_mask).enhance(0.4)
        shadow_canvas = Image.new("L", model_img.size, 255)
        shadow_canvas.paste(shadow_mask_soft, (x, y))
        
        blended_rgb = ImageChops.multiply(blended_rgb, Image.merge("RGB", (shadow_canvas, shadow_canvas, shadow_canvas)))
        final_graphic = Image.merge("RGBA", (blended_rgb.split()[0], blended_rgb.split()[1], blended_rgb.split()[2], alpha))
    else:
        # For white/cream shirts, multiply blend is ideal but we over-emboss folds
        # so that details are crisp.
        blended_rgb = ImageChops.multiply(rgb_graphic, Image.merge("RGB", (full_crease, full_crease, full_crease)))
        final_graphic = Image.merge("RGBA", (blended_rgb.split()[0], blended_rgb.split()[1], blended_rgb.split()[2], alpha))
        
    # Final composite
    composite = Image.alpha_composite(model_img, final_graphic)
    composite.convert("RGB").save(out_path, "PNG")
    print(f"✨ Blended Model Fit -> {os.path.basename(out_path)}")

def main():
    print("🚀 Punch the Monkey Mockup Generation Starting...")
    
    # -------------------------------------------------------------------------
    # 1. FLAT LAYS
    # -------------------------------------------------------------------------
    # Black Flat-Lays: Copy original flats
    orig_front_black = os.path.join(FLATS_OUT_DIR, "flat_monkey_front.png")
    orig_back_black = os.path.join(FLATS_OUT_DIR, "flat_monkey_back.png")
    
    front_black_out = os.path.join(FLATS_OUT_DIR, "flat_monkey_front_black.png")
    back_black_out = os.path.join(FLATS_OUT_DIR, "flat_monkey_back_black.png")
    
    if os.path.exists(orig_front_black):
        Image.open(orig_front_black).save(front_black_out)
        print("📦 Copied Flat-Lay Front -> flat_monkey_front_black.png")
    if os.path.exists(orig_back_black):
        Image.open(orig_back_black).save(back_black_out)
        print("📦 Copied Flat-Lay Back -> flat_monkey_back_black.png")
        
    # White Flat-Lays: Erase Sage Archives and composite Monkey graphic
    clean_white_flat_front = create_clean_flat_white_blank()
    composite_flat_lay(clean_white_flat_front, GRAPHIC_FRONT, os.path.join(FLATS_OUT_DIR, "flat_monkey_front_white.png"), is_back=False)
    
    clean_white_flat_back = Image.open(FLAT_SAGE_BACK).convert("RGBA")
    composite_flat_lay(clean_white_flat_back, GRAPHIC_BACK, os.path.join(FLATS_OUT_DIR, "flat_monkey_back_white.png"), is_back=True)

    # -------------------------------------------------------------------------
    # 2. MODEL FITS (WHITE/CREAM)
    # -------------------------------------------------------------------------
    print("🎨 Rendering White/Cream model fits...")
    composite_model_fit(
        blank_path=BLANK_WHITE_1,
        graphic_path=GRAPHIC_FRONT,
        out_path=os.path.join(MODELS_OUT_DIR, "curator_2_white.png"),
        x=370, y=360, width=280,
        is_black_shirt=False,
        shadow_intensity=1.35
    )
    composite_model_fit(
        blank_path=BLANK_WHITE_2,
        graphic_path=GRAPHIC_FRONT,
        out_path=os.path.join(MODELS_OUT_DIR, "curator_5_white.png"),
        x=390, y=380, width=240,
        is_black_shirt=False,
        shadow_intensity=1.35
    )

    # -------------------------------------------------------------------------
    # 3. MODEL FITS (BLACK)
    # -------------------------------------------------------------------------
    print("🎨 Rendering Black model fits...")
    composite_model_fit(
        blank_path=BLANK_BLACK_1,
        graphic_path=GRAPHIC_FRONT,
        out_path=os.path.join(MODELS_OUT_DIR, "curator_2_black.png"),
        x=370, y=360, width=280,
        is_black_shirt=True,
        shadow_intensity=1.35
    )
    composite_model_fit(
        blank_path=BLANK_BLACK_2,
        graphic_path=GRAPHIC_FRONT,
        out_path=os.path.join(MODELS_OUT_DIR, "curator_5_black.png"),
        x=390, y=380, width=240,
        is_black_shirt=True,
        shadow_intensity=1.35
    )
    
    # Also generate the default files (curator_2.png and curator_5.png)
    # The default files should be black, matching the original black t-shirt product design!
    Image.open(os.path.join(MODELS_OUT_DIR, "curator_2_black.png")).save(os.path.join(MODELS_OUT_DIR, "curator_2.png"))
    Image.open(os.path.join(MODELS_OUT_DIR, "curator_5_black.png")).save(os.path.join(MODELS_OUT_DIR, "curator_5.png"))
    print("✅ Successfully mapped default curator_2.png and curator_5.png to Black fits.")
    print("🎉 Punch the Monkey Mockup Generation Complete!")

if __name__ == "__main__":
    main()
