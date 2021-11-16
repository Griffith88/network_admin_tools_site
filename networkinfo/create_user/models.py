from django.db import models


# Create your models here.
class UserCreateModel(models.Model):
    department_id = models.IntegerField(verbose_name='Номер подразделения', )
    second_name = models.CharField(max_length=100, verbose_name='Фамилия')
    first_name = models.CharField(max_length=100, verbose_name='Имя')
    middle_name = models.CharField(max_length=100, verbose_name='Отчество')
    position = models.CharField(max_length=500, verbose_name='Должность')
    db_id = models.IntegerField(verbose_name='Уникальный индификатор')
    full_name = models.CharField(max_length=300, verbose_name='ФИО')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Создано')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Обновлено')
    is_created = models.BooleanField(default=False, verbose_name='Пользователь создан')
    personal_number = models.IntegerField(verbose_name='Табельный номер')

    def __str__(self):
        return self.full_name
