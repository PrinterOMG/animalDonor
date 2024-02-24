from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from database.models import ServiceToken


class ServiceTokenService:
    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def get_by_token(self, key):
        stmt = select(ServiceToken).where(ServiceToken.token == key)

        return await self.db_session.scalar(stmt)
