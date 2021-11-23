import datetime
from abc import ABC, abstractmethod

from django.db import connections


class FilterMethod(ABC):

    def __init__(self, start_date=None, end_date=None):
        self.start_date = start_date if start_date else None
        self.end_date = end_date if end_date else None

    @abstractmethod
    def request_department_list(self):
        pass


class DepartmentListNumbers:

    def __init__(self, filter_method: FilterMethod):
        self._filter_method = filter_method

    @property
    def filter_method(self) -> FilterMethod:
        return self._filter_method

    @filter_method.setter
    def filter_method(self, filter_method):
        self._filter_method = filter_method

    def get_department_number_list(self) -> list:
        number_list = self._filter_method.request_department_list()
        return number_list


class BothDatesFilterMethod(FilterMethod):

    def request_department_list(self):
        number_list = []
        with connections['statisticdb'].cursor() as cursor:
            cursor.execute(f"select * "
                           f"from "
                           f"(select caller_id_number, sum(billsec) as sum_mezhgorod "
                           f"from cdr "
                           f"where LENGTH (caller_id_number) = 7 and char_length(destination_number) >= 11 "
                           f"and hangup_cause = 'NORMAL_CLEARING' and start_stamp >= '{self.start_date}' "
                           f"and start_stamp <= '{self.end_date}' "
                           f"group by caller_id_number) t1 "
                           f"full join "
                           f"(select caller_id_number, sum(billsec) as sum_gorod "
                           f"from cdr "
                           f"where LENGTH (caller_id_number) = 7 and char_length(destination_number) >= 7 "
                           f"and char_length(destination_number) <= 8 "
                           f"and hangup_cause = 'NORMAL_CLEARING' and start_stamp >= '{self.start_date}' "
                           f"and start_stamp <= '{self.end_date}' "
                           f"group by caller_id_number) t2 "
                           f"on t1.caller_id_number = t2.caller_id_number; ")
            data = cursor.fetchall()
        for number in data:
            number_list.append(number)
        return number_list


class StartDateFilterMethod(FilterMethod):

    def request_department_list(self):
        number_list = []
        with connections['statisticdb'].cursor() as cursor:
            cursor.execute(f"select * "
                           f"from "
                           f"(select caller_id_number, sum(billsec) as sum_mezhgorod "
                           f"from cdr "
                           f"where LENGTH (caller_id_number) = 7 and char_length(destination_number) >= 11 "
                           f"and hangup_cause = 'NORMAL_CLEARING' and start_stamp >= '{self.start_date}' "
                           f"group by caller_id_number) t1 "
                           f"full join "
                           f"(select caller_id_number, sum(billsec) as sum_gorod "
                           f"from cdr "
                           f"where LENGTH (caller_id_number) = 7 and char_length(destination_number) >= 7 "
                           f"and char_length(destination_number) <= 8 "
                           f"and hangup_cause = 'NORMAL_CLEARING' and start_stamp >= '{self.start_date}' "
                           f"group by caller_id_number) t2 "
                           f"on t1.caller_id_number = t2.caller_id_number; ")
            data = cursor.fetchall()
        for number in data:
            number_list.append(number)
        return number_list


class EndDateFilterMethod(FilterMethod):

    def request_department_list(self):
        number_list = []
        with connections['statisticdb'].cursor() as cursor:
            cursor.execute(f"select * "
                           f"from "
                           f"(select caller_id_number, sum(billsec) as sum_mezhgorod "
                           f"from cdr "
                           f"where LENGTH (caller_id_number) = 7 and char_length(destination_number) >= 11 "
                           f"and hangup_cause = 'NORMAL_CLEARING' and start_stamp <= '{self.end_date}' "
                           f"group by caller_id_number) t1 "
                           f"full join "
                           f"(select caller_id_number, sum(billsec) as sum_gorod "
                           f"from cdr "
                           f"where LENGTH (caller_id_number) = 7 and char_length(destination_number) >= 7 "
                           f"and char_length(destination_number) <= 8 "
                           f"and hangup_cause = 'NORMAL_CLEARING' and start_stamp <= '{self.end_date}' "
                           f"group by caller_id_number) t2 "
                           f"on t1.caller_id_number = t2.caller_id_number; ")
            data = cursor.fetchall()
        for number in data:
            number_list.append(number)
        return number_list

