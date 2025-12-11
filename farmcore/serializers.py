from farmcore.models import Farmer, SeasonPlan, PlannedActivity, ActualActivity, Farm
from django import serializers    

class FarmerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Farmer
        fields = '__all__'

class FarmSerializer(serializers.ModelSerializer):
    class Meta:
        model = Farm
        fields = '__all__'
class SeasonPlanSerializer(serializers.ModelSerializer):
    planned_activities =  serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    actual_activities =  serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    class Meta:
        model = SeasonPlan
        fields = '__all__'
                
class PlannedActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = PlannedActivity
        fields = '__all__'

class ActualActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = ActualActivity
        fields = '__all__'


# -----------------------------
# SEASON SUMMARY SERIALIZER
# -----------------------------
class ActivitySummarySerializer(serializers.Serializer):
    activity = PlannedActivitySerializer()
    status = serializers.CharField()
    actual = ActualActivitySerializer(allow_null=True)

class SeasonSummarySerializer(serializers.Serializer):
    season_plan = SeasonPlanSerializer()
    total_estimated_cost = serializers.FloatField()
    total_actual_cost = serializers.FloatField()
    overdue_count = serializers.IntegerField()
    activities = ActivitySummarySerializer(many=True)