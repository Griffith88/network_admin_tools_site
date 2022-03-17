from django.http import HttpResponse
from django.shortcuts import render
from django.views import View

from programmers.utils.get_all_win7_with_internet import get_all_win7, get_all_users_with_win7inet
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


class Win7WithInet(View):
    def get(self, request):
        data = get_all_users_with_win7inet()
        return render(request, 'programmers/win7_search.html', context={'data': data})
