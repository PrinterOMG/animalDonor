from fastapi import APIRouter, HTTPException
from starlette import status

from api.dependencies import current_active_user_dep, db_session_dep
from api.schemas.social_network import SocialNetworkCreate, SocialNetworkRead, SocialNetworkUpdate
from database.models import SocialNetwork, SocialNetworkType

router = APIRouter(prefix='/me/social_networks', tags=['Social networks'])


@router.post('', response_model=SocialNetworkRead)
async def add_social_network(
        social_network: SocialNetworkCreate,
        current_active_user: current_active_user_dep,
        db_session: db_session_dep
):
    social_network_type = await db_session.get(SocialNetworkType, social_network.social_network_type_id)
    if social_network_type is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    new_social_network = SocialNetwork(**social_network.model_dump(), user_id=current_active_user.id)

    db_session.add(new_social_network)
    await db_session.commit()

    await db_session.refresh(new_social_network, ['social_network_type'])

    return new_social_network


@router.delete('/{social_network_id}}', status_code=status.HTTP_204_NO_CONTENT)
async def remove_social_network(
        social_network_id: int,
        current_active_user: current_active_user_dep,
        db_session: db_session_dep
):
    social_network = await db_session.get(SocialNetwork, social_network_id)
    if social_network is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    if social_network.user_id != current_active_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)

    await db_session.delete(social_network)
    await db_session.commit()


@router.put('/{social_network_id}', response_model=SocialNetworkRead)
async def update_social_network(
        social_network_id: int,
        social_network_update: SocialNetworkUpdate,
        current_active_user: current_active_user_dep,
        db_session: db_session_dep
):
    social_network = await db_session.get(SocialNetwork, social_network_id)
    if social_network is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    if social_network.user_id != current_active_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)

    social_network_type = await db_session.get(SocialNetworkType, social_network_update.social_network_type_id)
    if social_network_type is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    update_data = social_network_update.model_dump()

    for field, value in update_data.items():
        setattr(social_network, field, value)

    await db_session.commit()

    await db_session.refresh(social_network, ['social_network_type'])

    return social_network
