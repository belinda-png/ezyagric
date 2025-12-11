from farmcore.models import Farmer, SeasonPlan, PlannedActivity, ActualActivity, Farm
from django import forms   

class FarmerForm(forms.ModelForm):
    class Meta:
        model = Farmer
        fields = '__all__'

class FarmForm(forms.ModelForm):
    class Meta:
        model = Farm
        fields = '__all__'
class SeasonPlanForm(forms.ModelForm):
    planned_activities =  forms.PrimaryKeyRelatedField(many=True, read_only=True)
    actual_activities =  forms.PrimaryKeyRelatedField(many=True, read_only=True)
    class Meta:
        model = SeasonPlan
        fields = '__all__'
                
class PlannedActivityForm(forms.ModelForm):
    class Meta:
        model = PlannedActivity
        fields = '__all__'

class ActualActivityForm(forms.ModelForm):
    class Meta:
        model = ActualActivity
        fields = '__all__'


# -----------------------------
# SEASON SUMMARY SERIALIZER
# -----------------------------
class ActivitySummaryForm(forms.Form):
    activity = PlannedActivityForm()
    status = forms.CharField()
    actual = ActualActivityForm(allow_null=True)

class SeasonSummaryForm(forms.Form):
    season_plan = SeasonPlanForm()
    total_estimated_cost = forms.FloatField()
    total_actual_cost = forms.FloatField()
    overdue_count = forms.IntegerField()
    activities = ActivitySummaryForm(many=True)