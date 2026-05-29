from rembg import remove
from PIL import Image

for path, out_path in [
    ("/Users/nathan/.gemini/antigravity/brain/a7767c39-388d-46af-bb4c-46ac48de3fdd/concept_1_1780015943207.png", "pipeline_staging/approved_back.png"),
    ("/Users/nathan/.gemini/antigravity/brain/a7767c39-388d-46af-bb4c-46ac48de3fdd/concept_front_1780015990101.png", "pipeline_staging/approved_front.png")
]:
    img = Image.open(path)
    out = remove(img)
    out.save(out_path)
