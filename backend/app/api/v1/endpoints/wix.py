from fastapi import APIRouter, Depends, HTTPException
from typing import Dict, Any, List
from pydantic import BaseModel
from app.services.wix_service import WixService
from app.core.security import get_current_user
from app.models.user import User

router = APIRouter()

class PageContent(BaseModel):
    title: str
    content: Dict[str, Any]

class PageUpdate(BaseModel):
    page_id: str
    content: Dict[str, Any]

def get_wix_service():
    return WixService()

@router.get("/pages")
async def get_wix_pages(
        wix_service: WixService = Depends(get_wix_service),
        current_user: User = Depends(get_current_user)
):
    """Get all pages from Wix"""
    pages = await wix_service.get_pages()
    return {"pages": pages}

@router.post("/pages")
async def create_wix_page(
        page_data: PageContent,
        wix_service: WixService = Depends(get_wix_service),
        current_user: User = Depends(get_current_user)
):
    """Create a new page in Wix"""
    result = await wix_service.create_page(page_data.title, page_data.content)
    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])
    return result

@router.patch("/pages")
async def update_wix_page(
        page_data: PageUpdate,
        wix_service: WixService = Depends(get_wix_service),
        current_user: User = Depends(get_current_user)
):
    """Update a page in Wix"""
    result = await wix_service.update_page_content(page_data.page_id, page_data.content)
    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])
    return result

@router.delete("/pages/{page_id}")
async def delete_wix_page(
        page_id: str,
        wix_service: WixService = Depends(get_wix_service),
        current_user: User = Depends(get_current_user)
):
    """Delete a page from Wix"""
    # Check if user is admin or has permissions
    if not current_user.is_superuser:
        raise HTTPException(status_code=403, detail="Not enough permissions")

    result = await wix_service.delete_page(page_id)
    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])
    return result