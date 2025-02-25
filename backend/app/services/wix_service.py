import httpx
from typing import Dict, Any, List, Optional
import json
import os
from dotenv import load_dotenv

load_dotenv()

class WixService:

    def __init__(self):
        self.api_key = os.getenv("WIX_API_KEY")
        self.site_id = os.getenv("WIX_SITE_ID")
        self.base_url = os.getenv("WIX_BASE_URL")
        self.headers = {
            "Authorization": self.api_key,
            "wix-site-id": self.site_id,
            "Content-Type": "application/json"
        }
    async def create_page(self, title: str, content: Dict[str, Any]) -> Dict[str, Any]:
        """Create a page in Wix"""
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.base_url}/pages",
                headers=self.headers,
                json={
                    "page": {
                        "name": title,
                        "title": title,
                        "content": json.dumps(content)
                    }
                }
            )
            response.raise_for_status()
            return response.json()

    async def get_pages(self) -> List[Dict[str, Any]]:
        """Get all pages from Wix"""
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{self.base_url}/pages",
                headers=self.headers
            )
            response.raise_for_status()
            return response.json().get("pages", [])

    async def update_page(self, page_id: str, content: Dict[str, Any]) -> Dict[str, Any]:
        """Update a page in Wix"""
        async with httpx.AsyncClient() as client:
            response = await client.patch(
                f"{self.base_url}/pages/{page_id}",
                headers=self.headers,
                json={"page": {"content": json.dumps(content)}}
            )
            response.raise_for_status()
            return response.json()
