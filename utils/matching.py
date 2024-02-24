from database.models import SearchCard, Pet, PetType


def get_matching_score(search_card: SearchCard, donor: Pet) -> float:
    """
    Returns the degree of compatibility with the recipient from 0 to 1
    """

    recipient = search_card.recipient
    score = 0

    if recipient.pet_type != donor.pet_type:
        return score
    if not blood_type_match(recipient.blood_type, donor.blood_type, donor.pet_type):
        return score
    possible_amount = get_possible_blood_donation_amount(donor)
    if possible_amount >= recipient.blood_amount:
        score += 0.8
    # если объем чуть ниже то тоже можно, но меньше процент 


def blood_type_match(recipient_blood_type: str, donor_blood_type: str, pet_type: PetType):
    if donor_blood_type == recipient_blood_type:
        return True
    if pet_type.id == 0:  # Собака
        if donor_blood_type == "DEA-":
            return True
    elif pet_type.id == 1:  # Кошка
        if donor_blood_type == "a" and recipient_blood_type == "ab":
            return True

    return False


def get_possible_blood_donation_amount(donor):
    DOG_AMOUNT_PER_KG = 88
    CAT_AMOUNT_PER_KG = 60
    if donor.pet_type == 0:
        per_kg = DOG_AMOUNT_PER_KG
    elif donor.pet_type == 1:
        per_kg = CAT_AMOUNT_PER_KG
    else:
        per_kg = 0
    return per_kg * donor.weight
