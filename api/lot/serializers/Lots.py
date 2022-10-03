from rest_framework import serializers
from lot.models import Lot, Ticket, LotsTicketRule


class LotsTicketRuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = LotsTicketRule
        fields = '__all__'


class LotSerializer(serializers.ModelSerializer):
    ticket_rule = LotsTicketRuleSerializer()

    class Meta:
        model = Lot
        fields = '__all__'



