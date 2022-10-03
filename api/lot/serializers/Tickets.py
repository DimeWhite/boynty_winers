from rest_framework import serializers

from lot.models import Ticket


class TicketSerializer(serializers.ModelSerializer):
    # lot = LotSerializer(source='get_lot')

    class Meta:
        model = Ticket
        fields = '__all__'


class TakeTicketSerializer(serializers.Serializer):
    tickets = serializers.PrimaryKeyRelatedField(queryset=Ticket.objects.all(), many=True)

    class Meta:
        fields = ('tickets', )
