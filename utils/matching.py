import difflib
import datetime

from database.models import SearchCard, Pet, PetType


def get_matching_score(search_card: SearchCard, donor: Pet) -> float:
    """
    Returns the degree of compatibility with the recipient from 0 to 1
    """

    recipient = search_card.recipient
    score = 0

    if recipient.pet_type != donor.pet_type:
        return score
    if not blood_type_match(recipient.blood_type.upper(), donor.blood_type.upper(), donor.pet_type):
        return score

    if compare_words(donor.breed, recipient.breed):
        score += 0.05

    today = datetime.date.today()
    donor_age = today.year - donor.birthday.year - ((today.month, today.day) < (donor.birthday.month, donor.birthday.day))
    recipient_age = today.year - recipient.birthday.year - ((today.month, today.day) < (recipient.birthday.month, recipient.birthday.day))

    if 1 <= donor_age <= 8:
        score += 0.1

    possible_amount = get_possible_blood_donation_amount(donor)
    if possible_amount >= search_card.blood_amount:
        score += 0.8
    elif possible_amount * 1.5 >= search_card.blood_amount:
        score += 0.7
    elif possible_amount * 2 >= search_card.blood_amount:
        score += 0.6

    # возраст
    # чем ближе к рецепиенту по возрасту в рамках разрешенных тем больше очков, но в рамках от 1 до 8
    return round(score, 2)


def blood_type_match(recipient_blood_type: str, donor_blood_type: str, pet_type: PetType):
    if donor_blood_type == recipient_blood_type:
        return True
    if pet_type.id == 0:  # Собака
        if donor_blood_type == "DEA-":
            return True
    elif pet_type.id == 1:  # Кошка
        if donor_blood_type == "A" and recipient_blood_type == "AB":
            return True

    return False


def get_possible_blood_donation_amount(donor):
    DOG_AMOUNT_PER_KG = 10
    CAT_AMOUNT_PER_KG = 15
    if donor.pet_type == 0:
        per_kg = DOG_AMOUNT_PER_KG
    elif donor.pet_type == 1:
        per_kg = CAT_AMOUNT_PER_KG
    else:
        per_kg = 0
    return per_kg * donor.weight


def compare_words(word1, word2):
    return difflib.get_close_matches(word1, [word2], n=1, cutoff=0.6)
