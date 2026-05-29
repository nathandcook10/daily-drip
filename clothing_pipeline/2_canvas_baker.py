import os
import sys
from PIL import Image, ImageOps, ImageChops

def get_float_input(prompt, default=1.0):
    try:
        val = input(prompt).strip()
        if not val: return default
        return float(val)
    except ValueError:
        print("Invalid input, using default.")
        return default

def get_int_input(prompt, default=0):
    try:
        val = input(prompt).strip()
        if not val: return default
        return int(val)
    except ValueError:
        print("Invalid input, using default.")
        return default

def invert_image_colors(img):
    """Invert colors of an RGBA image while preserving the alpha channel."""
    if img.mode != 'RGBA':
        img = img.convert('RGBA')
    r, g, b, a = img.split()
    rgb_img = Image.merge('RGB', (r, g, b))
    inverted_rgb = ImageOps.invert(rgb_img)
    ir, ig, ib = inverted_rgb.split()
    return Image.merge('RGBA', (ir, ig, ib, a))

def is_grayscale(img):
    """Check if an image is purely grayscale/monochrome (single shade)."""
    rgb = img.convert('RGB')
    gray = rgb.convert('L').convert('RGB')
    diff = ImageChops.difference(rgb, gray)
    max_diff = max([ex[1] for ex in diff.getextrema()])
    return max_diff < 15

def main():
    staging_dir = "pipeline_staging"
    
    # Check for available approved files
    possible_files = ["approved_front.png", "approved_back.png", "approved_design.png"]
    found_files = [f for f in possible_files if os.path.exists(os.path.join(staging_dir, f))]
    
    if not found_files:
        print(f"Error: Could not find any approved design files in '{staging_dir}'.")
        sys.exit(1)
        
    if len(found_files) > 1:
        print("Found multiple approved designs:")
        for i, f in enumerate(found_files):
            print(f"{i+1}. {f}")
        choice = get_int_input(f"Select which file to process (1-{len(found_files)}): ", 1)
        # Ensure choice is within bounds
        choice = max(1, min(choice, len(found_files)))
        input_filename = found_files[choice - 1]
    else:
        input_filename = found_files[0]
        
    input_path = os.path.join(staging_dir, input_filename)

    placement = "front"
    if "front" in input_filename.lower():
        placement = "front"
    elif "back" in input_filename.lower():
        placement = "back"
    else:
        while True:
            placement_input = input("Is this design for the 'front' or 'back' of the shirt?: ").strip().lower()
            if placement_input in ['front', 'back']:
                placement = placement_input
                break
            print("Please enter 'front' or 'back'.")

    print(f"Loading '{input_path}'...")
    try:
        # Increase max image pixels to avoid DecompressionBombError for large images
        Image.MAX_IMAGE_PIXELS = None
        img = Image.open(input_path).convert("RGBA")
    except Exception as e:
        print(f"Error loading image: {e}")
        sys.exit(1)

    # 1. Upscale the image so the shortest side is at least 4000px
    width, height = img.size
    shortest_side = min(width, height)
    
    if shortest_side < 4000:
        scale_ratio = 4000 / shortest_side
        new_size = (int(width * scale_ratio), int(height * scale_ratio))
        print(f"Upscaling image from {width}x{height} to {new_size[0]}x{new_size[1]}...")
        img = img.resize(new_size, Image.Resampling.LANCZOS)
    else:
        print(f"Image is already large enough ({width}x{height}). Shortest side is {shortest_side}px.")

    # 2. Ask if photo or graphic
    while True:
        img_type = input("Is the image a photo or a graphic? (photo/graphic): ").strip().lower()
        if img_type in ['photo', 'graphic']:
            break
        print("Please enter 'photo' or 'graphic'.")

    # 3. Ask for X/Y coordinates and scale factor
    print("\nThe final canvas will be 4500x5100.")
    print("You can specify a scale factor for the design (1.0 = current size) and X/Y coordinates to place it.")
    
    scale_factor = get_float_input("Enter scale factor for the design (default 1.0): ", 1.0)
    x_coord = get_int_input("Enter X coordinate for placement (default 0): ", 0)
    y_coord = get_int_input("Enter Y coordinate for placement (default 0): ", 0)

    # Scale the image based on user input
    if scale_factor != 1.0:
        scaled_size = (int(img.width * scale_factor), int(img.height * scale_factor))
        print(f"Scaling design to {scaled_size[0]}x{scaled_size[1]}...")
        design_img = img.resize(scaled_size, Image.Resampling.LANCZOS)
    else:
        design_img = img

    # Function to create canvas and paste
    def save_to_canvas(paste_img, filename):
        # 4500x5100 transparent canvas
        canvas = Image.new("RGBA", (4500, 5100), (0, 0, 0, 0))
        # Paste the design onto the canvas at the specified coordinates
        # using the design itself as the mask to preserve transparency
        canvas.paste(paste_img, (x_coord, y_coord), paste_img)
        
        out_path = os.path.join(staging_dir, filename)
        canvas.save(out_path, "PNG")
        print(f"Saved: {out_path}")

    # Create the light shirt variant (original colors)
    print("\nBaking canvases...")
    save_to_canvas(design_img, f"{placement}_light_ready.png")

    # Create the dark shirt variant
    if img_type == 'graphic':
        if is_grayscale(design_img):
            print("Graphic is a single shade (grayscale). Creating inverted color variant...")
            inverted_design = invert_image_colors(design_img)
            save_to_canvas(inverted_design, f"{placement}_dark_ready.png")
        else:
            print("Graphic is full color. Keeping original colors for dark variant...")
            save_to_canvas(design_img, f"{placement}_dark_ready.png")
    else:
        print("Using original colors for dark variant (photo)...")
        save_to_canvas(design_img, f"{placement}_dark_ready.png")
        
    print("\nPhase 2 Complete!")

if __name__ == "__main__":
    main()
