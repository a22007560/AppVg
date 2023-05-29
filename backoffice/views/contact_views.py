from django.shortcuts import render, redirect, get_object_or_404

from backoffice.forms import ClientForm, AddressForm, ContactForm
from backoffice.models.client import Client, Contact, Address
from backoffice.models.pool import Pool


def new_contact_client(request, client_id):
    client = get_object_or_404(Client, id=client_id)

    if request.method == 'POST':
        form = ContactForm(request.POST, client=client)
        if form.is_valid():
            contact = form.save(commit=False)
            contact.client = client
            contact.save()
            return redirect('client_details', client_id=client_id)
    else:
        form = ContactForm(client=client)

    context = {
        'form': form,
        'client': client
    }
    return render(request, 'client/new_contact.html', context)
