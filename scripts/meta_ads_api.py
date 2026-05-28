import os
import json
import requests
from typing import Dict, List, Any, Optional

class MetaAdsClient:
    """
    A robust Python helper client for the Meta Marketing API.
    Enables creating ad campaigns, uploading ad images, building ad creatives, and launching ads.
    """
    
    BASE_URL = "https://graph.facebook.com/v16.0"
    
    def __init__(self, access_token: Optional[str] = None, ad_account_id: Optional[str] = None):
        # Read credentials from constructor or environment variables
        self.access_token = access_token or os.getenv("META_ACCESS_TOKEN")
        self.ad_account_id = ad_account_id or os.getenv("META_AD_ACCOUNT_ID")
        
        if not self.access_token or not self.ad_account_id:
            print("⚠️ Warning: META_ACCESS_TOKEN or META_AD_ACCOUNT_ID is not set. API calls will fail.")
            
        # Clean ad_account_id format to ensure it has the "act_" prefix
        if self.ad_account_id and not self.ad_account_id.startswith("act_"):
            self.ad_account_id = f"act_{self.ad_account_id}"

        self.params = {
            "access_token": self.access_token
        }

    def _post(self, endpoint: str, data: Dict[str, Any], files: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        url = f"{self.BASE_URL}/{endpoint.lstrip('/')}"
        response = requests.post(url, params=self.params, data=data, files=files)
        response.raise_for_status()
        return response.json()

    def create_campaign(self, name: str, objective: str = "OUTCOMES", status: str = "PAUSED") -> Dict[str, Any]:
        """
        Creates a new marketing campaign.
        - objective: OUTCOMES (sales), BRAND_AWARENESS, ENGAGEMENT, etc.
        - status: ACTIVE or PAUSED
        """
        payload = {
            "name": name,
            "objective": objective,
            "special_ad_categories": "NONE",
            "status": status
        }
        return self._post(f"{self.ad_account_id}/campaigns", payload)

    def upload_ad_image(self, image_path: str) -> Dict[str, Any]:
        """
        Uploads a local image file to Meta's Ad Library.
        Returns the uploaded image hash.
        """
        if not os.path.exists(image_path):
            raise FileNotFoundError(f"Ad image file not found: {image_path}")
            
        with open(image_path, "rb") as img_file:
            files = {
                "filename": (os.path.basename(image_path), img_file, "image/png")
            }
            # Uploading requires sending as a multipart form file
            return self._post(f"{self.ad_account_id}/adimages", {}, files=files)

    def create_ad_set(
        self, 
        campaign_id: str, 
        name: str, 
        daily_budget_usd: float = 10.00, 
        targeting_interests: Optional[List[str]] = None,
        status: str = "PAUSED"
    ) -> Dict[str, Any]:
        """
        Creates an ad set targeting specific user interests (e.g. Streetwear, Graphic Design).
        - daily_budget_usd: daily spend limit
        """
        # Convert budget to cents/microcents as required by Meta
        daily_budget_cents = int(daily_budget_usd * 100)
        
        # Build interest-targeting payload if provided
        targeting = {
            "geo_locations": {"countries": ["US", "CA", "GB", "AU"]},
            "publisher_platforms": ["instagram", "facebook"],
            "age_min": 18,
            "age_max": 35
        }
        
        if targeting_interests:
            # Structuring interests array according to Meta specifications
            interests_list = []
            for interest in targeting_interests:
                # In production, these should be verified IDs, but names can be passed or resolved
                interests_list.append({"id": interest, "name": interest})
            targeting["interests"] = interests_list

        payload = {
            "name": name,
            "campaign_id": campaign_id,
            "daily_budget": daily_budget_cents,
            "billing_event": "IMPRESSIONS",
            "optimization_goal": "REACH", # Standard awareness/reach goal for streetwear release
            "targeting": json.dumps(targeting),
            "status": status
        }
        
        return self._post(f"{self.ad_account_id}/adsets", payload)

    def create_ad_creative(
        self, 
        name: str, 
        page_id: str, 
        image_hash: str, 
        message: str, 
        link_url: str = "https://thedailydrip.com"
    ) -> Dict[str, Any]:
        """
        Assembles an Ad Creative blending the image hash, streetwear text, Page connection, and Shop Now CTA.
        """
        # Standard shop button layout spec
        object_story_spec = {
            "page_id": page_id,
            "link_data": {
                "image_hash": image_hash,
                "link": link_url,
                "message": message,
                "call_to_action": {
                    "type": "SHOP_NOW",
                    "value": {
                        "link": link_url
                    }
                }
            }
        }
        
        payload = {
            "name": name,
            "object_story_spec": json.dumps(object_story_spec)
        }
        
        return self._post(f"{self.ad_account_id}/adcreatives", payload)

    def create_ad(self, ad_set_id: str, creative_id: str, name: str, status: str = "PAUSED") -> Dict[str, Any]:
        """
        Publishes the ad by associating the creative asset with the targeted ad set.
        """
        payload = {
            "name": name,
            "adset_id": ad_set_id,
            "creative": json.dumps({"creative_id": creative_id}),
            "status": status
        }
        return self._post(f"{self.ad_account_id}/ads", payload)

if __name__ == "__main__":
    print("🧪 Testing Meta Ads Client structure...")
    client = MetaAdsClient(access_token="mock_token", ad_account_id="mock_acc")
    print("Class compiled successfully.")
