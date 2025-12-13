"""
URL configuration for farmease project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from farmcore import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.dashboard, name='dashboard'),
    path('farmer/', views.farmers, name='farmer'),
    
    # Farmer management URLs
    path('base/', views.base, name='base'),
    path('add/', views.add_farmer, name='add_farmer'),
    path("farmer/<int:farmer_id>/", views.farmer_details, name="farmer_details"),
    path('farmer/<int:farmer_id>/edit/', views.edit_farmer, name='edit_farmer'),
    path('farmer/<int:farmer_id>/delete/', views.delete_farmer, name='delete_farmer'),
    
    # Farm management URLs
    path('farmer/<int:farmer_id>/add_farm/', views.add_farm, name='add_farm'),
    path('farm/<int:farm_id>/edit/', views.edit_farm, name='edit_farm'),
    path('farm/<int:farm_id>/delete/', views.delete_farm, name='delete_farm'),
      # SEASON PLAN
    path("seasonplans/", views.seasonplan_list, name="seasonplan_list"),
    path("seasonplans/create/", views.seasonplan_create, name="seasonplan_create"),
    path("seasonplans/<int:pk>/", views.seasonplan_detail, name="seasonplan_detail"),
    path("seasonplans/<int:pk>/summary/", views.seasonplan_summary, name="seasonplan_summary"),
    path("seasonplans/<int:pk>/edit/", views.seasonplan_edit, name="seasonplan_edit"),
    path("seasonplans/<int:pk>/delete/", views.seasonplan_delete, name="seasonplan_delete"),

    # PLANNED ACTIVITIES
    path("plannedactivities/", views.plannedactivities_list, name="plannedactivities_list"),
    path("plannedactivities/create/", views.plannedactivity_create, name="plannedactivity_create"),
    path("plannedactivities/delete/<int:pk>/", views.plannedactivity_delete, name="plannedactivity_delete"),

    # ACTUAL ACTIVITIES
    path("actualactivities/", views.actualactivities_list, name="actualactivities_list"),
    path("actualactivities/create/", views.actualactivity_create, name="actualactivity_create"),
    path("actualactivities/edit/<int:pk>/", views.actualactivity_edit, name="actualactivity_edit"),
    path("actualactivities/delete/<int:pk>/", views.actualactivity_delete, name="actualactivity_delete"),
    
    # SEASON SUMMARY
    path("season-summary/", views.season_summary_page, name="season_summary_page"),
]
