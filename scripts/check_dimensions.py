import os
from PIL import Image

def main():
    brain_dir = "/Users/nathan/.gemini/antigravity/brain/affe4f09-1adf-4c4a-8e08-54786009d8b9"
    flats_dir = "/Users/nathan/Daily Drip/Core Art/extracted"
    
    print("--- Model Blanks ---")
    blanks = [f for f in os.listdir(brain_dir) if "blank" in f and f.endswith(".png")]
    for b in sorted(blanks):
        img = Image.open(os.path.join(brain_dir, b))
        print(f"{b}: {img.size}")
        
    print("\n--- Extracted Graphics ---")
    flats = [f for f in os.listdir(flats_dir) if f.endswith(".png")]
    for f in sorted(flats):
        img = Image.open(os.path.join(flats_dir, f))
        print(f"{f}: {img.size}")

if __name__ == "__main__":
    main()
