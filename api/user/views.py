from base64 import b64encode

from django.contrib.auth import authenticate, login, logout
from django.core.mail import send_mail
from django.urls import reverse
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from api.user.serializer import UserSerializer, AuthorizationSerializer, ChangePasswordSerializer
from boynty_winers import settings

from user.models import User


class APIUser(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    serializers = {
        'list': UserSerializer,
        'retrieve': UserSerializer,
        'update': UserSerializer,
        'create': UserSerializer,
        'authorization': AuthorizationSerializer,
        'change_password': ChangePasswordSerializer,
    }

    @action(detail=False, methods=["POST"])
    def change_password(self, request):
        data = ChangePasswordSerializer(data=request.data, context={"request": request})
        if data.is_valid():
            data = data.validated_data
            if request.user.is_authenticated:
                if request.user.check_password(data['old_password']):
                    request.user.set_password(data['new_password'])
                    request.user.save()
                    return Response({'success': True})
            else:
                user = User.objects.get(email=data['email'])
                if user:
                    token = b64encode(bytes(str({"id": user.id, 'new_password': data['new_password']}), encoding='utf8')).decode("utf-8")
                    link = request.build_absolute_uri(reverse("api:password-confirm", kwargs={"token": token}))

                    send_mail("Перейдите по ссылке для смены пароля", f"Ссылка для смены пароля \n{link}",
                              settings.EMAIL_HOST_USER, [data['email']])
                    return Response({'success': True})

        else:
            return Response({"error": data.errors})

        return Response({'success': False})

    @action(detail=False, methods=["GET"])
    def logout(self, request):
        if request.user.is_authenticated:
            logout(request)
            return Response({'success': True})
        else:
            return Response({'success': False})

    @action(detail=False, methods=["GET", 'POST'])
    def authorization(self, request):
        if request.method == "GET":
            if request.user.is_authenticated:
                return Response({"is_authorization": True, "user": UserSerializer(request.user, context={"request": request}).data})
            else:
                return Response({"is_authorization": False, "user": []})
        elif request.method == "POST":
            data = AuthorizationSerializer(data=request.data)
            if data.is_valid():
                data = data.validated_data
                user = User.objects.get(username=data['username'])
                if user.is_active:
                    user = authenticate(username=data['username'],
                                        password=data['password'],)
                    if user:
                        login(request, user)
                        return Response({"is_authorization": True, "user": UserSerializer(request.user, context={"request": request}).data})
                    else:
                        return Response({'success': False})
                else:
                    token = b64encode(bytes(f"{user.id}", encoding='utf8')).decode("utf-8")
                    link = request.build_absolute_uri(reverse("api:email-confirm", kwargs={"token": token}))
                    send_mail("Подвтвердите почту для входа", f"Ваша ссылка для подтверждения\n{link}",
                              settings.EMAIL_HOST_USER, [user.email])
                    return Response({"error": "you don't confirm email"})
            else:
                return Response({"error": data.errors})

    def get_serializer_class(self):
        for i in list(self.serializers.keys()):
            return self.serializers.get(self.action,
                                        self.serializers[i])