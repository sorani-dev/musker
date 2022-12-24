import os
import secrets
import sys

from django.core.management.utils import get_random_secret_key
info=sys.version_info
print(info)
if info[0] == 3 and info[1] >= 6:
    print('secrets generated: ')
    print(secrets.token_urlsafe())
    print()
print('django generated: ')
print(get_random_secret_key())
print()
