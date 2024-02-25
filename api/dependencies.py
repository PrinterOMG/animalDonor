from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError

from api.schemas.auth import TokenData
from sqlalchemy.ext.asyncio import AsyncSession

from database.base import get_async_session
from database.models import User, Pet
from settings import settings

db_session_dep = Annotated[AsyncSession, Depends(get_async_session)]

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/auth/login')


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)], db_session: db_session_dep):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail='Could not validate credentials',
        headers={'WWW-Authenticate': 'Bearer'},
    )

    try:
        payload = jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
        user_id: str = payload.get('sub')
        if user_id is None or not user_id.isdigit():
            raise credentials_exception
        token_data = TokenData(user_id=int(user_id))
    except JWTError:
        raise credentials_exception

    user = await db_session.get(User, token_data.user_id)

    if user is None:
        raise credentials_exception

    await db_session.refresh(user, ['social_networks'])
    for soc_net in user.social_networks:
        await db_session.refresh(soc_net, ['social_network_type'])

    return user


async def get_current_active_user(current_user: Annotated[User, Depends(get_current_user)]):
    if not current_user.is_active:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Inactive user')

    return current_user


current_active_user_dep = Annotated[User, Depends(get_current_active_user)]


async def check_user_pet(
        pet_id: int,
        current_active_user: current_active_user_dep,
        db_session: db_session_dep
):
    pet = await db_session.get(Pet, pet_id)
    if pet is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    if pet.owner_id != current_active_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
