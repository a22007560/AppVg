from bootstrap_datepicker_plus.widgets import DatePickerInput
from django import forms
from django.forms import inlineformset_factory, CheckboxSelectMultiple, DateInput
from django.shortcuts import get_object_or_404

from backoffice.models.client import Client, Address, Contact
from backoffice.models.equipment import Equipment
from backoffice.models.pool import Pool
from backoffice.models.quotation import Quotation
from django_select2 import forms as Select2Forms


class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ['client', 'name', 'fiscal_name', 'tax_number', 'notes']
        widgets = {
            'client': forms.TextInput(attrs={'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'fiscal_name': forms.TextInput(attrs={'class': 'form-control'}),
            'tax_number': forms.TextInput(attrs={'class': 'form-control'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }


class AddressForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        client = kwargs.pop('client', None)
        super().__init__(*args, **kwargs)

        if client:
            self.fields['client'].widget = forms.HiddenInput()
            self.fields['client'].initial = client

    class Meta:
        model = Address
        fields = ('client', 'street', 'number', 'city', 'postal_code', 'coordinate_x', 'coordinate_y', 'notes')
        widgets = {
            'street': forms.TextInput(attrs={'class': 'form-control'}),
            'number': forms.TextInput(attrs={'class': 'form-control'}),
            'city': forms.TextInput(attrs={'class': 'form-control'}),
            'postal_code': forms.TextInput(attrs={'class': 'form-control'}),
            'coordinate_x': forms.NumberInput(attrs={'class': 'form-control'}),
            'coordinate_y': forms.NumberInput(attrs={'class': 'form-control'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
        }


class ContactForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        client = kwargs.pop('client', None)
        super().__init__(*args, **kwargs)

        if client:
            self.fields['client'].widget = forms.HiddenInput()
            self.fields['client'].initial = client

    class Meta:
        model = Contact
        fields = ['client', 'type', 'contact', 'notes']
        widgets = {
            'type': forms.Select(attrs={'class': 'form-select'}),
            'contact': forms.TextInput(attrs={'class': 'form-control'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }


class EquipmentForm(forms.ModelForm):
    class Meta:
        model = Equipment
        fields = ['name', 'description', 'image', 'price']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
        }


class PoolForm(forms.ModelForm):
    class Meta:
        model = Pool
        fields = [
            'address',
            'length',
            'width',
            'min_depth',
            'max_depth',
            'circulation_type',
        ]

    def __init__(self, *args, addresses=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['address'].widget.attrs.update({'class': 'form-control'})
        self.fields['length'].widget.attrs.update({'class': 'form-control'})
        self.fields['width'].widget.attrs.update({'class': 'form-control'})
        self.fields['min_depth'].widget.attrs.update({'class': 'form-control'})
        self.fields['max_depth'].widget.attrs.update({'class': 'form-control'})
        self.fields['circulation_type'].widget.attrs.update({'class': 'form-control'})
        if addresses:
            self.fields['address'].queryset = addresses


class QuotationForm(forms.ModelForm):
    """
        client_address = forms.ModelChoiceField(queryset=Address.objects.none())
        client_phone = forms.ModelChoiceField(queryset=Contact.objects.none())
        client_email = forms.ModelChoiceField(queryset=Contact.objects.none())
    """

    equipments = forms.ModelMultipleChoiceField(queryset=Equipment.objects.all(),
                                                widget=Select2Forms.Select2MultipleWidget)
    extra_recommendations = forms.ModelMultipleChoiceField(queryset=Equipment.objects.all(),
                                                           widget=Select2Forms.Select2MultipleWidget)
    date = forms.DateField(widget=DatePickerInput())

    def __init__(self, *args, **kwargs):
        client = kwargs.pop('client', None)
        quotation = kwargs.pop('quotation', None)
        super().__init__(*args, **kwargs)

        if client:
            self.fields['client'].widget = forms.HiddenInput()
            self.fields['client'].initial = client
            self.initial['client'] = client
            self.fields['client_address'].queryset = Address.objects.filter(client=client)
            self.fields['client_phone'].queryset = Contact.objects.filter(client=client, type='phone')
            self.fields['client_email'].queryset = Contact.objects.filter(client=client, type='email')
            self.fields['pool'].queryset = Pool.objects.filter(
                address__in=Address.objects.filter(client=client)
            )

        if quotation:
            self.fields['client_address'].queryset = Address.objects.filter(client=quotation.client)
            self.fields['client_phone'].queryset = Contact.objects.filter(client=quotation.client, type='phone')
            self.fields['client_email'].queryset = Contact.objects.filter(client=quotation.client, type='email')
            self.initial['client_address'] = quotation.client_address
            self.initial['client_phone'] = quotation.client_phone
            self.initial['client_email'] = quotation.client_email

    def clean(self):
        cleaned_data = super().clean()
        if not cleaned_data.get('client_address'):
            self.add_error('client_address', 'Please select a client address.')
        if not cleaned_data.get('equipments'):
            self.add_error('equipments', 'Please select at least one equipment.')
        return cleaned_data

    class Meta:
        model = Quotation
        fields = ('quotation_type', 'client', 'client_address', 'client_phone', 'client_email', 'equipments', 'pool',
                  'date', 'greetings', 'extra_recommendations', 'comments', 'transportation_fee', 'labor_rate',
                  'status')
