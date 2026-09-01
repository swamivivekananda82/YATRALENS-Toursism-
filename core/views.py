import json
import io
import uuid
from django.db.models import Count, Avg
from django.utils import timezone
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.views.decorators.http import require_http_methods
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from .models import (
    Destination, SafetyZone, Attraction, VerifiedHotel,
    EmergencyService, SafetyAlert, LiveShareSession,
    TravelMemory, TripPlan, IncidentReport,
    TourismPackage, CustomerFeedback, PostTripReview, CrimeStatistic,
    UserProfile, Booking, Payment
)
from .serializers import (
    DestinationSerializer, SafetyZoneSerializer, AttractionSerializer,
    VerifiedHotelSerializer, EmergencyServiceSerializer, SafetyAlertSerializer,
    LiveShareSessionSerializer, TravelMemorySerializer, TripPlanSerializer,
    IncidentReportSerializer, TourismPackageSerializer, CustomerFeedbackSerializer,
    PostTripReviewSerializer, CrimeStatisticSerializer
)
from .ai_service import (
    generate_travel_story, generate_smart_itinerary,
    ai_travel_assistant_reply, calculate_safe_routes
)

from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle


# ==========================================
# TEMPLATE VIEWS (Pages)
# ==========================================

def index_view(request):
    """YATRALENS Professional Landing Page"""
    destinations = Destination.objects.all().order_by('-safety_score')
    alerts = SafetyAlert.objects.filter(is_active=True).order_by('-created_at')[:3]
    recent_memories = TravelMemory.objects.all().order_by('-created_at')[:3]
    featured_packages = TourismPackage.objects.filter(is_featured=True, is_available=True).order_by('-rating')[:6]
    popular_packages = TourismPackage.objects.filter(is_available=True).order_by('-review_count', '-rating')[:8]

    # Crime-rate snapshot: top destinations with most recent crime data
    crime_snapshot = []
    for dest in destinations[:6]:
        latest_stats = dest.crime_statistics.order_by('-recorded_at').first()
        crime_snapshot.append({
            'destination': dest,
            'latest_stat': latest_stats,
            'trend': dest.crime_trend,
            'last_update': dest.last_crime_update,
        })

    # Public feedback / reviews for social proof
    recent_reviews = PostTripReview.objects.filter(is_published=True, moderated=True).order_by('-created_at')[:4]

    # Aggregate stats for landing page
    total_reviews = PostTripReview.objects.filter(is_published=True, moderated=True).count()
    total_feedback = CustomerFeedback.objects.count()
    avg_feedback = CustomerFeedback.objects.aggregate(avg=Avg('rating'))['avg']
    avg_feedback = round(avg_feedback, 1) if avg_feedback else None

    review_stats = {
        'total_reviews': total_reviews,
        'total_feedback': total_feedback,
        'avg_rating': avg_feedback,
    }

    return render(request, 'index.html', {
        'destinations': destinations,
        'alerts': alerts,
        'recent_memories': recent_memories,
        'featured_packages': featured_packages,
        'popular_packages': popular_packages,
        'crime_snapshot': crime_snapshot,
        'recent_reviews': recent_reviews,
        'review_stats': review_stats,
        'active_tab': 'home'
    })


def safety_intelligence_view(request, destination_name="Rajahmundry"):
    # Default to Rajahmundry or first available
    dest = Destination.objects.filter(name__icontains=destination_name).first()
    if not dest:
        dest = Destination.objects.first()
    
    all_destinations = Destination.objects.all().order_by('name')
    safety_zones = dest.safety_zones.all() if dest else []
    alerts = SafetyAlert.objects.filter(is_active=True)

    # Crime statistics for trend charting
    crime_statistics = dest.crime_statistics.order_by('recorded_at') if dest else []
    # Recent incident reports for this destination
    recent_incidents = dest.incident_reports.order_by('-created_at')[:10] if dest else []

    return render(request, 'safety_intelligence.html', {
        'destination': dest,
        'all_destinations': all_destinations,
        'safety_zones': safety_zones,
        'alerts': alerts,
        'crime_statistics': crime_statistics,
        'recent_incidents': recent_incidents,
        'active_tab': 'safety'
    })


def women_safety_view(request):
    dest = Destination.objects.filter(name__icontains="Rajahmundry").first() or Destination.objects.first()
    emergency_services = EmergencyService.objects.filter(destination=dest) if dest else EmergencyService.objects.all()
    verified_hotels = VerifiedHotel.objects.filter(destination=dest, women_friendly=True) if dest else []
    
    # Active live sessions
    default_session = LiveShareSession.objects.first()
    if not default_session:
        default_session = LiveShareSession.objects.create(
            session_token=str(uuid.uuid4())[:8],
            traveler_name="Priya Sharma",
            trusted_contact_name="Mom",
            trusted_contact_phone="+91 98765 43210",
            current_location_name="Godavari Pushkar Ghat, Rajahmundry",
            current_latitude=16.9891,
            current_longitude=81.7840
        )
    
    return render(request, 'women_safety.html', {
        'destination': dest,
        'emergency_services': emergency_services,
        'verified_hotels': verified_hotels,
        'live_session': default_session,
        'active_tab': 'women_safety'
    })


def verified_hotels_view(request):
    destinations = Destination.objects.all()
    selected_dest_id = request.GET.get('destination')
    women_only = request.GET.get('women_friendly')
    
    hotels = VerifiedHotel.objects.filter(verified=True)
    if selected_dest_id:
        hotels = hotels.filter(destination_id=selected_dest_id)
    if women_only:
        hotels = hotels.filter(women_friendly=True)
        
    return render(request, 'verified_hotels.html', {
        'hotels': hotels,
        'destinations': destinations,
        'selected_dest_id': selected_dest_id,
        'active_tab': 'hotels'
    })


def emergency_map_view(request):
    dest = Destination.objects.filter(name__icontains="Rajahmundry").first() or Destination.objects.first()
    services = EmergencyService.objects.all()
    destinations = Destination.objects.all()
    return render(request, 'emergency_map.html', {
        'destination': dest,
        'services': services,
        'destinations': destinations,
        'active_tab': 'emergency'
    })


def ai_assistant_view(request):
    destinations = Destination.objects.all()
    return render(request, 'ai_assistant.html', {
        'destinations': destinations,
        'active_tab': 'ai_assistant'
    })


def trip_planner_view(request):
    destinations = Destination.objects.all()
    return render(request, 'trip_planner.html', {
        'destinations': destinations,
        'active_tab': 'trip_planner'
    })


def memory_maker_view(request):
    destinations = Destination.objects.all()
    rajahmundry = Destination.objects.filter(name__icontains="Rajahmundry").first()
    attractions = rajahmundry.attractions.all() if rajahmundry else Attraction.objects.all()
    memories = TravelMemory.objects.all().order_by('-created_at')
    
    return render(request, 'memory_maker.html', {
        'destinations': destinations,
        'attractions': attractions,
        'memories': memories,
        'active_tab': 'memories'
    })


def memory_detail_view(request, memory_id):
    memory = get_object_or_404(TravelMemory, id=memory_id)
    return render(request, 'memory_detail.html', {
        'memory': memory,
        'active_tab': 'memories'
    })


def live_tracker_view(request, token):
    session = get_object_or_404(LiveShareSession, session_token=token)
    emergency_services = EmergencyService.objects.all()[:5]
    return render(request, 'live_tracker.html', {
        'session': session,
        'emergency_services': emergency_services
    })


def profile_view(request):
    if not request.user.is_authenticated:
        messages.info(request, 'Please login or register to view your profile.')
        return redirect(f'{reverse("login")}?next={request.path}')

    user = request.user
    profile = getattr(user, 'profile', None)

    memories = TravelMemory.objects.all().order_by('-created_at')
    trip_plans = TripPlan.objects.all().order_by('-created_at')
    verified_hotels = VerifiedHotel.objects.filter(verified=True)[:3]
    user_reviews = PostTripReview.objects.filter(moderated=True, is_published=True).order_by('-created_at')[:5]
    user_feedback = CustomerFeedback.objects.order_by('-created_at')[:5]
    bookings = Booking.objects.filter(user=user).order_by('-created_at')[:5]

    # Build user initials for avatar
    display_name = user.get_full_name() or user.username
    initials = ''.join([part[0].upper() for part in display_name.split() if part])[:2] or user.username[:2].upper()

    return render(request, 'profile.html', {
        'profile_user': user,
        'profile': profile,
        'display_name': display_name,
        'initials': initials,
        'memories': memories,
        'trip_plans': trip_plans,
        'verified_hotels': verified_hotels,
        'user_reviews': user_reviews,
        'user_feedback': user_feedback,
        'bookings': bookings,
        'active_tab': 'profile'
    })


@require_http_methods(["GET", "POST"])
def login_view(request):
    if request.user.is_authenticated:
        return redirect(request.GET.get('next') or 'profile')

    next_url = request.GET.get('next') or request.POST.get('next') or ''
    # Prevent open-redirect
    if next_url and not next_url.startswith('/'):
        next_url = ''

    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            if not request.POST.get('remember'):
                request.session.set_expiry(0)
            messages.success(request, f'Welcome back, {user.username}!')
            if next_url:
                return redirect(next_url)
            return redirect('profile')
        messages.error(request, 'Invalid username or password.')

    return render(request, 'login.html', {
        'active_tab': 'profile',
        'next': next_url,
    })


@require_http_methods(["GET", "POST"])
def logout_view(request):
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('index')


@require_http_methods(["GET", "POST"])
def register_view(request):
    if request.user.is_authenticated:
        return redirect(request.GET.get('next') or 'profile')

    next_url = request.GET.get('next') or request.POST.get('next') or ''
    if next_url and not next_url.startswith('/'):
        next_url = ''

    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        full_name = request.POST.get('full_name', '').strip()
        email = request.POST.get('email', '').strip()
        password = request.POST.get('password', '')
        confirm_password = request.POST.get('confirm_password', '')
        phone = request.POST.get('phone', '').strip()
        address = request.POST.get('address', '').strip()
        city = request.POST.get('city', '').strip()
        state = request.POST.get('state', '').strip()
        travel_style = request.POST.get('travel_style', 'Solo Woman')
        interests = request.POST.get('interests', '').strip()
        emergency_name = request.POST.get('emergency_contact_name', '').strip()
        emergency_phone = request.POST.get('emergency_contact_phone', '').strip()

        # --- Validations ---
        errors = []
        if not username or not password or not email:
            errors.append('Username, email and password are required.')
        if User.objects.filter(username=username).exists():
            errors.append('This username is already taken.')
        if User.objects.filter(email=email).exists():
            errors.append('An account with this email already exists.')
        if password != confirm_password:
            errors.append('Passwords do not match.')
        if len(password) < 6:
            errors.append('Password must be at least 6 characters.')

        if errors:
            for error in errors:
                messages.error(request, error)
            return render(request, 'register.html', {
                'active_tab': 'profile',
                'form_data': request.POST,
                'next': next_url,
            })

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
        )
        user.first_name = full_name.split(' ')[0] if full_name else username
        if len(full_name.split(' ')) > 1:
            user.last_name = ' '.join(full_name.split(' ')[1:])
        user.save()

        UserProfile.objects.create(
            user=user,
            phone=phone,
            address=address,
            city=city,
            state=state,
            travel_style=travel_style,
            interests=interests,
            emergency_contact_name=emergency_name,
            emergency_contact_phone=emergency_phone,
        )

        login(request, user)
        messages.success(request, f'Welcome to YATRALENS, {username}! Your account has been created.')
        if next_url:
            return redirect(next_url)
        return redirect('profile')

    return render(request, 'register.html', {'active_tab': 'profile', 'next': next_url})


@require_http_methods(["GET", "POST"])
def booking_view(request, package_slug):
    """Gather traveler count and create a booking, then send to payment."""
    package = get_object_or_404(TourismPackage, slug=package_slug, is_available=True)

    if not request.user.is_authenticated:
        messages.info(request, 'Please login or register to book a package.')
        return redirect(f'{reverse("login")}?next={request.path}')

    if request.method == 'POST':
        try:
            num_travelers = int(request.POST.get('num_travelers', 1))
        except ValueError:
            num_travelers = 1
        num_travelers = max(1, min(num_travelers, package.max_group_size))

        unit_price = package.price
        total = unit_price * num_travelers
        booking = Booking.objects.create(
            user=request.user,
            package=package,
            num_travelers=num_travelers,
            unit_price=unit_price,
            total_amount=total,
        )
        return redirect('payment', booking_ref=booking.booking_ref)

    return render(request, 'booking.html', {
        'package': package,
        'active_tab': 'packages',
    })


@require_http_methods(["GET", "POST"])
def payment_view(request, booking_ref):
    """Simulated payment gateway checkout for a pending booking."""
    booking = get_object_or_404(Booking, booking_ref=booking_ref, user=request.user)

    if booking.status == 'Paid':
        return redirect('payment_success', booking_ref=booking.booking_ref)

    if request.method == 'POST':
        method = request.POST.get('method', 'UPI')
        # Simulated processing result based on card number heuristics for demo
        holder_name = request.POST.get('holder_name', '')
        card_number = request.POST.get('card_number', '')
        upi_id = request.POST.get('upi_id', '')
        bank = request.POST.get('bank', '')

        # Demo rule: payment "fails" if user enters digits 0000 or empty holder
        simulated_failure = False
        if method == 'Card' and card_number.replace(' ', '').endswith('0000'):
            simulated_failure = True
        if method == 'Card' and not holder_name.strip():
            simulated_failure = True
        if method == 'UPI' and not upi_id.strip():
            simulated_failure = True
        if method == 'NetBanking' and not bank:
            simulated_failure = True

        # Create payment record with retryable status
        payment = Payment.objects.create(
            booking=booking,
            amount=booking.total_amount,
            method=method,
            status='Pending',
        )

        if simulated_failure:
            payment.status = 'Failed'
            payment.save()
            messages.error(request, 'Payment failed. Please verify your details and try again. (Demo hint: avoid card numbers ending in 0000)')
            return redirect('payment', booking_ref=booking.booking_ref)

        payment.status = 'Success'
        payment.save()
        booking.status = 'Paid'
        booking.save()
        messages.success(request, 'Payment successful! Your booking is confirmed.')
        return redirect('payment_success', booking_ref=booking.booking_ref)

    return render(request, 'payment.html', {
        'booking': booking,
        'active_tab': 'packages',
    })


def payment_success_view(request, booking_ref):
    """Booking confirmation shown after a successful simulated payment."""
    booking = get_object_or_404(Booking, booking_ref=booking_ref, user=request.user)
    return render(request, 'payment_success.html', {
        'booking': booking,
        'active_tab': 'packages',
    })


def booking_history_view(request):
    bookings = Booking.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'booking_history.html', {
        'bookings': bookings,
        'active_tab': 'profile',
    })


# ==========================================
# TOURISM PACKAGES VIEWS
# ==========================================

def tourism_package_list_view(request):
    """Browse and filter tourism packages with seamless exploration."""
    destinations = Destination.objects.all().order_by('name')

    packages = TourismPackage.objects.filter(is_available=True).order_by('-is_featured', '-rating')

    # Filters
    dest_filter = request.GET.get('destination')
    if dest_filter:
        packages = packages.filter(destination_id=dest_filter)

    type_filter = request.GET.get('type')
    if type_filter:
        packages = packages.filter(package_type=type_filter)

    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    if min_price:
        packages = packages.filter(price__gte=float(min_price))
    if max_price:
        packages = packages.filter(price__lte=float(max_price))

    min_rating = request.GET.get('min_rating')
    if min_rating:
        packages = packages.filter(rating__gte=float(min_rating))

    search = request.GET.get('q')
    if search:
        packages = packages.filter(title__icontains=search)

    packages = packages[:24]

    return render(request, 'tourism_packages.html', {
        'packages': packages,
        'destinations': destinations,
        'active_tab': 'packages'
    })


def tourism_package_detail_view(request, package_slug):
    """Detailed view of a single tourism package."""
    package = get_object_or_404(TourismPackage, slug=package_slug, is_available=True)
    destination = package.destination
    related_packages = TourismPackage.objects.filter(
        destination=destination, is_available=True
    ).exclude(id=package.id).order_by('-rating')[:3]
    verified_hotels = VerifiedHotel.objects.filter(destination=destination, verified=True, women_friendly=True)[:4]
    post_trip_reviews = PostTripReview.objects.filter(
        destination=destination, is_published=True, moderated=True
    ).order_by('-created_at')[:6]
    crime_statistics = destination.crime_statistics.order_by('recorded_at')

    return render(request, 'package_detail.html', {
        'package': package,
        'destination': destination,
        'related_packages': related_packages,
        'verified_hotels': verified_hotels,
        'post_trip_reviews': post_trip_reviews,
        'crime_statistics': crime_statistics,
        'active_tab': 'packages'
    })


def customer_feedback_view(request):
    """Customer feedback submission + display of public feedback."""
    destinations = Destination.objects.all().order_by('name')
    packages = TourismPackage.objects.filter(is_available=True).order_by('-rating')[:10]

    if request.method == 'POST':
        feedback = CustomerFeedback.objects.create(
            name=request.POST.get('name', 'Anonymous'),
            email=request.POST.get('email', ''),
            category=request.POST.get('category', 'General'),
            rating=int(request.POST.get('rating', 5)),
            subject=request.POST.get('subject', ''),
            message=request.POST.get('message', ''),
            contact_allowed=request.POST.get('contact_allowed') == 'on',
        )
        dest_name = request.POST.get('destination')
        if dest_name:
            dest = Destination.objects.filter(name__iexact=dest_name).first()
            if dest:
                feedback.destination = dest
                feedback.save()
        pkg_id = request.POST.get('package')
        if pkg_id:
            pkg = TourismPackage.objects.filter(id=pkg_id).first()
            if pkg:
                feedback.package = pkg
                feedback.save()

        messages.success(request, 'Thank you! Your feedback has been submitted and received.')
        return redirect('customer_feedback')

    # Public feedback (only General category, no internal comments)
    public_feedback = CustomerFeedback.objects.filter(
        category='General'
    ).order_by('-created_at')[:10]

    # Rating distribution for stats display
    rating_distribution = CustomerFeedback.objects.values('rating').annotate(
        count=Count('rating')
    ).order_by('rating')
    rating_counts = {item['rating']: item['count'] for item in rating_distribution}
    total_feedback = CustomerFeedback.objects.count()
    avg_rating = CustomerFeedback.objects.aggregate(avg_rating=Avg('rating'))['avg_rating']
    if avg_rating:
        avg_rating = round(avg_rating, 1)

    return render(request, 'customer_feedback.html', {
        'destinations': destinations,
        'packages': packages,
        'public_feedback': public_feedback,
        'rating_counts': rating_counts,
        'total_feedback': total_feedback,
        'avg_rating': avg_rating,
        'active_tab': 'feedback'
    })


def post_trip_review_view(request):
    """Post-trip review submission and public review browsing."""
    destinations = Destination.objects.all().order_by('name')
    packages = TourismPackage.objects.filter(is_available=True).order_by('-rating')[:10]

    if request.method == 'POST':
        dest_id = request.POST.get('destination')
        destination = get_object_or_404(Destination, id=dest_id) if dest_id else None

        pkg_id = request.POST.get('package')
        package = TourismPackage.objects.filter(id=pkg_id).first() if pkg_id else None

        review = PostTripReview.objects.create(
            destination=destination,
            package=package,
            reviewer_name=request.POST.get('reviewer_name', 'Anonymous Traveler'),
            traveler_type=request.POST.get('traveler_type', 'Individual Traveler'),
            overall_rating=float(request.POST.get('overall_rating', 0) or 0),
            safety_rating=float(request.POST.get('safety_rating', 0) or 0),
            value_rating=float(request.POST.get('value_rating', 0) or 0),
            title=request.POST.get('title', ''),
            detailed_notes=request.POST.get('detailed_notes', ''),
            pros=request.POST.getlist('pros'),
            cons=request.POST.getlist('cons'),
            travel_tips=request.POST.get('travel_tips', ''),
            would_recommend=request.POST.get('would_recommend') == 'on',
            photos=request.POST.getlist('photos') or [],
            is_published=True,
        )
        messages.success(request, 'Your post-trip review has been submitted! It will appear publicly after a quick moderation check.')
        return redirect('post_trip_review')

    # All published, moderated reviews — grouped by destination
    all_reviews = PostTripReview.objects.filter(
        is_published=True, moderated=True
    ).order_by('-created_at')

    # Aggregate stats per destination
    review_stats = {}
    for dest in destinations:
        dest_reviews = all_reviews.filter(destination=dest)
        if dest_reviews.exists():
            avg_overall = dest_reviews.aggregate(avg_rating=Avg('overall_rating'))['avg_rating']
            review_stats[dest.id] = {
                'count': dest_reviews.count(),
                'avg_rating': round(avg_overall, 1) if avg_overall else None,
            }

    return render(request, 'post_trip_review.html', {
        'destinations': destinations,
        'packages': packages,
        'all_reviews': all_reviews,
        'review_stats': review_stats,
        'active_tab': 'reviews'
    })


def reviews_by_destination_view(request, destination_name=""):
    """Browse all published post-trip reviews for a specific destination."""
    dest = Destination.objects.filter(name__icontains=destination_name).first()
    if not dest:
        dest = Destination.objects.first()
    all_reviews = PostTripReview.objects.filter(
        destination=dest, is_published=True, moderated=True
    ).order_by('-created_at')
    destinations = Destination.objects.all().order_by('name')
    return render(request, 'reviews_destination.html', {
        'destination': dest,
        'all_reviews': all_reviews,
        'destinations': destinations,
        'active_tab': 'reviews'
    })


def admin_dashboard_view(request):
    destinations = Destination.objects.all()
    hotels = VerifiedHotel.objects.all()
    incidents = IncidentReport.objects.all().order_by('-created_at')
    alerts = SafetyAlert.objects.all().order_by('-created_at')
    total_memories = TravelMemory.objects.count()
    
    # Calculate summary metrics
    avg_safety = sum(d.safety_score for d in destinations) / max(len(destinations), 1)
    
    return render(request, 'admin_dashboard.html', {
        'destinations': destinations,
        'hotels': hotels,
        'incidents': incidents,
        'alerts': alerts,
        'total_memories': total_memories,
        'avg_safety': round(avg_safety, 1),
        'active_tab': 'admin'
    })


# ==========================================
# REST API ENDPOINTS
# ==========================================

@api_view(['GET'])
def api_destinations(request):
    query = request.GET.get('q', '')
    if query:
        destinations = Destination.objects.filter(name__icontains=query)
    else:
        destinations = Destination.objects.all()
    serializer = DestinationSerializer(destinations, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def api_destination_detail(request, name):
    destination = Destination.objects.filter(name__icontains=name).first()
    if not destination:
        return Response({'error': 'Destination not found'}, status=status.HTTP_404_NOT_FOUND)
    serializer = DestinationSerializer(destination)
    return Response(serializer.data)


@api_view(['POST'])
def api_safe_route(request):
    data = request.data or {}
    start_loc = data.get('start', 'Rajahmundry Railway Station')
    end_loc = data.get('end', 'Dowleswaram Barrage')
    dest_name = data.get('destination', 'Rajahmundry')
    
    dest = Destination.objects.filter(name__icontains=dest_name).first()
    lat = dest.latitude if dest else 16.9891
    lng = dest.longitude if dest else 81.7840
    
    routes_data = calculate_safe_routes(start_loc, end_loc, lat, lng)
    return Response(routes_data)


@api_view(['POST'])
def api_sos_trigger(request):
    data = request.data or {}
    traveler_name = data.get('traveler_name', 'Solo Traveler')
    lat = float(data.get('latitude', 16.9891))
    lng = float(data.get('longitude', 81.7840))
    location_name = data.get('location_name', 'Godavari Pushkar Ghat, Rajahmundry')
    
    # Create or update emergency incident
    incident = IncidentReport.objects.create(
        reporter_name=traveler_name,
        incident_type='Medical Emergency',
        location_name=location_name,
        latitude=lat,
        longitude=lng,
        description=f"🚨 EMERGENCY SOS ACTIVATED by {traveler_name} at {location_name}. Automated emergency alert dispatched to trusted contacts and nearest police control room.",
        status='Under Review'
    )
    
    # Retrieve nearest police and hospitals
    police_stations = EmergencyService.objects.filter(service_type='Police')[:3]
    hospitals = EmergencyService.objects.filter(service_type='Hospital')[:3]
    
    police_data = EmergencyServiceSerializer(police_stations, many=True).data
    hospital_data = EmergencyServiceSerializer(hospitals, many=True).data
    
    return Response({
        'status': 'SOS_DISPATCHED',
        'alert_id': incident.id,
        'message': f"Emergency alert broadcasted. Coordinates: ({lat}, {lng}). SMS sent to trusted contacts.",
        'helplines': {
            'national_emergency': '112',
            'women_helpline': '1091',
            'women_distress': '1090',
            'tourist_helpline': '1363',
            'police_control_room': '0883-2471033'
        },
        'nearest_police': police_data,
        'nearest_hospitals': hospital_data
    })


@api_view(['POST'])
def api_live_share_create(request):
    data = request.data or {}
    session = LiveShareSession.objects.create(
        session_token=str(uuid.uuid4())[:8],
        traveler_name=data.get('traveler_name', 'Priya Sharma'),
        trusted_contact_name=data.get('trusted_contact_name', 'Mom'),
        trusted_contact_phone=data.get('trusted_contact_phone', '+91 98765 43210'),
        current_location_name=data.get('current_location_name', 'Godavari Riverfront, Rajahmundry'),
        current_latitude=float(data.get('current_latitude', 16.9891)),
        current_longitude=float(data.get('current_longitude', 81.7840)),
        battery_level=int(data.get('battery_level', 88))
    )
    return Response(LiveShareSessionSerializer(session).data)


@api_view(['GET', 'POST'])
def api_live_share_detail(request, token):
    session = get_object_or_404(LiveShareSession, session_token=token)
    if request.method == 'POST':
        data = request.data or {}
        if 'latitude' in data:
            session.current_latitude = float(data['latitude'])
        if 'longitude' in data:
            session.current_longitude = float(data['longitude'])
        if 'location_name' in data:
            session.current_location_name = data['location_name']
        if 'status' in data:
            session.status = data['status']
        if 'battery' in data:
            session.battery_level = int(data['battery'])
        session.save()
    return Response(LiveShareSessionSerializer(session).data)


@api_view(['POST'])
def api_ai_chat(request):
    data = request.data or {}
    message = data.get('message', '')
    if not message:
        return Response({'reply': 'Please ask a travel or safety question!'})
    reply = ai_travel_assistant_reply(message)
    return Response({'reply': reply})


@api_view(['POST'])
def api_generate_itinerary(request):
    data = request.data or {}
    dest_name = data.get('destination', 'Rajahmundry')
    duration = int(data.get('duration', 2))
    budget = float(data.get('budget', 5000))
    traveler_type = data.get('traveler_type', 'Solo Woman')
    interests = data.get('interests', 'Culture, Riverfront, Safe Sightseeing')
    
    itinerary_data = generate_smart_itinerary(dest_name, duration, budget, traveler_type, interests)
    
    # Save to TripPlan
    trip = TripPlan.objects.create(
        destination=dest_name,
        duration_days=duration,
        budget=budget,
        traveler_type=traveler_type,
        interests=interests,
        generated_itinerary=itinerary_data
    )
    
    return Response({
        'plan_id': trip.id,
        'itinerary': itinerary_data
    })


@api_view(['POST'])
def api_generate_story(request):
    data = request.data or {}
    title = data.get('title', '🌅 My Day in Rajahmundry')
    destination = data.get('destination', 'Rajahmundry')
    traveler_name = data.get('traveler_name', 'Solo Explorer')
    places = data.get('places', ['Godavari River', 'Dowleswaram Barrage', 'Markandeyeshwara Temple'])
    foods = data.get('foods', ['Authentic Andhra Meals', 'Atreyapuram Pootharekulu'])
    facts = data.get('facts', ['Dowleswaram Barrage was engineered by Sir Arthur Cotton across the Godavari River.'])
    favorite_moment = data.get('favorite_moment', 'Watching the golden sunset over the Godavari River from Pushkar Ghat.')
    
    generated_story = generate_travel_story(title, destination, traveler_name, places, foods, facts, favorite_moment)
    
    return Response({
        'story': generated_story,
        'title': title,
        'destination': destination
    })


@api_view(['POST'])
def api_save_memory(request):
    data = request.data or {}
    memory = TravelMemory.objects.create(
        title=data.get('title', '🌅 My Day in Rajahmundry'),
        destination=data.get('destination', 'Rajahmundry'),
        traveler_name=data.get('traveler_name', 'Priya Sharma'),
        traveler_type=data.get('traveler_type', 'Solo Woman Traveler'),
        places_visited=data.get('places_visited', []),
        food_tried=data.get('food_tried', []),
        historical_facts=data.get('historical_facts', []),
        favorite_moment=data.get('favorite_moment', ''),
        photos=data.get('photos', []),
        generated_story=data.get('generated_story', '')
    )
    return Response(TravelMemorySerializer(memory).data)


def export_memory_pdf_view(request, memory_id):
    """
    Generates a beautifully styled PDF Travel Album & Memory Story
    using ReportLab.
    """
    memory = get_object_or_404(TravelMemory, id=memory_id)
    
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=letter,
        rightMargin=40, leftMargin=40,
        topMargin=40, bottomMargin=40
    )
    
    styles = getSampleStyleSheet()
    
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=24,
        leading=28,
        textColor=colors.HexColor('#0f766e'), # teal-700
        alignment=1, # Center
        spaceAfter=8
    )
    
    subtitle_style = ParagraphStyle(
        'DocSubtitle',
        parent=styles['Normal'],
        fontName='Helvetica-Oblique',
        fontSize=12,
        leading=16,
        textColor=colors.HexColor('#64748b'), # slate-500
        alignment=1,
        spaceAfter=15
    )
    
    heading2_style = ParagraphStyle(
        'Heading2Custom',
        parent=styles['Heading2'],
        fontName='Helvetica-Bold',
        fontSize=14,
        leading=18,
        textColor=colors.HexColor('#1e293b'),
        spaceBefore=12,
        spaceAfter=6
    )
    
    body_style = ParagraphStyle(
        'BodyCustom',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=10.5,
        leading=15,
        textColor=colors.HexColor('#334155'),
        spaceAfter=10
    )
    
    highlight_box_style = ParagraphStyle(
        'HighlightBox',
        parent=styles['Normal'],
        fontName='Helvetica-Oblique',
        fontSize=11,
        leading=16,
        textColor=colors.HexColor('#b45309'),
        spaceBefore=6,
        spaceAfter=6
    )
    
    story_elements = []
    
    # Header
    story_elements.append(Paragraph(f"🌟 SafeTrip Memories – Travel Story", subtitle_style))
    story_elements.append(Paragraph(memory.title, title_style))
    story_elements.append(Paragraph(f"Destination: <b>{memory.destination}</b> | Traveler: <b>{memory.traveler_name}</b> ({memory.traveler_type})", subtitle_style))
    story_elements.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor('#0d9488'), spaceBefore=5, spaceAfter=15))
    
    # AI Story
    story_elements.append(Paragraph("📖 The Digital Travel Story", heading2_style))
    story_paragraphs = memory.generated_story.split('\n\n')
    for p in story_paragraphs:
        if p.strip():
            story_elements.append(Paragraph(p.replace('\n', '<br/>'), body_style))
    
    story_elements.append(Spacer(1, 10))
    
    # Favorite Moment Box
    if memory.favorite_moment:
        fav_content = [
            [Paragraph("⭐ <b>My Favorite Moment</b>", ParagraphStyle('FavHeader', fontName='Helvetica-Bold', fontSize=11, textColor=colors.HexColor('#92400e')))],
            [Paragraph(f'"{memory.favorite_moment}"', highlight_box_style)]
        ]
        fav_table = Table(fav_content, colWidths=[520])
        fav_table.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#fef3c7')), # amber-100
            ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#f59e0b')),
            ('PADDING', (0,0), (-1,-1), 10),
            ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ]))
        story_elements.append(fav_table)
        story_elements.append(Spacer(1, 12))
    
    # Places Visited & Food Tried Table
    summary_data = [
        [
            Paragraph("📍 <b>Places Visited</b>", heading2_style),
            Paragraph("🍛 <b>Local Culinary Tastes</b>", heading2_style)
        ],
        [
            Paragraph("<br/>• ".join([""] + (memory.places_visited if memory.places_visited else [memory.destination])), body_style),
            Paragraph("<br/>• ".join([""] + (memory.food_tried if memory.food_tried else ["Local Delicacies"])), body_style)
        ]
    ]
    summary_table = Table(summary_data, colWidths=[260, 260])
    summary_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#f8fafc')),
        ('BOX', (0,0), (-1,-1), 0.5, colors.HexColor('#cbd5e1')),
        ('PADDING', (0,0), (-1,-1), 8),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
    ]))
    story_elements.append(summary_table)
    story_elements.append(Spacer(1, 12))
    
    # Historical Facts
    if memory.historical_facts:
        story_elements.append(Paragraph("🏛️ Historical Facts & Heritage Notes", heading2_style))
        for fact in memory.historical_facts:
            story_elements.append(Paragraph(f"• {fact}", body_style))
        story_elements.append(Spacer(1, 10))
        
    # Safety Verification Seal
    footer_data = [
        [
            Paragraph("🛡️ <b>SafeTrip Verified Journey</b><br/><font size=8 color='#64748b'>Traveled with Safety-Optimized Routing & Live Protection Support</font>", body_style),
            Paragraph("🇮🇳 <b>Smart Tourism India</b><br/><font size=8 color='#64748b'>Emergency Helpline: 112 | Women Helpline: 1091</font>", body_style)
        ]
    ]
    footer_table = Table(footer_data, colWidths=[260, 260])
    footer_table.setStyle(TableStyle([
        ('LINEABOVE', (0,0), (-1,-1), 1, colors.HexColor('#0f766e')),
        ('PADDING', (0,0), (-1,-1), 6),
    ]))
    story_elements.append(footer_table)

    doc.build(story_elements)
    buffer.seek(0)
    
    response = HttpResponse(buffer, content_type='application/pdf')
    filename = f"SafeTrip_Memory_{memory.destination}_{memory.id}.pdf"
    response['Content-Disposition'] = f'attachment; filename="{filename}"'
    return response


@api_view(['POST'])
def api_admin_broadcast_alert(request):
    data = request.data or {}
    alert = SafetyAlert.objects.create(
        title=data.get('title', 'Safety Notice'),
        alert_type=data.get('alert_type', 'Safety Alert'),
        message=data.get('message', ''),
        severity=data.get('severity', 'Moderate'),
        is_active=True
    )
    return Response(SafetyAlertSerializer(alert).data)


@api_view(['POST'])
def api_admin_toggle_hotel(request):
    data = request.data or {}
    hotel_id = data.get('hotel_id')
    hotel = get_object_or_404(VerifiedHotel, id=hotel_id)
    hotel.verified = not hotel.verified
    hotel.save()
    return Response({'id': hotel.id, 'name': hotel.name, 'verified': hotel.verified})


@api_view(['POST'])
def api_report_incident(request):
    data = request.data or {}
    dest_name = data.get('destination', 'Rajahmundry')
    dest = Destination.objects.filter(name__icontains=dest_name).first()
    
    incident = IncidentReport.objects.create(
        reporter_name=data.get('reporter_name', 'Anonymous Tourist'),
        incident_type=data.get('incident_type', 'Suspicious Activity'),
        location_name=data.get('location_name', 'Main Road'),
        destination=dest,
        latitude=float(data.get('latitude', 16.9891)),
        longitude=float(data.get('longitude', 81.7840)),
        description=data.get('description', ''),
        status='Under Review'
    )
    return Response(IncidentReportSerializer(incident).data)


# ==========================================
# TOURISM PACKAGES API ENDPOINTS
# ==========================================

@api_view(['GET'])
def api_packages(request):
    """List all available tourism packages with optional filtering."""
    packages = TourismPackage.objects.filter(is_available=True).order_by('-rating')

    dest_filter = request.GET.get('destination')
    if dest_filter:
        packages = packages.filter(destination__name__icontains=dest_filter)

    type_filter = request.GET.get('type')
    if type_filter:
        packages = packages.filter(package_type=type_filter)

    min_rating = request.GET.get('min_rating')
    if min_rating:
        packages = packages.filter(rating__gte=float(min_rating))

    search = request.GET.get('q')
    if search:
        packages = packages.filter(title__icontains=search)

    serializer = TourismPackageSerializer(packages, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def api_package_detail(request, slug):
    """Retrieve detailed information for a single tourism package."""
    package = get_object_or_404(TourismPackage, slug=slug, is_available=True)
    serializer = TourismPackageSerializer(package)
    return Response(serializer.data)


@api_view(['GET'])
def api_crime_stats(request, destination_name):
    """Retrieve crime statistics and real-time crime data for a destination."""
    dest = Destination.objects.filter(name__icontains=destination_name).first()
    if not dest:
        return Response({'error': 'Destination not found'}, status=status.HTTP_404_NOT_FOUND)

    stats = dest.crime_statistics.order_by('recorded_at')
    stats_serializer = CrimeStatisticSerializer(stats, many=True)
    dest_serializer = DestinationSerializer(dest)

    # Build trend chart data
    periods = [s.period_label for s in stats]
    crime_rates = [s.crime_rate_per_100k for s in stats]
    theft_data = [s.theft_cases for s in stats]
    harassment_data = [s.harassment_cases for s in stats]
    violent_data = [s.violent_crime_cases for s in stats]

    return Response({
        'destination': dest_serializer.data,
        'crime_statistics': stats_serializer.data,
        'trend_chart': {
            'periods': periods,
            'crime_rates': crime_rates,
            'theft_cases': theft_data,
            'harassment_cases': harassment_data,
            'violent_crime_cases': violent_data,
        },
    })


# ==========================================
# CUSTOMER FEEDBACK API ENDPOINTS
# ==========================================

@api_view(['GET', 'POST'])
def api_feedback(request):
    """List public feedback or submit new feedback."""
    if request.method == 'GET':
        feedback = CustomerFeedback.objects.all().order_by('-created_at')
        serializer = CustomerFeedbackSerializer(feedback, many=True)
        return Response(serializer.data)

    data = request.data or {}
    dest = None
    if data.get('destination'):
        dest = Destination.objects.filter(name__icontains=data['destination']).first()
    pkg = None
    if data.get('package_id'):
        pkg = TourismPackage.objects.filter(id=data['package_id']).first()

    feedback = CustomerFeedback.objects.create(
        name=data.get('name', 'Anonymous'),
        email=data.get('email', ''),
        category=data.get('category', 'General'),
        rating=int(data.get('rating', 5)),
        subject=data.get('subject', ''),
        message=data.get('message', ''),
        destination=dest,
        package=pkg,
        contact_allowed=data.get('contact_allowed', False),
    )
    return Response(CustomerFeedbackSerializer(feedback).data, status=status.HTTP_201_CREATED)


@api_view(['GET'])
def api_feedback_stats(request):
    """Aggregate feedback statistics for the landing page."""
    total = CustomerFeedback.objects.count()
    avg = CustomerFeedback.objects.aggregate(avg=Avg('rating'))['avg']
    rating_dist = CustomerFeedback.objects.values('rating').annotate(
        count=Count('rating')
    ).order_by('rating')
    category_dist = CustomerFeedback.objects.values('category').annotate(
        count=Count('category')
    ).order_by('-count')
    return Response({
        'total_feedback': total,
        'average_rating': round(avg, 1) if avg else 0,
        'rating_distribution': {str(i): 0 for i in range(1, 6)} | {str(item['rating']): item['count'] for item in rating_dist},
        'category_distribution': list(category_dist),
    })


# ==========================================
# POST-TRIP REVIEW API ENDPOINTS
# ==========================================

@api_view(['GET', 'POST'])
def api_reviews(request):
    """List published reviews or submit a new post-trip review."""
    if request.method == 'GET':
        destination_filter = request.GET.get('destination')
        reviews = PostTripReview.objects.filter(is_published=True, moderated=True).order_by('-created_at')
        if destination_filter:
            reviews = reviews.filter(destination__name__icontains=destination_filter)
        serializer = PostTripReviewSerializer(reviews, many=True)
        return Response(serializer.data)

    data = request.data or {}
    dest = None
    if data.get('destination'):
        dest = Destination.objects.filter(name__icontains=data['destination']).first()
    if not dest and data.get('destination_id'):
        dest = Destination.objects.filter(id=data['destination_id']).first()

    pkg = None
    if data.get('package_id'):
        pkg = TourismPackage.objects.filter(id=data['package_id']).first()

    review = PostTripReview.objects.create(
        destination=dest,
        package=pkg,
        reviewer_name=data.get('reviewer_name', 'Anonymous Traveler'),
        traveler_type=data.get('traveler_type', 'Individual Traveler'),
        overall_rating=float(data.get('overall_rating', 0)),
        safety_rating=float(data.get('safety_rating', 0)),
        value_rating=float(data.get('value_rating', 0)),
        title=data.get('title', ''),
        detailed_notes=data.get('detailed_notes', ''),
        pros=data.get('pros', []),
        cons=data.get('cons', []),
        travel_tips=data.get('travel_tips', ''),
        would_recommend=data.get('would_recommend', True),
        photos=data.get('photos', []),
        is_published=True,
    )
    return Response(PostTripReviewSerializer(review).data, status=status.HTTP_201_CREATED)


@api_view(['GET'])
def api_reviews_stats(request):
    """Aggregate post-trip review statistics per destination."""
    destinations = Destination.objects.all()
    stats = []
    for dest in destinations:
        reviews = PostTripReview.objects.filter(destination=dest, is_published=True, moderated=True)
        count = reviews.count()
        if count > 0:
            avg_overall = reviews.aggregate(avg=Avg('overall_rating'))['avg']
            avg_safety = reviews.aggregate(avg=Avg('safety_rating'))['avg']
            avg_value = reviews.aggregate(avg=Avg('value_rating'))['avg']
            stats.append({
                'destination': dest.name,
                'state': dest.state,
                'review_count': count,
                'avg_overall': round(avg_overall, 1) if avg_overall else 0,
                'avg_safety': round(avg_safety, 1) if avg_safety else 0,
                'avg_value': round(avg_value, 1) if avg_value else 0,
                'safety_score': dest.safety_score,
            })
    return Response(stats)
