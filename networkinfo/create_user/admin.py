from django.contrib import admin
from create_user.models import UserCreateModel


# Register your models here.


@admin.register(UserCreateModel)
class CreateAdmin(admin.ModelAdmin):
    list_display = ['id', 'full_name', 'position', 'department_id', 'personal_number', 'created_at', 'updated_at',
                    'db_id', 'is_created']
    ordering = ['id']
