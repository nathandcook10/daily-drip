import os
import shutil
import re

brain_dir = "/Users/nathan/.gemini/antigravity/brain/affe4f09-1adf-4c4a-8e08-54786009d8b9"
public_base = "/Users/nathan/Daily Drip/public/assets/models"

mappings = {
    "modernist_7_sage": ("option2", "modernist_7_sage.png"),
    "modernist_8_sage_layer": ("option2", "modernist_8_sage_layer.png"),
    "cyber_7_binary": ("option4", "cyber_7_binary.png"),
    "cyber_8_binary_back": ("option4", "cyber_8_binary_back.png"),
    "retro_7_vapor": ("option5", "retro_7_vapor.png"),
    "retro_8_vapor_layer": ("option5", "retro_8_vapor_layer.png"),
    "modernist_9_neural": ("option2", "modernist_9_neural.png"),
    "modernist_10_neural_layer": ("option2", "modernist_10_neural_layer.png"),
    "retro_9_pixel": ("option5", "retro_9_pixel.png"),
    "retro_10_pixel_layer": ("option5", "retro_10_pixel_layer.png")
}

def main():
    print("Starting organization of newly generated assets...")
    files = os.listdir(brain_dir)
    print(f"Found {len(files)} files in brain directory.")
    
    copied = 0
    for filename in files:
        if not filename.endswith(".png"):
            continue
            
        # Match pattern: e.g. modernist_7_sage_1779477047526.png
        # Extract the prefix of the filename
        match = re.match(r"^([a-z0-9_]+?)_\d+\.png$", filename)
        if match:
            prefix = match.group(1)
            if prefix in mappings:
                opt_folder, clean_name = mappings[prefix]
                src_path = os.path.join(brain_dir, filename)
                dest_path = os.path.join(public_base, opt_folder, clean_name)
                
                shutil.copy2(src_path, dest_path)
                print(f"Copied {filename} -> models/{opt_folder}/{clean_name}")
                copied += 1
                
    print(f"Finished copying new assets! Total copied: {copied}/10")

if __name__ == "__main__":
    main()
