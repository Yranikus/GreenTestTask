from fastapi import APIRouter
from .get_and_save_and_delete import router as operations
from .secure import router as secure


router = APIRouter()
router.include_router(operations)
router.include_router(secure)
