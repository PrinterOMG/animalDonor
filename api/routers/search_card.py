from typing import Annotated

from fastapi import APIRouter, HTTPException, status, Query

from api.dependencies import current_active_user_dep, db_session_dep
from api.schemas.search_card import SearchCardRead, SearchCardCreate, SearchCardUpdate, CountResult
from database.models import SearchCard, User, Pet
from services.search_card import SearchCardService

router = APIRouter(prefix='/search_cards', tags=['Search card'])


@router.get('/count', response_model=CountResult)
async def get_active_search_cards_count(db_session: db_session_dep):
    search_card_service = SearchCardService(db_session)

    count = await search_card_service.get_active_search_cards_count()

    return CountResult(count=count)


@router.get('/my', response_model=list[SearchCardRead])
async def get_my_search_cards(current_active_user: current_active_user_dep, db_session: db_session_dep):
    await db_session.refresh(current_active_user, ['search_cards'])

    search_card_service = SearchCardService(db_session)
    await search_card_service.refresh_attrs_in_sequence(current_active_user.search_cards, ['author', 'recipient'])

    return current_active_user.search_cards


@router.get(
    '/{search_card_id}',
    responses={
        404: {

        }
    }
)
async def get_search_card(
        search_card_id: int,
        db_session: db_session_dep
) -> SearchCardRead:
    search_card = await db_session.get(SearchCard, search_card_id)

    if not search_card:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    await db_session.refresh(search_card, ['author', 'recipient'])
    await db_session.refresh(search_card.recipient, ['pet_type', 'unavailable_lists', 'vaccinations'])
    await db_session.refresh(search_card.author, ['social_networks'])
    
    for soc_net in search_card.author.social_networks:
        await db_session.refresh(soc_net, ['social_network_type'])
        
        if not soc_net.is_public:
            soc_net.link = 'Скрыто'
            
    return search_card


@router.get('/', response_model=list[SearchCardRead])
async def get_first_active_search_cards(
        limit: Annotated[int, Query(ge=1, le=100)] = 100,
        offset: Annotated[int, Query(ge=0)] = 0,
        *,
        db_session: db_session_dep
):
    """
    Returns the **oldest** active search cards
    """
    search_card_service = SearchCardService(db_session)

    search_cards = await search_card_service.get_first_active_search_cards(limit, offset)

    for search_card in search_cards:
        for soc_net in search_card.author.social_networks:
            if not soc_net.is_public:
                soc_net.link = 'Скрыто'

    return search_cards


@router.post(
    '/',
    response_model=SearchCardRead,
    responses={
        404: {

        }
    }
)
async def create_search_card(
        search_card: SearchCardCreate,
        current_active_user: current_active_user_dep,
        db_session: db_session_dep
):
    """
    The author of the search card will be the current user
    """
    recipient = await db_session.get(Pet, search_card.recipient_id)
    if recipient is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'Pet {search_card.recipient_id} does not exists')

    new_search_card = SearchCard(**search_card.model_dump(), author_id=current_active_user.id)

    db_session.add(new_search_card)
    await db_session.commit()

    await db_session.refresh(new_search_card, ['author', 'recipient'])
    await db_session.refresh(new_search_card.recipient, ['pet_type', 'unavailable_lists', 'vaccinations'])
    await db_session.refresh(search_card.author, ['social_networks'])

    for soc_net in search_card.author.social_networks:
        await db_session.refresh(soc_net, ['social_network_type'])

    return new_search_card


@router.patch(
    '/{search_card_id}',
    response_model=SearchCardRead,
    responses={
        404: {

        },
        403: {

        }
    }
)
async def update_search_card(
        search_card_id: int,
        search_card_update: SearchCardUpdate,
        current_active_user: current_active_user_dep,
        db_session: db_session_dep
):
    search_card = await db_session.get(SearchCard, search_card_id)
    if search_card is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    if search_card.author_id != current_active_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)

    update_data = search_card_update.dict(exclude_unset=True)

    if update_data.get('recipient_id'):
        recipient = await db_session.get(Pet, search_card_update.recipient_id)
        if recipient is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    for field, value in update_data.items():
        setattr(search_card, field, value)

    await db_session.commit()

    await db_session.refresh(search_card, ['author', 'recipient'])
    await db_session.refresh(search_card.recipient, ['pet_type', 'unavailable_lists', 'vaccinations'])
    await db_session.refresh(search_card.author, ['social_networks'])

    for soc_net in search_card.author.social_networks:
        await db_session.refresh(soc_net, ['social_network_type'])

    return search_card
