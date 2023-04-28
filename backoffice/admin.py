from django.contrib import admin

from backoffice.models.client import Client, Address, Contact
from backoffice.models.equipment import Equipment
from backoffice.models.quotation import Quotation

admin.site.register(Client)
admin.site.register(Address)
admin.site.register(Contact)
admin.site.register(Equipment)
admin.site.register(Quotation)
