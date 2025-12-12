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
    season_name = forms.ChoiceField(
        choices=SeasonPlan.SEASON_CHOICES,
        widget=forms.Select(attrs={
            'class': 'form-control',
            'style': 'width: 100%; padding: 10px; border: 1px solid #ddd; border-radius: 4px;'
        }),
        label='Select Season'
    )
    
    status = forms.ChoiceField(
        choices=SeasonPlan.STATUS_CHOICES,
        widget=forms.Select(attrs={
            'class': 'form-control',
            'style': 'width: 100%; padding: 10px; border: 1px solid #ddd; border-radius: 4px;'
        }),
        label='Season Status'
    )
    
    class Meta:
        model = SeasonPlan
        fields = ['farm', 'crop_name', 'season_name', 'status', 'start_date']
        widgets = {
            'crop_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter crop name (e.g., Maize, Beans, Cassava)',
                'style': 'width: 100%; padding: 10px; border: 1px solid #ddd; border-radius: 4px;'
            }),
            'farm': forms.Select(attrs={
                'class': 'form-control',
                'style': 'width: 100%; padding: 10px; border: 1px solid #ddd; border-radius: 4px;'
            }),
            'start_date': forms.DateInput(attrs={
                'type': 'date',
                'class': 'form-control',
                'style': 'width: 100%; padding: 10px; border: 1px solid #ddd; border-radius: 4px;'
            }),
        }
                
class PlannedActivityForm(forms.ModelForm):
    activity_type = forms.ChoiceField(
        choices=PlannedActivity.ACTIVITY_CHOICES,
        widget=forms.Select(attrs={
            'class': 'form-control',
            'style': 'width: 100%; padding: 10px; border: 1px solid #ddd; border-radius: 4px;'
        }),
        label='Type of Activity'
    )
    
    class Meta:
        model = PlannedActivity
        fields = '__all__'
        widgets = {
            'season_plan': forms.Select(attrs={
                'class': 'form-control',
                'style': 'width: 100%; padding: 10px; border: 1px solid #ddd; border-radius: 4px;'
            }),
            'target_date': forms.DateInput(attrs={
                'type': 'date',
                'class': 'form-control',
                'style': 'width: 100%; padding: 10px; border: 1px solid #ddd; border-radius: 4px;'
            }),
            'estimated_cost_ugx': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter estimated cost in UGX',
                'style': 'width: 100%; padding: 10px; border: 1px solid #ddd; border-radius: 4px;'
            }),
        }

class ActualActivityForm(forms.ModelForm):
    class Meta:
        model = ActualActivity
        fields = '__all__'

