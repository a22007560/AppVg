from django.shortcuts import render, redirect, get_object_or_404

from backoffice.forms import ClientForm
from backoffice.models.client import Client


def clients(request):
    clientsList = Client.objects.all()

    context = {
        'clients': clientsList,
    }
    return render(request, 'client/clients.html', context)


def new_client(request):
    if request.method == 'POST':
        form = ClientForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('clients')
    else:
        form = ClientForm()
    return render(request, 'client/new_client.html', {'form': form})


def client_details(request, client_id):
    client = get_object_or_404(Client, id=client_id)
    context = {
        'client': client,
    }
    return render(request, 'client/client_details.html', context)


