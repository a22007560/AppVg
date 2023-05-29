from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.decorators import login_required
from django.urls import path
from django.contrib.auth import views as auth_views
from .views import views, quotation_views, client_views, equipment_views, pool_views, address_views, contact_views, \
    user_views

urlpatterns = [
    path('test/', login_required(views.test), name='test'),

    path('', login_required(views.dashboard), name='dashboard'),
    path('clients/', login_required(client_views.clients), name='clients'),
    path('new_client/', login_required(client_views.new_client), name='new_client'),
    path('clients/<int:client_id>/', login_required(client_views.client_details), name='client_details'),
    path('clients/<int:client_id>/edit', login_required(client_views.edit_client), name='edit_client'),
    path('clients/<int:client_id>/new_address/', login_required(address_views.new_address_client), name='new_address_client'),
    path('clients/<int:client_id>/new_contact/', login_required(contact_views.new_contact_client), name='new_contact_client'),

    path('equipments/', login_required(equipment_views.equipments), name='equipments'),
    path('new_equipment/', login_required(equipment_views.new_equipment), name='new_equipment'),

    path('quotations/', login_required(quotation_views.quotations), name='quotations'),
    path('new_quotation/<int:client_id>', login_required(quotation_views.new_quotation), name='new_quotation'),
    path('quotations/<int:quotation_id>/', login_required(quotation_views.quotation_details), name='quotation_details'),
    path('print_quotation/<int:quotation_id>/', login_required(quotation_views.print_quotation), name='print_quotation'),
    path('quotation/<int:quotation_id>/edit/', login_required(quotation_views.edit_quotation), name='edit_quotation'),
    path('quotation/<int:quotation_id>/delete/', login_required(quotation_views.quotation_delete), name='quotation_delete'),

    path('pools/', login_required(pool_views.pools), name='pools'),
    path('new_pool/', login_required(pool_views.new_pool), name='new_pool'),
    path('pools/<int:pool_id>/', login_required(pool_views.pool_details), name='pool_details'),
    path('clients/<int:client_id>/new_pool/', login_required(pool_views).new_pool_client, name='new_pool_client'),

    path("login", auth_views.LoginView.as_view(template_name="login/login.html"), name='login'),
    path('logout/', user_views.logout_view, name='logout'),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

