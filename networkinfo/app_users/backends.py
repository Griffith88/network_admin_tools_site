import ldap3.core.exceptions
from django.contrib.auth.models import User, Group
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
                        conn.search(search_base='DC=ashipyards,DC=com',
                                    search_filter=f'(&(objectClass=person)(sAMAccountName={username}))',
                                    search_scope='SUBTREE',
                                    attributes=['distinguishedName', ])
                        user_dn = conn.entries[0].distinguishedName
                        user = User.objects.create_user(username=username,
                                                        password=password,
                                                        email=f'{username}@ashipyards.com')
                        conn.search(search_base='CN=Администраторы домена,CN=Users,DC=ashipyards,DC=com',
                                    search_filter='(objectClass=group)',
                                    search_scope='SUBTREE',
                                    attributes=['member', ])
                        if user_dn in conn.entries[0].member.values:
                            user.groups.add(Group.objects.get(name='domain_admins'))
                        return user
        except ldap3.core.exceptions.LDAPBindError:
            return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
