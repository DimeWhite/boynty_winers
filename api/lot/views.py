from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from api.lot.filter import LotFilter
from api.lot.serializers.Bonuses import BonusSerializer
from api.lot.serializers.Tickets import TicketSerializer, TakeTicketSerializer
from api.lot.serializers.Lots import LotSerializer

from lot.models import Lot, Ticket, Bonus


class APILot(viewsets.ReadOnlyModelViewSet):
    queryset = Lot.objects.all()
    serializer_class = LotSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = LotFilter


class APIBonus(viewsets.ViewSet):
    queryset = Bonus.objects.all()
    serializer_class = BonusSerializer


class APITicket(viewsets.ModelViewSet):
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer

    serializers = {
        'list': TicketSerializer,
        'retrieve': TicketSerializer,
        'update': TicketSerializer,
        'create': TicketSerializer,
        'take': TakeTicketSerializer,
    }

    @action(detail=False, methods=['POST'])
    def take(self, request):
        tickets = TakeTicketSerializer(data=request.data)
        user = request.user
        if user.is_authenticated:
            if tickets.is_valid():
                ids = tickets.data['tickets']
                tickets = Ticket.objects.filter(id__in=ids)
                rules = tickets.first().lot.ticket_rule
                if len(ids) < rules.max_tickets_take:

                    if tickets.filter(user=user):
                        return Response({"error": "У этого пользователя уже есть такие номера"})
                    elif tickets.filter(status="UNAVAILABLE"):
                        return Response({"error": "Какой-то номера уже занята"})
                    else:
                        total = sum([i[0] for i in tickets.values_list("price")])
                        if user.balance >= total:
                            user.balance -= total
                            bonus_logic = Bonus.objects.first()
                            user.bonus += total / 100 * bonus_logic.cashback
                            user.save()
                            tickets.update(user=user, status="UNAVAILABLE")
                        else:
                            return Response({"error": "Недостаточно денег"})
                    return Response({"log": ids})
                else:
                    return Response(
                        {"error": f"Вы взяли слишком много билетов.\nМаксимальное число {rules.max_tickets_take}"})
            else:
                return Response({"error": True})
        else:
            return Response({"error": "Вы должны авторизоваться"})
        # tickets = self.serializer_class(data=tickets.initial_data, many=True)
        # print(tickets.initial_data)

    def get_serializer_class(self):
        for i in list(self.serializers.keys()):
            return self.serializers.get(self.action,
                                        self.serializers[i])
