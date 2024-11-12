import random
import string


def generate_random_string(length=6):
    """
    You can add a custom length of the random string to be generated, the default value will be 6
    """
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(length))

