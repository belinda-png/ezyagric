from django.shortcuts import render
from django.utils import timezone
from farmcore.models import *

def dashboard(request):
    today = timezone.now().date()

    total_farmers = Farmer.objects.count()
    active_seasons = SeasonPlan.objects.filter(is_active=True).count()

    # Overdue tasks (target_date < today and no matching actual activity)
    overdue_tasks = PlannedActivity.objects.filter(
        target_date__lt=today,
        actual_activities__isnull=True
    ).count()

    # Total investment = sum of actual_cost_ugx from ActualActivity
    total_investment = ActualActivity.objects.all().values_list("actual_cost_ugx", flat=True)
    total_investment = sum(total_investment) if total_investment else 0

    # Active seasons list
    active_season_list = SeasonPlan.objects.filter(is_active=True).select_related("farm__farmer")

    # Recent activity = last 5 actual activities
    recent_activities = ActualActivity.objects.order_by("-actual_date")[:5]

    # Farmers with farms for the table
    farmers_with_farms = Farmer.objects.prefetch_related('farms').all()

    context = {
        "total_farmers": total_farmers,
        "active_seasons": active_seasons,
        "overdue_tasks": overdue_tasks,
        "total_investment": total_investment,
        "active_season_list": active_season_list,
        "recent_activities": recent_activities,
        "farmers_with_farms": farmers_with_farms,
    }

    return render(request, "dashboard.html", context)
# views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db.models import Q
from .models import Farmer, Farm
from .forms import FarmerForm, FarmForm


def farmers(request):
    """Display list of all registered farmers"""
    search_query = request.GET.get('search', '')
    
    farmers = Farmer.objects.all()
    
    if search_query:
        farmers = farmers.filter(
            Q(name__icontains=search_query) |
            Q(farmer_id__icontains=search_query) |
            Q(phone__icontains=search_query)
        )
    
    context = {
        'farmers': farmers,
        'search_query': search_query,
    }
    return render(request, 'farmer.html', context)
def base(request):
    """Render the base template"""
    return render(request, 'base.html')

def farmer_details(request, farmer_id):
    """Display details of a specific farmer and their farms"""
    farmer = get_object_or_404(Farmer, id=farmer_id)
    farms = farmer.farms.all()
    
    context = {
        'farmer': farmer,
        'farms': farms,
    }
    return render(request, 'view.html', context)


def add_farmer(request):
    """Add a new farmer to the registry"""
    if request.method == 'POST':
        form = FarmerForm(request.POST)
        if form.is_valid():
            farmer = form.save()
            messages.success(request, f'Farmer {farmer.name} added successfully!')
            return redirect('farmer')
    else:
        form = FarmerForm()
    
    context = {
        'form': form,
        'title': 'Add New Farmer',
    }
    return render(request, 'farmer_form.html', context)


def edit_farmer(request, farmer_id):
    """Edit an existing farmer's information"""
    farmer = get_object_or_404(Farmer, id=farmer_id)
    
    if request.method == 'POST':
        form = FarmerForm(request.POST, instance=farmer)
        if form.is_valid():
            farmer = form.save()
            messages.success(request, f'Farmer {farmer.name} updated successfully!')
            return redirect('farmer_details', farmer_id=farmer.id)
    else:
        form = FarmerForm(instance=farmer)
    
    context = {
        'form': form,
        'title': f'Edit {farmer.name}',
        'farmer': farmer,
    }
    return render(request, 'farmer_form.html', context)


def delete_farmer(request, farmer_id):
    """Delete a farmer from the registry"""
    farmer = get_object_or_404(Farmer, id=farmer_id)
    
    if request.method == 'POST':
        farmer_name = farmer.name
        farmer.delete()
        messages.success(request, f'Farmer {farmer_name} deleted successfully!')
        return redirect('farmer')
    
    context = {
        'farmer': farmer,
    }
    return render(request, 'confirm_delete.html', context)


def add_farm(request, farmer_id):
    """Add a new farm for a specific farmer"""
    farmer = get_object_or_404(Farmer, id=farmer_id)
    
    if request.method == 'POST':
        form = FarmForm(request.POST)
        if form.is_valid():
            farm = form.save(commit=False)
            farm.farmer = farmer
            farm.save()
            messages.success(request, f'Farm {farm.name} added successfully!')
            return redirect('farmer_details', farmer_id=farmer.id)
    else:
        form = FarmForm()
    
    context = {
        'form': form,
        'farmer': farmer,
        'title': f'Add Farm for {farmer.name}',
    }
    return render(request, 'farm_form.html', context)


def edit_farm(request, farm_id):
    """Edit an existing farm's information"""
    farm = get_object_or_404(Farm, id=farm_id)
    
    if request.method == 'POST':
        form = FarmForm(request.POST, instance=farm)
        if form.is_valid():
            farm = form.save()
            messages.success(request, f'Farm {farm.name} updated successfully!')
            return redirect('farmer_details', farmer_id=farm.farmer.id)
    else:
        form = FarmForm(instance=farm)
    
    context = {
        'form': form,
        'farmer': farm.farmer,
        'title': f'Edit {farm.name}',
        'farm': farm,
    }
    return render(request, 'farm_form.html', context)


def delete_farm(request, farm_id):
    """Delete a farm"""
    farm = get_object_or_404(Farm, id=farm_id)
    farmer = farm.farmer
    
    if request.method == 'POST':
        farm_name = farm.name
        farm.delete()
        messages.success(request, f'Farm {farm_name} deleted successfully!')
        return redirect('farmer_details', farmer_id=farmer.id)
    
    context = {
        'farm': farm,
        'farmer': farmer,
    }
    return render(request, 'confirm_delete_farm.html', context)
def seasonplan_list(request):
    plans = SeasonPlan.objects.all()
    return render(request, "seasonplan_list.html", {"plans": plans})
def seasonplan_create(request):
    form = SeasonPlanForm()

    if request.method == "POST":
        form = SeasonPlanForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("seasonplan_list")

    return render(request, "seasonplan_form.html", {
        "form": form,
        "title": "Create Season Plan"
    })
def seasonplan_edit(request, pk):
    plan = SeasonPlan.objects.get(id=pk)
    form = SeasonPlanForm(instance=plan)

    if request.method == "POST":
        form = SeasonPlanForm(request.POST, instance=plan)
        if form.is_valid():
            form.save()
            return redirect("seasonplan_list")

    return render(request, "seasonplan_form.html", {
        "form": form,
        "title": "Edit Season Plan"
    })
def seasonplan_delete(request, pk):
    plan = SeasonPlan.objects.get(id=pk)
    plan.delete()
    return redirect("seasonplan_list")
def plannedactivities_list(request):
    activities = PlannedActivity.objects.all()
    return render(request, "plannedactivities_list.html", {"activities": activities})

def plannedactivity_create(request):
    form = PlannedActivityForm()

    if request.method == "POST":
        form = PlannedActivityForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("plannedactivities_list")

    return render(request, "plannedactivity_form.html", {
        "form": form,
        "title": "Create Planned Activity"
    })
def plannedactivity_delete(request, pk):
    activity = PlannedActivity.objects.get(id=pk)
    activity.delete()
    return redirect("plannedactivities_list")
def actualactivities_list(request):
    actuals = ActualActivity.objects.all()
    return render(request, "actualactivities_list.html", {"activities": actuals})

def actualactivity_create(request):
    form = ActualActivityForm()

    if request.method == "POST":
        form = ActualActivityForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("actualactivities_list")

    return render(request, "actualactivity_form.html", {
        "form": form,
        "title": "Create Actual Activity"
    })
def actualactivity_edit(request, pk):
    act = ActualActivity.objects.get(id=pk)
    form = ActualActivityForm(instance=act)

    if request.method == "POST":
        form = ActualActivityForm(request.POST, instance=act)
        if form.is_valid():
            form.save()
            return redirect("actualactivities_list")

    return render(request, "actualactivity_form.html", {
        "form": form,
        "title": "Edit Actual Activity"
    })
def actualactivity_delete(request, pk):
    act = ActualActivity.objects.get(id=pk)
    act.delete()
    return redirect("actualactivities_list")
