import re
from ldap3 import Connection, NTLM

from networkinfo import settings
from networkinfo.settings import LDAP_SERVER

LOGIN_PATTERN = re.compile(r'^Login:\s{1}(\w+.\w+|\w+)$')
IP_PATTERN = re.compile(r'^\s{1}IP:\s{2}(\d+.\d+.\d+.\d+)')


class Computer:
    def __init__(self, name):
        self.name = name
        self.conn = Connection(server=LDAP_SERVER,
                               user=settings.LDAP_USERNAME,
                               password=settings.LDAP_PASSWORD,
                               auto_bind=True,
                               return_empty_attributes=True,
                               authentication=NTLM)

    @property
    def info(self):
        return self.get_info()

    def get_info(self):
        with self.conn as conn:
            conn.search(
                search_base="ou=Corp_Computers,dc=ashipyards,dc=com",
                search_filter=f'(&(objectClass=computer)(name={self.name}))',
                attributes=['description', ])
            if not conn.entries:
                return None, None, None
            ip, login = self.parse_computer_description(conn)
            cn = self.get_distinguished_name(login, conn)
        return login.lower(), ip, cn

    def parse_computer_description(self, conn):
        entry = conn.entries[0]
        entry = str(entry.description).split(';')
        raw_login, raw_ip = entry[0:2]
        login = re.search(LOGIN_PATTERN, raw_login).group(1)
        ip = re.search(IP_PATTERN, raw_ip).group(1)
        return ip, login

    def get_distinguished_name(self, username, conn):
        conn.search(
            search_base="dc=ashipyards,dc=com",
            search_filter=f'(&(objectClass=person)(samaccountname={username}))',
            attributes=['ipPhone', 'cn'])
        entry = conn.entries[0]
        cn = str(entry.cn)
        return cn
