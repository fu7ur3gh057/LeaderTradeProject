import random


def generate_verification_code() -> int:
    return random.randint(100000, 999999)
