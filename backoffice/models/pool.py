from decimal import Decimal
from django.db import models

from backoffice.models.client import Address

CIRCULATION_TYPE = (
    ('skimmer', 'Skimmer'),
    ('transbordo', 'Transbordo'),
)


class Pool(models.Model):
    address = models.ForeignKey(Address, on_delete=models.CASCADE, related_name='pools')
    length = models.DecimalField(max_digits=5, decimal_places=2)
    width = models.DecimalField(max_digits=5, decimal_places=2)
    min_depth = models.FloatField()
    max_depth = models.FloatField()
    volume = models.FloatField(blank=True, null=True)
    surface_area = models.FloatField(blank=True, null=True)
    circulation_type = models.CharField(max_length=50, choices=CIRCULATION_TYPE, default='skimmer')

    def save(self, *args, **kwargs):
        if self.min_depth and self.max_depth:
            self.volume = self.calculate_volume()
            self.surface_area = self.calculate_surface_area()
        super().save(*args, **kwargs)

    def calculate_volume(self):
        surface_area = self.calculate_surface_area()
        average_depth = (self.min_depth + self.max_depth) / 2
        return surface_area * Decimal(average_depth)

    def calculate_surface_area(self):
        return self.length * self.width

    def __str__(self):
        return f"{self.length}x{self.width}m - {self.address}"
