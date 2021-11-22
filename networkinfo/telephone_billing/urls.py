from django.urls import path
from django.views.decorators.cache import cache_page

from telephone_billing.views import BillingMainPage

urlpatterns = [
    path('', cache_page(15)(BillingMainPage.as_view()), name='billing_main')
]
