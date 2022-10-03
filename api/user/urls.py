from django.urls import path, include
from rest_framework.routers import DefaultRouter

from api.user.views import APIUser

router = DefaultRouter()

app_name = 'user-api'

router.register("user", APIUser)

urlpatterns = [
    path('user/', include(router.urls))
]