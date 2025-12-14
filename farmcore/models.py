from django.db import models


class Farmer(models.Model):
    name = models.CharField(max_length=255,blank=False, null=False, default="")
    phone = models.CharField(max_length=15, unique=True, blank=False, null=False)    

    def __str__(self):
        return self.name

    def total_farms(self):
        return self.farms.count()

    def total_acreage(self):
        return sum(farm.size_in_acres for farm in self.farms.all())


class Farm(models.Model):
    farmer = models.ForeignKey( Farmer, on_delete=models.CASCADE, related_name='farms')
    name = models.CharField( max_length=255, blank=False, null=False)
    size_in_acres = models.FloatField(max_length=100, blank=False, null=False)
    location = models.CharField( max_length=255,
        blank=False, null=False )

    def __str__(self):
        return f"{self.farmer.name}'s Farm - {self.name}"


class SeasonPlan(models.Model):
    SEASON_CHOICES = [
        ('rainy', 'Rainy'),
        ('sunny', 'Sunny'),
    ]

    STATUS_CHOICES = [
        ('is_active', 'Is Active'),
        ('completed', 'Completed'),
        ('planned', 'Planned'),
    ]

    farm = models.ForeignKey(Farm, on_delete=models.CASCADE)
    crop_name = models.CharField(max_length=100)
    season_name = models.CharField(max_length=100, choices=SEASON_CHOICES)
    status = models.CharField( max_length=20, choices=STATUS_CHOICES, default='planned' )
    start_date = models.DateField( null=True, blank=True )

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
    activity_type = models.CharField(max_length=100, choices=ACTIVITY_CHOICES, null=False, blank=False)
    target_date = models.DateField(blank=False, null=False)
    estimated_cost_ugx = models.FloatField( null=False, blank=False, default=0.0)

    def __str__(self):
        return f"{self.get_activity_type_display()} on {self.target_date}"


class ActualActivity(models.Model):
    season_plan = models.ForeignKey( SeasonPlan, on_delete=models.CASCADE, related_name='actual_activities')
    activity_type = models.CharField(max_length=50, choices=PlannedActivity.ACTIVITY_CHOICES, blank=False, null=False  )
    actual_date = models.DateField(blank=False, null=False)
    actual_cost_ugx = models.FloatField(blank=False, null=False, default=0.0)
    notes = models.CharField(max_length=255, blank=False, null=False, default="")

    planned_activity = models.ForeignKey(PlannedActivity, on_delete=models.SET_NULL, null=True, blank=True, related_name='actual_activities')

    def __str__(self):
        return f"{self.get_activity_type_display()} ({self.season_plan})"
