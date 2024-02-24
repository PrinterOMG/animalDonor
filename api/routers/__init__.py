from fastapi import APIRouter

from .example import router as example_router
from .auth import router as auth_router
from .users import router as users_router
from .pets import router as pet_router
from .search_card import router as search_card_router
from .vaccination import router as vaccination_router
from .unavailable_list import router as unavailable_list_router
from .pet_type import router as pet_type_router
from .telegram import router as telegram_router

router = APIRouter(prefix='/api')

router.include_router(example_router)
router.include_router(auth_router)
router.include_router(users_router)

pet_router.include_router(vaccination_router)
pet_router.include_router(unavailable_list_router)
router.include_router(pet_router)

router.include_router(search_card_router)
router.include_router(pet_type_router)
router.include_router(telegram_router)
