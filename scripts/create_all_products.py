#!/usr/bin/env python3
import os
import sys
import json
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from daily_drip_manager import load_env
from printify_api import PrintifyClient

def main():
    load_env()
    shop_id = os.getenv("PRINTIFY_SHOP_ID")
    if not shop_id:
        print("❌ Error: PRINTIFY_SHOP_ID is not configured in .env")
        sys.exit(1)
        
    print(f"💧 [Daily Drip Batch Uploader] Initiating batch uploads for shop {shop_id}...")
    client = PrintifyClient()
    
    # The 5 archived products that need to be created on Printify
    products_to_create = [
        {
            "key": "prod_sage_009",
            "title": "Sage Archives Graphic Tee",
            "desc": "A calm organic streetwear catalog design with intelligence. Hand-printed on heavy cotton.",
            "design_url": "https://raw.githubusercontent.com/nathandcook10/daily-drip/main/Core%20Art/extracted/sage_front.png",
            "price": 29.99,
            "color": "Natural"
        },
        {
            "key": "prod_binary_008",
            "title": "Binary Genesis",
            "desc": "Visualizing the dawn of artificial cognition. A rich tapestry of binary matrices and biological forms.",
            "design_url": "https://raw.githubusercontent.com/nathandcook10/daily-drip/main/Core%20Art/extracted/binary_front.png",
            "price": 34.99,
            "color": "Black"
        },
        {
            "key": "prod_vapor_007",
            "title": "Vaporwave Paradox",
            "desc": "Glitch art aesthetic detailing consumerist nostalgia and cyberspace relics in neon slate.",
            "design_url": "https://raw.githubusercontent.com/nathandcook10/daily-drip/main/Core%20Art/extracted/vapor_front.png",
            "price": 29.99,
            "color": "Black"
        },
        {
            "key": "prod_neural_006",
            "title": "Neural Echoes",
            "desc": "Intricate line-work conveying the residual signals of artificial minds. Thought-provoking and minimalist.",
            "design_url": "https://raw.githubusercontent.com/nathandcook10/daily-drip/main/Core%20Art/extracted/neural_front.png",
            "price": 29.99,
            "color": "Olive"
        },
        {
            "key": "prod_pixel_005",
            "title": "Pixelated Soul",
            "desc": "Where classic human portraits meet 8-bit digital deconstruction. An ultimate expression of hybrid identity.",
            "design_url": "https://raw.githubusercontent.com/nathandcook10/daily-drip/main/Core%20Art/extracted/pixel_front.png",
            "price": 32.99,
            "color": "White"
        }
    ]
    
    results = {}
    
    for p in products_to_create:
        print(f"\n🎨 Pushing '{p['title']}'...")
        try:
            # 1. Upload Design Artwork
            file_name = f"{p['title'].replace(' ', '_')}_design.png"
            print(f"   - Uploading design: {p['design_url']}...")
            upload_res = client.upload_image(file_name, p["design_url"])
            image_id = upload_res["id"]
            print(f"   ✅ Uploaded. Image ID: {image_id}")
            
            # 2. Create Product
            print(f"   - Creating custom t-shirt (Color: {p['color']})...")
            product_res = client.create_daily_tshirt(
                shop_id=int(shop_id),
                title=p["title"],
                description=p["desc"],
                image_id=image_id,
                price_usd=p["price"],
                color_name=p["color"]
            )
            product_id = product_res["id"]
            mockup_url = product_res.get('images', [{}])[0].get('src', 'N/A')
            print(f"   ✅ Created Product! ID: {product_id}")
            print(f"   🔗 Mockup: {mockup_url}")
            
            results[p["key"]] = {
                "id": product_id,
                "title": p["title"],
                "mockup_url": mockup_url
            }
        except Exception as e:
            print(f"   ❌ Failed to create product '{p['title']}': {e}")
            
    print("\n🎉 BATCH UPLOADS COMPLETED!")
    print(json.dumps(results, indent=2))
    
    # Save the mapping file for easy reference
    with open("scripts/printify_created_mapping.json", "w") as f:
        json.dump(results, f, indent=2)

if __name__ == "__main__":
    main()
