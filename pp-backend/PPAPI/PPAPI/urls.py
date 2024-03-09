"""
URL configuration for PPAPI project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.urls import path
from PPApp import endpoints
from PPApp.endpoints import user

urlpatterns = [
    path('admin/', admin.site.urls),
    path('user/', endpoints.user),
    path('session/', endpoints.sessions),
    path('chat/', endpoints.chat),
    path('product/', endpoints.products),
    path('lists/', endpoints.listasCompra),
    path('lists/<int:list_pk>/', endpoints.list_info),
    path('lists/<int:list_pk>/items/', endpoints.productsinList),
    path('lists/<int:list_id>/items/<int:item_id>/', endpoints.edit_item),

]


