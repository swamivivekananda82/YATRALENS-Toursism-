from django.contrib import admin
from .models import (
    Destination, SafetyZone, Attraction, VerifiedHotel,
    EmergencyService, SafetyAlert, LiveShareSession,
    TravelMemory, TripPlan, IncidentReport,
    TourismPackage, CustomerFeedback, PostTripReview, CrimeStatistic
)


@admin.register(Destination)
class DestinationAdmin(admin.ModelAdmin):
    list_display = ('name', 'state', 'safety_score', 'risk_level', 'crime_data_source', 'crime_trend', 'last_crime_update')
    list_filter = ('risk_level', 'crime_trend', 'crime_data_source', 'popular')
    search_fields = ('name', 'state', 'tagline')


@admin.register(SafetyZone)
class SafetyZoneAdmin(admin.ModelAdmin):
    list_display = ('name', 'destination', 'zone_type', 'risk_level')
    list_filter = ('zone_type', 'risk_level')
    search_fields = ('name', 'destination__name')


@admin.register(Attraction)
class AttractionAdmin(admin.ModelAdmin):
    list_display = ('name', 'destination', 'category', 'safety_rating', 'women_safety_certified')
    list_filter = ('category', 'women_safety_certified')


@admin.register(VerifiedHotel)
class VerifiedHotelAdmin(admin.ModelAdmin):
    list_display = ('name', 'destination', 'rating', 'verified', 'women_friendly')
    list_filter = ('verified', 'women_friendly', 'reception_24_7', 'cctv_security')


@admin.register(EmergencyService)
class EmergencyServiceAdmin(admin.ModelAdmin):
    list_display = ('name', 'destination', 'service_type', 'phone', 'is_24_7')
    list_filter = ('service_type', 'is_24_7')


@admin.register(SafetyAlert)
class SafetyAlertAdmin(admin.ModelAdmin):
    list_display = ('title', 'alert_type', 'severity', 'is_active', 'created_at')
    list_filter = ('alert_type', 'severity', 'is_active')


@admin.register(LiveShareSession)
class LiveShareSessionAdmin(admin.ModelAdmin):
    list_display = ('traveler_name', 'trusted_contact_name', 'status', 'current_location_name', 'last_updated')
    list_filter = ('status',)


@admin.register(TravelMemory)
class TravelMemoryAdmin(admin.ModelAdmin):
    list_display = ('title', 'traveler_name', 'destination', 'created_at')
    search_fields = ('title', 'traveler_name', 'destination')


@admin.register(TripPlan)
class TripPlanAdmin(admin.ModelAdmin):
    list_display = ('destination', 'duration_days', 'budget', 'traveler_type', 'created_at')


@admin.register(IncidentReport)
class IncidentReportAdmin(admin.ModelAdmin):
    list_display = ('reporter_name', 'incident_type', 'location_name', 'status', 'created_at')
    list_filter = ('incident_type', 'status')


@admin.register(TourismPackage)
class TourismPackageAdmin(admin.ModelAdmin):
    list_display = ('title', 'destination', 'package_type', 'price', 'duration_days', 'rating', 'review_count', 'is_featured', 'is_available')
    list_filter = ('package_type', 'difficulty', 'is_featured', 'is_available', 'destination')
    search_fields = ('title', 'subtitle', 'description')
    prepopulated_fields = {'slug': ('title',)}


@admin.register(CustomerFeedback)
class CustomerFeedbackAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'rating', 'subject', 'destination', 'is_resolved', 'created_at')
    list_filter = ('category', 'rating', 'is_resolved', 'contact_allowed')
    search_fields = ('name', 'email', 'subject', 'message')


@admin.register(PostTripReview)
class PostTripReviewAdmin(admin.ModelAdmin):
    list_display = ('reviewer_name', 'destination', 'overall_rating', 'safety_rating', 'value_rating', 'would_recommend', 'is_published', 'moderated', 'created_at')
    list_filter = ('traveler_type', 'would_recommend', 'is_published', 'moderated', 'destination')
    search_fields = ('reviewer_name', 'title', 'detailed_notes')


@admin.register(CrimeStatistic)
class CrimeStatisticAdmin(admin.ModelAdmin):
    list_display = ('destination', 'period_label', 'recorded_at', 'total_cases', 'crime_rate_per_100k', 'data_source')
    list_filter = ('data_source',)
    search_fields = ('destination__name', 'period_label')
