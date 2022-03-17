from django.urls import path

from programmers.views import SearchPcView, Win7WithInet

urlpatterns = [
    path('', SearchPcView.as_view(), name='search-pc'),
    path('win7inet', Win7WithInet.as_view(), name='win7inet')
]