import string
import random


def get_random_name(length=10):
    """https://stackoverflow.com/a/23728630/2213647"""
    return ''.join(
        random.SystemRandom().choice(
            string.ascii_uppercase + string.ascii_lowercase + string.digits
        )
        for _ in range(length)
    )
