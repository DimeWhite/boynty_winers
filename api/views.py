from django.core.mail import send_mail
from django.http import HttpResponse
from django.shortcuts import render, redirect
from base64 import b64decode
import json
from boynty_winers import settings
from user.models import User
from ast import literal_eval


def email_confirm(request, token):
    id = int(b64decode(token))
    user = User.objects.filter(id=id)
    if user:
        user = user[0]
        if not user.is_active:
            user.is_active = True
            user.save()
            send_mail("Регистрация подтверждена", f"Вы успешно зарегестрировались. Остальсоь только войти", settings.EMAIL_HOST_USER,
                      [user.email])
            return HttpResponse({"success": True})
        else:
            return HttpResponse({"error": "You already confirm"})
    else:
        return HttpResponse({"success": False})


def password_confirm(request, token):
    token = literal_eval(b64decode(token).decode("utf-8"))

    id = token['id']
    password = token['new_password']

    user = User.objects.filter(id=id)
    if user:
        user = user[0]
        if user.is_active:
            user.set_password(password)
            user.save()
            send_mail("Успешно сменили пароль", f"Пароль успешно сменен.",
                      settings.EMAIL_HOST_USER,
                      [user.email])
            return HttpResponse({"success": True})
        else:
            return HttpResponse({"error": "You already confirm"})
    else:
        return HttpResponse({"success": False})
