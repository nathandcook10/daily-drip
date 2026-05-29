"""
LOCAL VTO PIPELINE SETUP INSTRUCTIONS
-------------------------------------
Virtual Try-On (VTO) locally requires significant computation. We are using a 
pure Python/Diffusers pipeline that leverages Hugging Face models to recreate 
the high-quality VTO without needing external APIs.

Because dedicated models like IDM-VTON require DensePose and Detectron2 (which 
are notoriously difficult to compile on Apple Silicon/Macs), this script uses a 
highly optimized, pure-diffusers approach that works seamlessly on Mac:

1.  Segformer Image Segmentation: Automatically identifies the exact pixels of the 
    clothing (the "Upper-clothes") to create a perfect pixel-level mask.
2.  Stable Diffusion Inpainting: Blends the t-shirt graphic perfectly into the 
    masked area, simulating realistic draping, folds, and lighting.

### Setup Instructions

1.  Create and activate a virtual environment:
    python3 -m venv vto_env
    source vto_env/bin/activate

2.  Install PyTorch with MPS (Apple Silicon/Metal) support:
    pip install --pre torch torchvision torchaudio --extra-index-url https://download.pytorch.org/whl/nightly/cpu

3.  Install necessary ML libraries:
    pip install diffusers transformers accelerate pillow scipy safetensors rembg

4.  Add some base photos to the `base_photos/` folder (the script will create it).
5.  Run the script! The first run will download model weights (~10GB+).

    python 4_local_vto.py
"""

import os
import glob
from PIL import Image
import torch
import numpy as np
from rembg import remove

# Diffusers & Transformers
from diffusers import AutoPipelineForInpainting
from transformers import SegformerImageProcessor, AutoModelForSemanticSegmentation

def setup_directories():
    """Create necessary directories if they don't exist."""
    os.makedirs("base_photos", exist_ok=True)
    os.makedirs("pipeline_staging", exist_ok=True)
    os.makedirs("final_pdp_assets", exist_ok=True)
    
def select_base_photo():
    """Let the user choose from a suite of base photos."""
    photos = glob.glob("base_photos/*.png") + glob.glob("base_photos/*.jpg") + glob.glob("base_photos/*.jpeg")
    if not photos:
        print("No base photos found in 'base_photos/' directory. Please add some model photos.")
        return None
        
    print("\n--- Available Base Photos ---")
    for i, p in enumerate(photos):
        print(f"[{i}] {p}")
        
    try:
        choice = int(input("\nSelect the base photo ID: "))
        return photos[choice]
    except (ValueError, IndexError):
        print("Invalid selection.")
        return None

def select_graphic():
    """Automatically selects the approved design graphic."""
    path = "pipeline_staging/approved_design.png"
    if not os.path.exists(path):
        print(f"Graphic not found at '{path}'. Please ensure Phase 1 completed successfully.")
        return None
    return path

def generate_semantic_mask(image_path):
    """
    Takes the base photo and automatically generates a garment mask using a 
    state-of-the-art Segformer trained specifically on clothing items.
    """
    print("\n[1/3] Generating semantic garment mask using Segformer...")
    
    # mattmdjaga/segformer_b2_clothes is an open-source model trained to parse human clothing
    processor = SegformerImageProcessor.from_pretrained("mattmdjaga/segformer_b2_clothes")
    model = AutoModelForSemanticSegmentation.from_pretrained("mattmdjaga/segformer_b2_clothes")
    
    image = Image.open(image_path).convert("RGB")
    inputs = processor(images=image, return_tensors="pt")
    
    with torch.no_grad():
        outputs = model(**inputs)
        
    # Scale the logits back to the original image size
    logits = outputs.logits.cpu()
    upsampled_logits = torch.nn.functional.interpolate(
        logits,
        size=image.size[::-1], # (height, width)
        mode="bilinear",
        align_corners=False,
    )
    
    # Get the predicted class for each pixel
    pred_seg = upsampled_logits.argmax(dim=1)[0].numpy()
    
    # Label 4 corresponds to 'Upper-clothes' in this dataset
    mask = np.zeros_like(pred_seg, dtype=np.uint8)
    mask[pred_seg == 4] = 255
    
    mask_image = Image.fromarray(mask).convert("L")
    return image, mask_image

def composite_graphic_for_inpainting(base_image, mask_image, graphic_path):
    """
    Overlays the graphic onto the base image in the masked region. 
    This composite serves as the "starting point" for the AI to understand 
    WHAT it is blending into the folds and shadows.
    """
    print("[2/3] Compositing graphic onto base photo...")
    
    # Load and remove background from graphic to prevent solid boxes
    raw_graphic = Image.open(graphic_path).convert("RGBA")
    print("      Removing background from graphic...")
    graphic = remove(raw_graphic)
    
    base = base_image.copy().convert("RGBA")
    
    # Calculate dimensions
    gw, gh = graphic.size
    bw, bh = base.size
    
    # Scale graphic to fit within the base photo's torso (roughly 40% of width)
    scale = min(bw/gw, bh/gh) * 0.4
    graphic = graphic.resize((int(gw*scale), int(gh*scale)), Image.LANCZOS)
    
    # Center placement
    x = (bw - graphic.width) // 2
    y = int(bh * 0.3) # Typically the chest area is around 30% down the image
    
    overlay = Image.new("RGBA", base.size, (0,0,0,0))
    overlay.paste(graphic, (x, y), graphic)
    
    # Combine
    composite = Image.alpha_composite(base, overlay).convert("RGB")
    return composite

def run_vto_pipeline(base_img, mask_img, composite_img):
    """
    Runs the Diffusers Inpainting pipeline to realistically blend the graphic 
    into the shirt, preserving lighting, identity, and adding realistic wrinkles.
    """
    print("[3/3] Loading VTO Diffusion Pipeline...")
    
    # Detect Apple Silicon (MPS), fallback to CPU or CUDA
    device = "mps" if torch.backends.mps.is_available() else "cpu"
    if torch.cuda.is_available(): 
        device = "cuda"
        
    print(f"Hardware acceleration: {device.upper()}")
    
    # SDXL Inpainting provides state-of-the-art photorealistic blending
    model_id = "diffusers/stable-diffusion-xl-1.0-inpainting-0.1"
    
    pipe = AutoPipelineForInpainting.from_pretrained(
        model_id,
        torch_dtype=torch.float16 if device != "cpu" else torch.float32,
        variant="fp16" if device != "cpu" else None,
        use_safetensors=True
    ).to(device)
    
    # Fix for SDXL VAE float16 math overflow on MPS (Black Image Bug)
    if device == "mps":
        print("      Using fp16-fix VAE to prevent MPS NaN black images...")
        from diffusers import AutoencoderKL
        pipe.vae = AutoencoderKL.from_pretrained("madebyollin/sdxl-vae-fp16-fix", torch_dtype=torch.float16).to(device)
    
    # Optimizations to save memory on Mac
    if device == "mps":
        pipe.enable_attention_slicing()
    
    # Prompt engineering for VTO
    prompt = (
        "Photorealistic, high quality, the graphic design is naturally printed on the t-shirt. "
        "The fabric drapes naturally, graphic conforms perfectly to folds, wrinkles, and shadows. "
        "The person's identity, pose, lighting, and background remain completely unchanged, masterpiece."
    )
    negative_prompt = (
        "distorted graphic, deformed face, changed background, changed person, "
        "illustration, lowres, text, watermark, bad anatomy, flat design"
    )
    
    print("Running diffusion generation (this will take time)...")
    
    # The 'strength' parameter is crucial. 
    # 0.0 = no change. 1.0 = completely overwrite.
    # ~0.6-0.75 gives the AI enough freedom to blend folds and shadows while keeping the graphic structure.
    result = pipe(
        prompt=prompt,
        negative_prompt=negative_prompt,
        image=composite_img,
        mask_image=mask_img,
        num_inference_steps=30,
        strength=0.65, 
        guidance_scale=7.5
    ).images[0]
    
    return result

def main():
    print(__doc__)
    setup_directories()
    
    base_path = select_base_photo()
    if not base_path: return
    
    graphic_path = select_graphic()
    if not graphic_path: return
    
    # 1. Masking
    base_image, mask_image = generate_semantic_mask(base_path)
    
    # Save the mask for debugging/visual check
    debug_mask_path = "final_pdp_assets/debug_garment_mask.png"
    mask_image.save(debug_mask_path)
    print(f"Saved debug semantic mask to {debug_mask_path}")
    
    # 2. Compositing
    composite = composite_graphic_for_inpainting(base_image, mask_image, graphic_path)
    
    # 3. Diffusion VTO
    final_image = run_vto_pipeline(base_image, mask_image, composite)
    
    # 4. Save
    graphic_filename = os.path.basename(graphic_path)
    base_filename = os.path.splitext(os.path.basename(base_path))[0]
    out_path = f"final_pdp_assets/vto_result_{base_filename}_{graphic_filename}"
    
    final_image.save(out_path)
    print(f"\n✅ Success! Saved photorealistic VTO to: {out_path}")

if __name__ == "__main__":
    main()
