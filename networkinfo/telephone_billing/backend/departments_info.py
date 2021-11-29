from abc import ABC

from utils.decorators import db_connections


class Line(ABC):

    def __init__(self, line: tuple):
        self.line = line[0] if line[0] else line[2]
        self.bill_sec_city = line[3] if line[3] else 0
        self.bill_sec_intercity = line[1] if line[1] else 0

    def __str__(self):
        return self.line


class DepartamentNumber(Line):

    @db_connections(connection_name='freeswitchdb')
    def get_info(self, cursor):
        query_line = f"'{self.line}'"
        cursor.execute(f'select description from directory_numbers where number = {query_line}')
        data = cursor.fetchone()
        if not data:
            return None
        description = data[0]
        return description.split('(')[0]

    @property
    def department(self):
        return self.get_info()
