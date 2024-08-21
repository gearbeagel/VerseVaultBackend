import random
import string

from django.contrib.auth.models import User

def generate_unique_username(base_username):
    username = base_username
    while User.objects.filter(username=username).exists():
        # Append a random number to the base username
        random_suffix = ''.join(random.choices(string.ascii_lowercase + string.digits, k=4))
        username = f"{base_username}_{random_suffix}"
    return username
