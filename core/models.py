from django.db import models
from django.contrib.auth.models import User
import uuid

class Destination(models.Model):
    name = models.CharField(max_length=150, unique=True)
    state = models.CharField(max_length=150)
    tagline = models.CharField(max_length=255, blank=True)
    description = models.TextField()
    latitude = models.FloatField()
    longitude = models.FloatField()
    
    # Safety Scoring (0 to 100)
    safety_score = models.IntegerField(default=80)
    risk_level = models.CharField(max_length=20, default='Low Risk', choices=[
        ('Low Risk', 'Low Risk'),
        ('Moderate Risk', 'Moderate Risk'),
        ('High Risk', 'High Risk'),
    ])
    
    # === REAL-TIME / STATISTICAL CRIME DATA ===
    crime_rate_index = models.FloatField(default=15.0, help_text="Crimes per 100k population")
    theft_reports = models.IntegerField(default=12, help_text="Quarterly reported theft cases")
    harassment_reports = models.IntegerField(default=2, help_text="Quarterly reported harassment cases")
    violent_crime_reports = models.IntegerField(default=1, help_text="Quarterly reported violent crime cases")
    
    # Real-time / statistical crime trend fields
    crime_data_source = models.CharField(
        max_length=50,
        default="Statistical (Historical Records)",
        choices=[
            ("Real-Time", "Real-Time API Feed"),
            ("Statistical", "Statistical (Historical Records)"),
            ("Manual", "Manual Authority Entry"),
        ],
        help_text="Source of the crime data displayed for this destination"
    )
    last_crime_update = models.DateTimeField(
        null=True, blank=True,
        help_text="Timestamp of the most recent crime data refresh"
    )
    crime_trend = models.CharField(
        max_length=20, default="Stable", choices=[
            ("Improving", "Improving ↓"),
            ("Deteriorating", "Deteriorating ↑"),
            ("Stable", "Stable →"),
        ],
        help_text="Direction of the crime trend over the last 30 days"
    )
    theft_change_pct = models.FloatField(default=0.0, help_text="Percentage change in theft reports (last quarter vs. previous)")
    harassment_change_pct = models.FloatField(default=0.0, help_text="Percentage change in harassment reports")
    
    # Granular Safety Factors
    night_safety_score = models.IntegerField(default=85, help_text="0-100 night lighting & safety rating")
    tourist_density = models.CharField(max_length=50, default='High Density')
    emergency_accessibility_score = models.IntegerField(default=90, help_text="0-100 emergency service reach")
    police_accessibility_score = models.IntegerField(default=88)
    hospital_accessibility_score = models.IntegerField(default=92)
    accident_prone_areas = models.TextField(blank=True, default="Caution near highway curves and unlit river banks after 9 PM.")
    
    image_url = models.CharField(max_length=500, blank=True)
    banner_image_url = models.CharField(max_length=500, blank=True, default="https://images.unsplash.com/photo-1507525428034-b723cf961d3e?auto=format&fit=crop&w=1200&q=80")
    popular = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name}, {self.state} (Safety Score: {self.safety_score}/100)"

    @property
    def risk_badge_color(self):
        if self.safety_score >= 75:
            return "emerald"
        elif self.safety_score >= 50:
            return "amber"
        return "rose"

    @property
    def crime_trend_icon(self):
        icons = {"Improving": "📉", "Deteriorating": "📈", "Stable": "➖"}
        return icons.get(self.crime_trend, "➖")

    @property
    def crime_category_breakdown(self):
        total = self.theft_reports + self.harassment_reports + self.violent_crime_reports
        if total == 0:
            return {"theft_pct": 0, "harassment_pct": 0, "violent_pct": 0}
        return {
            "theft_pct": round(self.theft_reports / total * 100, 1),
            "harassment_pct": round(self.harassment_reports / total * 100, 1),
            "violent_pct": round(self.violent_crime_reports / total * 100, 1),
        }


class SafetyZone(models.Model):
    destination = models.ForeignKey(Destination, on_delete=models.CASCADE, related_name='safety_zones')
    name = models.CharField(max_length=200)
    zone_type = models.CharField(max_length=50, choices=[
        ('Tourist Area', 'Tourist Area'),
        ('Main Market', 'Main Market'),
        ('Highway Area', 'Highway Area'),
        ('Isolated Area', 'Isolated Area'),
        ('Residential Zone', 'Residential Zone'),
        ('Riverfront Area', 'Riverfront Area'),
    ])
    risk_level = models.CharField(max_length=30, choices=[
        ('Low Risk', 'Low Risk 🟢'),
        ('Moderate Risk', 'Moderate Risk 🟡'),
        ('High Risk', 'High Risk 🔴'),
    ])
    latitude = models.FloatField()
    longitude = models.FloatField()
    radius_meters = models.IntegerField(default=600)
    lighting_status = models.CharField(max_length=100, default='Well-Lit')
    police_patrol = models.CharField(max_length=100, default='Regular 24/7 Mobile Patrol')
    cctv_coverage = models.CharField(max_length=100, default='High CCTV Presence')
    safety_notes = models.TextField()

    def __str__(self):
        return f"{self.name} - {self.risk_level} ({self.destination.name})"


class Attraction(models.Model):
    destination = models.ForeignKey(Destination, on_delete=models.CASCADE, related_name='attractions')
    name = models.CharField(max_length=200)
    category = models.CharField(max_length=80, choices=[
        ('Historical', 'Historical'),
        ('Riverfront & Nature', 'Riverfront & Nature'),
        ('Temple & Culture', 'Temple & Culture'),
        ('Eco-Tourism', 'Eco-Tourism'),
        ('Local Market & Food', 'Local Market & Food'),
    ])
    latitude = models.FloatField()
    longitude = models.FloatField()
    description = models.TextField()
    historical_fact = models.TextField(help_text="Automated historical trivia for tourist memory maker")
    best_visiting_hours = models.CharField(max_length=100, default="06:00 AM - 07:00 PM")
    safety_rating = models.FloatField(default=4.8)
    women_safety_certified = models.BooleanField(default=True)
    entry_fee = models.CharField(max_length=50, default="Free")
    image_url = models.CharField(max_length=500, blank=True)

    def __str__(self):
        return f"{self.name} ({self.destination.name})"


class VerifiedHotel(models.Model):
    destination = models.ForeignKey(Destination, on_delete=models.CASCADE, related_name='hotels')
    name = models.CharField(max_length=200)
    rating = models.FloatField(default=4.5)
    price_range = models.CharField(max_length=100, default="₹1,800 - ₹3,500/night")
    verified = models.BooleanField(default=True)
    women_friendly = models.BooleanField(default=True)
    reception_24_7 = models.BooleanField(default=True)
    cctv_security = models.BooleanField(default=True)
    
    # Distance Indicators
    dist_city_center = models.FloatField(default=1.2, help_text="Distance in km")
    dist_police_station = models.FloatField(default=0.8, help_text="Distance in km")
    dist_hospital = models.FloatField(default=1.5, help_text="Distance in km")
    
    latitude = models.FloatField()
    longitude = models.FloatField()
    contact_number = models.CharField(max_length=50, default="+91 883 245 8899")
    address = models.CharField(max_length=255)
    amenities = models.TextField(default="24/7 Guard, Keycard Access, Female Staff on Duty, Free Wi-Fi, Doctor on Call")
    image_url = models.CharField(max_length=500, blank=True)

    def __str__(self):
        return f"{self.name} - ⭐ {self.rating} ({self.destination.name})"


class EmergencyService(models.Model):
    SERVICE_TYPES = [
        ('Police', 'Police Station'),
        ('Hospital', 'Hospital & Trauma Center'),
        ('Ambulance', 'Ambulance Standby Unit'),
        ('Pharmacy', '24/7 Pharmacy'),
        ('Fuel', 'Fuel & EV Station'),
    ]
    destination = models.ForeignKey(Destination, on_delete=models.CASCADE, related_name='emergency_services')
    name = models.CharField(max_length=200)
    service_type = models.CharField(max_length=50, choices=SERVICE_TYPES)
    phone = models.CharField(max_length=50)
    latitude = models.FloatField()
    longitude = models.FloatField()
    address = models.CharField(max_length=255)
    is_24_7 = models.BooleanField(default=True)
    distance_km = models.FloatField(default=0.8)

    def __str__(self):
        return f"{self.get_service_type_display()}: {self.name}"


class SafetyAlert(models.Model):
    ALERT_TYPES = [
        ('Safety Alert', 'Safety Alert ⚠️'),
        ('Weather Warning', 'Severe Weather 🌧️'),
        ('Destination Closure', 'Destination Advisory 🚫'),
        ('Route Disruption', 'Route Caution 🚧'),
        ('General Advisory', 'Tourism Info ℹ️'),
    ]
    SEVERITY_CHOICES = [
        ('Low', 'Informational'),
        ('Moderate', 'Caution'),
        ('High', 'Urgent'),
        ('Critical', 'Emergency'),
    ]
    title = models.CharField(max_length=200)
    alert_type = models.CharField(max_length=50, choices=ALERT_TYPES, default='Safety Alert')
    message = models.TextField()
    severity = models.CharField(max_length=20, choices=SEVERITY_CHOICES, default='Moderate')
    destination = models.ForeignKey(Destination, on_delete=models.SET_NULL, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"[{self.severity}] {self.title}"


class LiveShareSession(models.Model):
    session_token = models.CharField(max_length=64, unique=True, default=uuid.uuid4)
    traveler_name = models.CharField(max_length=150, default="Priya Sharma")
    trusted_contact_name = models.CharField(max_length=150, default="Mom")
    trusted_contact_phone = models.CharField(max_length=50, default="+91 98765 43210")
    current_latitude = models.FloatField(default=16.9891)
    current_longitude = models.FloatField(default=81.7840)
    current_location_name = models.CharField(max_length=255, default="Near Godavari River Pushkar Ghat, Rajahmundry")
    battery_level = models.IntegerField(default=84)
    status = models.CharField(max_length=30, default='Active', choices=[
        ('Active', 'Active Sharing 🟢'),
        ('SOS_Active', '🚨 EMERGENCY SOS ACTIVE'),
        ('Completed', 'Trip Completed'),
    ])
    created_at = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Share: {self.traveler_name} with {self.trusted_contact_name} ({self.status})"


class TravelMemory(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='memories')
    title = models.CharField(max_length=200, default="🌅 My Unforgettable Day in Rajahmundry")
    destination = models.CharField(max_length=150, default="Rajahmundry")
    traveler_name = models.CharField(max_length=150, default="Aarohi Reddy")
    traveler_type = models.CharField(max_length=50, default="Solo Woman Traveler")
    travel_date = models.DateField(null=True, blank=True)
    places_visited = models.JSONField(default=list, help_text="List of visited spots")
    food_tried = models.JSONField(default=list, help_text="List of foods tried")
    historical_facts = models.JSONField(default=list, help_text="Enriched historical trivia")
    favorite_moment = models.TextField(default="Watching the golden sunset over the Godavari River while standing by the historical Dowleswaram Barrage.")
    photos = models.JSONField(default=list, help_text="List of photo objects {url, caption, time, location}")
    generated_story = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} - {self.traveler_name} ({self.created_at.strftime('%d %b %Y')})"


class TripPlan(models.Model):
    destination = models.CharField(max_length=150, default="Rajahmundry")
    duration_days = models.IntegerField(default=2)
    budget = models.DecimalField(max_digits=10, decimal_places=2, default=5000)
    traveler_type = models.CharField(max_length=50, default="Solo Woman")
    interests = models.CharField(max_length=255, default="Culture, Riverfront, Safe Sightseeing, Local Food")
    generated_itinerary = models.JSONField(default=dict)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Plan for {self.destination} ({self.duration_days} Days - ₹{self.budget})"


class IncidentReport(models.Model):
    reporter_name = models.CharField(max_length=150, default="Anonymous Tourist")
    incident_type = models.CharField(max_length=60, choices=[
        ('Harassment', 'Harassment Report'),
        ('Theft', 'Theft / Pickpocketing'),
        ('Unlit/Unsafe Area', 'Unlit / Isolated Area Report'),
        ('Overcharging/Scam', 'Tourist Overcharging / Scam'),
        ('Accident', 'Road / River Accident'),
        ('Medical Emergency', 'Medical Emergency'),
    ])
    location_name = models.CharField(max_length=200)
    destination = models.ForeignKey(Destination, on_delete=models.CASCADE, related_name='incident_reports', null=True, blank=True)
    latitude = models.FloatField(default=16.9891)
    longitude = models.FloatField(default=81.7840)
    description = models.TextField()
    status = models.CharField(max_length=30, default='Under Review', choices=[
        ('Under Review', 'Under Review'),
        ('Verified by Police', 'Verified by Police'),
        ('Resolved', 'Resolved & Safe'),
    ])
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"[{self.incident_type}] {self.location_name} - {self.status}"


class GovernmentDispatchLog(models.Model):
    """Ministry of Home Affairs ERSS 112 Computer Aided Dispatch (CAD) Log."""
    STATUS_CHOICES = [
        ('QUEUED', '⏳ ERSS 112 Queued'),
        ('DISPATCHED_TO_PCR', '🚔 PCR Unit Dispatched'),
        ('PCR_EN_ROUTE', '🚨 PCR Unit En Route'),
        ('ON_SCENE', '📍 First Responders On Scene'),
        ('RESOLVED', '✅ Incident Resolved & Safe'),
    ]

    cad_reference_id = models.CharField(max_length=60, unique=True, db_index=True)
    incident = models.ForeignKey(IncidentReport, on_delete=models.SET_NULL, null=True, blank=True, related_name='erss_dispatches')
    traveler_name = models.CharField(max_length=150, default="Solo Traveler")
    traveler_phone = models.CharField(max_length=50, blank=True)
    emergency_contact = models.CharField(max_length=150, blank=True)
    latitude = models.FloatField(default=16.9891)
    longitude = models.FloatField(default=81.7840)
    location_name = models.CharField(max_length=255, default="Godavari Riverfront")
    jurisdiction_police_station = models.CharField(max_length=200, default="Rajahmundry I Town Police Station")
    pcr_callsign = models.CharField(max_length=100, default="PCR-UNIT-1")
    dispatch_status = models.CharField(max_length=40, choices=STATUS_CHOICES, default='DISPATCHED_TO_PCR')
    cad_payload = models.JSONField(default=dict, blank=True)
    is_offline_sync = models.BooleanField(default=False, help_text="Was this alert synced after being offline?")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.cad_reference_id} — {self.traveler_name} ({self.get_dispatch_status_display()})"


class TourismPackage(models.Model):
    """A curated tourism package that bundles destinations, stays, and activities
    for seamless exploration by travelers."""
    PACKAGE_TYPES = [
        ('Weekend', 'Weekend Getaway'),
        ('Adventure', 'Adventure & Activity'),
        ('Cultural', 'Cultural & Heritage'),
        ('Luxury', 'Luxury Escape'),
        ('Budget', 'Budget Backpacker'),
        ('WomenSafe', 'Women-Safe Solo'),
    ]
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=220, unique=True, blank=True, help_text="URL-friendly identifier, auto-generated if left blank")
    subtitle = models.CharField(max_length=300, blank=True, help_text="Short tagline for the package card")
    description = models.TextField()
    package_type = models.CharField(max_length=20, choices=PACKAGE_TYPES, default='Cultural')
    destination = models.ForeignKey(Destination, on_delete=models.CASCADE, related_name='packages')
    price = models.DecimalField(max_digits=10, decimal_places=2, help_text="Base price in INR")
    duration_days = models.IntegerField(default=2, help_text="Length of the package in days")
    rating = models.FloatField(default=4.5, help_text="Average customer rating (0-5)")
    review_count = models.IntegerField(default=0, help_text="Total number of reviews")
    highlights = models.JSONField(default=list, help_text="Key selling points of the package")
    inclusions = models.JSONField(default=list, help_text="What is included (meals, transport, entry fees, etc.)")
    exclusions = models.JSONField(default=list, help_text="What is NOT included")
    itinerary_summary = models.JSONField(default=list, help_text="Day-wise high-level itinerary preview")
    image_url = models.CharField(max_length=500, blank=True)
    is_featured = models.BooleanField(default=False, help_text="Showcase on landing page carousel")
    is_available = models.BooleanField(default=True)
    max_group_size = models.IntegerField(default=6, help_text="Maximum travelers per booking")
    age_from = models.IntegerField(default=5, help_text="Minimum recommended age")
    age_to = models.IntegerField(default=65, help_text="Maximum recommended age")
    difficulty = models.CharField(max_length=30, default="Easy", choices=[
        ('Easy', 'Easy'),
        ('Moderate', 'Moderate'),
        ('Challenging', 'Challenging'),
    ])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-is_featured', '-created_at']

    def __str__(self):
        return f"{self.title} ({self.destination.name})"

    @property
    def price_per_day(self):
        return round(self.price / max(self.duration_days, 1), 0)

    @property
    def badge_label(self):
        type_map = dict(self.PACKAGE_TYPES)
        return type_map.get(self.package_type, self.package_type)


class CustomerFeedback(models.Model):
    """Customer feedback system — allows users to submit structured feedback
    on destinations, hotels, packages, or general platform experience."""
    FEEDBACK_CATEGORIES = [
        ('General', 'General Platform Feedback'),
        ('Destination', 'Destination Experience'),
        ('Safety', 'Safety / Crime Data Accuracy'),
        ('Hotel', 'Verified Hotel Experience'),
        ('Package', 'Tourism Package Experience'),
        ('App', 'App / UX Feedback'),
    ]
    RATING_CHOICES = [(i, str(i)) for i in range(1, 6)]

    name = models.CharField(max_length=150, help_text="Customer name (or Anonymous)")
    email = models.EmailField(blank=True, help_text="Optional — for follow-up")
    category = models.CharField(max_length=50, choices=FEEDBACK_CATEGORIES, default='General')
    rating = models.IntegerField(choices=RATING_CHOICES, help_text="1 = Poor, 5 = Excellent")
    subject = models.CharField(max_length=200, blank=True, help_text="Brief subject line")
    message = models.TextField(help_text="Detailed feedback message")
    destination = models.ForeignKey(
        Destination, on_delete=models.SET_NULL, null=True, blank=True,
        related_name='feedback'
    )
    package = models.ForeignKey(
        TourismPackage, on_delete=models.SET_NULL, null=True, blank=True,
        related_name='feedback'
    )
    contact_allowed = models.BooleanField(default=False, help_text="Allow follow-up contact?")
    is_resolved = models.BooleanField(default=False, help_text="Internal status — feedback addressed")
    responded_at = models.DateTimeField(null=True, blank=True, help_text="When a team member responded")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"[{self.get_rating_display()}/5] {self.category} — {self.name}"


class PostTripReview(models.Model):
    """Post-trip review module — allows travelers to write detailed reviews
    and notes after completing a trip to a destination."""
    destination = models.ForeignKey(
        Destination, on_delete=models.CASCADE, related_name='post_trip_reviews'
    )
    package = models.ForeignKey(
        TourismPackage, on_delete=models.SET_NULL, null=True, blank=True,
        related_name='post_trip_reviews'
    )
    reviewer_name = models.CharField(max_length=150, default="Anonymous Traveler")
    traveler_type = models.CharField(max_length=60, default="Individual Traveler", choices=[
        ('Solo Woman', 'Solo Woman Traveler'),
        ('Solo Man', 'Solo Man Traveler'),
        ('Family', 'Family Group'),
        ('Friends', 'Friends Group'),
        ('Couple', 'Couple'),
        ('Individual Traveler', 'Individual Traveler'),
    ])
    overall_rating = models.FloatField(default=0.0, help_text="Overall trip rating (0-5)")
    safety_rating = models.FloatField(default=0.0, help_text="Safety experience rating (0-5)")
    value_rating = models.FloatField(default=0.0, help_text="Value for money rating (0-5)")
    title = models.CharField(max_length=200, help_text="Review headline")
    detailed_notes = models.TextField(blank=True, help_text="Detailed post-trip notes and reflections")
    pros = models.JSONField(default=list, help_text="Positive aspects of the trip")
    cons = models.JSONField(default=list, help_text="Areas for improvement")
    travel_tips = models.TextField(blank=True, help_text="Tips for future travelers")
    would_recommend = models.BooleanField(default=True, help_text="Would you recommend this destination?")
    photos = models.JSONField(default=list, help_text="Photo URLs with captions [{url, caption}]")
    is_published = models.BooleanField(default=False, help_text="Display publicly on destination page")
    moderated = models.BooleanField(default=False, help_text="Review has been admin-approved")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.reviewer_name} — {self.destination.name} ({self.overall_rating}/5)"

    @property
    def average_rating(self):
        ratings = [r for r in [self.overall_rating, self.safety_rating, self.value_rating] if r > 0]
        return round(sum(ratings) / max(len(ratings), 1), 1)


class CrimeStatistic(models.Model):
    """Historical crime statistics over time for trend analysis and charting."""
    destination = models.ForeignKey(
        Destination, on_delete=models.CASCADE, related_name='crime_statistics'
    )
    period_label = models.CharField(max_length=50, help_text="e.g. 'Q1 2025', 'Jan 2026'")
    recorded_at = models.DateField(help_text="Reporting period end date")
    theft_cases = models.IntegerField(default=0)
    harassment_cases = models.IntegerField(default=0)
    violent_crime_cases = models.IntegerField(default=0)
    other_cases = models.IntegerField(default=0)
    total_cases = models.IntegerField(default=0, help_text="Sum of all crime categories")
    population_estimate = models.IntegerField(default=200000, help_text="Reference population for rate calculation")
    crime_rate_per_100k = models.FloatField(default=0.0, help_text="Computed crime rate per 100k population")
    data_source = models.CharField(max_length=100, default="Local Police Records")
    notes = models.TextField(blank=True)

    class Meta:
        ordering = ['-recorded_at']
        unique_together = ['destination', 'period_label']

    def __str__(self):
        return f"{self.destination.name} — {self.period_label} ({self.total_cases} cases, {self.crime_rate_per_100k}/100k)"

    def save(self, *args, **kwargs):
        self.total_cases = self.theft_cases + self.harassment_cases + self.violent_crime_cases + self.other_cases
        if self.population_estimate > 0:
            self.crime_rate_per_100k = round(self.total_cases / self.population_estimate * 100000, 2)
        super().save(*args, **kwargs)


class UserProfile(models.Model):
    """Extended profile data for a registered traveler, linked to Django's User."""
    TRAVEL_STYLES = [
        ('Solo Woman', 'Solo Woman Traveler'),
        ('Solo Man', 'Solo Man Traveler'),
        ('Family', 'Family Group'),
        ('Couple', 'Couple'),
        ('Friends', 'Friends Group'),
        ('Group', 'Group Tour'),
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    phone = models.CharField(max_length=20, blank=True)
    address = models.CharField(max_length=255, blank=True)
    city = models.CharField(max_length=100, blank=True)
    state = models.CharField(max_length=100, blank=True)
    travel_style = models.CharField(max_length=50, choices=TRAVEL_STYLES, default='Solo Woman')
    interests = models.CharField(max_length=255, blank=True, help_text="Comma-separated interests, e.g. Culture, Riverfront, Local Food")
    emergency_contact_name = models.CharField(max_length=150, blank=True)
    emergency_contact_phone = models.CharField(max_length=50, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} ({self.get_travel_style_display()})"


class Booking(models.Model):
    """A package booking initiated by a logged-in traveler."""
    STATUS_CHOICES = [
        ('Pending', 'Pending Payment'),
        ('Paid', 'Confirmed & Paid'),
        ('Cancelled', 'Cancelled'),
    ]
    booking_ref = models.CharField(max_length=40, unique=True, default=uuid.uuid4)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bookings')
    package = models.ForeignKey(TourismPackage, on_delete=models.CASCADE, related_name='bookings')
    num_travelers = models.IntegerField(default=1)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    
    # Traveler manifest & trip specifics
    travelers_data = models.JSONField(default=list, blank=True, help_text="List of traveler details [{name, age, gender, id_type, id_number, phone, emergency_contact, dietary_pref}]")
    contact_email = models.EmailField(blank=True)
    contact_phone = models.CharField(max_length=30, blank=True)
    travel_date = models.DateField(null=True, blank=True)
    special_requests = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.booking_ref} — {self.package.title} ({self.get_status_display()})"


class Payment(models.Model):
    """Simulated payment record tied to a booking."""
    METHOD_CHOICES = [
        ('UPI', 'UPI (GPay / PhonePe / Paytm)'),
        ('Card', 'Credit / Debit Card'),
        ('NetBanking', 'Net Banking'),
    ]
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Success', 'Success'),
        ('Failed', 'Failed'),
    ]
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE, related_name='payments')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    method = models.CharField(max_length=20, choices=METHOD_CHOICES, default='UPI')
    transaction_id = models.CharField(max_length=50, blank=True, default=uuid.uuid4, unique=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    paid_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-paid_at']

    def __str__(self):
        return f"{self.booking.booking_ref} — ₹{self.amount} ({self.get_method_display()}, {self.status})"
