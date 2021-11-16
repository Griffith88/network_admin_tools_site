from django.urls import path
from main_page.views import MainPageView

urlpatterns = [
    path('', MainPageView.as_view(), name='main')
]