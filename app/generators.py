import random
import string
from app import app

def generate_short_url(length=app.config['SHORT_LINK_LENGTH']):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))