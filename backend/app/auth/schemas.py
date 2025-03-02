from typing import List, Optional, Dict, Any, Union
from pydantic import BaseModel, Field
from enum import Enum

class DifficultyLevel(str, Enum):
    BEGINNER = "beginner"
    INTERMEDIATE = "intermediate"
    ADVANCED = "advanced"

class MathCategory(str, Enum):
    ALGEBRA = "algebra"
    GEOMETRY = "geometry"
    TRIGONOMETRY = "trigonometry"
    PRECALCULUS = "precalculus"
    CALCULUS_I = "calculus_i"
    CALCULUS_II = "calculus_ii"

class ContentType(str, Enum):
    TEXT = "text"
    VIDEO = "video"
    INTERACTIVE = "interactive"
    QUIZ = "quiz"
    PRACTICE = "practice"

class Example(BaseModel):
    problem: str
    solution: str
    explanation: Optional[str] = None

class Exercise(BaseModel):
    question: str
    options: Optional[List[str]] = None
    answer: Union[str, int, List[int]]
    hint: Optional[str] = None

class MathContent(BaseModel):
    type: ContentType
    title: str
    content: str
    additional_resources: Optional[List[Dict[str, str]]] = None

class MathTopicBase(BaseModel):
    title: str
    category: MathCategory
    subcategory: str
    difficulty: DifficultyLevel
    description: str
    content: List[MathContent]
    examples: List[Example]
    exercises: List[Exercise]
    prerequisites: Optional[List[str]] = None
    keywords: List[str] = Field(default_factory=list)

class MathTopicCreate(MathTopicBase):
    pass

class MathTopicInDB(MathTopicBase):
    id: str = Field(..., alias="_id")

class MathTopic(MathTopicBase):
    id: str

# Example for Linear Equations schema
class LinearEquationExample(BaseModel):
    equation: str
    solution: float
    steps: List[Dict[str, str]]

class LinearEquationsContent(MathTopicBase):
    solving_methods: List[Dict[str, Any]]
    interactive_graph: Optional[Dict[str, Any]] = None
    common_mistakes: List[str]
    applications: List[Dict[str, str]]