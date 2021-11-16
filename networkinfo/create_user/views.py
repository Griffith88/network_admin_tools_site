from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.shortcuts import render
from django.views import View
from create_user.models import UserCreateModel
from create_user.utils.ldap import LdapUser, LdapServer
from django.forms.models import model_to_dict


class CreateUserView(PermissionRequiredMixin, LoginRequiredMixin, View):
    permission_required = 'create_user.view_usercreatemodel'

    def get(self, request):
        template_name = 'create_user/create_user.html'
        if request.GET.get('personal_number'):
            user = LdapUser.from_sql(int(request.GET.get('personal_number')))
            context = {
                'full_name': user.info['full_name'],
                'position': user.info['position'],
                'department': user.info['department_id'],
                'personal_number': request.GET.get('personal_number'),
                'db_id': user.info['db_id']
            }
            server = LdapServer(user)
            if server.is_user_exists_by_pn():
                messages.error(request, message='Такой табельный номер уже есть в Active Directory')
                return render(request, template_name, {})
            try:
                UserCreateModel.objects.get(db_id=user.info['db_id'])
            except UserCreateModel.DoesNotExist:
                UserCreateModel.objects.create(**user.info)
            return render(request, template_name, context)
        else:
            return render(request, template_name, {})

    def post(self, request):
        template_name = 'create_user/create_user.html'
        user_model = UserCreateModel.objects.get(db_id=request.POST.get('db_id'))
        user = LdapUser.from_dict(model_to_dict(user_model))
        server = LdapServer(user, is_secretary=request.POST.get('secretary'))
        if server.is_user_exists_by_login(request.POST.get('login')):
            messages.error(request, message='Пользователь с таким логином уже есть в базе данных Active Directory')
            context = {
                'full_name': user.info['full_name'],
                'position': user.info['position'],
                'department': user.info['department_id'],
                'personal_number': request.GET.get('personal_number'),
                'db_id': user.info['db_id']
            }
            return render(request, template_name, context)
        server.create_user(request.POST.get('login'))
        user_model.is_created = True
        user_model.save()
        return render(request, template_name, {'success': True})
