import datetime

from django.db import models
from django.utils import timezone

from backoffice.models.client import Client, Address, Contact
from backoffice.models.equipment import Equipment
from backoffice.models.pool import Pool

STATUS_CHOICES = (
    ('draft', 'Rascunho'),
    ('sent', 'Enviado'),
    ('accepted', 'Aceite'),
    ('rejected', 'Rejeitado'),
)

QUOTATION_TYPE_CHOICES = (
    ('renovation', 'Renovação'),
    ('equipment', 'Fornecimento de Equipamento'),
)


class Quotation(models.Model):
    quotation_id = models.CharField(max_length=20, unique=True, blank=True)
    quotation_type = models.CharField(max_length=20, choices=QUOTATION_TYPE_CHOICES, default='equipment')
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    client_address = models.CharField(max_length=50, null=True, blank=True)
    client_phone = models.CharField(max_length=50, null=True, blank=True)
    client_email = models.CharField(max_length=50, null=True, blank=True)
    equipments = models.ManyToManyField(Equipment)
    pool = models.ForeignKey(Pool, on_delete=models.SET_NULL, null=True, blank=True)
    date = models.DateField()
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    greetings = models.TextField()
    extra_recommendations = models.ManyToManyField(Equipment, related_name='extra_recommendations')
    comments = models.TextField()
    labor_rate = models.IntegerField(null=True, blank=True, default=0)
    transportation_fee = models.IntegerField(null=True, blank=True, default=0)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')

    def save(self, *args, **kwargs):
        if not self.quotation_id:
            # Get the current date in the desired format (ddMMyy)
            current_date = timezone.now().strftime('%d%m%y')

            # Get the number of quotations created on the current day
            quotation_count = Quotation.objects.filter(date_created__date=datetime.date.today()).count() + 1

            # Format the quotation ID
            self.quotation_id = f'VG-{current_date}-{quotation_count}'

        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.client} - {self.date_created}'

    def get_total_price(self):
        total_price = sum([equipment.price for equipment in self.equipments.all()])
        return total_price

