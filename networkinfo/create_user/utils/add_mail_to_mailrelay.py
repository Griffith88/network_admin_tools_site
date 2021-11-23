import os.path
import paramiko
from networkinfo.settings import BASE_DIR


def add_mail_to_relay(mail: str) -> None:
    """
    method for adding user's mail into mailrelay server. remote call of bash script
    :param mail:
    """
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect('192.168.100.108', username='defuser', key_filename=os.path.join(BASE_DIR, 'id_rsa'))
    ssh.exec_command(f'/home/defuser/addToRelayMap.sh {mail}')
    ssh.close()
