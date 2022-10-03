from django.contrib.auth.models import User
from django.db import models
# Create your models here.
from boynty_winers import settings


class Bonus(models.Model):
    cashback = models.IntegerField(default=5, help_text="Введите проценты от потраченной суммы")
    is_super = models.BooleanField(default=False)


class LotsTicketRule(models.Model):
    number_tickets = models.IntegerField()
    price_tickets = models.IntegerField()
    max_tickets_take = models.IntegerField()

    def __str__(self):
        return f"Total: {self.number_tickets}; " \
               f"Ticket price: {self.price_tickets}; " \
               f"Max Take: {self.max_tickets_take}"


class Lot(models.Model):
    prize1 = models.CharField(max_length=50)
    prize2 = models.CharField(max_length=50, null=True, blank=True, default=None)
    name = models.CharField(max_length=120)
    result_date = models.DateTimeField(null=True, blank=True)
    is_finished = models.BooleanField(default=False)
    ticket_rule = models.ForeignKey(LotsTicketRule, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        super(Lot, self).save(*args, **kwargs)
        for i in range(1, self.ticket_rule.number_tickets+1):
            ticket = Ticket.objects.create(number=i, price=self.ticket_rule.price_tickets,
                                           status="AVAILABLE", lot=self)
            ticket.save()

    def __str__(self):
        return self.name


class Ticket(models.Model):
    STATUS_CHOICES = (
        ('available', 'AVAILABLE'),
        ('unavailable', 'UNAVAILABLE')
    )

    number = models.IntegerField()
    price = models.IntegerField()
    status = models.CharField(choices=STATUS_CHOICES, max_length=15)
    lot = models.ForeignKey(Lot, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    is_winner = models.BooleanField(default=False)

    def get_lot(self):
        return self.lot

    def __str__(self):
        return f"{self.lot.name} {self.number}"


