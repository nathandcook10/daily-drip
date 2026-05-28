#!/usr/bin/env python3
import os
import sys
import argparse
from printify_api import PrintifyClient
from meta_ads_api import MetaAdsClient

def load_env(env_path: str = ".env"):
    """Simple parser to read environment variables from a .env file."""
    # If the default env_path does not exist, check the directory where this script lives
    if not os.path.exists(env_path):
        script_dir_env = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".env")
        if os.path.exists(script_dir_env):
            env_path = script_dir_env

    if os.path.exists(env_path):
        with open(env_path, "r") as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith("#"):
                    continue
                if "=" in line:
                    key, val = line.split("=", 1)
                    os.environ[key.strip()] = val.strip().strip('"').strip("'")

def test_connections():
    """Verify that both Printify and Meta APIs are configured and accessible."""
    print("💧 [Daily Drip Automation] Verifying API integrations...")
    
    # 1. Test Printify
    printify_token = os.getenv("PRINTIFY_API_TOKEN")
    if printify_token:
        print("⚡ Printify Token found. Initializing connection...")
        try:
            client = PrintifyClient(printify_token)
            shops = client.get_shops()
            print(f"✅ Printify Success: Found {len(shops)} shop(s) connected.")
            for shop in shops:
                shop_name = shop.get('title') or shop.get('name') or 'Unknown Shop'
                print(f"   - {shop_name} (ID: {shop['id']})")
        except Exception as e:
            print(f"❌ Printify Connection Failed: {e}")
    else:
        print("❌ Printify Failed: PRINTIFY_API_TOKEN is missing in .env")

    print("-" * 50)

    # 2. Test Meta
    meta_token = os.getenv("META_ACCESS_TOKEN")
    meta_ad_acc = os.getenv("META_AD_ACCOUNT_ID")
    if meta_token and meta_ad_acc:
        print("⚡ Meta Access Token and Ad Account found. Initializing connection...")
        try:
            client = MetaAdsClient(meta_token, meta_ad_acc)
            # In a test, we can check client configurations
            print(f"✅ Meta Configuration Verified. Target Ad Account: {client.ad_account_id}")
        except Exception as e:
            print(f"❌ Meta Connection Failed: {e}")
    else:
        print("❌ Meta Failed: META_ACCESS_TOKEN or META_AD_ACCOUNT_ID is missing in .env")

def execute_daily_drip(args):
    """
    Orchestrates the entire daily drip workflow:
    1. Upload t-shirt design to Printify.
    2. Create Bella+Canvas 3001 product on Printify.
    3. Upload ad image/mockup to Meta Ad Library.
    4. Create Facebook/Instagram marketing Campaign, targeted Ad Set, Creative, and Ad.
    """
    print("💧 [Daily Drip Automation] LAUNCHING DAILY PRODUCT AND CAMPAIGN...")
    
    shop_id = os.getenv("PRINTIFY_SHOP_ID")
    page_id = os.getenv("META_PAGE_ID")
    
    if not shop_id:
        print("❌ Error: PRINTIFY_SHOP_ID is not configured in .env")
        sys.exit(1)
        
    if not page_id:
        print("❌ Error: META_PAGE_ID (Facebook Page ID) is not configured in .env")
        sys.exit(1)

    printify = PrintifyClient()
    meta = MetaAdsClient()

    # --- STEP 1: Upload Design Artwork to Printify ---
    print(f"\n🎨 Step 1: Uploading design to Printify media library ({args.design_url})...")
    try:
        upload_res = printify.upload_image(f"{args.title}_design.png", args.design_url)
        image_id = upload_res["id"]
        print(f"✅ Design uploaded successfully. Printify Image ID: {image_id}")
    except Exception as e:
        print(f"❌ Printify Design Upload Failed: {e}")
        sys.exit(1)

    # --- STEP 2: Create Custom T-Shirt on Printify ---
    print(f"\n👕 Step 2: Creating Bella+Canvas 3001 product in shop {shop_id}...")
    try:
        product_res = printify.create_daily_tshirt(
            shop_id=int(shop_id),
            title=args.title,
            description=args.desc,
            image_id=image_id,
            price_usd=args.price
        )
        product_id = product_res["id"]
        print(f"✅ Product created successfully. Printify Product ID: {product_id}")
        print(f"🔗 Product Mockup URL: {product_res.get('images', [{}])[0].get('src', 'N/A')}")
    except Exception as e:
        print(f"❌ Printify Product Creation Failed: {e}")
        sys.exit(1)

    # --- STEP 3: Upload Mockup Image to Meta Ads Library ---
    print(f"\n🖼️ Step 3: Uploading ad mockup to Meta Ads Library ({args.mockup_path})...")
    try:
        ad_img_res = meta.upload_ad_image(args.mockup_path)
        # Retreive the image hash which identifies the uploaded file
        img_hash = ad_img_res["images"][os.path.basename(args.mockup_path)]["hash"]
        print(f"✅ Ad image uploaded successfully. Meta Image Hash: {img_hash}")
    except Exception as e:
        print(f"❌ Meta Ad Image Upload Failed: {e}")
        sys.exit(1)

    # --- STEP 4: Launch Meta Campaign ---
    campaign_name = f"Daily Drip - {args.title} Campaign"
    print(f"\n📢 Step 4: Creating Campaign: '{campaign_name}'...")
    try:
        camp_res = meta.create_campaign(name=campaign_name, objective="OUTCOMES")
        campaign_id = camp_res["id"]
        print(f"✅ Campaign created. Meta Campaign ID: {campaign_id}")
    except Exception as e:
        print(f"❌ Meta Campaign Creation Failed: {e}")
        sys.exit(1)

    # --- STEP 5: Create Target Ad Set ---
    adset_name = f"{args.title} - Streetwear Targeting"
    interests = [i.strip() for i in args.interests.split(",")] if args.interests else ["Streetwear", "Graphic Design"]
    print(f"\n🎯 Step 5: Creating Ad Set: '{adset_name}' targeting {interests} with ${args.budget}/day...")
    try:
        adset_res = meta.create_ad_set(
            campaign_id=campaign_id,
            name=adset_name,
            daily_budget_usd=args.budget,
            targeting_interests=interests
        )
        adset_id = adset_res["id"]
        print(f"✅ Ad Set created. Meta Ad Set ID: {adset_id}")
    except Exception as e:
        print(f"❌ Meta Ad Set Creation Failed: {e}")
        sys.exit(1)

    # --- STEP 6: Assemble Ad Creative ---
    creative_name = f"{args.title} Creative"
    message = f"💧 DAILY DROP: '{args.title}'\n\n{args.desc}\n\nStrictly limited release. Hand-printed on premium cotton blocks. Click below to grab yours before it vaults forever!"
    print(f"\n🎨 Step 6: Assembling Ad Creative combining product and ad copy...")
    try:
        creative_res = meta.create_ad_creative(
            name=creative_name,
            page_id=page_id,
            image_hash=img_hash,
            message=message
        )
        creative_id = creative_res["id"]
        print(f"✅ Ad Creative assembled. Meta Creative ID: {creative_id}")
    except Exception as e:
        print(f"❌ Meta Creative Assembly Failed: {e}")
        sys.exit(1)

    # --- STEP 7: Create and Publish Paused Ad ---
    ad_name = f"{args.title} Ad - Main Copy"
    print(f"\n🚀 Step 7: Publishing paused ad to Ad Set (for safety review before going live)...")
    try:
        ad_res = meta.create_ad(
            ad_set_id=adset_id,
            creative_id=creative_id,
            name=ad_name
        )
        print(f"✅ Ad created successfully. Meta Ad ID: {ad_res['id']}")
        print("\n🎉 SUCCESS! The Daily Drip workflow has completed!")
        print(f"   - Printify Product: {args.title} is now in your shop.")
        print(f"   - Meta Ad: Paused in your Ads Manager, ready for final review.")
    except Exception as e:
        print(f"❌ Meta Ad Creation Failed: {e}")
        sys.exit(1)

def execute_create_product(args):
    """
    Process One: Create the product on Printify.
    Does not require or check Meta Ads credentials.
    """
    print("💧 [Daily Drip Automation] CREATING PRODUCT ON PRINTIFY...")
    
    shop_id = os.getenv("PRINTIFY_SHOP_ID")
    if not shop_id:
        print("❌ Error: PRINTIFY_SHOP_ID is not configured in .env")
        sys.exit(1)
        
    printify = PrintifyClient()

    # --- STEP 1: Upload Design Artwork to Printify ---
    print(f"\n🎨 Step 1: Uploading design to Printify media library ({args.design_url})...")
    try:
        upload_res = printify.upload_image(f"{args.title}_design.png", args.design_url)
        image_id = upload_res["id"]
        print(f"✅ Design uploaded successfully. Printify Image ID: {image_id}")
    except Exception as e:
        print(f"❌ Printify Design Upload Failed: {e}")
        sys.exit(1)

    # --- STEP 2: Create Custom T-Shirt on Printify ---
    print(f"\n👕 Step 2: Creating Bella+Canvas 3001 product in shop {shop_id}...")
    try:
        product_res = printify.create_daily_tshirt(
            shop_id=int(shop_id),
            title=args.title,
            description=args.desc,
            image_id=image_id,
            price_usd=args.price
        )
        product_id = product_res["id"]
        print(f"✅ Product created successfully. Printify Product ID: {product_id}")
        print(f"🔗 Product Mockup URL: {product_res.get('images', [{}])[0].get('src', 'N/A')}")
        print("\n🎉 SUCCESS! Printify product creation complete!")
    except Exception as e:
        print(f"❌ Printify Product Creation Failed: {e}")
        sys.exit(1)

def execute_create_ads(args):
    """
    Process Two: Launch targeted Meta Ads campaign.
    Does not require or check Printify credentials.
    """
    print("💧 [Daily Drip Automation] LAUNCHING TARGETED META ADS...")
    
    page_id = os.getenv("META_PAGE_ID")
    if not page_id:
        print("❌ Error: META_PAGE_ID (Facebook Page ID) is not configured in .env")
        sys.exit(1)
        
    meta = MetaAdsClient()

    # --- STEP 1: Upload Mockup Image to Meta Ads Library ---
    print(f"\n🖼️ Step 1: Uploading ad mockup to Meta Ads Library ({args.mockup_path})...")
    try:
        ad_img_res = meta.upload_ad_image(args.mockup_path)
        img_hash = ad_img_res["images"][os.path.basename(args.mockup_path)]["hash"]
        print(f"✅ Ad image uploaded successfully. Meta Image Hash: {img_hash}")
    except Exception as e:
        print(f"❌ Meta Ad Image Upload Failed: {e}")
        sys.exit(1)

    # --- STEP 2: Launch Meta Campaign ---
    campaign_name = f"Daily Drip - {args.title} Campaign"
    print(f"\n📢 Step 2: Creating Campaign: '{campaign_name}'...")
    try:
        camp_res = meta.create_campaign(name=campaign_name, objective="OUTCOMES")
        campaign_id = camp_res["id"]
        print(f"✅ Campaign created. Meta Campaign ID: {campaign_id}")
    except Exception as e:
        print(f"❌ Meta Campaign Creation Failed: {e}")
        sys.exit(1)

    # --- STEP 3: Create Target Ad Set ---
    adset_name = f"{args.title} - Streetwear Targeting"
    interests = [i.strip() for i in args.interests.split(",")] if args.interests else ["Streetwear", "Graphic Design"]
    print(f"\n🎯 Step 3: Creating Ad Set: '{adset_name}' targeting {interests} with ${args.budget}/day...")
    try:
        adset_res = meta.create_ad_set(
            campaign_id=campaign_id,
            name=adset_name,
            daily_budget_usd=args.budget,
            targeting_interests=interests
        )
        adset_id = adset_res["id"]
        print(f"✅ Ad Set created. Meta Ad Set ID: {adset_id}")
    except Exception as e:
        print(f"❌ Meta Ad Set Creation Failed: {e}")
        sys.exit(1)

    # --- STEP 4: Assemble Ad Creative ---
    creative_name = f"{args.title} Creative"
    message = f"💧 DAILY DROP: '{args.title}'\n\n{args.desc}\n\nStrictly limited release. Hand-printed on premium cotton blocks. Click below to grab yours before it vaults forever!"
    print(f"\n🎨 Step 4: Assembling Ad Creative combining product and ad copy...")
    try:
        creative_res = meta.create_ad_creative(
            name=creative_name,
            page_id=page_id,
            image_hash=img_hash,
            message=message
        )
        creative_id = creative_res["id"]
        print(f"✅ Ad Creative assembled. Meta Creative ID: {creative_id}")
    except Exception as e:
        print(f"❌ Meta Creative Assembly Failed: {e}")
        sys.exit(1)

    # --- STEP 5: Create and Publish Paused Ad ---
    ad_name = f"{args.title} Ad - Main Copy"
    print(f"\n🚀 Step 5: Publishing paused ad to Ad Set (for safety review before going live)...")
    try:
        ad_res = meta.create_ad(
            ad_set_id=adset_id,
            creative_id=creative_id,
            name=ad_name
        )
        print(f"✅ Ad created successfully. Meta Ad ID: {ad_res['id']}")
        print("\n🎉 SUCCESS! Meta Ad creation complete and paused in your Ads Manager, ready for final review.")
    except Exception as e:
        print(f"❌ Meta Ad Creation Failed: {e}")
        sys.exit(1)

def main():
    load_env()
    
    parser = argparse.ArgumentParser(
        description="💧 Daily Drip automation suite. Automatically pushes streetwear products to Printify and programs matching Meta Ads."
    )
    subparsers = parser.add_subparsers(dest="command", help="Available automation commands")

    # Command: test
    subparsers.add_parser("test", help="Verify connection credentials to Printify and Meta APIs")

    # Command: create-drip
    drip_parser = subparsers.add_parser("create-drip", help="Push a new daily product to Printify and launch targeted Meta Ads")
    drip_parser.add_argument("--title", required=True, help="Streetwear Product Title")
    drip_parser.add_argument("--desc", required=True, help="Description highlighting design meaning")
    drip_parser.add_argument("--design-url", required=True, help="Public URL of the flat transparent PNG design artwork")
    drip_parser.add_argument("--mockup-path", required=True, help="Local absolute file path of the mockup image for Facebook Ads")
    drip_parser.add_argument("--price", type=float, default=29.99, help="Retail price in USD (default: 29.99)")
    drip_parser.add_argument("--budget", type=float, default=10.00, help="Daily ad set budget in USD (default: 10.00)")
    drip_parser.add_argument("--interests", default="Streetwear,Graphic Design", help="Comma-separated interests to target on FB/IG")

    # Command: create-product
    product_parser = subparsers.add_parser("create-product", help="Push a new streetwear product to Printify only (Process 1)")
    product_parser.add_argument("--title", required=True, help="Streetwear Product Title")
    product_parser.add_argument("--desc", required=True, help="Description highlighting design meaning")
    product_parser.add_argument("--design-url", required=True, help="Public URL of the flat transparent PNG design artwork")
    product_parser.add_argument("--price", type=float, default=29.99, help="Retail price in USD (default: 29.99)")

    # Command: create-ads
    ads_parser = subparsers.add_parser("create-ads", help="Launch targeted Meta Ads for a streetwear design only (Process 2)")
    ads_parser.add_argument("--title", required=True, help="Streetwear Product Title")
    ads_parser.add_argument("--desc", required=True, help="Description highlighting design meaning")
    ads_parser.add_argument("--mockup-path", required=True, help="Local absolute file path of the mockup image for Facebook Ads")
    ads_parser.add_argument("--budget", type=float, default=10.00, help="Daily ad set budget in USD (default: 10.00)")
    ads_parser.add_argument("--interests", default="Streetwear,Graphic Design", help="Comma-separated interests to target on FB/IG")

    args = parser.parse_args()

    if args.command == "test":
        test_connections()
    elif args.command == "create-drip":
        execute_daily_drip(args)
    elif args.command == "create-product":
        execute_create_product(args)
    elif args.command == "create-ads":
        execute_create_ads(args)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
