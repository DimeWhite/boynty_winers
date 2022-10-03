from django.contrib.auth.password_validation import validate_password
from django.core import exceptions
from django.core.mail import send_mail
from django.urls import reverse
from rest_framework.serializers import ModelSerializer, Serializer, HyperlinkedModelSerializer
from rest_framework import serializers

from base64 import b64encode

from api.lot.serializers import Tickets
from boynty_winers import settings
from lot.models import Ticket
from user.models import User


def valid_password(password):
    try:
        validate_password(password=password)
    except exceptions.ValidationError as e:
        raise e


class ChangePasswordSerializer(Serializer):
    email = serializers.EmailField()
    old_password = serializers.CharField(validators=[valid_password])
    new_password = serializers.CharField(validators=[valid_password])

    def __init__(self, *args, **kwargs):
        super(ChangePasswordSerializer, self).__init__(*args, **kwargs)
        if self.context['request']:
            if self.context['request'].user.is_authenticated:
                self.fields.pop('email')
            else:
                self.fields.pop('old_password')

    class Meta:
        fields = ('email', 'old_password', "new_password")


class AuthorizationSerializer(Serializer):
    username = serializers.CharField()
    password = serializers.CharField(validators=[valid_password])

    class Meta:
        fields = ('username', 'password')


class UserSerializer(ModelSerializer):
    password = serializers.CharField(validators=[valid_password])
    static = serializers.SerializerMethodField("get_static")

    def get_static(self, obj):
        from itertools import groupby

        lots = []

        tickets_q = Ticket.objects.filter(user=obj)
        lots_id = tickets_q.values("lot")
        lots_id = [i for i, _ in groupby(lots_id)]
        lots_id = [i['lot'] for i in lots_id]

        take_part = len(lots_id)
        tickets_count = len(tickets_q)

        for i in lots_id:
            lots.append({"lot_id": i, "tickets": [i[0] for i in tickets_q.filter(lot_id=i).values_list("number")]})

        return {"tickets_count": tickets_count, "take_part": take_part, "lots": lots}

    def __init__(self, *args, **kwargs):
        super(UserSerializer, self).__init__(*args, **kwargs)
        if self.context['request']:
            if self.context['request'].method in ['POST']:
                self.fields.pop('balance')
                self.fields.pop('bonus')
            elif self.context['request'].method in ['PUT']:
                self.fields.pop('username')
                self.fields.pop('email')
                self.fields.pop('password')
                self.fields.pop('bonus')
                self.fields.pop('balance')
            else:
                self.fields.pop("password")

    def create(self, validated_data):
        password = validated_data['password']
        validated_data.pop("password")
        obj = User.objects.create(**validated_data)
        obj.set_password(password)
        obj.is_active = False
        obj.save()
        token = b64encode(bytes(f"{obj.id}", encoding='utf8')).decode("utf-8")
        link = self.context['request'].build_absolute_uri(reverse("api:email-confirm", kwargs={"token": token}))
        send_mail("Подвтвердите почту для регистрации", f"Ваша ссылка для подтверждения\n{link}", settings.EMAIL_HOST_USER, [obj.email])
        return obj

    class Meta:
        model = User
        fields = ('id', 'username', "password", "last_name", "middle_name",
                  "first_name", "email", "balance", "bonus", 'static')
