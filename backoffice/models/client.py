from django.db import models


class Client(models.Model):
    client = models.IntegerField()
    name = models.CharField(max_length=100)
    fiscal_name = models.CharField(max_length=100)
    tax_number = models.CharField(max_length=20)
    notes = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name


CONTACT_TYPE = (
    ('phone', 'Telemovel'),
    ('email', 'Email'),
)


class Contact(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    type = models.CharField(max_length=20, choices=CONTACT_TYPE, default='phone')
    contact = models.CharField(max_length=20, blank=True)
    notes = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.contact


class Address(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    street = models.CharField(max_length=100)
    number = models.CharField(max_length=10)
    city = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=10)
    coordinate_x = models.DecimalField(max_digits=9, decimal_places=6)
    coordinate_y = models.DecimalField(max_digits=9, decimal_places=6)
    notes = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"{self.street} {self.number}, {self.city}, {self.postal_code}"

