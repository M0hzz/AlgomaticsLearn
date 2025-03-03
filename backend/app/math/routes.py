from fastapi import APIRouter, Depends, HTTPException, Query, Path
from typing import List, Optional
from bson.objectid import ObjectId
from backend.app.db import get_collection, MATH_TOPICS_COLLECTION
from backend.app.math.schemas import (
    MathTopic,
    MathTopicCreate,
    MathCategory,
    DifficultyLevel
)
from backend.app.auth.utils import get_current_active_user

router = APIRouter()

@router.get("/topics", response_model=List[MathTopic])
async def get_math_topics(
        category: Optional[MathCategory] = None,
        difficulty: Optional[DifficultyLevel] = None,
        search: Optional[str] = None,
        skip: int = Query(0, ge=0),
        limit: int = Query(10, ge=1, le=100)
):
    """
    Get all math topics with optional filtering.
    """
    math_collection = get_collection(MATH_TOPICS_COLLECTION)

    # Build query
    query = {}
    if category:
        query["category"] = category
    if difficulty:
        query["difficulty"] = difficulty
    if search:
        query["$or"] = [
            {"title": {"$regex": search, "$options": "i"}},
            {"keywords": {"$in": [search]}},
            {"description": {"$regex": search, "$options": "i"}}
        ]

    # Execute query
    cursor = math_collection.find(query).skip(skip).limit(limit)
    topics = await cursor.to_list(length=limit)

    # Convert ObjectId to string
    for topic in topics:
        topic["id"] = str(topic.pop("_id"))

    return topics

@router.get("/topics/{topic_id}", response_model=MathTopic)
async def get_math_topic(topic_id: str = Path(..., title="The ID of the math topic")):
    """
    Get a specific math topic by ID.
    """
    math_collection = get_collection(MATH_TOPICS_COLLECTION)

    try:
        topic = await math_collection.find_one({"_id": ObjectId(topic_id)})
    except:
        raise HTTPException(status_code=404, detail="Invalid topic ID format")

    if not topic:
        raise HTTPException(status_code=404, detail="Math topic not found")

    # Convert ObjectId to string
    topic["id"] = str(topic.pop("_id"))

    return topic

@router.post("/topics", response_model=MathTopic)
async def create_math_topic(
        topic: MathTopicCreate,
        current_user: dict = Depends(get_current_active_user)
):
    """
    Create a new math topic (admin only).
    """
    # Check if user is admin
    if not current_user.get("is_admin", False):
        raise HTTPException(status_code=403, detail="Not authorized to create topics")

    math_collection = get_collection(MATH_TOPICS_COLLECTION)

    # Check if topic with same title already exists
    existing = await math_collection.find_one({"title": topic.title})
    if existing:
        raise HTTPException(status_code=400, detail="Topic with this title already exists")

    # Insert new topic
    topic_dict = topic.dict()
    result = await math_collection.insert_one(topic_dict)

    # Return created topic
    created_topic = topic_dict.copy()
    created_topic["id"] = str(result.inserted_id)

    return created_topic

@router.get("/categories", response_model=List[str])
async def get_math_categories():
    """
    Get all math categories.
    """
    return [category.value for category in MathCategory]

@router.get("/algebra", response_model=List[MathTopic])
async def get_algebra_topics(
        difficulty: Optional[DifficultyLevel] = None,
        skip: int = Query(0, ge=0),
        limit: int = Query(10, ge=1, le=100)
):
    """
    Get algebra topics with optional difficulty filtering.
    """
    math_collection = get_collection(MATH_TOPICS_COLLECTION)

    # Build query
    query = {"category": MathCategory.ALGEBRA}
    if difficulty:
        query["difficulty"] = difficulty

    # Execute query
    cursor = math_collection.find(query).skip(skip).limit(limit)
    topics = await cursor.to_list(length=limit)

    # Convert ObjectId to string
    for topic in topics:
        topic["id"] = str(topic.pop("_id"))

    return topics