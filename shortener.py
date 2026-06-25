import secrets
from database import get_url

# Generate a unique short code
# Keeps regenerating if collision is found
def generate_short_code(length: int = 6) -> str:
    while True:
        # Generate a random URL-safe string
        code = secrets.token_urlsafe(length)[:length]

        # Guarantee uniqueness — check against DB
        if get_url(code) is None:
            return code