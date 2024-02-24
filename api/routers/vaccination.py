from fastapi import APIRouter, HTTPException, status, Depends

from api.dependencies import current_active_user_dep, db_session_dep, check_user_pet
from api.schemas.vaccination import VaccinationCreate, VaccinationUpdate, VaccinationRead
from database.models import Pet, Vaccination


router = APIRouter(prefix='/{pet_id}/vaccinations', tags=['Pet vaccination'], dependencies=[Depends(check_user_pet)])


@router.post('/', response_model=VaccinationRead)
async def add_vaccination(
        pet_id: int,
        vaccination: VaccinationCreate,
        db_session: db_session_dep
):
    new_vaccination = Vaccination(
        **vaccination.model_dump(),
        pet_id=pet_id
    )

    db_session.add(new_vaccination)
    await db_session.commit()

    return new_vaccination


@router.delete('/{vaccination_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_vaccination(
        vaccination_id: int,
        db_session: db_session_dep
):
    vaccination = await db_session.get(Vaccination, vaccination_id)
    if vaccination is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    await db_session.delete(vaccination)
    await db_session.commit()


@router.put('/{vaccination_id}', response_model=VaccinationRead)
async def update_vaccination(
        vaccination_id: int,
        vaccination_update: VaccinationUpdate,
        db_session: db_session_dep
):
    vaccination = await db_session.get(Vaccination, vaccination_id)
    if vaccination is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    update_data = vaccination_update.model_dump()

    for field, value in update_data.items():
        setattr(vaccination, field, value)

    await db_session.commit()

    return vaccination
