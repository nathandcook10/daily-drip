#!/usr/bin/env python3
import os
import re

TEMPLATE_FILE = "/Users/nathan/Daily Drip/docs/clothing-ecommerce-design/pdp_punch_the_monkey.html"
DOCS_DIR = "/Users/nathan/Daily Drip/docs/clothing-ecommerce-design"

PRODUCTS_DATA = [
    {
        "id": "69c856f897378918e2031d54",
        "filename": "pdp_outperformed_by_robot.html",
        "slug": "outperformed_by_robot",
        "title": "Outperformed by a ROBOT. Again.",
        "seo_title": "Outperformed by a ROBOT. Again. Vintage Streetwear Tee",
        "price": "29.99",
        "badge": "TODAY'S DRIP #012",
        "sku": "DD-ROBOT-012",
        "model_folder": "option4",
        "model_fit": "cyber_1.png",
        "model_layered": "cyber_4.png",
        "image_front": "/assets/flats/flat_robot_front.png",
        "image_back": "/assets/flats/flat_robot_back.png",
        "description": "A bold streetwear graphic celebrating the inevitable takeover of our digital counterparts. Outperformed, but stylish. Recommended styling: layered under a tech shell jacket with industrial tactical trousers.",
        "vibe_story": "Celebrating the creative tension between biological intelligence and digital algorithmics. 'Outperformed by a ROBOT. Again.' is a witty, self-aware commentary on machine learning, set in high-contrast technical typography and neon accents. Built to project an avant-garde digital posture.",
        "weight": "240 GSM Heavyweight",
        "composition": "100% Certified Organic Cotton",
        "printing": "Direct-To-Garment DTG Fluid Inks",
        "fit": "Boxy 90s Vintage Drape",
        "origin": "Printify Eco-Direct Production"
    },
    {
        "id": "69d1b80c2e352db3e70cf7c5",
        "filename": "pdp_peace_sign.html",
        "slug": "peace_sign",
        "title": "Peace Sign and Hands T-Shirt",
        "seo_title": "Peace Sign and Hands Streetwear Graphic T-Shirt",
        "price": "29.99",
        "badge": "ARCHIVE #010",
        "sku": "DD-PEACE-010",
        "model_folder": "option3",
        "model_fit": "rebel_3.png",
        "model_layered": "rebel_6.png",
        "image_front": "/assets/flats/flat_peace_front.png",
        "image_back": "/assets/flats/flat_peace_back.png",
        "description": "Iconic streetwear symbol of peace, connection, and visual expression. An elegant dark-mode fit. Recommended styling: layered over a premium long-sleeve mesh shirt with box-pleated canvas trousers.",
        "vibe_story": "A bold visual statement capturing iconic hand-drawn peace sign iconography. By blending raw subculture brushstrokes with soft typography, it speaks directly to our shared human connection. It projects a relaxed, authentic confidence suited for modern street style.",
        "weight": "240 GSM Heavyweight",
        "composition": "100% Certified Organic Cotton",
        "printing": "Direct-To-Garment DTG Fluid Inks",
        "fit": "Boxy 90s Vintage Drape",
        "origin": "Printify Eco-Direct Production"
    },
    {
        "id": "6a1121add4d1eee5d1083056",
        "filename": "pdp_sage_archives.html",
        "slug": "sage_archives",
        "title": "Sage Archives Graphic Tee",
        "seo_title": "Sage Archives Clean Streetwear Graphic Tee",
        "price": "29.99",
        "badge": "VAULT #009",
        "sku": "DD-SAGE-009",
        "model_folder": "option2",
        "model_fit": "modernist_7_sage.png",
        "model_layered": "modernist_8_sage_layer.png",
        "image_front": "/assets/flats/flat_sage_front.png",
        "image_back": "/assets/flats/flat_sage_back.png",
        "description": "A calm organic streetwear catalog design with intelligence. Hand-printed on heavy cotton. Recommended styling: best paired with cream-toned knitted cardigans or heavy duck canvas carpenters.",
        "vibe_story": "The core catalog piece of our organic street line. 'Sage Archives' showcases clean typography and minimal branding layouts, emphasizing a calm, modern intelligence. A versatile wardrobe staple designed for long-term comfort and timeless visual appeal.",
        "weight": "240 GSM Heavyweight",
        "composition": "100% Certified Organic Cotton",
        "printing": "Direct-To-Garment DTG Fluid Inks",
        "fit": "Boxy 90s Vintage Drape",
        "origin": "Printify Eco-Direct Production"
    },
    {
        "id": "6a1121b24a67803eff0228ad",
        "filename": "pdp_binary_genesis.html",
        "slug": "binary_genesis",
        "title": "Binary Genesis",
        "seo_title": "Binary Genesis Matrix Graphic Streetwear Tee",
        "price": "34.99",
        "badge": "VAULT #008",
        "sku": "DD-BINARY-008",
        "model_folder": "option4",
        "model_fit": "cyber_7_binary.png",
        "model_layered": "cyber_8_binary_back.png",
        "image_front": "/assets/flats/flat_binary_front.png",
        "image_back": "/assets/flats/flat_binary_back.png",
        "description": "Visualizing the dawn of artificial cognition. A rich tapestry of binary matrices and biological forms. Recommended styling: layered with dark, technical windbreakers and high-performance trail shoes.",
        "vibe_story": "Exploring the synthesis of computational mathematics and biological evolution. 'Binary Genesis' superimposes dense blocks of green matrix code over organic flora layouts, symbolizing the dawn of silicon-based consciousness. An ultimate graphic for the technologist-streetwear enthusiast.",
        "weight": "240 GSM Heavyweight",
        "composition": "100% Certified Organic Cotton",
        "printing": "Direct-To-Garment DTG Fluid Inks",
        "fit": "Boxy 90s Vintage Drape",
        "origin": "Printify Eco-Direct Production"
    },
    {
        "id": "6a1121b7a8fde5fbe80e64b5",
        "filename": "pdp_vaporwave_paradox.html",
        "slug": "vaporwave_paradox",
        "title": "Vaporwave Paradox",
        "seo_title": "Vaporwave Paradox Glitch Art Graphic T-Shirt",
        "price": "29.99",
        "badge": "VAULT #007",
        "sku": "DD-VAPOR-007",
        "model_folder": "option5",
        "model_fit": "retro_7_vapor.png",
        "model_layered": "retro_8_vapor_layer.png",
        "image_front": "/assets/flats/flat_vapor_front.png",
        "image_back": "/assets/flats/flat_vapor_back.png",
        "description": "Glitch art aesthetic detailing consumerist nostalgia and cyberspace relics in neon slate. Recommended styling: paired with baggy vintage track pants and retro bulky runners.",
        "vibe_story": "A beautiful design paradox exploring obsolete hardware culture and early cyberspace memory. Featuring high-contrast pink-to-cyan neon chromatic glitches on a sleek charcoal canvas, it bridges nostalgic vaporwave art with modern street volumes.",
        "weight": "240 GSM Heavyweight",
        "composition": "100% Certified Organic Cotton",
        "printing": "Direct-To-Garment DTG Fluid Inks",
        "fit": "Boxy 90s Vintage Drape",
        "origin": "Printify Eco-Direct Production"
    },
    {
        "id": "6a1121bc674926aa27006347",
        "filename": "pdp_neural_echoes.html",
        "slug": "neural_echoes",
        "title": "Neural Echoes",
        "seo_title": "Neural Echoes Minimalist Graphic Streetwear Tee",
        "price": "29.99",
        "badge": "VAULT #006",
        "sku": "DD-NEURAL-006",
        "model_folder": "option2",
        "model_fit": "modernist_9_neural.png",
        "model_layered": "modernist_10_neural_layer.png",
        "image_front": "/assets/flats/flat_neural_front.png",
        "image_back": "/assets/flats/flat_neural_back.png",
        "description": "Intricate line-work conveying the residual signals of artificial minds. Thought-provoking and minimalist. Recommended styling: worn boxy over relaxed trousers with premium suede slides.",
        "vibe_story": "A study in quiet design. 'Neural Echoes' presents abstract, layered wireframes representing neural synapses firing in sleeping machines. Designed with absolute restraint using neutral ink hues, it offers a deeply sophisticated, intellectual addition to standard graphic collections.",
        "weight": "240 GSM Heavyweight",
        "composition": "100% Certified Organic Cotton",
        "printing": "Direct-To-Garment DTG Fluid Inks",
        "fit": "Boxy 90s Vintage Drape",
        "origin": "Printify Eco-Direct Production"
    },
    {
        "id": "6a1121c14a67803eff0228bb",
        "filename": "pdp_pixelated_soul.html",
        "slug": "pixelated_soul",
        "title": "Pixelated Soul",
        "seo_title": "Pixelated Soul 8-Bit Deconstructed Graphic Tee",
        "price": "32.99",
        "badge": "VAULT #005",
        "sku": "DD-PIXEL-005",
        "model_folder": "option5",
        "model_fit": "retro_9_pixel.png",
        "model_layered": "retro_10_pixel_layer.png",
        "image_front": "/assets/flats/flat_pixel_front.png",
        "image_back": "/assets/flats/flat_pixel_back.png",
        "description": "Where classic human portraits meet 8-bit digital deconstruction. An ultimate expression of hybrid identity. Recommended styling: layered with technical utility vests and chunky retro trainers.",
        "vibe_story": "Highlighting the beautiful friction between human emotion and digital abstraction. 'Pixelated Soul' features a traditional oil-painted portrait block fading into distinct, digital 8-bit squares, representing our evolving hybrid identities. A unique design statement on a premium organic canvas.",
        "weight": "240 GSM Heavyweight",
        "composition": "100% Certified Organic Cotton",
        "printing": "Direct-To-Garment DTG Fluid Inks",
        "fit": "Boxy 90s Vintage Drape",
        "origin": "Printify Eco-Direct Production"
    }
]

def assert_replace(content, pattern, replacement, flags=0):
    match = re.search(pattern, content, flags=flags)
    if not match:
        raise ValueError(f"Pattern not found: {pattern}")
    return re.sub(pattern, replacement, content, flags=flags)

def main():
    print(f"Reading template file: {TEMPLATE_FILE}")
    with open(TEMPLATE_FILE, "r", encoding="utf-8") as f:
        template = f.read()

    for p in PRODUCTS_DATA:
        out_file = os.path.join(DOCS_DIR, p["filename"])
        print(f"Processing: {p['title']} -> {p['filename']}")

        content = template

        # 1. Update logo link src (plain replace)
        content = content.replace('../../Core Art/logo-long.png', '/assets/logo-long.png')
        content = content.replace('/Core Art/logo-long.png', '/assets/logo-long.png')

        # 2. Update head titles, descriptions, links, OG tags
        content = assert_replace(
            content,
            r"<title>.*?</title>",
            f"<title>{p['seo_title']} | The Daily Drip</title>"
        )
        content = assert_replace(
            content,
            r'<meta name="description" content=".*?" />',
            f'<meta name="description" content="Vaulted Archive {p["badge"]}: {p["description"]}" />'
        )
        content = assert_replace(
            content,
            r'<link rel="canonical" href=".*?" />',
            f'<link rel="canonical" href="https://daily-drip.club/products/{p["id"]}" />'
        )
        content = assert_replace(
            content,
            r'<meta property="og:url" content=".*?" />',
            f'<meta property="og:url" content="https://daily-drip.club/products/{p["id"]}" />'
        )
        content = assert_replace(
            content,
            r'<meta property="og:title" content=".*?" />',
            f'<meta property="og:title" content="{p["title"]} | The Daily Drip" />'
        )
        content = assert_replace(
            content,
            r'<meta property="og:description" content=".*?" />',
            f'<meta property="og:description" content="Vaulted Archive {p["badge"]}: {p["description"]}" />'
        )
        content = assert_replace(
            content,
            r'<meta property="og:image" content=".*?" />',
            f'<meta property="og:image" content="/assets/models/{p["model_folder"]}/{p["model_fit"]}" />'
        )
        content = assert_replace(
            content,
            r'<meta property="product:price:amount" content=".*?" />',
            f'<meta property="product:price:amount" content="{p["price"]}" />'
        )

        # 3. JSON-LD structured data block
        json_ld = f"""{{
    "@context": "https://schema.org/",
    "@type": "Product",
    "name": "{p['title']}",
    "image": [
      "/assets/models/{p['model_folder']}/{p['model_fit']}",
      "/assets/models/{p['model_folder']}/{p['model_layered']}"
    ],
    "description": "Vaulted Archive {p['badge']}: {p['description']}",
    "sku": "{p['sku']}",
    "mpn": "{p['sku']}",
    "brand": {{
      "@type": "Brand",
      "name": "The Daily Drip"
    }},
    "offers": {{
      "@type": "Offer",
      "url": "https://daily-drip.club/products/{p['id']}",
      "priceCurrency": "USD",
      "price": "{p['price']}",
      "priceValidUntil": "2027-12-31",
      "itemCondition": "https://schema.org/NewCondition",
      "availability": "https://schema.org/InStock",
      "seller": {{
        "@type": "Organization",
        "name": "The Daily Drip"
      }}
    }}
  }}"""
        content = assert_replace(
            content,
            r'<script type="application/ld\+json">.*?</script>',
            f'<script type="application/ld+json">\n  {json_ld}\n  </script>',
            flags=re.DOTALL
        )

        # 4. Replace left scrollable portrait gallery
        gallery_html = f"""<!-- ==========================================================================
         LEFT: Scrollable Portrait Image Gallery (Best Practice #1)
         ========================================================================== -->
      <section class="pdp-gallery" aria-label="Product Image Gallery">
        
        <!-- Image 01: Flat-Lay Front -->
        <div class="gallery-img-wrapper">
          <span class="gallery-badge">01 // FLAT LAY FRONT</span>
          <img src="{p['image_front']}" alt="{p['title']} flat lay front" id="gallery-img-flat-front">
        </div>

        <!-- Image 02: Flat-Lay Back -->
        <div class="gallery-img-wrapper">
          <span class="gallery-badge">02 // FLAT LAY BACK</span>
          <img src="{p['image_back']}" alt="{p['title']} flat lay back" id="gallery-img-flat-back">
        </div>
        
        <!-- Image 03: The Hook — On-Model Front -->
        <div class="gallery-img-wrapper">
          <span class="gallery-badge">03 // THE HOOK</span>
          <img src="/assets/models/{p['model_folder']}/{p['model_fit']}" alt="{p['title']} on-model front hook shot" id="gallery-img-hook">
        </div>

        <!-- Image 04: The Structure — On-Model Back -->
        <div class="gallery-img-wrapper">
          <span class="gallery-badge">04 // THE STRUCTURE</span>
          <img src="/assets/editorial/{p['slug']}/structure_back.png" alt="{p['title']} on-model back structure shot" id="gallery-img-structure">
        </div>

        <!-- Image 05: The Style — Layered Outfit Context -->
        <div class="gallery-img-wrapper">
          <span class="gallery-badge">05 // THE STYLE</span>
          <img src="/assets/models/{p['model_folder']}/{p['model_layered']}" alt="{p['title']} layered outfit styling" id="gallery-img-style">
        </div>

        <!-- Image 06: The Fabric Truss — Macro Close-Up -->
        <div class="gallery-img-wrapper">
          <span class="gallery-badge">06 // FABRIC TRUSS</span>
          <img src="/assets/editorial/{p['slug']}/fabric_truss.png" alt="{p['title']} fabric and print macro detail" id="gallery-img-fabric">
        </div>

        <!-- Image 07: The Silhouette — 3/4 Drape Angle -->
        <div class="gallery-img-wrapper">
          <span class="gallery-badge">07 // SILHOUETTE</span>
          <img src="/assets/editorial/{p['slug']}/silhouette.png" alt="{p['title']} silhouette drape profile" id="gallery-img-silhouette">
        </div>

        <!-- Image 08: The Life — Ambient Lifestyle -->
        <div class="gallery-img-wrapper">
          <span class="gallery-badge">08 // THE LIFE</span>
          <img src="/assets/editorial/{p['slug']}/the_life.png" alt="{p['title']} lifestyle ambient shot" id="gallery-img-life">
        </div>

      </section>"""

        content = assert_replace(
            content,
            r'<!-- ==========================================================================\s+LEFT: Scrollable Portrait Image Gallery.*?-->\s*<section class="pdp-gallery".*?>.*?</section>',
            gallery_html,
            flags=re.DOTALL
        )

        # 5. Purchase Sticky column details
        # Release badge:
        content = assert_replace(
            content,
            r'<span class="release-badge" id="release-badge">.*?</span>',
            f'<span class="release-badge" id="release-badge">{p["badge"]}</span>'
        )
        # Title:
        content = assert_replace(
            content,
            r'<h1 class="product-title">.*?</h1>',
            f'<h1 class="product-title">{p["title"]}</h1>'
        )
        # Price:
        content = assert_replace(
            content,
            r'<span class="product-price">.*?</span>',
            f'<span class="product-price">${p["price"]}</span>'
        )
        # Narrative description:
        content = assert_replace(
            content,
            r'<p class="product-narrative">.*?</p>',
            f'<p class="product-narrative">\n          {p["description"]}\n        </p>',
            flags=re.DOTALL
        )

        # 6. Accordions (fully clean and correct, removing legacy duplicates)
        accordions_html = f"""<!-- Product specifications & drop circular accordion information -->
        <div class="accordions-container">
          
          <!-- Accordion 1: Cultural Context -->
          <div class="accordion-item active">
            <button class="accordion-trigger" onclick="toggleAccordion(this)">
              Product Story & Vibe
              <span class="accordion-icon">+</span>
            </button>
            <div class="accordion-content" style="max-height: 100px;">
              <div class="accordion-content-inner">
                {p["vibe_story"]}
              </div>
            </div>
          </div>

          <!-- Accordion 2: Specs (Diagnostic Monospace Layout) -->
          <div class="accordion-item">
            <button class="accordion-trigger" onclick="toggleAccordion(this)">
              Technical Specifications
              <span class="accordion-icon">+</span>
            </button>
            <div class="accordion-content">
              <div class="accordion-content-inner">
                <div class="specs-monospace">
                  <div class="specs-row">
                    <span>WEIGHT // SLUB</span>
                    <span>{p["weight"]}</span>
                  </div>
                  <div class="specs-row">
                    <span>COMPOSITION // FABRIC</span>
                    <span>{p["composition"]}</span>
                  </div>
                  <div class="specs-row">
                    <span>PRINTING // INKS</span>
                    <span>{p["printing"]}</span>
                  </div>
                  <div class="specs-row">
                    <span>FIT // DRAFE</span>
                    <span>{p["fit"]}</span>
                  </div>
                  <div class="specs-row">
                    <span>PRODUCTION // ORIGIN</span>
                    <span>{p["origin"]}</span>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <!-- Accordion 3: Zero-Waste Cycle -->
          <div class="accordion-item">
            <button class="accordion-trigger" onclick="toggleAccordion(this)">
              Zero-Waste Drop Cycle
              <span class="accordion-icon">+</span>
            </button>
            <div class="accordion-content">
              <div class="accordion-content-inner">
                To combat fashion excess, Daily Drip operates on a strict zero-waste printing model. Products are manufactured on-demand directly via organic direct-to-garment Printify setups once ordered. This vaulted archive edition is highly exclusive: once vault doors close, it will never be printed again.
              </div>
            </div>
          </div>

        </div>"""

        content = assert_replace(
            content,
            r'<!-- Product specifications & drop circular accordion information -->.*?<\/section>',
            accordions_html + "\n\n      </section>",
            flags=re.DOTALL
        )

        # 7. Side drawer updates
        content = assert_replace(
            content,
            r'<h4 class="cart-item-name">.*?</h4>',
            f'<h4 class="cart-item-name">{p["title"].upper()}</h4>'
        )
        content = assert_replace(
            content,
            r'<img src="/assets/models/[^"]+" alt="Cart thumbnail" class="cart-item-img" id="cart-item-thumbnail">',
            f'<img src="/assets/models/{p["model_folder"]}/{p["model_fit"]}" alt="Cart thumbnail" class="cart-item-img" id="cart-item-thumbnail">'
        )

        # 8. JavaScript replacements
        content = assert_replace(
            content,
            r'const pricePerUnit = \d+\.\d+;',
            f'const pricePerUnit = {p["price"]};'
        )
        
        # Replace Toast success message
        content = content.replace('SUCCESS: Added PUNCH THE MONKEY', f'SUCCESS: Added {p["title"].upper()}')

        # Color picker toggle function body
        color_function_js = f"""function setProductColor(color, element) {{
      selectedColor = color;
      
      // Update Swatches active state
      document.querySelectorAll('.color-swatch-btn').forEach(btn => btn.classList.remove('active'));
      element.classList.add('active');
      
      // Update label
      document.getElementById('active-color-label').textContent = color.toUpperCase();
      
      // Swap colorway-sensitive gallery images (use the default ones as there are no separate files for other products)
      document.getElementById('gallery-img-flat-front').src = `{p['image_front']}`;
      document.getElementById('gallery-img-flat-back').src = `{p['image_back']}`;
      document.getElementById('gallery-img-hook').src = `/assets/models/{p['model_folder']}/{p['model_fit']}`;
      document.getElementById('gallery-img-style').src = `/assets/models/{p['model_folder']}/{p['model_layered']}`;
      
      // Update cart drawer thumbnail proactively so if opened it's correct
      document.getElementById('cart-item-thumbnail').src = `/assets/models/{p['model_folder']}/{p['model_fit']}`;
      
      triggerToast(`Color Switched to: ${{color.toUpperCase()}}`);
    }}"""

        content = assert_replace(
            content,
            r'function setProductColor\(color, element\)\s*\{.*?triggerToast\(`Color Switched to: \${color\.toUpperCase\(\)}`\);\s*\n\s*\}',
            color_function_js,
            flags=re.DOTALL
        )

        # AddToBag image update
        content = assert_replace(
            content,
            r"document\.getElementById\('cart-item-thumbnail'\)\.src = `/assets/models/option1/curator_2_\$\{selectedColor\}\.png`;",
            f"document.getElementById('cart-item-thumbnail').src = `/assets/models/{p['model_folder']}/{p['model_fit']}`;",
            flags=re.DOTALL
        )

        # Checkout simulation image reset
        initiate_checkout_resets = f"""// Reset colorway-sensitive images
      document.getElementById('gallery-img-flat-front').src = `{p['image_front']}`;
      document.getElementById('gallery-img-flat-back').src = `{p['image_back']}`;
      document.getElementById('gallery-img-hook').src = `/assets/models/{p['model_folder']}/{p['model_fit']}`;
      document.getElementById('gallery-img-style').src = `/assets/models/{p['model_folder']}/{p['model_layered']}`;
      
      document.getElementById('cart-item-thumbnail').src = `/assets/models/{p['model_folder']}/{p['model_fit']}`;"""

        content = assert_replace(
            content,
            r'// Reset colorway-sensitive images.*?document\.getElementById\(\'cart-item-thumbnail\'\)\.src = `/assets/models/option1/curator_2_black\.png`;',
            initiate_checkout_resets,
            flags=re.DOTALL
        )

        # Save to output file
        with open(out_file, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"✅ Generated high-fidelity PDP: {out_file}")

    print("All 7 T-shirt PDPs successfully updated to Design V2.5!")

if __name__ == "__main__":
    main()
