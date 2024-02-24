from fastapi import APIRouter, HTTPException, status

from api.dependencies import current_active_user_dep, db_session_dep
from api.schemas.pets import PetRead, PetCreate
from database.models import Pet
from services.pets import PetService

router = APIRouter(prefix='/pets', tags=['Pets'])


@router.get('/id/{pet_id}')
async def get_pet_by_id(pet_id: int, db_session: db_session_dep) -> PetRead:
    pet = await db_session.get(Pet, pet_id)

    if pet is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'Pet with id {pet_id} does not exist')

    return pet


@router.get('/', response_model=list[PetRead])
async def get_pets_by_user_id(current_active_user: current_active_user_dep, db_session: db_session_dep) -> list[Pet]:
    pet_service = PetService(db_session)
    result = await pet_service.get_pets(current_active_user.id)
    return result


@router.post('/', response_model=PetRead)
async def create_pet(
        pet_create: PetCreate,
        db_session: db_session_dep
) -> Pet:
    new_pet = Pet(**pet_create.model_dump())
    db_session.add(new_pet)
    await db_session.commit()

    await db_session.refresh(new_pet, ["pet_type"])

    return new_pet
