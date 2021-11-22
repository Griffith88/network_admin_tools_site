from django.shortcuts import render
# Create your views here.
from django.views import View

from telephone_billing.backend.departments_info import DepartamentNumber


class BillingMainPage(View):

    def get(self, request):
        line_dict = {}
        template_name = 'telephone_billing/main_billing_page.html'
        context = {
            'line_dict': line_dict
        }
        # TODO make filter here for view
        # numbers_list = get_departament_list_numbers()
        # for line in numbers_list:
        #     line_obj = DepartamentNumber(line)
        #     if not line_obj.department:
        #         continue
        #     if line_obj.department in line_dict:
        #         line_dict.update({
        #             line_obj.department: [line_dict[line_obj.department][0] + line_obj.bill_sec_city,
        #                                   line_dict[line_obj.department][1] + line_obj.bill_sec_intercity]})
        #     else:
        #         line_dict.update({line_obj.department: [line_obj.bill_sec_city, line_obj.bill_sec_intercity]})
        return render(request, template_name, context)
