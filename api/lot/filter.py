import django_filters
from django_filters import rest_framework
from lot.models import Lot, Ticket
from user.models import User


class LotFilter(rest_framework.FilterSet):

    # discount = django_filters.ChoiceFilter(choices=DISCOUNT_TYPES, method='filter_discount', label='discount')
    #ticket = django_filters.ModelChoiceFilter(queryset=lambda q: User.objects.filter(is_active=True), method='filter_ticket', label="tickets")

    # def filter_ticket(self, queryset, name, value):
    #     tickets = Ticket.objects.filter(user=value, lot=)
    #     print(tickets)
    #     return queryset
    #     #discount_product = [i['products'] for i in Lot.objects.filter(type=value).values('products')]
    #     #return queryset.filter(article__in=discount_product)

    # def filter_characteristic(self, queryset, name, value):
    #     if value:
    #         print(value[0])
    #         print(value[0].objects.values())
    #     return Product.objects.all()

    # def filter_characteristic__id(self):

    class Meta:
        model = Lot
        fields = ["is_finished"]