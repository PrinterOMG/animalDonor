from fastapi import APIRouter, HTTPException, status

from api.dependencies import current_active_user_dep, db_session_dep
from api.schemas.users import UserRead, UserUpdate

router = APIRouter(prefix='/users', tags=['Users'])


@router.get('/me')
async def get_me(current_active_user: current_active_user_dep) -> UserRead:
    return current_active_user


@router.patch('/me')
async def update_me(
        user_update: UserUpdate,
        current_active_user: current_active_user_dep,
        db_session: db_session_dep
) -> UserRead:
    update_data = user_update.model_dump(exclude_unset=True)

    if not update_data:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='At least one field is required')

    for field, value in update_data.items():
        setattr(current_active_user, field, value)

    await db_session.commit()

    return current_active_user
