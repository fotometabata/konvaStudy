"""konvastudy URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
from rest_framework_jwt.views import obtain_jwt_token, verify_jwt_token
from django.contrib import admin
from django.urls import path, include
from users.urls import ACT_ROUTER
from utils.views import FileBase64Upload

API_URLPATTERN = [
    path('acts/', include(ACT_ROUTER.urls)),
    path('token/', obtain_jwt_token),
    path('token/verify', verify_jwt_token),
    path('saveImageFile/', FileBase64Upload.as_view()),
]

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/1.0/', include(API_URLPATTERN)),
]
