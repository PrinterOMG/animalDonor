from sqlalchemy import select, Sequence
from sqlalchemy.ext.asyncio import AsyncSession

from database.models import Pet


class PetService:
    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def get_pets(self, user_id: int) -> Sequence[Pet]:
        stmt = select(Pet).where(Pet.owner_id == user_id)
        result = await self.db_session.scalars(stmt)
        records = result.all()

        for record in records:
            await self.db_session.refresh(record, ['pet_type', 'unavailable_lists', 'vaccinations'])

        return records
