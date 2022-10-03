from django.urls import path, include
from rest_framework.routers import DefaultRouter

from api.lot.views import APILot, APITicket

router = DefaultRouter()

app_name = 'lot-api'

router.register("ticket", APITicket)
router.register("lot", APILot)


urlpatterns = [
    path('lottery/', include(router.urls)),
]

