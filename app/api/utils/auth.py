import secrets
import string


def generate_secret(length: int = 32):
    alphabet = string.ascii_letters + string.digits
    return "".join(secrets.choice(alphabet) for i in range(length))
