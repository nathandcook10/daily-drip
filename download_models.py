import torch
from diffusers import AutoPipelineForInpainting
from transformers import SegformerImageProcessor, AutoModelForSemanticSegmentation

print("Downloading Segformer...")
processor = SegformerImageProcessor.from_pretrained("mattmdjaga/segformer_b2_clothes")
model = AutoModelForSemanticSegmentation.from_pretrained("mattmdjaga/segformer_b2_clothes")

print("Downloading SDXL Inpainting...")
pipe = AutoPipelineForInpainting.from_pretrained("diffusers/stable-diffusion-xl-1.0-inpainting-0.1", use_safetensors=True)

print("All models downloaded and cached successfully!")
