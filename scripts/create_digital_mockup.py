#!/usr/bin/env python3
"""
💧 [The Daily Drip] Programmatic Digital Mockup Compositing Engine
------------------------------------------------------------------
This script programmatically overlays high-resolution graphic prints (PNG with transparency)
onto model fits wearing blank T-shirts. To achieve photo-realism, it extracts the fabric's 
natural texture, creases, and shadows from the blank garment area and composites them 
back over the print using advanced blending modes (Multiply/Overlay).

This guarantees 100% mathematical consistency of the graphic elements, colors, and 
typography between flat-lay product photos and model lifestyle photography.
"""

import os
import sys
import argparse
from PIL import Image, ImageEnhance, ImageOps, ImageChops

def create_mockup(model_blank_path, graphic_path, output_path, x_offset, y_offset, target_width, blend_mode="multiply", shadow_intensity=1.0):
    """
    Overlays a transparent graphic onto a model blank with lighting/crease preservation.
    
    Parameters:
      model_blank_path (str): Path to the model wearing a blank T-shirt.
      graphic_path (str): Path to the high-res transparent design artwork.
      output_path (str): Destination path for the completed mockup.
      x_offset (int): X coordinate for the top-left corner of the graphic placement.
      y_offset (int): Y coordinate for the top-left corner of the graphic placement.
      target_width (int): Target width for resizing the graphic (maintains aspect ratio).
      blend_mode (str): Blending method ('multiply', 'normal', 'overlay').
      shadow_intensity (float): Multiplier for creases and shadow depth (1.0 = normal).
    """
    if not os.path.exists(model_blank_path):
        print(f"❌ Error: Model blank file not found at '{model_blank_path}'")
        return False
    if not os.path.exists(graphic_path):
        print(f"❌ Error: Graphic artwork not found at '{graphic_path}'")
        return False

    print(f"🎨 Loading assets...")
    model_img = Image.open(model_blank_path).convert("RGBA")
    graphic_img = Image.open(graphic_path).convert("RGBA")
    
    # Calculate height to maintain original aspect ratio
    aspect_ratio = graphic_img.height / graphic_img.width
    target_height = int(target_width * aspect_ratio)
    
    print(f"📏 Resizing graphic print to: {target_width}x{target_height}px")
    resized_graphic = graphic_img.resize((target_width, target_height), Image.Resampling.LANCZOS)
    
    # Create an empty canvas matching the model image size to position the graphic
    graphic_canvas = Image.new("RGBA", model_img.size, (0, 0, 0, 0))
    graphic_canvas.paste(resized_graphic, (x_offset, y_offset))
    
    # Separate color channels and alpha mask
    r, g, b, alpha = graphic_canvas.split()
    rgb_graphic = Image.merge("RGB", (r, g, b))
    
    # Crop the exact region on the blank shirt where the graphic will go
    # to extract lighting mask (shadows, wrinkles, and folds)
    crop_box = (x_offset, y_offset, x_offset + target_width, y_offset + target_height)
    shirt_region = model_img.crop(crop_box).convert("RGBA")
    
    # Extract the brightness/lighting profile from the blank shirt
    l_mask = shirt_region.convert("L")
    
    # Enhance the contrast of the lighting profile to make folds/creases pop
    enhancer = ImageEnhance.Contrast(l_mask)
    crease_map = enhancer.enhance(1.3 * shadow_intensity)
    
    # Resize the crease map back to full canvas size
    full_crease_canvas = Image.new("L", model_img.size, 128)  # 128 = Neutral Gray
    full_crease_canvas.paste(crease_map, (x_offset, y_offset))
    
    print(f"💧 Applying blending rules: blend_mode='{blend_mode}'")
    
    if blend_mode == "multiply":
        # Best for white/light T-shirts. Multiplies the graphic's colors with the shirt's lighting map
        # to inherit shadows and folds perfectly.
        blended_rgb = ImageChops.multiply(rgb_graphic, Image.merge("RGB", (full_crease_canvas, full_crease_canvas, full_crease_canvas)))
        final_graphic = Image.merge("RGBA", (blended_rgb.split()[0], blended_rgb.split()[1], blended_rgb.split()[2], alpha))
        
    elif blend_mode == "overlay":
        # Good for medium-toned T-shirts (Sage, Charcoal). Overlays mid-tones, preserves highlights.
        # We overlay the crease map directly on top of the graphic.
        overlay_canvas = Image.new("RGB", model_img.size, (128, 128, 128))
        overlay_canvas.paste(crease_map.convert("RGB"), (x_offset, y_offset))
        
        # Simple math-based overlay simulation
        blended_rgb = ImageChops.overlay(rgb_graphic, overlay_canvas)
        final_graphic = Image.merge("RGBA", (blended_rgb.split()[0], blended_rgb.split()[1], blended_rgb.split()[2], alpha))
        
    else:  # "normal"
        # Standard transparent overlay (used if no fabric shadows are needed or for dark black shirts)
        final_graphic = graphic_canvas
        
    # Composite the blended graphic on top of the original model blank
    print("🚀 Compositing final assets...")
    composite_img = Image.alpha_composite(model_img, final_graphic)
    
    # Save the output image
    composite_img.convert("RGB").save(output_path, "PNG")
    print(f"✅ Success! Mockup saved to: {output_path}")
    return True

def main():
    parser = argparse.ArgumentParser(
        description="💧 Programmatic Digital Mockup Compositing Engine. Overlay transparent prints onto blank model fits."
    )
    parser.add_argument("--model", required=True, help="Path to model blank image (RGBA)")
    parser.add_argument("--graphic", required=True, help="Path to transparent design artwork (RGBA)")
    parser.add_argument("--out", required=True, help="Path to save the generated mockup")
    parser.add_argument("--x", type=int, default=150, help="X offset for top-left corner of graphic (default: 150)")
    parser.add_argument("--y", type=int, default=200, help="Y offset for top-left corner of graphic (default: 200)")
    parser.add_argument("--width", type=int, default=250, help="Target pixel width for the graphic (default: 250)")
    parser.add_argument("--blend", choices=["multiply", "overlay", "normal"], default="multiply", 
                        help="Blending mode: 'multiply' (light shirts), 'overlay' (colored/mid-tone), 'normal' (dark/black shirts)")
    parser.add_argument("--shadows", type=float, default=1.0, help="Shadow intensity multiplier (default: 1.0)")
    
    # Add help note about standard coordinates for current models
    args = parser.parse_args()
    
    create_mockup(
        model_blank_path=args.model,
        graphic_path=args.graphic,
        output_path=args.out,
        x_offset=args.x,
        y_offset=args.y,
        target_width=args.width,
        blend_mode=args.blend,
        shadow_intensity=args.shadows
    )

if __name__ == "__main__":
    main()
