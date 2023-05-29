from django.shortcuts import render, redirect, get_object_or_404

from backoffice.forms import PoolForm
from backoffice.models.client import Client
from backoffice.models.pool import Pool


def pools(request):
    poolList = Pool.objects.all()
    context = {'pools': poolList}
    return render(request, 'pool/pools.html', context)


def new_pool(request):
    if request.method == 'POST':
        form = PoolForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('pools')
    else:
        form = PoolForm()

    context = {
        'form': form
    }

    return render(request, 'pool/new_pool.html', context)


def new_pool_client(request, client_id):
    client = get_object_or_404(Client, id=client_id)
    addresses = client.address_set.all()
    if request.method == 'POST':
        form = PoolForm(request.POST)
        if form.is_valid():
            pool = form.save(commit=False)
            pool.address = client.address_set.first()
            pool.save()
            return redirect('new_quotation', client_id=client.id)
    else:
        form = PoolForm(addresses=addresses)

    context = {
        'form': form,
        'client': client,
        'addresses': addresses,
    }
    return render(request, 'pool/new_pool_client.html', context)


def pool_details(request, pool_id):
    pool = get_object_or_404(Pool, id=pool_id)
    context = {
        'pool': pool,
    }
    return render(request, 'pool/pool_details.html', context)
