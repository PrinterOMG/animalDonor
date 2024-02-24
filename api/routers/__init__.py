from fastapi import APIRouter

from .example import router as example_router
from .auth import router as auth_router
from .users import router as users_router
from .pets import router as pet_router
from .search_card import router as search_card_router
from .vaccination import router as vaccination_router
from .unavailable_list import router as unavailable_list_router

router = APIRouter()

router.include_router(example_router)
router.include_router(auth_router)
router.include_router(users_router)

pet_router.include_router(vaccination_router)
pet_router.include_router(unavailable_list_router)
router.include_router(pet_router)

router.include_router(search_card_router)
