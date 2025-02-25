# backend/app/services/wix_service.py
import httpx
from typing import Dict, Any, List
import json
import os
from dotenv import load_dotenv

load_dotenv()

class WixService:
    """Service for integrating with the Wix API"""

    def __init__(self):
        self.api_key = os.getenv("WIX_API_KEY", "")
        self.site_id = os.getenv("WIX_SITE_ID", "")
        self.base_url = "https://www.wixapis.com/v1"
        self.headers = {
            "Authorization": self.api_key,
            "wix-site-id": self.site_id,
            "Content-Type": "application/json"
        }

    async def get_pages(self) -> List[Dict[str, Any]]:
        """Get all pages from Wix"""
        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(
                    f"{self.base_url}/pages",
                    headers=self.headers
                )
                response.raise_for_status()
                return response.json().get("pages", [])
            except Exception as e:
                print(f"Error getting Wix pages: {str(e)}")
                return []

    async def update_page_content(self, page_id: str, content: Dict[str, Any]) -> Dict[str, Any]:
        """Update page content in Wix"""
        async with httpx.AsyncClient() as client:
            try:
                response = await client.patch(
                    f"{self.base_url}/pages/{page_id}",
                    headers=self.headers,
                    json={"page": {"content": json.dumps(content)}}
                )
                response.raise_for_status()
                return response.json()
            except Exception as e:
                print(f"Error updating Wix page: {str(e)}")
                return {"error": str(e)}