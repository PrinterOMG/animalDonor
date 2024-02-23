from fastapi import APIRouter

from api.dependencies import current_active_user_dep
from api.schemas.users import UserRead

router = APIRouter(prefix='/users', tags=['Users'])


@router.get('/me')
async def get_me(current_active_user: current_active_user_dep) -> UserRead:
    return current_active_user
