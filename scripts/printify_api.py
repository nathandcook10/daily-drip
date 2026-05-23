import os
import json
import requests
from typing import Dict, List, Any, Optional

class PrintifyClient:
    """
    A robust Python helper client for the Printify REST API (v1).
    Allows listing shops, uploading designs, creating products, and submitting orders.
    """
    
    BASE_URL = "https://api.printify.com/v1"
    
    def __init__(self, api_token: Optional[str] = None):
        # Read from constructor or environment variable
        self.api_token = api_token or os.getenv("PRINTIFY_API_TOKEN")
        if not self.api_token:
            print("⚠️ Warning: PRINTIFY_API_TOKEN is not set. API calls will fail.")
            
        self.headers = {
            "Authorization": f"Bearer {self.api_token}",
            "Content-Type": "application/json",
            "User-Agent": "DailyDripAutomation/1.0"
        }

    def _get(self, endpoint: str) -> Dict[str, Any]:
        url = f"{self.BASE_URL}/{endpoint.lstrip('/')}"
        response = requests.get(url, headers=self.headers)
        response.raise_for_status()
        return response.json()

    def _post(self, endpoint: str, data: Dict[str, Any]) -> Dict[str, Any]:
        url = f"{self.BASE_URL}/{endpoint.lstrip('/')}"
        response = requests.post(url, headers=self.headers, json=data)
        response.raise_for_status()
        return response.json()

    def get_shops(self) -> List[Dict[str, Any]]:
        """Retrieve all shops connected to the Printify account."""
        return self._get("shops.json")

    def upload_image(self, file_name: str, url: str) -> Dict[str, Any]:
        """
        Uploads an image from a public URL to the Printify media library.
        Returns the uploaded image metadata containing the 'id'.
        """
        payload = {
            "file_name": file_name,
            "url": url
        }
        return self._post("uploads/images.json", payload)

    def upload_image_base64(self, file_name: str, contents_base64: str) -> Dict[str, Any]:
        """
        Uploads an image via raw base64 contents.
        """
        payload = {
            "file_name": file_name,
            "contents": contents_base64
        }
        return self._post("uploads/images.json", payload)

    def get_blueprints(self) -> List[Dict[str, Any]]:
        """List all available product blueprints (e.g. Bella+Canvas 3001)."""
        return self._get("catalog/blueprints.json")

    def get_print_providers(self, blueprint_id: int) -> List[Dict[str, Any]]:
        """Get the print providers available for a specific blueprint."""
        return self._get(f"catalog/blueprints/{blueprint_id}/print_providers.json")

    def get_variants(self, blueprint_id: int, print_provider_id: int) -> Dict[str, Any]:
        """Retrieve variants (sizes, colors) for a blueprint and print provider."""
        return self._get(f"catalog/blueprints/{blueprint_id}/print_providers/{print_provider_id}/variants.json")

    def create_product(self, shop_id: int, product_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create a new product in the specified shop.
        product_data should match Printify's schema.
        """
        return self._post(f"shops/{shop_id}/products.json", product_data)

    def create_daily_tshirt(
        self, 
        shop_id: int, 
        title: str, 
        description: str, 
        image_id: str, 
        price_usd: float = 29.99,
        blueprint_id: int = 12, # Bella+Canvas 3001
        print_provider_id: int = 29, # Monster Digital (highly recommended)
        color_name: str = "Solid Black Blend"
    ) -> Dict[str, Any]:
        """
        High-level wrapper to create a standard streetwear t-shirt on Printify.
        Uses Bella+Canvas 3001 Unisex Tee, Monster Digital, and positions the uploaded design.
        """
        # 1. Fetch provider details to identify variant IDs for sizes S, M, L, XL in Black
        variants_info = self.get_variants(blueprint_id, print_provider_id)
        
        target_sizes = ["S", "M", "L", "XL"]
        selected_variants = []
        
        for v in variants_info.get("variants", []):
            opts = v.get("options", {})
            # Find matching sizes for black color
            is_color_match = any(color_name.lower() in str(val).lower() for val in opts.values())
            is_size_match = any(opts.get("size") == sz for sz in target_sizes)
            
            if is_color_match and is_size_match and v.get("placeholder") == "front":
                selected_variants.append({
                    "id": v["id"],
                    "price": int(price_usd * 100), # Price in cents
                    "is_enabled": True
                })

        if not selected_variants:
            # Fallback: Just enable the first 4 front variants
            print("⚠️ Specific color/size match not found. Falling back to default variants.")
            for v in list(variants_info.get("variants", []))[:4]:
                selected_variants.append({
                    "id": v["id"],
                    "price": int(price_usd * 100),
                    "is_enabled": True
                })

        # 2. Define print placement on front of t-shirt
        print_areas = [
            {
                "variant_ids": [v["id"] for v in selected_variants],
                "placeholders": [
                    {
                        "position": "front",
                        "images": [
                            {
                                "id": image_id,
                                "x": 0.5, # Centered horizontally
                                "y": 0.45, # Positioned on chest
                                "scale": 0.4, # 40% scaling
                                "angle": 0
                            }
                        ]
                    }
                ]
            }
        ]

        product_payload = {
            "title": title,
            "description": description,
            "blueprint_id": blueprint_id,
            "print_provider_id": print_provider_id,
            "variants": selected_variants,
            "print_areas": print_areas
        }

        return self.create_product(shop_id, product_payload)

    def submit_order(self, shop_id: int, order_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Submits a custom order to Printify for printing and fulfillment.
        order_data should contain shipping_to_address and line_items.
        """
        return self._post(f"shops/{shop_id}/orders.json", order_data)

# Simple self-test code when run directly
if __name__ == "__main__":
    print("🧪 Testing Printify Client structure...")
    client = PrintifyClient(api_token="mock_token_for_verification")
    print("Class compiled successfully.")
