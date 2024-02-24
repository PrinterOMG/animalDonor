from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, HTTPException, Query
from starlette import status

from api.dependencies import db_session_dep, current_active_user_dep
from api.schemas.telegram import CreateRequestResult
from database.models import TelegramLinkRequest
from services.service_token import ServiceTokenService
from services.telegram_link_request import TelegramLinkRequestService
from settings import settings

router = APIRouter(prefix='/telegram', tags=['Telegram'])


@router.post('/link', status_code=status.HTTP_204_NO_CONTENT)
async def link_telegram(
        key: UUID,
        service_token: UUID,
        telegram_id: int,
        phone: Annotated[str, Query(pattern=r'')],
        db_session: db_session_dep
):
    token = await ServiceTokenService(db_session).get_by_token(service_token)
    if token is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

    telegram_link_request = await TelegramLinkRequestService(db_session).get_by_key(key)
    if telegram_link_request is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    await db_session.refresh(token, ['user'])

    telegram_link_request.user.telegram_id = telegram_id
    telegram_link_request.user.phone = phone

    await db_session.commit()


@router.post('/unlink', status_code=status.HTTP_204_NO_CONTENT)
async def unlink_telegram(current_active_user: current_active_user_dep, db_session: db_session_dep):
    current_active_user.telegram_id = None
    await db_session.commit()


@router.post('/create_link_request', response_model=CreateRequestResult)
async def create_link_request(current_active_user: current_active_user_dep, db_session: db_session_dep):
    if current_active_user.telegram_id is not None:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail='Telegram already linked')

    new_telegram_link_request = TelegramLinkRequest(user_id=current_active_user.id)
    db_session.add(new_telegram_link_request)
    await db_session.commit()

    url_with_deeplink = settings.telegram_bot_base_url + f'?start={new_telegram_link_request.key}'

    return CreateRequestResult(link_url=url_with_deeplink)
