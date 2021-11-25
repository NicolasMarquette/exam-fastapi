"""Models for the questionnary."""

from pydantic import BaseModel
from typing import Optional, Dict


class Question(BaseModel):
    "Base model for the questionnary."
    question: str
    subject: str
    use: str
    correct: str
    responseA: str
    responseB: str
    responseC: str
    responseD: Optional[str] = None


class QuestionIn(BaseModel):
    """Model for the return when adding a question in the database."""
    status: str
    created_item: Dict[str, Optional[str]]