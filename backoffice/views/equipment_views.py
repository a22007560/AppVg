from django.shortcuts import render, redirect, get_object_or_404

from backoffice.forms import EquipmentForm
from backoffice.models.equipment import Equipment


def equipments(request):
    equipmentsList = Equipment.objects.all()

    context = {
        'equipments': equipmentsList,
    }
    return render(request, 'equipment/equipments.html', context)


def new_equipment(request):
    if request.method == 'POST':
        form = EquipmentForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('equipments')
    else:
        form = EquipmentForm()
    return render(request, 'equipment/new_equipment.html', {'form': form})


def edit_equipment(request, equipment_id):
    equipment = get_object_or_404(Equipment, id=equipment_id)

    if request.method == 'POST':
        form = EquipmentForm(request.POST, request.FILES, instance=equipment)
        if form.is_valid():
            form.save()
            return redirect('equipments')
    else:
        form = EquipmentForm(instance=equipment)

    return render(request, 'equipment/edit_equipment.html', {'form': form})
