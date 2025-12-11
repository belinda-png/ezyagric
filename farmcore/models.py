from django.db import models

# Create your models here.
class Farmer(models.Model):
    name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=15, unique=True)
    def __str__(self):
        return self.name

class Farm(models.Model):
    farmer = models.ForeignKey(Farmer, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    size_in_acres = models.FloatField()
    def __str__(self):
        return f"{self.farmer.name}'s Farm at {self.location}"    
    
class SeasonPlan(models.Model):
    farm = models.ForeignKey(Farm, on_delete=models.CASCADE)
    crop_name = models.CharField(max_length=100)
    season_name = models.CharField(max_length=100)
    def __str__(self):
        return f"{self.crop_name} Season ({self.season_name})"  

class PlannedActivity(models.Model):
    ACTIVITY_CHOICES = [
        ('land_preparation', 'Land Preparation'),
        ('planting', 'Planting'),
        ('weeding', 'Weeding'),
        ('spraying', 'Spraying'),
        ('harvesting', 'Harvesting'),   
    ]
    season_plan = models.ForeignKey(SeasonPlan, on_delete=models.CASCADE)
    activity_type = models.CharField(max_length=100)
    target_date = models.DateField()
    actual_cost = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    def __str__(self):
        return f"{self.activity_type} on {self.target_date}"      

class ActualActivity(models.Model):
    season_plan = models.ForeignKey(SeasonPlan, on_delete=models.CASCADE, related_name='actual_activities')
    activity_type = models.CharField(max_length=50, choices=PlannedActivity.ACTIVITY_CHOICES)
    actual_date = models.DateField()
    actual_cost_ugx = models.FloatField()
    notes = models.TextField(blank=True, null=True)
    planned_activity = models.ForeignKey(PlannedActivity, on_delete=models.SET_NULL, null=True, blank=True, related_name='actual_activities')

    def __str__(self):
        return f"{self.activity_type} ({self.season_plan})"    