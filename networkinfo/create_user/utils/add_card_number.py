import mysql.connector

from networkinfo.settings import skud_config


def add_card_number(personal_number: str) -> str or None:
    """
    method for executing card_number from user's card from SCUD database for subsequent adding into ActiveDirectory attr
    :param personal_number:
    """
    db = mysql.connector.Connect(**skud_config)
    result = ''
    cursor = db.cursor()
    cursor.execute(f"select name,codekey from personal where tabid={personal_number} and status='AVAILABLE';")
    array_of_bytes = cursor.fetchone()
    if not array_of_bytes:
        return None
    for byte_position in range(1, len(array_of_bytes[1]) - 4):
        byte = hex(array_of_bytes[1][byte_position])
        byte = byte.replace('0x', '')
        result += byte if len(byte) != 1 else '0' + byte
    cursor.close()
    db.close()
    return clear_zero(result)


def clear_zero(array):
    while array.startswith('0'):
        array = array[1:]
    return array
