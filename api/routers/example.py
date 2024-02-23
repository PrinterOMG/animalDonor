from typing import Annotated

from fastapi import APIRouter, Query, HTTPException, status

from api.dependencies import db_session_dep
from api.schemas.example import UserCreate, UserRead
from database.models import User

router = APIRouter(prefix='/example', tags=['example'])


@router.get('/ping')
def ping(pong: Annotated[str, Query(description='You can provide a custom pong')] = 'pong'):
    return pong


@router.post('/user', response_model=UserRead)
async def create_user(user: UserCreate, db_session: db_session_dep):
    new_user = User(**user.model_dump())

    db_session.add(new_user)
    await db_session.commit()

    return new_user


@router.get('/user/{user_id}')
async def get_user(user_id: int, db_session: db_session_dep) -> UserRead:
    user = await db_session.get(User, user_id)

    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    return user
