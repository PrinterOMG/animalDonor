from datetime import datetime
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

    async def match_recipients(self, pet: Pet) -> list[tuple[SearchCard, float]]:
        stmt = (
            select(SearchCard)
            .where(SearchCard.is_active == True, SearchCard.active_until >= datetime.utcnow().date())
            .where(SearchCard.recipient_id != pet.id)
        )

        result = await self.db_session.scalars(stmt)
        search_cards = result.all()

        scores = {}

        await self.db_session.refresh(pet, ['pet_type'])
        for search_card in search_cards:
            await self.db_session.refresh(search_card, ['recipient'])
            await self.db_session.refresh(search_card.recipient, ['pet_type'])
            scores[search_card] = get_matching_score(search_card, pet)

        sorted_ratings = sorted(scores.items(), key=lambda x: x[1], reverse=True)
        return sorted_ratings

    async def match_donors(self, search_card: SearchCard) -> list[tuple[Pet, float]]:
        recipient = search_card.recipient
        await self.db_session.refresh(recipient, ['pet_type'])

        # todo: exclude recipient
        stmt = select(Pet).where(Pet.pet_type == recipient.pet_type, Pet.id != recipient.id)
        result = await self.db_session.scalars(stmt)
        donors = result.all()

        scores = {}

        for donor in donors:
            await self.db_session.refresh(donor, ['pet_type'])
            scores[donor] = get_matching_score(search_card, donor)

        print(scores)
        sorted_ratings = sorted(scores.items(), key=lambda x: x[1], reverse=True)
        return sorted_ratings
