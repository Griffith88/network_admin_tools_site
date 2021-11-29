from abc import ABC
from programmers.utils.convert_ip import IpAddress
from utils.decorators import db_connections


class User(ABC):

    def __init__(self, login: str):
        self.login = login


class KasperUser(User):

    @property
    def info(self):
        return self.get_info()

    @db_connections(connection_name='kav')
    def get_info(self, cursor):
        info_list = []
        cursor.execute(
            f"SELECT dbo.v_akpub_host.wstrDisplayName, "
            f"dbo.v_akpub_host.nIp, dbo.v_akpub_users_and_groups.wstrDisplayName "
            f"FROM dbo.v_akpub_users_and_groups  "
            f"JOIN dbo.v_akpub_hst_loggedin_users "
            f"ON (dbo.v_akpub_users_and_groups.binId = dbo.v_akpub_hst_loggedin_users.binUserId) "
            f"JOIN dbo.v_akpub_host "
            f"ON (dbo.v_akpub_hst_loggedin_users.nHost = dbo.v_akpub_host.nId) "
            f"WHERE dbo.v_akpub_users_and_groups.wstrSamAccountName = '{self.login}'")
        data_list = cursor.fetchall()
        if not data_list:
            return {}
        for computer in data_list:
            pc_name, pc_ip_bin, user_full_name = computer
            ip = IpAddress(str(pc_ip_bin))
            ip = ip.convert()
            info_list.append({'pc_name': pc_name, 'ip': ip, 'user_full_name': user_full_name})
        return info_list
