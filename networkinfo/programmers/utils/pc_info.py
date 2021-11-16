import os.path
import re
from abc import ABC
import json
from ldap3 import Connection, NTLM
from django.db import connections
from networkinfo import settings
from networkinfo.settings import LDAP_SERVER, BASE_DIR
from programmers.utils.convert_ip import IpAddress

LOGIN_PATTERN = re.compile(r'^Login:\s{1}(\w+.\w+|\w+)$')
IP_PATTERN = re.compile(r'^\s{1}IP:\s{2}(\d+.\d+.\d+.\d+)')


class Computer(ABC):
    def __init__(self, name):
        self.name = name

    def get_info(self):
        pass

    @property
    def info(self):
        return self.get_info()


class LdapComputer(Computer):
    conn = Connection(server=LDAP_SERVER,
                      user=f'av\\{settings.LDAP_USERNAME}',
                      password=settings.LDAP_PASSWORD,
                      auto_bind=True,
                      return_empty_attributes=True,
                      authentication=NTLM)

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
        return {'login': login.lower(),
                'ip': ip,
                'cn': cn}

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


class KasperComputer(Computer):
    def get_info(self) -> dict:
        with connections['kav'].cursor() as cursor:
            cursor.execute(
                f"SELECT "
                f"dbo.v_akpub_host.nId, "
                f"dbo.v_akpub_users_and_groups.wstrDisplayName, "
                f"dbo.v_akpub_users_and_groups.wstrSamAccountName, "
                f"dbo.v_akpub_host.wstrDisplayName, "
                f"dbo.v_akpub_host.nIp, "
                f"dbo.v_akpub_users_and_groups.wstrDepartment "
                f"FROM dbo.v_akpub_users_and_groups "
                f"JOIN dbo.v_akpub_hst_loggedin_users "
                f"ON (dbo.v_akpub_hst_loggedin_users.binUserId = dbo.v_akpub_users_and_groups.binId) "
                f"JOIN dbo.v_akpub_host "
                f"ON (dbo.v_akpub_host.nId = dbo.v_akpub_hst_loggedin_users.nHost) "
                f"WHERE dbo.v_akpub_host.wstrDisplayName = '{self.name}'")
            data = cursor.fetchone()
            if not data:
                return {}
            host_id, cn, login, comp_name, ip_raw, department = data
            ip = IpAddress(str(ip_raw))
            ip = ip.convert()
            os_info = self.get_os_info()
            motherboard = self.get_motherboard_info(cursor, host_id)
            ram_list, ram_full_capacity = {'ram_list': self.get_ram_info(cursor, host_id)[0]}, \
                                          {'ram_full_capacity': self.get_ram_info(cursor, host_id)[1]}
            cpu = self.get_cpu_info(cursor, host_id)
            hd_list = {'hd_list': self.get_hd_info(cursor, host_id)}
            video_list = {'video_list': self.get_video_info(cursor, host_id)}
            network_list = {'network_list': self.get_network_info(cursor, host_id)}
            return {'login': login.lower(),
                    'ip': ip,
                    'cn': cn,
                    'department': department,
                    **motherboard,
                    **ram_list,
                    **ram_full_capacity,
                    **cpu,
                    **hd_list,
                    **video_list,
                    **network_list,
                    **os_info}

    def get_motherboard_info(self, cursor, host_id):
        cursor.execute(
            f"SELECT "
            f"dbo.v_akpub_hwinv.wstrName, "
            f"dbo.v_akpub_hwinv.wstrManufacturer, "
            f"dbo.v_akpub_hwinv.strBiosManuf, "
            f"dbo.v_akpub_hwinv.strBiosVersion "
            f"FROM KAV.dbo.v_akpub_hwinv WHERE dbo.v_akpub_hwinv.nType = 0 and dbo.v_akpub_hwinv.nHost = {host_id};"
        )
        data = cursor.fetchone()
        name, manufacturer, bios_manufacturer, bios_version = data
        motherboard = {'motherboard_name': name,
                       'manufacturer': manufacturer,
                       'bios_manufacturer': bios_manufacturer,
                       'bios_version': bios_version,
                       }
        return motherboard

    def get_cpu_info(self, cursor, host_id):
        cursor.execute(f"SELECT wstrName, nCpuSpeed, nCpuCores, nCpuThreads "
                       f"FROM dbo.v_akpub_hwinv vah "
                       f"WHERE nType = 1 and nHost = {host_id}")

        data = cursor.fetchone()
        cpu, cpu_speed, cpu_cores, cpu_threads = data
        return {'cpu': cpu,
                'cpu_speed': cpu_speed,
                'cpu_cores': cpu_cores,
                'cpu_threads': cpu_threads}

    def get_ram_info(self, cursor, host_id):
        ram_list = []
        ram_full_capacity = 0
        cursor.execute(f"SELECT wstrName, nCapacity, nSpeed "
                       f"FROM dbo.v_akpub_hwinv vah "
                       f"WHERE nType = 2 and nHost = {host_id}")
        data = cursor.fetchall()
        for elem in data:
            ram, ram_capacity, ram_speed = elem
            ram_list.append({'ram': ram,
                             'ram_capacity': ram_capacity,
                             'ram_speed': ram_speed})
            ram_full_capacity += int(ram_capacity)
        return ram_list, ram_full_capacity

    def get_hd_info(self, cursor, host_id):
        hd_list = []
        cursor.execute(f"SELECT wstrName, nCapacity "
                       f"FROM dbo.v_akpub_hwinv vah "
                       f"WHERE nType = 3 and nHost = {host_id}")

        data = cursor.fetchall()
        for elem in data:
            hd, hd_capacity = elem
            hd_list.append({'hd': hd, 'hd_capacity': hd_capacity // 1000})
        return hd_list

    def get_video_info(self, cursor, host_id):
        video_list = []
        cursor.execute(f"SELECT wstrName, wstrDriverVersion "
                       f"FROM dbo.v_akpub_hwinv vah "
                       f"WHERE nType = 4 and nHost = {host_id}")

        data = cursor.fetchall()
        for elem in data:
            video, video_driver = elem
            if video.startswith('DameWare'):
                continue
            video_list.append({'video': video, 'video_driver': video_driver})
        return video_list

    def get_network_info(self, cursor, host_id):
        network_list = []
        cursor.execute(f"SELECT wstrName, strMAC, nSpeed "
                       f"FROM dbo.v_akpub_hwinv vah "
                       f"WHERE nType = 6 and nHost = {host_id}")

        data = cursor.fetchall()
        for elem in data:
            network, network_mac, network_speed = elem
            network_list.append({'network': network, 'network_mac': network_mac, 'network_speed': network_speed})
        return network_list

    def get_os_info(self):
        conn = LdapComputer.conn
        with conn:
            conn.search(
                search_base="ou=Corp_Computers,dc=ashipyards,dc=com",
                search_filter=f'(&(objectClass=computer)(name={self.name}))',
                attributes=['operatingSystem', 'operatingSystemVersion', ])
            if not conn.entries:
                return {}
            data = conn.entries[0]
            result = {'os': data.operatingSystem,
                      'os_build': data.operatingSystemVersion}
            if data.operatingSystem == 'Windows 10 Корпоративная':
                with open(file=os.path.join(BASE_DIR, 'win10_versions.json')) as file:
                    data = json.load(file)
                    try:
                        os_version = data[str(result['os_build'])]
                        result.update({'os_version': os_version})
                    except KeyError:
                        pass
            elif data.operatingSystem == 'Windows 10 Корпоративная 2016 с долгосрочным обслуживанием':
                result.update({'os_version': 'LTSB 2016'})
            return result
