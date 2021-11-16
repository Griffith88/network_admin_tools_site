from django.urls import path

from create_user.views import CreateUserView

urlpatterns = [
    path('', CreateUserView.as_view(), name='create-user')
]