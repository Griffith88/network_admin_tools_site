from django.shortcuts import render

# Create your views here.
from django.views import View


class MainPageView(View):
    def get(self, request):
        template_name = 'main_page/main.html'
        return render(request, template_name, {})
