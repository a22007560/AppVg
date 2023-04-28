from django import forms

from backoffice.models.client import Client
from backoffice.models.equipment import Equipment
from backoffice.models.quotation import Quotation


class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = '__all__'
        widgets = {
            'client': forms.NumberInput(attrs={'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'fiscal_name': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.TextInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'tax_number': forms.TextInput(attrs={'class': 'form-control'}),
            'address2': forms.TextInput(attrs={'class': 'form-control'}),
            'city': forms.TextInput(attrs={'class': 'form-control'}),
            'postal_code': forms.TextInput(attrs={'class': 'form-control'}),
            'city_postal_code': forms.TextInput(attrs={'class': 'form-control'}),
            'phone2': forms.TextInput(attrs={'class': 'form-control'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': '3'}),
        }


class EquipmentForm(forms.ModelForm):
    class Meta:
        model = Equipment
        fields = ['name', 'description', 'image', 'price']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
        }


class QuotationForm(forms.ModelForm):
    class Meta:
        model = Quotation
        fields = ['client', 'equipments', 'greetings', 'extra_recommendations', 'comments', 'status']

    widgets = {
        'equipments': forms.CheckboxSelectMultiple(),
        'extra_recommendations': forms.CheckboxSelectMultiple(),
        'comments': forms.Textarea(attrs={'rows': 3}),
    }
