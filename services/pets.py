from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from database.models import Pet


class PetService:
    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def get_pets(self, user_id: int) -> list[Pet]:
        stmt = select(Pet).where(Pet.owner_id == user_id)
        result = await self.db_session.execute(stmt)

        return list(result.scalars().all())
