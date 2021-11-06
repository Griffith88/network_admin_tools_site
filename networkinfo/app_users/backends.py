import ldap3.core.exceptions
from django.contrib.auth.models import User
from ldap3 import Connection

from networkinfo.settings import LDAP_SERVER


class LDAPBackend:
    def authenticate(self, request, username=None, password=None, **kwargs):
        username = username.lower()
        try:
            with Connection(server=LDAP_SERVER,
                            user=f'av\{username}',
                            password=password,
                            auto_bind=True, ) as conn:
                if conn.bind():
                    try:
                        user = User.objects.get(username=username)
                        return user
                    except User.DoesNotExist:
                        user = User.objects.create_user(username=username,
                                                        password=password,
                                                        email=f'{username}@ashipyards.com')
                        return user
        except ldap3.core.exceptions.LDAPBindError:
            return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
