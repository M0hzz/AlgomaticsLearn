# backend/app/api/v1/endpoints/wix.py
from fastapi import APIRouter, Depends, HTTPException
from typing import Dict, Any, List
from backend.app.services.wix_service import WixService
from pydantic import BaseModel

router = APIRouter()

class PageContent(BaseModel):
    title: str
    content: Dict[str, Any]

class PageUpdate(BaseModel):
    page_id: str
    content: Dict[str, Any]

def get_wix_service():
    return WixService()

@router.post("/pages")
async def create_wix_page(
        page: PageContent,
        wix_service: WixService = Depends(get_wix_service)
):
    """Create a page in Wix"""
    try:
        result = await wix_service.create_page(page.title, page.content)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/pages")
async def get_wix_pages(
        wix_service: WixService = Depends(get_wix_service)
):
    """Get all pages from Wix"""
    try:
        pages = await wix_service.get_pages()
        return {"pages": pages}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.patch("/pages")
async def update_wix_page(
        page: PageUpdate,
        wix_service: WixService = Depends(get_wix_service)
):
    """Update a page in Wix"""
    try:
        result = await wix_service.update_page(page.page_id, page.content)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))