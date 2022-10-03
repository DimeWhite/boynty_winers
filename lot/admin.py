from django.contrib import admin
from lot.models import Lot, Ticket, LotsTicketRule, Bonus


# Register your models here.


@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    fields = ('number', 'status', 'lot', 'user',)


@admin.register(LotsTicketRule)
class LotsTicketRuleAdmin(admin.ModelAdmin):
    fields = ('number_tickets', 'price_tickets', 'max_tickets_take')


@admin.register(Bonus)
class BonusAdmin(admin.ModelAdmin):
    fields = ('cashback', "is_super")


@admin.register(Lot)
class LotAdmin(admin.ModelAdmin):
    fields = ('prize1', 'prize2', 'name', 'ticket_rule', "finished_date", "is_finished")


