from django.shortcuts import render, redirect, get_object_or_404

from backoffice.forms import AddressForm
from backoffice.models.client import Client


def new_address_client(request, client_id):
    client = get_object_or_404(Client, id=client_id)

    if request.method == 'POST':
        form = AddressForm(request.POST, client=client)
        if form.is_valid():
            address = form.save(commit=False)
            address.client = client
            address.save()
            return redirect('client_details', client_id=client_id)
    else:
        form = AddressForm(client=client)

    context = {
        'form': form,
        'client': client
    }
    return render(request, 'client/new_address.html', context)
