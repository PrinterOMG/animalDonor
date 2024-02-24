from fastapi import APIRouter

from api.dependencies import db_session_dep
from api.schemas.pet_type import PetTypeRead
from services.pet_type import PetTypeService

router = APIRouter(prefix='/pet_type', tags=['Pet type'])


@router.get('', response_model=list[PetTypeRead])
async def get_pet_types(db_session: db_session_dep):
    pet_type_service = PetTypeService(db_session)

    return await pet_type_service.get_pet_types()
