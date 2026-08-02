import secrets
import string

Alphabet = string.ascii_letters + string.digits

def generate_short_code(length: int = 7) -> str:
    """Generate a random short code of specified length."""
    return ''.join(secrets.choice(Alphabet) for _ in range(length))