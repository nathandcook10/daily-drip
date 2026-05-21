import os
import shutil
import re

# Source directory containing generated images
brain_dir = "/Users/nathan/.gemini/antigravity/brain/fed3221b-8e39-400a-9b28-1b2766abfa80"
# Target base directory
public_base = "/Users/nathan/Daily Drip/public/assets/models"

# Prefix to folder mapping and output name
mappings = {
    "curator_1": ("option1", "curator_1.png"),
    "curator_2": ("option1", "curator_2.png"),
    "curator_3": ("option1", "curator_3.png"),
    "curator_4": ("option1", "curator_4.png"),
    "curator_5": ("option1", "curator_5.png"),
    "curator_6": ("option1", "curator_6.png"),
    
    "modernist_1": ("option2", "modernist_1.png"),
    "modernist_2": ("option2", "modernist_2.png"),
    "modernist_3": ("option2", "modernist_3.png"),
    "modernist_4": ("option2", "modernist_4.png"),
    "modernist_5": ("option2", "modernist_5.png"),
    "modernist_6": ("option2", "modernist_6.png"),
    
    "rebel_1": ("option3", "rebel_1.png"),
    "rebel_2": ("option3", "rebel_2.png"),
    "rebel_3": ("option3", "rebel_3.png"),
    "rebel_4": ("option3", "rebel_4.png"),
    "rebel_5": ("option3", "rebel_5.png"),
    "rebel_6": ("option3", "rebel_6.png"),
    
    "cyber_1": ("option4", "cyber_1.png"),
    "cyber_2": ("option4", "cyber_2.png"),
    "cyber_3": ("option4", "cyber_3.png"),
    "cyber_4": ("option4", "cyber_4.png"),
    "cyber_5": ("option4", "cyber_5.png"),
    "cyber_6": ("option4", "cyber_6.png"),
    
    "retro_1": ("option5", "retro_1.png"),
    "retro_2": ("option5", "retro_2.png"),
    "retro_3": ("option5", "retro_3.png"),
    "retro_4": ("option5", "retro_4.png"),
    "retro_5": ("option5", "retro_5.png"),
    "retro_6": ("option5", "retro_6.png")
}

def main():
    print("Starting asset organization...")
    
    # Create target directories
    for opt in ["option1", "option2", "option3", "option4", "option5"]:
        opt_dir = os.path.join(public_base, opt)
        os.makedirs(opt_dir, exist_ok=True)
        print(f"Ensured folder exists: {opt_dir}")
        
    # Get all files in brain_dir
    files = os.listdir(brain_dir)
    print(f"Found {len(files)} files in brain directory.")
    
    copied_count = 0
    for filename in files:
        if not filename.endswith(".png"):
            continue
            
        # Match pattern: e.g. curator_1_robot_1779337341576.png
        # We want to extract the prefix like "curator_1"
        match = re.match(r"^([a-z]+_\d+)_", filename)
        if match:
            prefix = match.group(1)
            if prefix in mappings:
                opt_folder, clean_name = mappings[prefix]
                src_path = os.path.join(brain_dir, filename)
                dest_path = os.path.join(public_base, opt_folder, clean_name)
                
                # Copy the file
                shutil.copy2(src_path, dest_path)
                print(f"Copied {filename} -> models/{opt_folder}/{clean_name}")
                copied_count += 1
                
    print(f"Completed! Successfully organized {copied_count} assets.")

if __name__ == "__main__":
    main()
