import datetime

from django.db import connections


class DateFilter:
    def get_departament_list_numbers(self,) -> list:
        number_list = []
        if not start_date and not end_date:
            end_date = datetime.date.today()

        with connections['statisticdb'].cursor() as cursor:
            cursor.execute(f"select * "
                           f"from "
                           f"(select caller_id_number, sum(billsec) as sum_mezhgorod "
                           f"from cdr "
                           f"where LENGTH (caller_id_number) = 7 and char_length(destination_number) >= 11 "
                           f"and hangup_cause = 'NORMAL_CLEARING' "
                           f"group by caller_id_number) t1 "
                           f"inner join "
                           f"(select caller_id_number, sum(billsec) as sum_gorod "
                           f"from cdr "
                           f"where LENGTH (caller_id_number) = 7 and char_length(destination_number) = 8 "
                           f"and hangup_cause = 'NORMAL_CLEARING' "
                           f"group by caller_id_number) t2 "
                           f"on t1.caller_id_number = t2.caller_id_number; ")
            data = cursor.fetchall()
        for number in data:
            number_list.append(number)
        return number_list
