from rest_framework import serializers
from lot.models import Bonus


class BonusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bonus
        fields = "__all__"