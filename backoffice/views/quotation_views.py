from django.shortcuts import render, redirect, get_object_or_404

from backoffice.forms import QuotationForm
from backoffice.models.quotation import Quotation


def quotations(request):
    quotationsList = Quotation.objects.values('id', 'client__name', 'address', 'comments', 'status')
    context = {
        'quotations': quotationsList,
    }
    return render(request, 'quotation/quotations.html', context)


def new_quotation(request):
    if request.method == 'POST':
        form = QuotationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('quotations')
    else:
        form = QuotationForm()
    return render(request, 'quotation/new_quotation.html', {'form': form})


def quotation_details(request, quotation_id):
    quotation = get_object_or_404(Quotation, id=quotation_id)
    context = {
        'quotation': quotation,
    }
    return render(request, 'quotation/quotation_details.html', context)
