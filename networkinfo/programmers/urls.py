from django.urls import path

from programmers.views import SearchPcView

urlpatterns = [
    path('', SearchPcView.as_view(), name='search-pc')
]