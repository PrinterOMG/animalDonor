from typing import List, Tuple

from sqlalchemy import select, Sequence
from sqlalchemy.ext.asyncio import AsyncSession

from database.models import Pet, SearchCard
from utils.matching import get_matching_score


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

    async def match_recipients(self, pet: Pet) -> list[SearchCard]:
        # stmt = select(Pet).where(Pet.pet_type == pet.pet_type)
        # result = await self.db_session.scalars(stmt)
        # records = result.all()
        #
        # scores = {}
        #
        # for record in records:
        #     await self.db_session.refresh(record, ['pet_type'])
        #     scores[record.id] = get_matching_score(pet)
        pass

    async def match_donors(self, search_card: SearchCard) -> list[tuple[Pet, float]]:
        stmt = select(Pet).where(Pet.pet_type == search_card.recipient.pet_type)
        result = await self.db_session.scalars(stmt)
        records = result.all()

        scores = {}

        for record in records:
            await self.db_session.refresh(record, ['pet_type'])
            scores[record] = get_matching_score(search_card, record)

        sorted_array = sorted(scores.items(), key=lambda x: (-x[1], x[0]))

        return sorted_array
