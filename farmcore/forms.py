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

