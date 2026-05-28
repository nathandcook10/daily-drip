import os
import sys
import json
import base64
import requests

PIPELINE_DIR = "pipeline_staging"
DARK_COLORS = ['black', 'navy', 'dark', 'charcoal', 'asphalt', 'maroon', 'forest', 'brown', 'oxblood', 'slate', 'iron', 'midnight']

def get_env_var(name):
    val = os.environ.get(name)
    if not val:
        print(f"Error: Environment variable '{name}' not set.")
        sys.exit(1)
    return val

def is_dark_variant(title):
    title = title.lower()
    return any(c in title for c in DARK_COLORS)

def upload_image(api_key, filepath):
    filename = os.path.basename(filepath)
    print(f"Uploading {filename} to Printify...")
    
    with open(filepath, "rb") as f:
        encoded_string = base64.b64encode(f.read()).decode("utf-8")
        
    url = "https://api.printify.com/v1/uploads/images.json"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    data = {
        "file_name": filename,
        "contents": encoded_string
    }
    
    response = requests.post(url, headers=headers, json=data)
    if response.status_code >= 400:
        print(f"Failed to upload {filename}: {response.text}")
        return None
        
    result = response.json()
    print(f"Successfully uploaded {filename}. ID: {result.get('id')}")
    return result.get("id")

def main():
    print("=== Phase 3: Printify Sync ===")
    
    api_key = get_env_var("PRINTIFY_API_TOKEN")
    shop_id = get_env_var("PRINTIFY_SHOP_ID")
    
    # 1. Identify local images
    images = {}
    for pos in ['front', 'back']:
        for mode in ['light', 'dark']:
            filename = f"{pos}_{mode}_ready.png"
            filepath = os.path.join(PIPELINE_DIR, filename)
            if os.path.exists(filepath):
                images[f"{pos}_{mode}"] = filepath
                
    if not images:
        print(f"Error: No baked canvases found in {PIPELINE_DIR}/")
        sys.exit(1)
        
    print(f"Found {len(images)} canvas(es): {', '.join(images.keys())}")
    
    # 2. Upload images to Printify
    upload_ids = {}
    for key, path in images.items():
        upload_id = upload_image(api_key, path)
        if upload_id:
            upload_ids[key] = upload_id
        else:
            print("Upload failed. Exiting.")
            sys.exit(1)
            
    # 3. Get Product ID from user
    product_id = input("\nEnter the Printify Product ID to sync: ").strip()
    if not product_id:
        print("Product ID is required.")
        sys.exit(1)
        
    # 4. Fetch the existing product
    print(f"\nFetching product {product_id}...")
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    url = f"https://api.printify.com/v1/shops/{shop_id}/products/{product_id}.json"
    response = requests.get(url, headers=headers)
    
    if response.status_code != 200:
        print(f"Failed to fetch product: {response.text}")
        sys.exit(1)
        
    product = response.json()
    print(f"Found product: {product.get('title')}")
    
    # 5. Build new print_areas by regrouping variants based on light/dark
    # We want to preserve existing placeholders (like neck, sleeves) while updating front/back
    
    variants = product.get('variants', [])
    old_print_areas = product.get('print_areas', [])
    
    # Map variant ID -> its old placeholders
    old_variant_placeholders = {}
    for pa in old_print_areas:
        for vid in pa.get('variant_ids', []):
            old_variant_placeholders[vid] = pa.get('placeholders', [])
            
    # Map variant ID -> new placeholders
    new_variant_placeholders = {}
    
    for variant in variants:
        vid = variant['id']
        title = variant.get('title', '')
        # Only process enabled variants, though we can map all of them
        is_dark = is_dark_variant(title)
        
        # Get old placeholders for this variant, default to empty
        placeholders = old_variant_placeholders.get(vid, [])
        # Deep copy to avoid reference sharing issues
        placeholders = json.loads(json.dumps(placeholders))
        
        # We need to make sure we update or add 'front' and 'back' placeholders
        # if we have images for them.
        for pos in ['front', 'back']:
            # Determine which image key to use
            if is_dark and f"{pos}_dark" in upload_ids:
                img_key = f"{pos}_dark"
            elif f"{pos}_light" in upload_ids:
                img_key = f"{pos}_light"
            elif f"{pos}_dark" in upload_ids:
                # fallback
                img_key = f"{pos}_dark"
            else:
                img_key = None
                
            if img_key:
                img_id = upload_ids[img_key]
                
                # Find existing placeholder for this position
                ph = next((p for p in placeholders if p.get('position') == pos), None)
                if ph:
                    # Update existing placeholder's images
                    ph['images'] = [{"id": img_id, "x": 0.5, "y": 0.5, "scale": 1.0, "angle": 0}]
                else:
                    # Add new placeholder
                    placeholders.append({
                        "position": pos,
                        "images": [{"id": img_id, "x": 0.5, "y": 0.5, "scale": 1.0, "angle": 0}]
                    })
            else:
                # No image provided for this position, so remove the placeholder entirely
                # This prevents old designs (like the back) from lingering when cloning products!
                placeholders = [p for p in placeholders if p.get('position') != pos]
                    
        # Filter out placeholders without images to prevent API validation errors (e.g. empty neck/sleeve)
        placeholders = [p for p in placeholders if p.get('images')]
        new_variant_placeholders[vid] = placeholders
        
    # Group variants by identical placeholders
    grouped_areas = {}
    for vid, ph in new_variant_placeholders.items():
        # Sort placeholders by position to ensure consistent JSON string
        ph_sorted = sorted(ph, key=lambda x: x.get('position', ''))
        ph_str = json.dumps(ph_sorted, sort_keys=True)
        if ph_str not in grouped_areas:
            grouped_areas[ph_str] = []
        grouped_areas[ph_str].append(vid)
        
    # Construct new print_areas array
    new_print_areas = []
    for ph_str, vids in grouped_areas.items():
        new_print_areas.append({
            "variant_ids": vids,
            "placeholders": json.loads(ph_str)
        })
        
    print(f"\nReconstructed {len(new_print_areas)} print area group(s) based on light/dark variants.")
    
    # 6. Update the product
    # The PUT endpoint requires a specific payload. We include the updated print_areas.
    # Other required fields: title, description, blueprint_id, print_provider_id, variants
    update_payload = {
        "title": product.get("title"),
        "description": product.get("description"),
        "blueprint_id": product.get("blueprint_id"),
        "print_provider_id": product.get("print_provider_id"),
        "variants": product.get("variants"),
        "print_areas": new_print_areas
    }
    
    print("\nPerforming surgical sync...")
    put_response = requests.put(url, headers=headers, json=update_payload)
    
    if put_response.status_code == 200:
        print("\nSuccess! Product successfully updated on Printify.")
    else:
        print(f"\nFailed to update product: {put_response.status_code}")
        print(put_response.text)

if __name__ == "__main__":
    main()
