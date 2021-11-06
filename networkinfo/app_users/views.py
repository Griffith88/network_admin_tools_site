from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.views import LogoutView
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import View
from ldap3 import NTLM
from app_users.backends import LDAPBackend


class UserLoginView(View):
    def get(self, request):
        return render(request, template_name='app_users/login.html', context={})

    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')
        back = LDAPBackend()
        user = back.authenticate(request=request, username=username, password=password, authentication=NTLM, )
        if user is not None:
            login(request, user, backend='app_users.backends.LDAPBackend')
            return HttpResponseRedirect(reverse_lazy('programmers:search-pc'))
        else:
            messages.error(request, 'Неправильное имя пользователя или пароль')
            return render(request, template_name='app_users/login.html', context={})


class UserLogoutView(LogoutView):
    template_name = 'app_users/logout.html'
