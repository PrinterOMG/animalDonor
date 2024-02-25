from fastapi import APIRouter

from api.dependencies import db_session_dep
from api.schemas.social_network_type import SocialNetworkTypeRead
from services.social_network_type import SocialNetworkTypeService

router = APIRouter(prefix='/social_network_type', tags=['Social network type'])


@router.get('', response_model=list[SocialNetworkTypeRead])
async def get_pet_types(db_session: db_session_dep):
    pet_type_service = SocialNetworkTypeService(db_session)

    return await pet_type_service.get_social_network_types()
