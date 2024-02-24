from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from database.models import TelegramLinkRequest


class TelegramLinkRequestService:
    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def get_by_key(self, key):
        stmt = select(TelegramLinkRequest).where(TelegramLinkRequest.key == key)

        return await self.db_session.scalar(stmt)
