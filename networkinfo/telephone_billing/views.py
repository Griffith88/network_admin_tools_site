import collections
import time

from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.shortcuts import render
from django.views import View
from telephone_billing.backend.departments_info import DepartamentNumber
from telephone_billing.utils.department_list_statistic import *


class BillingMainPage(LoginRequiredMixin, PermissionRequiredMixin, View):
    permission_required = 'create_user.view_usercreatemodel'

    def get(self, request):
        line_dict = {}
        template_name = 'telephone_billing/main_billing_page.html'
        filter_method, start_date, end_date = self.handle_get_request(request)
        department_numbers = DepartmentListNumbers(filter_method)
        numbers_list = department_numbers.get_department_number_list()
        for line in numbers_list:
            line_obj = DepartamentNumber(line)
            if not line_obj.department or line_obj.department == 'pass':
                continue
            if line_obj.department in line_dict:
                line_dict.update({
                    line_obj.department: [line_dict[line_obj.department][0] + line_obj.bill_sec_city,
                                          line_dict[line_obj.department][1] + line_obj.bill_sec_intercity]})
            else:
                line_dict.update({line_obj.department: [line_obj.bill_sec_city, line_obj.bill_sec_intercity]})
        self.format_seconds_into_time(line_dict)

        context = {'line_dict': collections.OrderedDict(sorted(line_dict.items(), reverse=False)),
                   'start_date': str(start_date),
                   'end_date': str(end_date)}
        return render(request, template_name, context)

    def format_seconds_into_time(self, line_dict):
        for dep, bill_secs in line_dict.items():
            for index, bill_sec in enumerate(bill_secs):
                line_dict[dep][index] = time.strftime('%H:%M:%S', time.gmtime(bill_sec))

    def handle_get_request(self, request):
        start_date = request.GET.get('start_date')
        end_date = request.GET.get('end_date')
        if start_date and end_date:
            filter_method = BothDatesFilterMethod(start_date=start_date,
                                                  end_date=end_date)
        elif start_date and not end_date:
            filter_method = StartDateFilterMethod(start_date=start_date)
        elif not start_date and end_date:
            filter_method = EndDateFilterMethod(end_date=end_date)
        else:
            end_date = datetime.date.today()
            start_date = end_date - datetime.timedelta(days=30)
            filter_method = BothDatesFilterMethod(start_date=start_date,
                                                  end_date=end_date)
        return filter_method, start_date, end_date
