from django.conf import settings
from ldap3 import Connection

from networkinfo.settings import LDAP_SERVER
from utils.decorators import db_connections


@db_connections('kav')
def get_all_win7(cursor):
    cursor.execute(f"""
     SELECT 
        dbo.v_akpub_host.wstrOSName,
        dbo.v_akpub_users_and_groups.wstrSamAccountName,
        dbo.v_akpub_users_and_groups.wstrDisplayName,
        dbo.v_akpub_host.wstrDisplayName
    FROM dbo.v_akpub_users_and_groups 
    JOIN dbo.v_akpub_hst_loggedin_users 
    ON (dbo.v_akpub_hst_loggedin_users.binUserId = dbo.v_akpub_users_and_groups.binId) 
    JOIN dbo.v_akpub_host 
    ON (dbo.v_akpub_host.nId = dbo.v_akpub_hst_loggedin_users.nHost)
    WHERE dbo.v_akpub_host.wstrOSName = 'Microsoft Windows 7'
    """)

    data = cursor.fetchall()
    return data


def get_all_users_with_win7inet():
    data = get_all_win7()
    conn = Connection(server=LDAP_SERVER,
                      user=f'{settings.LDAP_USERNAME}',
                      password=settings.LDAP_PASSWORD,
                      return_empty_attributes=True, )

    with conn:
        conn.search(
            search_base='CN=InternetUsers,DC=ashipyards,DC=com',
            search_filter='(objectClass=group)',
            attributes=['member']
        )
        list_of_internet_users = [item.member.values for item in conn.entries]
        conn.search(
            search_base='CN=FInternetUsers,DC=ashipyards,DC=com',
            search_filter='(objectClass=group)',
            attributes=['member']
        )
        list_of_full_internet_users = [item.member.values for item in conn.entries]
        list_of_users = list_of_internet_users + list_of_full_internet_users
        list_of_users_with_inet = []
        for user in data:
            if user[2] in str(list_of_users):
                list_of_users_with_inet.append(user)
        print(len(list_of_users_with_inet))
        return list_of_users_with_inet


if __name__ == '__main__':
    get_all_win7()
