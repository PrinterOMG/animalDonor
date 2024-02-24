from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from database.models import PetType


class PetTypeService:
    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def get_pet_types(self):
        stmt = select(PetType)

        records = await self.db_session.scalars(stmt)
        return records.all()
