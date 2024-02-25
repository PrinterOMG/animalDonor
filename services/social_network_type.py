from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from database.models import SocialNetworkType


class SocialNetworkTypeService:
    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def get_social_network_types(self):
        stmt = select(SocialNetworkType)

        records = await self.db_session.scalars(stmt)
        return records.all()
