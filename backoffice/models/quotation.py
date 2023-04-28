from django.db import models

from backoffice.models.client import Client
from backoffice.models.equipment import Equipment


STATUS_CHOICES = (
    ('draft', 'Rascunho'),
    ('sent', 'Enviado'),
    ('accepted', 'Aceito'),
    ('rejected', 'Rejeitado'),
)


class Quotation(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    equipments = models.ManyToManyField(Equipment)
    address = models.CharField(max_length=255, blank=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    greetings = models.CharField(max_length=255)
    extra_recommendations = models.ManyToManyField(Equipment, related_name='extra_recommendations')
    comments = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')

    def __str__(self):
        return f'{self.client} - {self.date_created}'

