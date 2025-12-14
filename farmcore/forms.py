from farmcore.models import *
from django import forms

class FarmerForm(forms.ModelForm):
    class Meta:
        model = Farmer
        fields = ['name', 'phone']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({
                'class': 'form-control'
            })
class FarmForm(forms.ModelForm):
    class Meta:
        model = Farm
        fields = ['name', 'size_in_acres', 'location']
        labels = {
            'name': 'Farm Name',
            'size_in_acres': 'Size (Acres)',
            'location': 'Location',
        }
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({
                'class': 'form-control'
            })

class SeasonPlanForm(forms.ModelForm):
    class Meta:
        model = SeasonPlan
        fields = ['farm', 'crop_name', 'season_name', 'status', 'start_date']
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({
                'class': 'form-control'
            })
class PlannedActivityForm(forms.ModelForm):
    class Meta:
        model = PlannedActivity
        fields = ['season_plan', 'activity_type', 'target_date', 'estimated_cost_ugx']
        widgets ={
            'target_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({
                'class': 'form-control'
            })

class ActualActivityForm(forms.ModelForm):
    class Meta:
        model = ActualActivity
        fields = ['season_plan', 'activity_type', 'actual_date', 'actual_cost_ugx',  'notes', 'planned_activity']
        widgets ={'actual_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
              }
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({
                'class': 'form-control'
            })