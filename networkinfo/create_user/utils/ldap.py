from ldap3 import Server, Connection as Ldap, MODIFY_REPLACE
from networkinfo.settings import AD_SERVER, AD_PASSWORD, AD_USER
from create_user.utils.add_card_number import add_card_number
from create_user.utils.add_mail_to_mailrelay import add_mail_to_relay
from utils.decorators import db_connections


class LdapUser:
    """
    class for creating User. 2 methods for init from_sql database or from SPSQL server
    """

    def __init__(self, personal_number: int, info: dict):
        self.personal_number = personal_number
        self.info = info

    @classmethod
    @db_connections(connection_name='spsql')
    def from_sql(cls, personal_number: int, cursor) -> object:
        cursor.execute(
            f'SELECT [DEPARTMENT],[FNAME],[NAME1],[NAME2],[FULL_NAME],[ISN_P] '
            f'FROM [MDS].[dbo].[V_Employers_AD] '
            f'WHERE [TABN] = {personal_number}')
        user = cursor.fetchone()
        return cls(personal_number=personal_number, info={
            'department_id': str(user[0]),
            'second_name': user[1],
            'first_name': user[2],
            'middle_name': user[3],
            'position': user[4],
            'db_id': int(user[5]),
            'full_name': f"{user[1]} {user[2]} {user[3]}",
            'personal_number': personal_number,
        })

    @classmethod
    def from_dict(cls, user_dict: dict) -> object:
        return cls(personal_number=user_dict['personal_number'], info=user_dict)


class LdapServer:
    """
    class for operations in Active Directory with user:LdapUser
    """
    server = Server(AD_SERVER, use_ssl=True)
    company = "ОАО 'Адмиралтейские Верфи'"
    all_in_company_dn = "CN=ВСЕ-В-КОМПАНИИ,OU=ОАО 'Адмиралтейские Верфи',DC=ashipyards,DC=com"
    cgate_group_dn = "CN=cgate_mailgroup,CN=Users,DC=ashipyards,DC=com"

    def __init__(self, user: LdapUser, is_secretary=False):
        self.user = user
        self.is_secretary = is_secretary
        self.data = {}
        self.conn = Ldap(server=self.server,
                         user=AD_USER,
                         password=AD_PASSWORD,
                         auto_bind=True,
                         return_empty_attributes=True
                         )

    def get_distinguished_name(self):
        with self.conn:
            self.conn.search(
                search_base="ou=ОАО 'Адмиралтейские Верфи',dc=ashipyards,dc=com",
                search_filter=f'(&(objectClass=organizationalUnit)(postalCode={self.user.info["department_id"]}))',
                attributes=['name', 'distinguishedName', 'objectGUID'])
            data = self.conn.entries[0]
            self.data.update({'dn': data.distinguishedName,
                              'department_name': str(data.name), })
        return self.data['dn']

    def is_user_exists_by_pn(self):
        with self.conn:
            self.conn.search(
                search_base="dc=ashipyards,dc=com",
                search_filter=f'(&(objectClass=person)(description={self.user.personal_number}))',
                attributes=['description', ])
            return True if self.conn.entries else False

    def is_user_exists_by_login(self, login: str):
        with self.conn:
            self.conn.search(
                search_base="dc=ashipyards,dc=com",
                search_filter=f'(&(objectClass=person)(sAMAccountName={login}))',
                attributes=['sAMAccountName', ])
            return True if self.conn.entries else False

    def create_user(self, login: str, ):
        dn = self.get_distinguished_name()
        user_dn = f"CN={self.user.info['full_name']},{dn}"
        with self.conn:
            self.conn.add(dn=user_dn,
                          object_class=['person', 'user'],
                          attributes={
                              'name': self.user.info['full_name'],
                              'userPrincipalName': f'{login}@ashipyards.com',
                              'department': self.data['department_name'],
                              'company': self.company,
                              'description': self.user.personal_number,
                              'postalCode': self.user.info['db_id'],
                              'givenName': self.user.info['first_name'],
                              'displayName': self.user.info['full_name'],
                              'sn': self.user.info['second_name'],
                              'samAccountName': login,
                              'title': self.user.info['position'],
                              'mail': f'{login}@ashipyards.com',
                              'mailNickname': login,
                          })
            self.handle_user(user_dn)
            self.handle_groups(user_dn)
            self.conn.modify(dn=user_dn, changes={"extensionAttribute2": (MODIFY_REPLACE, [self.user.info['db_id']]),
                                                  "extensionAttribute3": (MODIFY_REPLACE, [self.user.personal_number])})
            add_mail_to_relay(f'{login}')
            card_number = add_card_number(str(self.user.personal_number))
            if card_number:
                self.conn.modify(dn=user_dn, changes={"extensionAttribute1": (MODIFY_REPLACE, [card_number])})

    def handle_user(self, user_dn):
        self.conn.extend.microsoft.unlock_account(user=user_dn)
        self.conn.extend.microsoft.modify_password(user=user_dn, old_password=None, new_password='123456')
        self.conn.modify(dn=user_dn, changes={"userAccountControl": (MODIFY_REPLACE, [512])})

    def handle_groups(self, user_dn):
        self.conn.extend.microsoft.add_members_to_groups(user_dn, self.all_in_company_dn)
        self.conn.extend.microsoft.add_members_to_groups(user_dn, self.cgate_group_dn)
        self.conn.extend.microsoft.add_members_to_groups(user_dn, self.get_departament_all_group_dn())
        if self.is_secretary:
            self.conn.extend.microsoft.add_members_to_groups(user_dn, self.get_departament_all_group_dn('Секретарь'))

    def get_departament_all_group_dn(self, who='Все'):
        group_name = f"{self.data['department_name']}-{who}"
        with self.conn:
            self.conn.search(search_base=str(self.data['dn']),
                             search_filter=f'(&(objectClass=group)(cn={group_name}))',
                             attributes=['distinguishedName', ])
            group = self.conn.entries[0]
            return str(group.distinguishedName)
