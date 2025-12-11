from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from datetime import date

from .models import Farmer, Farm, SeasonPlan, PlannedActivity, ActualActivity
from .forms import (
    FarmerSerializer,
    FarmSerializer,
    SeasonPlanSerializer,
    PlannedActivitySerializer,
    ActualActivitySerializer,
    ActivitySummarySerializer,
    SeasonSummarySerializer
)


# FARMER VIEWSET

class FarmerViewSet(viewsets.ModelViewSet):
    queryset = Farmer.objects.all()
    serializer_class = FarmerSerializer


# FARM VIEWSET

class FarmViewSet(viewsets.ModelViewSet):
    queryset = Farm.objects.all()
    serializer_class = FarmSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        farmer_id = self.request.query_params.get('farmer_id')
        if farmer_id:
            queryset = queryset.filter(farmer_id=farmer_id)
        return queryset


# SEASON PLAN VIEWSET

class SeasonPlanViewSet(viewsets.ModelViewSet):
    queryset = SeasonPlan.objects.all()
    serializer_class = SeasonPlanSerializer

    # Add planned activity
    @action(detail=True, methods=['post'])
    def planned_activities(self, request, pk=None):
        season = self.get_object()
        serializer = PlannedActivitySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(season_plan=season)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # Add actual activity
    @action(detail=True, methods=['post'])
    def actual_activities(self, request, pk=None):
        season = self.get_object()
        serializer = ActualActivitySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(season_plan=season)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # Get season summary
    @action(detail=True, methods=['get'])
    def summary(self, request, pk=None):
        season = self.get_object()
        planned_activities = season.planned_activities.all()
        actual_activities = season.actual_activities.all()

        total_estimated_cost = sum(p.estimated_cost_ugx for p in planned_activities)
        total_actual_cost = sum(a.actual_cost_ugx for a in actual_activities)

        today = date.today()
        overdue_count = 0
        activity_summaries = []

        for planned in planned_activities:
            # Find matching actual activity
            actual = actual_activities.filter(planned_activity=planned).first()
            
            if actual:
                status_str = 'COMPLETED'
            elif planned.target_date >= today:
                status_str = 'UPCOMING'
            else:
                status_str = 'OVERDUE'
                overdue_count += 1

            summary_data = {
                'activity': PlannedActivitySerializer(planned).data,
                'status': status_str,
                'actual': ActualActivitySerializer(actual).data if actual else None
            }
            activity_summaries.append(summary_data)

        summary_serializer = SeasonSummarySerializer({
            'season_plan': SeasonPlanSerializer(season).data,
            'total_estimated_cost': total_estimated_cost,
            'total_actual_cost': total_actual_cost,
            'overdue_count': overdue_count,
            'activities': activity_summaries
        })

        return Response(summary_serializer.data)