"""networkinfo URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(('main_page.urls', 'main_page'), namespace='main_page')),
    path('users/', include(('app_users.urls', 'app_users'), namespace='app_users')),
    path('programmers/', include(('programmers.urls', 'programmers'), namespace='programmers')),
    path('create/', include(('create_user.urls', 'create_user'), namespace='create_user')),
    path('billing/', include(('telephone_billing.urls', 'telephone_billing'), namespace='telephone_billing'))
]