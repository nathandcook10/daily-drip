# Prompt 05: Shopify to React PDP Schema Converter

Use this prompt when you have an existing product from a standard Shopify store (or a CSV export / raw details) that you want to migrate into our highly custom, premium Earth-Tone React storefront. It converts standard, basic product info into a rich, compliant, search-optimized component data block.

---

## 🔧 1. Parameters Checklist
Before copying the template, fill out these six key values. They are highlighted in **red emoji markers** inside the template below so you can locate them instantly.

*   <span style="color: #e11d48; font-weight: bold; font-size: 1.1em;">🔴 [SHOPIFY_TITLE] 🔴</span>: The current title of the product in Shopify.
*   <span style="color: #e11d48; font-weight: bold; font-size: 1.1em;">🔴 [SHOPIFY_DESCRIPTION] 🔴</span>: The current description text.
*   <span style="color: #e11d48; font-weight: bold; font-size: 1.1em;">🔴 [SHOPIFY_PRICE] 🔴</span>: Price of the product in Shopify (e.g. *29.99*).
*   <span style="color: #e11d48; font-weight: bold; font-size: 1.1em;">🔴 [SHOPIFY_SIZES] 🔴</span>: List of sizes (e.g. *S, M, L, XL*).
*   <span style="color: #e11d48; font-weight: bold; font-size: 1.1em;">🔴 [SHOPIFY_MAIN_IMAGE] 🔴</span>: URL to the primary Shopify product image.
*   <span style="color: #e11d48; font-weight: bold; font-size: 1.1em;">🔴 [SHOPIFY_OTHER_DETAILS] 🔴</span>: SKU, material weights, or print specifications.

---

## 📋 2. Copy-Paste Prompt Template

```text
Hi assistant! I need to migrate an existing apparel product from our Shopify catalog into our premium custom React storefront for "The Daily Drip".

Here are the raw product details from Shopify:
- Title: 🔴 [SHOPIFY_TITLE] 🔴
- Description: 🔴 [SHOPIFY_DESCRIPTION] 🔴
- Price: 🔴 [SHOPIFY_PRICE] 🔴
- Sizes Available: 🔴 [SHOPIFY_SIZES] 🔴
- Main Image URL: 🔴 [SHOPIFY_MAIN_IMAGE] 🔴
- Other Details: 🔴 [SHOPIFY_OTHER_DETAILS] 🔴

Please convert this basic product listing into our premium design standard:
1. ELEVATE COPYWRITING:
   - Rewrite the Shopify description. Turn it into a 2-3 sentence high-end brand narrative in the "Daily Drip" voice.
   - Extract fabric details and format them into uppercase monospace technical specs (GSM, cotton type, sustainability tags).

2. GENERATE REACT COMPONENT CODE:
   - Output the exact React product object structure to merge into `src/components/ProductList.jsx` or our storefront catalog.
   - Include variables for dynamic UI elements:
     - `availableSizes` mapped as chips.
     - `outOfStock` sizes styled at 35% opacity with the strike-through slash.
     - `images` mapped to our strict **3:4 Portrait Aspect Ratio** grid. Specify the dual-image source fields: `imgFlat` (garment flat-lay on load) and `imgModel` (editorial fit on hover).

3. SOCIAL & SEO SCHEMA GENERATION:
   - Generate the search-optimized `<title>` tag and open-graph tags (`og:title`, `og:description`, `og:image`, `og:price:amount`).
   - Construct the full JSON-LD structured schema block (`<script type="application/ld+json">`) mapped to Google's Product standard to unlock rich review and pricing snippets in Search.

Let's do the conversion! Please review the files `docs/clothing-ecommerce-design/playbook.md` and `docs/clothing-ecommerce-design/pdp_guidelines.md` first to guarantee full alignment with our e-commerce DNA.
```

---

## 💡 Pro-Tips for Nathan & Alby:
- Standard Shopify descriptions are often generic. This prompt automatically upgrades them into high-end fashion copywriting.
- When the AI generates the schema, it ensures that your new migrated product is instantly recognized by search engines, keeping your organic traffic flowing seamlessly.
