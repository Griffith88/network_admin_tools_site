from django.shortcuts import render

# Create your views here.
from django.views import View

from programmers.utils.pc_info import KasperComputer


class SearchPcView(View):
    def get(self, request):
        template_name = 'programmers/search_page.html'
        pc_name = request.GET.get('pc_name')
        if pc_name:
            pc = KasperComputer(pc_name)
            context = {**pc.info,
                       'pc_name': pc_name,
                       'search': True}
            return render(request, template_name, context)
        return render(request, template_name, {})
