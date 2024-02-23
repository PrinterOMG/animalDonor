from fastapi import APIRouter

from .example import router as example_router
from .auth import router as auth_router
from .users import router as users_router

router = APIRouter()

router.include_router(example_router)
router.include_router(auth_router)
router.include_router(users_router)
