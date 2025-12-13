from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.utils import timezone
from farmcore.models import *
from farmcore.forms import *


def dashboard(request):
    today = timezone.now().date()

    total_farmers = Farmer.objects.count()
    active_seasons = SeasonPlan.objects.filter(status='is_active').count()

    # Overdue tasks (target_date < today and no matching actual activity)
    overdue_tasks = PlannedActivity.objects.filter(
        target_date__lt=today,
        actual_activities__isnull=True
    ).count()

    # Total investment = sum of actual_cost_ugx from ActualActivity
    total_investment = ActualActivity.objects.all().values_list("actual_cost_ugx", flat=True)
    total_investment = sum(total_investment) if total_investment else 0

    # All seasons list
    all_season_list = SeasonPlan.objects.all().select_related("farm__farmer")

    # All activities
    all_activities = ActualActivity.objects.all().order_by("-actual_date")

    # Farmers with farms for the table
    farmers_with_farms = Farmer.objects.prefetch_related('farms').all()

    # Season plan summary statistics
    completed_seasons = SeasonPlan.objects.filter(status='completed').count()
    pending_seasons = SeasonPlan.objects.filter(status='planned').count()
    active_seasons_count = SeasonPlan.objects.filter(status='is_active').count()
    total_seasons = SeasonPlan.objects.count()

    context = {
        "total_farmers": total_farmers,
        "active_seasons": active_seasons,
        "overdue_tasks": overdue_tasks,
        "total_investment": total_investment,
        "all_season_list": all_season_list,
        "all_activities": all_activities,
        "farmers_with_farms": farmers_with_farms,
        "completed_seasons": completed_seasons,
        "pending_seasons": pending_seasons,
        "active_seasons_count": active_seasons_count,
        "total_seasons": total_seasons,
    }

    return render(request, "dashboard.html", context)

# Farmer Management Views
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

# Basic Views
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

# Farmer Management Views
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

# Farm Management Views
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

# Season Plan Views
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
    
    # Get planned and completed activities
    planned_count = PlannedActivity.objects.filter(season_plan=plan).count()
    completed_count = ActualActivity.objects.filter(season_plan=plan).count()

    if request.method == "POST":
        form = SeasonPlanForm(request.POST, instance=plan)
        if form.is_valid():
            form.save()
            return redirect("seasonplan_list")

    return render(request, "seasonplan_form.html", {
        "form": form,
        "title": "Edit Season Plan",
        "plan": plan,
         "planned_count": planned_count,
         "completed_count": completed_count,
    })
def seasonplan_delete(request, pk):
    plan = SeasonPlan.objects.get(id=pk)
    plan.delete()
    return redirect("seasonplan_list")

def seasonplan_detail(request, pk):
    """Display season plan details with planned and actual activities"""
    plan = SeasonPlan.objects.get(id=pk)
    planned_activities = PlannedActivity.objects.filter(season_plan=plan)
    actual_activities = ActualActivity.objects.filter(season_plan=plan)
    
    context = {
        'plan': plan,
        'planned_activities': planned_activities,
        'actual_activities': actual_activities,
    }
    return render(request, 'seasonplan_detail.html', context)

def seasonplan_summary(request, pk):
    plan = SeasonPlan.objects.get(id=pk)
    planned_activities = PlannedActivity.objects.filter(season_plan=plan)
    actual_activities = ActualActivity.objects.filter(season_plan=plan)
    
    today = timezone.now().date()
    overdue_tasks = planned_activities.filter(
        target_date__lt=today,
        actual_activities__isnull=True
    ).count()
    
    planned_cost = sum(float(a.estimated_cost_ugx or 0) for a in planned_activities)
    actual_cost = sum(float(a.actual_cost_ugx or 0) for a in actual_activities)
    
    # Count activities by status
    completed_count = actual_activities.count()
    pending_count = planned_activities.count() - completed_count
    
    # Calculate completion rate
    total_planned = planned_activities.count()
    completion_rate = (completed_count * 100 // total_planned) if total_planned > 0 else 0
    
    context = {
        'plan': plan,
        'planned_activities': planned_activities,
        'actual_activities': actual_activities,
        'overdue_tasks': overdue_tasks,
        'planned_cost': planned_cost,
        'actual_cost': actual_cost,
        'completed_count': completed_count,
        'pending_count': pending_count,
        'completion_rate': completion_rate,
        'today': today,
    }
    return render(request, 'seasonplan_summary.html', context)

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

    return render(request, "plannedactivities_form.html", {
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
        "title": "Log Actual Activity"
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

@login_required(login_url='login')
def season_summary_page(request):
    """Display overall season summary statistics"""
    completed_seasons = SeasonPlan.objects.filter(status='completed')
    pending_seasons = SeasonPlan.objects.filter(status='planned')
    active_seasons = SeasonPlan.objects.filter(status='is_active')
    
    completed_count = completed_seasons.count()
    pending_count = pending_seasons.count()
    active_count = active_seasons.count()
    total_count = SeasonPlan.objects.count()
    
    context = {
        'completed_seasons': completed_seasons,
        'pending_seasons': pending_seasons,
        'active_seasons': active_seasons,
        'completed_count': completed_count,
        'pending_count': pending_count,
        'active_count': active_count,
        'total_count': total_count,
    }
    return render(request, 'season_summary_page.html', context)
