import os.path
import paramiko
from networkinfo.settings import BASE_DIR


def add_mail_to_relay(mail: str):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect('192.168.100.108', username='defuser', key_filename=os.path.join(BASE_DIR, 'id_rsa'))
    ssh.exec_command(f'/home/defuser/addToRelayMap.sh {mail}')
    ssh.close()
