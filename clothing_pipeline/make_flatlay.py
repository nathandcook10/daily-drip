from PIL import Image
import glob

flatlay_path = glob.glob('/Users/nathan/.gemini/antigravity/brain/a7767c39-388d-46af-bb4c-46ac48de3fdd/blank_white_flatlay_*.png')[0]
flatlay = Image.open(flatlay_path).convert("RGBA")
design = Image.open('pipeline_staging/approved_design.png').convert("RGBA")

# Resize design to fit nicely on the chest (e.g., width 400px on a 1024x1024 flatlay)
design.thumbnail((400, 400))
w, h = design.size

# Calculate chest coordinates
x = (flatlay.width - w) // 2
y = 300

flatlay.paste(design, (x, y), design)
flatlay.save('pipeline_staging/white_tshirt_with_graphic.png')
print("Saved pipeline_staging/white_tshirt_with_graphic.png")
