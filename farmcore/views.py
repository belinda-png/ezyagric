from django.shortcuts import render
from django.utils import timezone
from farmcore.models import *

def dashboard(request):
    today = timezone.now().date()

    total_farmers = Farmer.objects.count()
    # active_seasons = SeasonPlan.objects.filter(is_active=True).count()

    # Overdue tasks (target_date < today and no matching actual activity)
    overdue_tasks = PlannedActivity.objects.filter(
        target_date__lt=today,
        actual_activities__isnull=True
    ).count()

    # Total investment = sum of actual_cost_ugx from ActualActivity
    total_investment = ActualActivity.objects.all().values_list("actual_cost_ugx", flat=True)
    total_investment = sum(total_investment) if total_investment else 0

    # Active seasons list
    # active_season_list = SeasonPlan.objects.filter(is_active=True).select_related("farm__farmer")

    # Recent activity = last 5 actual activities
    recent_activities = ActualActivity.objects.order_by("-actual_date")[:5]

    context = {
        "total_farmers": total_farmers,
        # "active_seasons": active_seasons,
        "overdue_tasks": overdue_tasks,
        "total_investment": total_investment,
        # "active_season_list": active_season_list,
        "recent_activities": recent_activities,
    }

    return render(request, "dashboard.html", context)
# views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db.models import Q
from .models import Farmer, Farm
from .forms import FarmerForm, FarmForm


def farmers_list(request):
    """Display list of all registered farmers"""
    search_query = request.GET.get('search', '')
    
    farmers = Farmer.objects.all()
    
    if search_query:
        farmers = farmers.filter(
            Q(name__icontains=search_query) |
            Q(farmer_id__icontains=search_query) |
            Q(district__icontains=search_query)
        )
    
    context = {
        'farmers': farmers,
        'search_query': search_query,
    }
    return render(request, 'farmers/farmers_list.html', context)


def farmer_details(request, farmer_id):
    """Display details of a specific farmer and their farms"""
    farmer = get_object_or_404(Farmer, farmer_id=farmer_id)
    farms = farmer.farms.all()
    
    context = {
        'farmer': farmer,
        'farms': farms,
    }
    return render(request, 'farmers/farmer_details.html', context)


def add_farmer(request):
    """Add a new farmer to the registry"""
    if request.method == 'POST':
        form = FarmerForm(request.POST)
        if form.is_valid():
            farmer = form.save()
            messages.success(request, f'Farmer {farmer.name} added successfully!')
            return redirect('farmers_list')
    else:
        form = FarmerForm()
    
    context = {
        'form': form,
        'title': 'Add New Farmer',
    }
    return render(request, 'farmers/farmer_form.html', context)


def edit_farmer(request, farmer_id):
    """Edit an existing farmer's information"""
    farmer = get_object_or_404(Farmer, farmer_id=farmer_id)
    
    if request.method == 'POST':
        form = FarmerForm(request.POST, instance=farmer)
        if form.is_valid():
            farmer = form.save()
            messages.success(request, f'Farmer {farmer.name} updated successfully!')
            return redirect('farmer_details', farmer_id=farmer.farmer_id)
    else:
        form = FarmerForm(instance=farmer)
    
    context = {
        'form': form,
        'title': f'Edit {farmer.name}',
        'farmer': farmer,
    }
    return render(request, 'farmers/farmer_form.html', context)


def delete_farmer(request, farmer_id):
    """Delete a farmer from the registry"""
    farmer = get_object_or_404(Farmer, farmer_id=farmer_id)
    
    if request.method == 'POST':
        farmer_name = farmer.name
        farmer.delete()
        messages.success(request, f'Farmer {farmer_name} deleted successfully!')
        return redirect('farmers_list')
    
    context = {
        'farmer': farmer,
    }
    return render(request, 'farmers/confirm_delete.html', context)


def add_farm(request, farmer_id):
    """Add a new farm for a specific farmer"""
    farmer = get_object_or_404(Farmer, farmer_id=farmer_id)
    
    if request.method == 'POST':
        form = FarmForm(request.POST)
        if form.is_valid():
            farm = form.save(commit=False)
            farm.farmer = farmer
            farm.save()
            messages.success(request, f'Farm {farm.name} added successfully!')
            return redirect('farmer_details', farmer_id=farmer.farmer_id)
    else:
        form = FarmForm()
    
    context = {
        'form': form,
        'farmer': farmer,
        'title': f'Add Farm for {farmer.name}',
    }
    return render(request, 'farmers/farm_form.html', context)


def edit_farm(request, farm_id):
    """Edit an existing farm's information"""
    farm = get_object_or_404(Farm, id=farm_id)
    
    if request.method == 'POST':
        form = FarmForm(request.POST, instance=farm)
        if form.is_valid():
            farm = form.save()
            messages.success(request, f'Farm {farm.name} updated successfully!')
            return redirect('farmer_details', farmer_id=farm.farmer.farmer_id)
    else:
        form = FarmForm(instance=farm)
    
    context = {
        'form': form,
        'farmer': farm.farmer,
        'title': f'Edit {farm.name}',
        'farm': farm,
    }
    return render(request, 'farmers/farm_form.html', context)


def delete_farm(request, farm_id):
    """Delete a farm"""
    farm = get_object_or_404(Farm, id=farm_id)
    farmer = farm.farmer
    
    if request.method == 'POST':
        farm_name = farm.name
        farm.delete()
        messages.success(request, f'Farm {farm_name} deleted successfully!')
        return redirect('farmer_details', farmer_id=farmer.farmer_id)
    
    context = {
        'farm': farm,
        'farmer': farmer,
    }
    return render(request, 'farmers/confirm_delete_farm.html', context)