from fastapi import APIRouter

from api.dictionary import router as dictionary_router
from api.translation import router as translation_router

api_router = APIRouter()
api_router.include_router(translation_router)
api_router.include_router(dictionary_router)
