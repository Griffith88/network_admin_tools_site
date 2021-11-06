from django.shortcuts import render

# Create your views here.
from django.views import View

from programmers.utils.pc_info import Computer


class SearchPcView(View):
    def get(self, request):
        template_name = 'programmers/search_page.html'
        pc_name = request.GET.get('pc_name')
        if pc_name:
            pc = Computer(pc_name)
            login, ip, name = pc.info
            return render(request, template_name, {
                'login': login,
                'ip': ip,
                'name': name,
                'pc_name': pc_name,
                'search': True
            })
        return render(request, template_name, {})
