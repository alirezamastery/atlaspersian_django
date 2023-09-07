import random


__all__ = [
    'generate_otp'
]


def generate_otp():
    return ''.join(str(random.randint(0, 9)) for _ in range(5))
