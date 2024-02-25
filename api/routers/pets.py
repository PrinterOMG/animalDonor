from typing import List

from fastapi import APIRouter, HTTPException, status, Query

from api.dependencies import current_active_user_dep, db_session_dep
from api.schemas.pets import PetRead, PetCreate, PetUpdate, PetMatchRead
from api.schemas.search_card import SearchCardRead
from database.models import Pet, PetType, SearchCard
from services.pets import PetService

router = APIRouter(prefix='/pets', tags=['Pets'])


@router.get('/my', response_model=list[PetRead])
async def get_my_pets(current_active_user: current_active_user_dep, db_session: db_session_dep):
    pet_service = PetService(db_session)
    result = await pet_service.get_pets(current_active_user.id)

    return result


@router.get('/{pet_id}')
async def get_pet_by_id(pet_id: int, db_session: db_session_dep) -> PetRead:
    pet = await db_session.get(Pet, pet_id)

    if pet is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'Pet with id {pet_id} does not exist')

    await db_session.refresh(pet, ['pet_type', 'unavailable_lists', 'vaccinations'])

    return pet


@router.post('/', response_model=PetRead)
async def create_pet(
        pet_create: PetCreate,
        current_active_user: current_active_user_dep,
        db_session: db_session_dep
) -> Pet:
    """
    Creates a pet on behalf of the current user
    """
    if pet_create.pet_type_id is not None:
        pet_type = await db_session.get(PetType, pet_create.pet_type_id)
        if pet_type is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    new_pet = Pet(**pet_create.model_dump(), owner_id=current_active_user.id)

    db_session.add(new_pet)
    await db_session.commit()

    await db_session.refresh(new_pet, ["pet_type", 'unavailable_lists', 'vaccinations'])

    return new_pet


@router.patch('/{pet_id}', response_model=PetRead)
async def update_pet(
        pet_id: int,
        pet_update: PetUpdate,
        current_active_user: current_active_user_dep,
        db_session: db_session_dep
):
    pet = await db_session.get(Pet, pet_id)
    if pet is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    if pet.owner_id != current_active_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)

    update_data = pet_update.dict(exclude_unset=True)

    if update_data.get('pet_type_id'):
        pet_type = await db_session.get(PetType, pet_update.pet_type_id)
        if pet_type is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    for field, value in update_data.items():
        setattr(pet, field, value)

    await db_session.commit()

    await db_session.refresh(pet, ['pet_type', 'unavailable_lists', 'vaccinations'])

    return pet


@router.get('/match/recipients/{pet_id}', response_model=list[SearchCardRead])
async def get_matched_recipients(
        pet_id: int,
        current_active_user: current_active_user_dep,
        db_session: db_session_dep
) -> list[SearchCard]:  # SearchMatchRead
    pet = await db_session.get(Pet, pet_id)
    if pet is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    if pet.owner_id != current_active_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)

    pet_service = PetService(db_session)


@router.get('/match/donors/{search_card_id}', response_model=list[PetMatchRead])
async def get_matched_donors(
        search_card_id: int,
        current_active_user: current_active_user_dep,
        db_session: db_session_dep,
) -> list[PetMatchRead]:
    search_card = await db_session.get(SearchCard, search_card_id)
    if search_card is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    if search_card.author_id != current_active_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)

    await db_session.refresh(search_card, ['recipient'])

    pet_service = PetService(db_session)
    matched_donors = await pet_service.match_donors(search_card)
    pet_matched_donors = []
    for (i, k) in matched_donors:
        i.match_percent = k
        await db_session.refresh(i, ['owner'])
        pet_matched_donors.append(PetMatchRead.model_validate(i))
    return pet_matched_donors
