#!/usr/bin/env python3
import os
import re

# Base paths
WORKSPACE_DIR = "/Users/nathan/Daily Drip"
DOCS_DIR = os.path.join(WORKSPACE_DIR, "docs/clothing-ecommerce-design")
MOCKUP_FILE = os.path.join(DOCS_DIR, "pdp_mockup.html")

# All 8 products with their detailed custom content and model/theme universes
PRODUCTS_DATA = [
    {
        "id": "prod_robot_012",
        "filename": "pdp_outperformed_by_robot.html",
        "title": "Outperformed by a ROBOT. Again.",
        "seo_title": "Outperformed by a ROBOT. Again. Vintage Streetwear Tee",
        "price": "29.99",
        "badge": "TODAY'S DRIP #012",
        "sku": "DD-ROBOT-012",
        "theme": "arcteryx",
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
        "id": "prod_monkey_011",
        "filename": "pdp_punch_the_monkey.html",
        "title": "Punch the Monkey",
        "seo_title": "Punch the Monkey Vintage Graphic T-Shirt | Streetwear",
        "price": "29.99",
        "badge": "ARCHIVE #011",
        "sku": "DD-MONK-011",
        "theme": "daily-drip",
        "model_folder": "option1",
        "model_fit": "curator_2.png",
        "model_layered": "curator_5.png",
        "image_front": "/assets/flats/flat_monkey_front.png",
        "image_back": "/assets/flats/flat_monkey_back.png",
        "description": "Classic vintage vibes meets modern street expression. A playful take on cultural nostalgia, screen-printed on premium heavyweight organic cotton for a structured 90s vintage drape.",
        "vibe_story": "The 'Punch the Monkey' graphic captures a playful, high-contrast moment of digital culture—featuring a high-fidelity photographic print of a real baby monkey hugging an orange stuffed toy monkey. It strikes a sophisticated balance between emotional street aesthetics, retro toy design curation, and modern streetwear attitude. Recommended styling: layered under an open cardigan with pleated trousers.",
        "weight": "240 GSM Heavyweight",
        "composition": "100% Certified Organic Cotton",
        "printing": "Direct-To-Garment DTG Fluid Inks",
        "fit": "Boxy 90s Vintage Drape",
        "origin": "Printify Eco-Direct Production"
    },
    {
        "id": "prod_peace_010",
        "filename": "pdp_peace_sign.html",
        "title": "Peace Sign and Hands T-Shirt",
        "seo_title": "Peace Sign and Hands Streetwear Graphic T-Shirt",
        "price": "29.99",
        "badge": "ARCHIVE #010",
        "sku": "DD-PEACE-010",
        "theme": "kith",
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
        "id": "prod_sage_009",
        "filename": "pdp_sage_archives.html",
        "title": "Sage Archives Graphic Tee",
        "seo_title": "Sage Archives Clean Streetwear Graphic Tee",
        "price": "29.99",
        "badge": "VAULT #009",
        "sku": "DD-SAGE-009",
        "theme": "aime-leon-dore",
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
        "id": "prod_binary_008",
        "filename": "pdp_binary_genesis.html",
        "title": "Binary Genesis",
        "seo_title": "Binary Genesis Matrix Graphic Streetwear Tee",
        "price": "34.99",
        "badge": "VAULT #008",
        "sku": "DD-BINARY-008",
        "theme": "arcteryx",
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
        "id": "prod_vapor_007",
        "filename": "pdp_vaporwave_paradox.html",
        "title": "Vaporwave Paradox",
        "seo_title": "Vaporwave Paradox Glitch Art Graphic T-Shirt",
        "price": "29.99",
        "badge": "VAULT #007",
        "sku": "DD-VAPOR-007",
        "theme": "kith",
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
        "id": "prod_neural_006",
        "filename": "pdp_neural_echoes.html",
        "title": "Neural Echoes",
        "seo_title": "Neural Echoes Minimalist Graphic Streetwear Tee",
        "price": "29.99",
        "badge": "VAULT #006",
        "sku": "DD-NEURAL-006",
        "theme": "fear-of-god",
        "model_folder": "option2",
        "model_fit": "modernist_9_neural.png",
        "model_layered": "modernist_10_neural_layer.png",
        "image_front": "/assets/flats/flat_neural_front.png",
        "image_back": "/assets/flats/flat_neural_back.png",
        "description": "Intricate line-work conveying the residual signals of artificial minds. Thought-provoking and minimalist. Recommended styling: worn boxy over relaxed trousers with premium suede slides.",
        "vibe_story": "A study in quiet design. 'Neural Echoes' presents abstract, layered wireframes representing neural synapses firing in a sleeping machine. Designed with absolute restraint using neutral ink hues, it offers a deeply sophisticated, intellectual addition to standard graphic collections.",
        "weight": "240 GSM Heavyweight",
        "composition": "100% Certified Organic Cotton",
        "printing": "Direct-To-Garment DTG Fluid Inks",
        "fit": "Boxy 90s Vintage Drape",
        "origin": "Printify Eco-Direct Production"
    },
    {
        "id": "prod_pixel_005",
        "filename": "pdp_pixelated_soul.html",
        "title": "Pixelated Soul",
        "seo_title": "Pixelated Soul 8-Bit Deconstructed Graphic Tee",
        "price": "32.99",
        "badge": "VAULT #005",
        "sku": "DD-PIXEL-005",
        "theme": "daily-drip",
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

def load_template():
    with open(MOCKUP_FILE, "r", encoding="utf-8") as f:
        return f.read()

def generate_pdp(p, template):
    html = template
    
    # 1. Update <title> and description
    html = re.sub(
        r"<title>.*?</title>",
        f"<title>{p['seo_title']} | The Daily Drip</title>",
        html
    )
    html = re.sub(
        r'<meta name="description" content=".*?" />',
        f'<meta name="description" content="Vaulted Archive {p["badge"]}: {p["description"]}" />',
        html
    )
    
    # 2. Canonical and OG URL
    html = re.sub(
        r'<link rel="canonical" href=".*?" />',
        f'<link rel="canonical" href="https://daily-drip.club/products/{p["id"]}" />',
        html
    )
    html = re.sub(
        r'<meta property="og:url" content=".*?" />',
        f'<meta property="og:url" content="https://daily-drip.club/products/{p["id"]}" />',
        html
    )
    
    # 3. OG Metadata
    html = re.sub(
        r'<meta property="og:title" content=".*?" />',
        f'<meta property="og:title" content="{p["title"]} | The Daily Drip" />',
        html
    )
    html = re.sub(
        r'<meta property="og:description" content=".*?" />',
        f'<meta property="og:description" content="Vaulted Archive {p["badge"]}: {p["description"]}" />',
        html
    )
    html = re.sub(
        r'<meta property="og:image" content=".*?" />',
        f'<meta property="og:image" content="/assets/models/{p["model_folder"]}/{p["model_fit"]}" />',
        html
    )
    html = re.sub(
        r'<meta property="product:price:amount" content=".*?" />',
        f'<meta property="product:price:amount" content="{p["price"]}" />',
        html
    )
    
    # 4. JSON-LD structured data
    # We will search and replace the JSON block carefully.
    # To do this robustly, we can build a new JSON-LD string and replace it.
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
    
    # Replace the JSON script tag contents
    html = re.sub(
        r'<script type="application/ld\+json">.*?</script>',
        f'<script type="application/ld+json">\n  {json_ld}\n  </script>',
        html,
        flags=re.DOTALL
    )

    # 5. Default theme selection on <html> (Forced to daily-drip globally for design consistency)
    # html = re.sub(
    #     r'<html lang="en" class="theme-daily-drip">',
    #     f'<html lang="en" class="theme-{p["theme"]}">',
    #     html
    # )
    

    # 6. Gallery Images
    # First, let's map model names to aesthetic descriptors
    model_descriptors = {
        "option1": "CURATOR",
        "option2": "MODERNIST",
        "option3": "REBEL",
        "option4": "CYBER",
        "option5": "RETRO"
    }
    desc = model_descriptors[p["model_folder"]]
    
    # Establish static immersive brand badges based on theme and model style
    brand_badges = {
        'daily-drip': [f'01 // THE {desc} FIT', '02 // LAYERED STYLING', '03 // FLAT-LAY DETAIL', '04 // REVERSE STRUCTURE'],
        'aime-leon-dore': ['FIG. 1 // QUEENS CLASSIC FIT', 'FIG. 2 // EDITORIAL LOOK', 'FIG. 3 // COTTON DETAIL', 'FIG. 4 // BACK REVEAL'],
        'fear-of-god': [f'{desc} // 01 ON-MODEL', f'{desc} // 02 LAYERED', f'{desc} // 03 FLAT-LAY', f'{desc} // 04 STRUCTURE'],
        'kith': [f'DROP 004 // {desc} SHOT', f'DROP 004 // OUT-FIT STYLING', f'DROP 004 // FRONT FACE', f'DROP 004 // BACK SIDE'],
        'arcteryx': [f'DIAGNOSTIC // {desc}_FIT', 'DIAGNOSTIC // STACKED_LAYER', 'DIAGNOSTIC // ANTERIOR_FLAT', 'DIAGNOSTIC // POSTERIOR_FLAT']
    }
    
    active_badges = brand_badges['daily-drip']

    # Image 1 (Model front):
    html = re.sub(
        r'<!-- Image 01: Hook On-Model.*?<img src=".*?" alt=".*?">',
        f'<!-- Image 01: Hook On-Model (Option Fit) -->\n        <div class="gallery-img-wrapper">\n          <span class="gallery-badge" id="gallery-badge-1">{active_badges[0]}</span>\n          <img src="/assets/models/{p["model_folder"]}/{p["model_fit"]}" alt="{p["title"]} front fit on model">',
        html,
        flags=re.DOTALL
    )
    # Image 2 (Model layered):
    html = re.sub(
        r'<!-- Image 02: Styled Layering.*?<img src=".*?" alt=".*?">',
        f'<!-- Image 02: Styled Layering Outfit Context -->\n        <div class="gallery-img-wrapper">\n          <span class="gallery-badge" id="gallery-badge-2">{active_badges[1]}</span>\n          <img src="/assets/models/{p["model_folder"]}/{p["model_layered"]}" alt="Layered outfit featuring {p["title"]}">',
        html,
        flags=re.DOTALL
    )
    # Image 3 (Shopify front flat-lay):
    html = re.sub(
        r'<!-- Image 03: Flat-Lay Front.*?<img src=".*?" alt=".*?">',
        f'<!-- Image 03: Flat-Lay Front Detail -->\n        <div class="gallery-img-wrapper">\n          <span class="gallery-badge" id="gallery-badge-3">{active_badges[2]}</span>\n          <img src="{p["image_front"]}" alt="{p["title"]} front graphic flat-lay view">',
        html,
        flags=re.DOTALL
    )
    # Image 4 (Shopify back flat-lay):
    html = re.sub(
        r'<!-- Image 04: Flat-Lay Back.*?<img src=".*?" alt=".*?">',
        f'<!-- Image 04: Flat-Lay Back Detail -->\n        <div class="gallery-img-wrapper">\n          <span class="gallery-badge" id="gallery-badge-4">{active_badges[3]}</span>\n          <img src="{p["image_back"]}" alt="{p["title"]} reverse side view">',
        html,
        flags=re.DOTALL
    )

    # 7. Purchase details column (Price, title, badge, narrative)
    # Release badge:
    html = re.sub(
        r'<span class="release-badge" id="release-badge">.*?</span>',
        f'<span class="release-badge" id="release-badge">{p["badge"]}</span>',
        html
    )
    # Title:
    html = re.sub(
        r'<h1 class="product-title">.*?</h1>',
        f'<h1 class="product-title">{p["title"]}</h1>',
        html
    )
    # Price:
    html = re.sub(
        r'<span class="product-price">.*?</span>',
        f'<span class="product-price">${p["price"]}</span>',
        html
    )
    # Description:
    html = re.sub(
        r'<p class="product-narrative">.*?</p>',
        f'<p class="product-narrative">\n          {p["description"]}\n        </p>',
        html,
        flags=re.DOTALL
    )

    # 8. Accordion contents
    # Accordion 1 (Story & Vibe):
    html = re.sub(
        r'<!-- Accordion 1: Cultural Context.*?<div class="accordion-content-inner">.*?</div>.*?</div>.*?</div>',
        f'<!-- Accordion 1: Cultural Context -->\n          <div class="accordion-item active">\n            <button class="accordion-trigger" onclick="toggleAccordion(this)">\n              Product Story & Vibe\n              <span class="accordion-icon">+</span>\n            </button>\n            <div class="accordion-content" style="max-height: 100px;">\n              <div class="accordion-content-inner">\n                {p["vibe_story"]}\n              </div>\n            </div>\n          </div>',
        html,
        flags=re.DOTALL
    )
    # Accordion 2 (Specs):
    html = re.sub(
        r'<!-- Accordion 2: Specs.*?<div class="specs-monospace">.*?</div>.*?</div>.*?</div>.*?</div>',
        f'<!-- Accordion 2: Specs (Diagnostic Monospace Layout) -->\n          <div class="accordion-item">\n            <button class="accordion-trigger" onclick="toggleAccordion(this)">\n              Technical Specifications\n              <span class="accordion-icon">+</span>\n            </button>\n            <div class="accordion-content">\n              <div class="accordion-content-inner">\n                <div class="specs-monospace">\n                  <div class="specs-row">\n                    <span>WEIGHT // SLUB</span>\n                    <span>{p["weight"]}</span>\n                  </div>\n                  <div class="specs-row">\n                    <span>COMPOSITION // FABRIC</span>\n                    <span>{p["composition"]}</span>\n                  </div>\n                  <div class="specs-row">\n                    <span>PRINTING // INKS</span>\n                    <span>{p["printing"]}</span>\n                  </div>\n                  <div class="specs-row">\n                    <span>FIT // DRAFE</span>\n                    <span>{p["fit"]}</span>\n                  </div>\n                  <div class="specs-row">\n                    <span>PRODUCTION // ORIGIN</span>\n                    <span>{p["origin"]}</span>\n                  </div>\n                </div>\n              </div>\n            </div>\n          </div>',
        html,
        flags=re.DOTALL
    )

    # 9. Side Drawer details
    # Drawer cart-item image thumbnail:
    html = re.sub(
        r'<!-- Image from option1 model fit serves as thumbnail! -->.*?<img src=".*?" alt="Cart thumbnail" class="cart-item-img">',
        f'<!-- Image from option model fit serves as thumbnail! -->\n        <img src="/assets/models/{p["model_folder"]}/{p["model_fit"]}" alt="Cart thumbnail" class="cart-item-img">',
        html,
        flags=re.DOTALL
    )
    # Drawer item title:
    html = re.sub(
        r'<h4 class="cart-item-name">.*?</h4>',
        f'<h4 class="cart-item-name">{p["title"].upper()}</h4>',
        html
    )

    # 10. JavaScript state and functions replacement
    # Update pricePerUnit variable:
    html = re.sub(
        r'const pricePerUnit = \d+\.\d+;',
        f'const pricePerUnit = {p["price"]};',
        html
    )
    # Update Toast notification product name:
    html = re.sub(
        r'SUCCESS: Added PUNCH THE MONKEY',
        f'SUCCESS: Added {p["title"].upper()}',
        html
    )
    
    return html

def main():
    print("Loading base template...")
    template = load_template()
    
    for p in PRODUCTS_DATA:
        out_path = os.path.join(DOCS_DIR, p["filename"])
        print(f"Generating bespoke PDP for '{p['title']}' -> '{p['filename']}'...")
        pdp_html = generate_pdp(p, template)
        
        with open(out_path, "w", encoding="utf-8") as f:
            f.write(pdp_html)
            
    print("All PDPs generated successfully!")

if __name__ == "__main__":
    main()
