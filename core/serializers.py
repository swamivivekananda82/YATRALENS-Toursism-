from rest_framework import serializers
from .models import (
    Destination, SafetyZone, Attraction, VerifiedHotel,
    EmergencyService, SafetyAlert, LiveShareSession,
    TravelMemory, TripPlan, IncidentReport,
    TourismPackage, CustomerFeedback, PostTripReview, CrimeStatistic
)

class SafetyZoneSerializer(serializers.ModelSerializer):
    class Meta:
        model = SafetyZone
        fields = '__all__'

class AttractionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attraction
        fields = '__all__'

class VerifiedHotelSerializer(serializers.ModelSerializer):
    class Meta:
        model = VerifiedHotel
        fields = '__all__'

class EmergencyServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmergencyService
        fields = '__all__'

class SafetyAlertSerializer(serializers.ModelSerializer):
    class Meta:
        model = SafetyAlert
        fields = '__all__'

class CrimeStatisticSerializer(serializers.ModelSerializer):
    class Meta:
        model = CrimeStatistic
        fields = '__all__'

class TourismPackageSerializer(serializers.ModelSerializer):
    destination_name = serializers.CharField(source='destination.name', read_only=True)
    destination_state = serializers.CharField(source='destination.state', read_only=True)
    destination_safety_score = serializers.IntegerField(source='destination.safety_score', read_only=True)
    destination_image_url = serializers.CharField(source='destination.image_url', read_only=True)

    class Meta:
        model = TourismPackage
        fields = '__all__'

class CustomerFeedbackSerializer(serializers.ModelSerializer):
    destination_name = serializers.CharField(source='destination.name', read_only=True, allow_null=True)
    package_title = serializers.CharField(source='package.title', read_only=True, allow_null=True)

    class Meta:
        model = CustomerFeedback
        fields = '__all__'

class PostTripReviewSerializer(serializers.ModelSerializer):
    destination_name = serializers.CharField(source='destination.name', read_only=True)
    destination_state = serializers.CharField(source='destination.state', read_only=True)
    package_title = serializers.CharField(source='package.title', read_only=True, allow_null=True)

    class Meta:
        model = PostTripReview
        fields = '__all__'

class DestinationSerializer(serializers.ModelSerializer):
    safety_zones = SafetyZoneSerializer(many=True, read_only=True)
    attractions = AttractionSerializer(many=True, read_only=True)
    hotels = VerifiedHotelSerializer(many=True, read_only=True)
    emergency_services = EmergencyServiceSerializer(many=True, read_only=True)
    crime_statistics = CrimeStatisticSerializer(many=True, read_only=True)
    packages = TourismPackageSerializer(many=True, read_only=True)
    post_trip_reviews = PostTripReviewSerializer(many=True, read_only=True)
    feedback = CustomerFeedbackSerializer(many=True, read_only=True)

    class Meta:
        model = Destination
        fields = '__all__'

class LiveShareSessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = LiveShareSession
        fields = '__all__'

class TravelMemorySerializer(serializers.ModelSerializer):
    class Meta:
        model = TravelMemory
        fields = '__all__'

class TripPlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = TripPlan
        fields = '__all__'

class IncidentReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = IncidentReport
        fields = '__all__'
