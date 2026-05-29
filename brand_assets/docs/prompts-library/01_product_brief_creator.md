# Prompt 01: Product Brief Creator & Storefront Updater

Use this prompt when you want to launch a brand new product drop (e.g. a new graphic t-shirt). It forces the AI to check the brand playbook, follow the 6-step visual storyboard, write premium copywriting, and format the product data for our custom React storefront.

---

## 🔧 1. Parameters Checklist
Before copying the template, fill out these two key values. They are highlighted in **red emoji markers** inside the template below so you can locate them instantly.

*   <span style="color: #e11d48; font-weight: bold; font-size: 1.1em;">🔴 [PRODUCT_NAME] 🔴</span>: The name of your new streetwear item (e.g., *Sage Earth Block Tee*).
*   <span style="color: #e11d48; font-weight: bold; font-size: 1.1em;">🔴 [INSERT_DESIGN_CONCEPT_AND_ARTWORK_DETAILS_HERE] 🔴</span>: Explain the graphic and theme (e.g., *A minimal forest green leaf print with concrete charcoal accents, hand-drawn skateboard lines, and 'STREET GROWTH' typography*).

---

## 📋 2. Copy-Paste Prompt Template

```text
Hi assistant! We are launching a brand-new streetwear drop for "The Daily Drip" called "🔴 [PRODUCT_NAME] 🔴" and need you to program it into our custom storefront.

First, you MUST view and read our local brand design standards in:
- Brand Playbook & DNA Profiles: docs/clothing-ecommerce-design/playbook.md
- PDP Conversion & Visual Storyboard Blueprint: docs/clothing-ecommerce-design/pdp_guidelines.md
- Visual Brand Lookbook: Daily_Drip_Model_Lookbook.pdf

Your task is to:
1. DESIGN THE PRODUCT BRIEF:
   - Identify the design concept: 🔴 [INSERT_DESIGN_CONCEPT_AND_ARTWORK_DETAILS_HERE] 🔴
   - Write a high-converting, premium narrative description in the Daily Drip voice (2-3 sentences).
   - Generate technical specifications in uppercase Monospace standard (e.g., GSM weight, fabric type, eco certifications, print method).
   
2. CODE THE STOREFRONT COMPONENT UPDATE:
   - Generate the React data block or list entry to add this product to the storefront catalog (typically in `src/components/ProductList.jsx` or similar).
   - Ensure the card utilizes the dual-image cross-fade hover reveal (flat-lay on load -> on-model fit shot on pointer hover) using standard aspect-ratio: 3/4.
   
3. BUILD THE PDP STORYBOARD SCHEMA:
   - Detail the 6-step visual storyboard gallery sequence for this item:
     - Image 01: On-Model Front Shot (Aspirational persona hook)
     - Image 02: On-Model Back Shot (Structural branding detail)
     - Image 03: Layered Outfit Styling Context
     - Image 04: Macro Close-up Quality Proof
     - Image 05: Profile Silhouette Drape
     - Image 06: Lifestyle Ambient Context
   - Include high-fidelity semantic alt texts for all 6 storyboard images.
   
4. SEO & SOCIAL METADATA:
   - Output the `<title>` tag structured for high-intent search (e.g. "[PRODUCT_NAME] Vintage Streetwear Graphic T-Shirt | The Daily Drip").
   - Output the `<meta name="description">` and `<meta property="og:*">` tags.
   - Generate the search engine rich-snippet schema (`<script type="application/ld+json">`).

Let's begin! Please read the files first and present the design proposal for my final approval before modifying the codebase.
```

---

## 💡 Pro-Tips for Nathan & Alby:
- When the AI outputs the React component update, you can immediately tell it: *"Looks perfect! Go ahead and write this update to `src/components/ProductList.jsx`."*
