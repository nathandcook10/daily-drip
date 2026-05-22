# Prompt 03: Model Photoshoot & AI Mockup Brief Generator

Use this prompt when you need to create the visual assets for a new t-shirt drop. It translates our brand style guidelines and model lookbook rules into highly detailed, direct photography briefs for a real photoshoot, or generates high-fidelity text-to-image prompts for AI generators (like Midjourney, DALL-E, or Stable Diffusion) to create our catalog photos.

---

## 🔧 1. Parameters Checklist
Before copying the template, fill out these two key values. They are highlighted in **red emoji markers** inside the template below so you can locate them instantly.

*   <span style="color: #e11d48; font-weight: bold; font-size: 1.1em;">🔴 [PRODUCT_NAME] 🔴</span>: The name of your new streetwear item (e.g., *Sage Earth Block Tee*).
*   <span style="color: #e11d48; font-weight: bold; font-size: 1.1em;">🔴 [INSERT_THEME_E.G._ORGANIC_SAGE_LEAF_GRAPHIC] 🔴</span>: The visual elements and design concept (e.g., *a hand-drawn organic sage forest leaf graphic*).
*   <span style="color: #e11d48; font-weight: bold; font-size: 1.1em;">🔴 [VISUAL_PALETTE] 🔴</span>: The core colors to integrate into the scene (e.g., *warm cream backdrop, sage green cotton, forest green accents*).

---

## 📋 2. Copy-Paste Prompt Template

```text
Hi assistant! I need to generate a visual asset photoshoot brief and matching AI image-generation prompts for our upcoming streetwear drop called "🔴 [PRODUCT_NAME] 🔴".

First, please read and absorb our visual standard rules:
- docs/clothing-ecommerce-design/playbook.md
- docs/clothing-ecommerce-design/pdp_guidelines.md
- Daily_Drip_Model_Lookbook.pdf

Here are the product details:
- Product Theme/Artwork: 🔴 [INSERT_THEME_E.G._ORGANIC_SAGE_LEAF_GRAPHIC] 🔴
- Visual Palette: 🔴 [VISUAL_PALETTE] 🔴

Your task is to:
1. CREATE A PHOTO DIRECTORS BRIEF:
   - Outline the styling requirements for the model (e.g. pleated trousers, open cardigans, luxury loafers, vintage caps) matching the "Daily Drip" organic streetwear style.
   - Describe the required model postures (relaxed confidence, natural movement, never stiff or overly posed).
   - Specify the lighting temperature (warm, soft ambient light, natural film grain texture, no harsh studio flashes).

2. GENERATE HIGH-FIDELITY AI PROMPTS:
   - Provide 6 distinct, highly detailed text-to-image prompts (e.g. for Midjourney) corresponding to our strict **6-Step PDP Visual Storyboard**:
     - Image 01: On-Model Front Shot (Aspirational persona hook, relaxed pose, 3:4 portrait crop)
     - Image 02: On-Model Back Shot (Clear back view showing shoulder drape and graphic placement)
     - Image 03: Layered Outfit Styling Context (Full-body editorial shot showcasing the styled streetwear outfit)
     - Image 04: Macro Close-up Quality Proof (Focusing on stitch detail, 240 GSM organic cotton knit texture, neck ribbed collar)
     - Image 05: Profile Silhouette Drape (3/4 angle, side profile showing fabric weight and volume under slight motion)
     - Image 06: Lifestyle Ambient Context (Ambient street backdrop: e.g. brownstone stoop, warm library lounge, rain-slicked industrial brick plaza)
   
   - Ensure every AI prompt strictly requests:
     - A 3:4 portrait aspect ratio (e.g. `--ar 3:4` suffix for Midjourney).
     - Cinematic natural lighting, analog 35mm film aesthetic, subtle grain, warm color grading.
     - Brand color coordination (sage green, soft oatmeal backgrounds, deep forest greens).

Let's generate these visual briefs and prompt sets!
```

---

## 💡 Pro-Tips for Nathan & Alby:
- When you get the Midjourney or Stable Diffusion prompts from the AI, copy them directly into your image generator to produce extremely premium, high-converting models that represent your brand.
- Once generated, name the files standardly using `public/assets/...` paths (e.g. `curator_1.png` to `curator_6.png`) and drop them in the project folder to update the React catalog.
