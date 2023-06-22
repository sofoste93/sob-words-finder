import random
import string


def generate_credentials():
    """Generate a random username and a 5-digit PIN."""
    username = ''.join(random.choices(string.ascii_letters, k=5))
    pin = ''.join(random.choices(string.digits, k=5))
    return username, pin


def verify_credentials(username, pin, session):
    """Verify if the provided username and PIN match the ones stored in session."""
    return session.get('username') == username and session.get('pin') == pin
