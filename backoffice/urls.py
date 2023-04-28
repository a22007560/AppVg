from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from .views import views, quotation_views,  client_views, equipment_views

urlpatterns = [
    path('', views.index, name='index'),
    path('clients/', client_views.clients, name='clients'),
    path('new_client/', client_views.new_client, name='new_client'),
    path('clients/<int:client_id>/', client_views.client_details, name='client_details'),

    path('equipments/', equipment_views.equipments, name='equipments'),
    path('new_equipment/', equipment_views.new_equipment, name='new_equipment'),

    path('quotations/', quotation_views.quotations, name='quotations'),
    path('new_quotation/', quotation_views.new_quotation, name='new_quotation'),
    path('quotations/<int:quotation_id>/', quotation_views.quotation_details, name='quotation_details'),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

