from abc import ABC
from django.db import connections


class Line(ABC):

    def __init__(self, line: tuple):
        self.line = line[0] if line[0] else line[2]
        self.bill_sec_city = line[1] if line[1] else 0
        self.bill_sec_intercity = line[3] if line[3] else 0

    def __str__(self):
        return self.line


class DepartamentNumber(Line):

    def get_info(self):
        query_line = f"'{self.line}'"
        with connections['freeswitchdb'].cursor() as cursor:
            cursor.execute(f'select description from directory_numbers where number = {query_line}')
            data = cursor.fetchone()
        if not data:
            return None
        description = data[0]
        return description.split('(')[0]

    @property
    def department(self):
        return self.get_info()
