from datetime import timedelta
from typing import Annotated

from fastapi import APIRouter, HTTPException, status, Depends, Body
from fastapi.security import OAuth2PasswordRequestForm

from api.dependencies import db_session_dep, current_active_user_dep
from api.schemas.auth import RegisterRequest, Token
from database.models import User
from services.users import UserService
from settings import settings
from utils.security import get_password_hash, create_access_token, verify_password

router = APIRouter(prefix='/auth', tags=['Authentication'])


@router.post('/register')
async def register(register_data: RegisterRequest, db_session: db_session_dep) -> Token:
    user_service = UserService(db_session)

    existing_user = await user_service.get_by_email(register_data.email)

    if existing_user is not None:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail='Email already registered')

    new_user = User(
        email=register_data.email,
        hashed_password=get_password_hash(register_data.password)
    )

    db_session.add(new_user)
    await db_session.commit()

    access_token_expires = timedelta(minutes=settings.access_token_expire_minutes)
    access_token = create_access_token(
        data={'sub': str(new_user.id)}, expires_delta=access_token_expires
    )

    return Token(access_token=access_token)


@router.post('/login')
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db_session: db_session_dep) -> Token:
    exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail='Incorrect username or password',
        headers={'WWW-Authenticate': 'Bearer'},
    )
    users_service = UserService(db_session)
    user = await users_service.get_by_email(form_data.username)
    if user is None:
        raise exception

    if not verify_password(form_data.password, user.hashed_password):
        raise exception

    access_token_expires = timedelta(minutes=settings.access_token_expire_minutes)
    access_token = create_access_token(
        data={'sub': str(user.id)}, expires_delta=access_token_expires
    )

    return Token(access_token=access_token)


@router.post('/change_password', status_code=204)
async def change_password(
        old_password: Annotated[str, Body()],
        new_password: Annotated[str, Body(min_length=8)],
        current_active_user: current_active_user_dep,
        db_session: db_session_dep
):
    if not verify_password(old_password, current_active_user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Incorrect old password')

    new_hashed_password = get_password_hash(new_password)

    current_active_user.hashed_password = new_hashed_password

    await db_session.commit()
