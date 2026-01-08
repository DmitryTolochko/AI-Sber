from typing import Any, Dict, List

from pydantic import BaseModel


class BaseModelRead(BaseModel):
    """Model for translation response."""

    text_to_translated: str


class TranslationResponse(BaseModel):
    """Model for word translation response."""

    original: str
    translations: List[str]


class SentenceResponse(BaseModel):
    """Model for sentence search response."""

    searched_word: str
    matches: List[Dict[str, Any]]
