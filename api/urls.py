from django.urls import path, include
from rest_framework.routers import DefaultRouter

from api.views import email_confirm, password_confirm

app_name = 'api'

routers = DefaultRouter()


urlpatterns = [
    path('objects/', include("api.lot.urls", namespace='lot-api')),
    path('objects/', include("api.user.urls", namespace='user-api')),
    path('email-confirm/<str:token>/', email_confirm, name='email-confirm'),
    path('password-confirm/<str:token>/', password_confirm, name='password-confirm')
]

urlpatterns += routers.urls
