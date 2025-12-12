from django.db import models

# Create your models here.
class Farmer(models.Model):
    farmer_id = models.CharField(max_length=20, unique=True, blank=True, null=True)
    name = models.CharField(max_length=255, blank=True, null=True)
    phone = models.CharField(max_length=15, unique=True)
    
    def __str__(self):
        return self.name
    
    # @property
    def total_farms(self):
        return self.farms.count()
    
    # @property
    def total_acreage(self):
        return sum(farm.size_in_acres for farm in self.farms.all())

class Farm(models.Model):
    farmer = models.ForeignKey(Farmer, on_delete=models.CASCADE, related_name='farms')
    name = models.CharField(max_length=255)
    size_in_acres = models.FloatField()
    location = models.CharField(max_length=255, default='')
    
    def __str__(self):
        return f"{self.farmer.name}'s Farm - {self.name}"    
    
class SeasonPlan(models.Model):
    SEASON_CHOICES = [
        ('season_a', 'Season A (March - July) - Long Rains'),
        ('season_b', 'Season B (August - November) - Short Rains'),
        ('season_c', 'Season C (December - February) - Dry Season'),
    ]
    
    STATUS_CHOICES = [
        ('is_active', 'Is Active'),
        ('completed', 'Completed'),
        ('planned', 'Planned'),
    ]
    
    farm = models.ForeignKey(Farm, on_delete=models.CASCADE)
    crop_name = models.CharField(max_length=100)
    season_name = models.CharField(max_length=100, choices=SEASON_CHOICES)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='planned')
    start_date = models.DateField(null=True, blank=True)
    
    def __str__(self):
        return f"{self.crop_name} - {self.get_season_name_display()}"  

class PlannedActivity(models.Model):
    ACTIVITY_CHOICES = [
        ('land_preparation', 'Land Preparation'),
        ('planting', 'Planting'),
        ('weeding', 'Weeding'),
        ('spraying', 'Spraying'),
        ('harvesting', 'Harvesting'),   
    ]
    season_plan = models.ForeignKey(SeasonPlan, on_delete=models.CASCADE)
    activity_type = models.CharField(max_length=100, choices=ACTIVITY_CHOICES)
    target_date = models.DateField()
    estimated_cost_ugx = models.FloatField(null=True, blank=True)
    
    def __str__(self):
        return f"{self.get_activity_type_display()} on {self.target_date}"      

class ActualActivity(models.Model):
    season_plan = models.ForeignKey(SeasonPlan, on_delete=models.CASCADE, related_name='actual_activities')
    activity_type = models.CharField(max_length=50, choices=PlannedActivity.ACTIVITY_CHOICES)
    actual_date = models.DateField()
    actual_cost_ugx = models.FloatField()
    notes = models.TextField(blank=True, null=True)
    planned_activity = models.ForeignKey(PlannedActivity, on_delete=models.SET_NULL, null=True, blank=True, related_name='actual_activities')

    def __str__(self):
        return f"{self.activity_type} ({self.season_plan})"    