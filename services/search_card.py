from datetime import datetime
from typing import Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from database.models import SearchCard


class SearchCardService:
    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def get_first_active_search_cards(self, limit: int = 100, offset: int = 0) -> Sequence[SearchCard]:
        stmt = (
            select(SearchCard)
            .where(SearchCard.is_active == True, SearchCard.active_until >= datetime.utcnow().date())
            .order_by(SearchCard.created_at)
            .limit(limit)
            .offset(offset)
        )

        records = await self.db_session.scalars(stmt)
        records = records.all()

        await self.refresh_attrs_in_sequence(records, ['author', 'recipient'])

        return records

    async def refresh_attrs_in_sequence(self, sequence, attrs):
        for obj in sequence:
            await self.db_session.refresh(obj, attrs)
            await self.db_session.refresh(obj.recipient,
                                          ['pet_type', 'unavailable_lists', 'vaccinations'])
