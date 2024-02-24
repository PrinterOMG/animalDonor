from fastapi import APIRouter, Depends, HTTPException
from starlette import status

from api.dependencies import db_session_dep, check_user_pet
from api.schemas.unavailable_list import UnavailableListCreate, UnavailableListUpdate, UnavailableListRead
from database.models import UnavailableList

router = APIRouter(prefix='/{pet_id}/unavailable_list', tags=['Unavailable list'],
                   dependencies=[Depends(check_user_pet)])


@router.post('/', response_model=UnavailableListRead)
async def create_unavailable_list(pet_id: int, unavailable_list: UnavailableListCreate, db_session: db_session_dep):
    new_unavailable_list = UnavailableList(**unavailable_list.model_dump(), pet_id=pet_id)

    db_session.add(new_unavailable_list)
    await db_session.commit()

    return new_unavailable_list


@router.delete('/{list_id}')
async def delete_unavailable_list(list_id: int, db_session: db_session_dep):
    unavailable_list = await db_session.get(UnavailableList, list_id=list_id)
    if unavailable_list is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    await db_session.delete(unavailable_list)
    await db_session.commit()


@router.put('/{list_id}')
async def update_unavailable_list(
        unavailable_list_update: UnavailableListUpdate,
        list_id: int,
        db_session: db_session_dep
):
    unavailable_list = await db_session.get(UnavailableList, list_id)
    if unavailable_list is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    update_data = unavailable_list_update.model_dump()

    for field, value in update_data.items():
        setattr(unavailable_list, field, value)

    await db_session.commit()

    return unavailable_list
