from django.shortcuts import render
from django.views import View
from programmers.utils.pc_info import KasperComputer
from programmers.utils.user_info import KasperUser


class SearchPcView(View):
    def get(self, request):
        template_name = 'programmers/search_page.html'
        value = request.GET.get('value')
        search_type = request.GET.get('search_type')
        if search_type == 'ПК' and value:
            pc = KasperComputer(value)
            context = {**pc.info,
                       'pc_name': value,
                       'search': 'pc'}
            return render(request, template_name, context)
        elif search_type == 'Пользователь' and value:
            user = KasperUser(value)
            context = {'pc_list': user.info,
                       'user_login': value,
                       'search': 'user'}
            return render(request, template_name, context)
        return render(request, template_name, {})
