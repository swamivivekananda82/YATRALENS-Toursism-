from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse
from django.utils import timezone
from datetime import timedelta
from .models import Destination, SafetyZone, VerifiedHotel, EmergencyService, TravelMemory, LiveShareSession
from .models import TourismPackage, CustomerFeedback, PostTripReview, CrimeStatistic, Booking
from .ai_service import generate_travel_story, generate_smart_itinerary, ai_travel_assistant_reply, calculate_safe_routes

class SafeTripCoreTests(TestCase):
    def setUp(self):
        self.client = Client()
        # Authenticate the page-render client so auth-gated pages render too.
        User = get_user_model()
        self.user = User.objects.create_user(username='setuptest', password='securepass123')
        self.client.force_login(self.user)
        self.destination = Destination.objects.create(
            name="Rajahmundry",
            state="Andhra Pradesh",
            description="Cultural capital by Godavari river",
            latitude=16.9891,
            longitude=81.7840,
            safety_score=82,
            risk_level="Low Risk",
            violent_crime_reports=1,
        )
        self.safety_zone = SafetyZone.objects.create(
            destination=self.destination,
            name="Godavari Pushkar Ghat",
            zone_type="Tourist Area",
            risk_level="Low Risk",
            latitude=16.9940,
            longitude=81.7780
        )
        self.hotel = VerifiedHotel.objects.create(
            destination=self.destination,
            name="SafeStay Godavari Grand",
            rating=4.7,
            verified=True,
            women_friendly=True,
            latitude=16.9920,
            longitude=81.7810
        )
        self.service = EmergencyService.objects.create(
            destination=self.destination,
            name="Central Police Station",
            service_type="Police",
            phone="0883-2471033",
            latitude=16.9930,
            longitude=81.7820
        )
        self.memory = TravelMemory.objects.create(
            title="🌅 My Day in Rajahmundry",
            destination="Rajahmundry",
            traveler_name="Aarohi Reddy",
            places_visited=["Godavari River", "Dowleswaram Barrage"],
            food_tried=["Andhra Thali", "Pootharekulu"],
            favorite_moment="Watching the sunset at Dowleswaram Barrage.",
            generated_story="My journey began along the holy Godavari River..."
        )
        # YATRALENS test data
        self.package = TourismPackage.objects.create(
            title="Heritage Escape",
            slug="heritage-escape",
            description="2-day cultural escape",
            package_type="Cultural",
            destination=self.destination,
            price=5499,
            duration_days=2,
            rating=4.8,
            review_count=10,
            highlights=["Sunset", "Museum"],
            inclusions=["Hotel", "Meals"],
            itinerary_summary=[{"theme": "Day 1", "description": "Tour"}],
            image_url="https://example.com/img.jpg",
        )
        self.crime_stat = CrimeStatistic.objects.create(
            destination=self.destination,
            period_label="Q1 2026",
            recorded_at=timezone.now().date(),
            theft_cases=10,
            harassment_cases=2,
            violent_crime_cases=1,
            other_cases=0,
            population_estimate=350000,
            data_source="Test Source",
        )
        self.feedback = CustomerFeedback.objects.create(
            name="Test User",
            category="General",
            rating=5,
            message="Excellent platform!",
        )
        self.review = PostTripReview.objects.create(
            destination=self.destination,
            reviewer_name="Traveler X",
            overall_rating=4.5,
            safety_rating=5.0,
            value_rating=4.0,
            title="Great trip!",
            detailed_notes="Highly recommended.",
            pros=["Clean", "Safe"],
            cons=["Crowded"],
            is_published=True,
            moderated=True,
        )

    def test_pages_render_successfully(self):
        pages = [
            reverse('index'),
            reverse('safety_intelligence'),
            reverse('safety_intelligence_dest', args=['Rajahmundry']),
            reverse('women_safety'),
            reverse('verified_hotels'),
            reverse('emergency_map'),
            reverse('ai_assistant'),
            reverse('trip_planner'),
            reverse('memory_maker'),
            reverse('memory_detail', args=[self.memory.id]),
            reverse('profile'),
            reverse('admin_dashboard'),
            reverse('tourism_packages'),
            reverse('package_detail', args=[self.package.slug]),
            reverse('customer_feedback'),
            reverse('post_trip_review'),
            reverse('reviews_by_destination', args=['Rajahmundry']),
        ]
        for url in pages:
            response = self.client.get(url)
            self.assertEqual(response.status_code, 200, f"Failed for url: {url}")

    def test_login_page_and_user_auth_flow(self):
        User = get_user_model()
        user = User.objects.create_user(username='demo', password='securepass123')

        client = Client()  # fresh anonymous session for the auth flow
        response = client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)

        response = client.post(reverse('login'), {
            'username': 'demo',
            'password': 'securepass123',
        }, follow=True)
        self.assertTrue(response.context['user'].is_authenticated)
        self.assertRedirects(response, reverse('profile'))

        response = client.post(reverse('logout'), follow=True)
        self.assertFalse(response.context['user'].is_authenticated)
        self.assertRedirects(response, reverse('index'))

    def test_destination_api(self):
        response = self.client.get(reverse('api_destinations'))
        self.assertEqual(response.status_code, 200)
        self.assertGreaterEqual(len(response.json()), 1)

    def test_safe_route_calculation(self):
        routes = calculate_safe_routes("Rajahmundry Station", "Dowleswaram Barrage", 16.9891, 81.7840)
        self.assertIn('routes', routes)
        self.assertEqual(len(routes['routes']), 3)
        # Check safer route has high safety score
        safer_route = next(r for r in routes['routes'] if r['id'] == 'safer')
        self.assertGreaterEqual(safer_route['safety_score'], 90)

    def test_sos_trigger_api(self):
        response = self.client.post(reverse('api_sos_trigger'), {
            'traveler_name': 'Test Traveler',
            'latitude': 16.9891,
            'longitude': 81.7840,
            'location_name': 'Pushkar Ghat'
        }, content_type='application/json')
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn('SOS_DISPATCHED', data['status'])
        self.assertIn('112', str(data['helplines']))

    def test_ai_story_generation(self):
        story = generate_travel_story(
            "My Day in Rajahmundry", "Rajahmundry", "Priya",
            ["Godavari River", "Dowleswaram Barrage"],
            ["Andhra Meals", "Pootharekulu"],
            ["Dowleswaram was built by Sir Arthur Cotton."],
            "Sunset at Godavari."
        )
        self.assertIn("Godavari", story)
        self.assertIn("Dowleswaram Barrage", story)
        self.assertIn("Pootharekulu", story)

    def test_pdf_export(self):
        response = self.client.get(reverse('export_memory_pdf', args=[self.memory.id]))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'application/pdf')
        self.assertTrue(response.has_header('Content-Disposition'))

    def test_welcome_intro_flow(self):
        """Landing page renders with the integrated intro animation overlay component."""
        fresh = Client()  # anonymous browser session
        response = fresh.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'yatralensIntroOverlay')
        self.assertContains(response, 'Explore YATRALENS')
        # Logged-in users also render the home page seamlessly
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Featured Tourism Packages')

    def test_ticket_pdf_export(self):
        """Paid bookings produce a downloadable e-Ticket PDF."""
        User = get_user_model()
        user = User.objects.create_user(username='ticketuser', password='securepass123')
        booking = Booking.objects.create(
            user=user,
            package=self.package,
            num_travelers=2,
            unit_price=self.package.price,
            total_amount=self.package.price * 2,
            status='Paid',
        )
        self.client.force_login(user)
        response = self.client.get(reverse('ticket_pdf', args=[booking.booking_ref]))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'application/pdf')
        self.assertTrue(response.has_header('Content-Disposition'))
        # Other users must not access the ticket
        stranger = User.objects.create_user(username='stranger', password='securepass123')
        self.client.force_login(stranger)
        response = self.client.get(reverse('ticket_pdf', args=[booking.booking_ref]))
        self.assertEqual(response.status_code, 404)

    def test_ai_trip_planner(self):
        itinerary = generate_smart_itinerary("Rajahmundry", 2, 5000, "Solo Woman", "Culture")
        self.assertEqual(itinerary['destination'], "Rajahmundry")
        self.assertEqual(len(itinerary['days']), 2)
        self.assertIn("safety_summary", itinerary)

    # ===== YATRALENS New Feature Tests =====
    def test_tourism_package_api(self):
        response = self.client.get(reverse('api_packages'))
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertGreaterEqual(len(data), 1)
        self.assertEqual(data[0]['title'], 'Heritage Escape')

    def test_tourism_package_detail_api(self):
        response = self.client.get(reverse('api_package_detail', args=[self.package.slug]))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['title'], 'Heritage Escape')

    def test_crime_stats_api(self):
        response = self.client.get(reverse('api_crime_stats', args=['Rajahmundry']))
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn('destination', data)
        self.assertIn('crime_statistics', data)
        self.assertIn('trend_chart', data)
        # Validate trend chart structure
        self.assertIn('periods', data['trend_chart'])
        self.assertIn('crime_rates', data['trend_chart'])

    def test_crime_statistic_auto_calculation(self):
        """Verify that the CrimeStatistic.save() auto-computes total_cases and rate."""
        stat = CrimeStatistic.objects.create(
            destination=self.destination,
            period_label="Q2 2026",
            recorded_at=timezone.now().date(),
            theft_cases=5,
            harassment_cases=1,
            violent_crime_cases=1,
            other_cases=1,
            population_estimate=100000,
            data_source="Test",
        )
        self.assertEqual(stat.total_cases, 8)
        self.assertEqual(stat.crime_rate_per_100k, 8.0)  # 8 / 100000 * 100000

    def test_customer_feedback_submission(self):
        """Verify the customer feedback form creates entries."""
        response = self.client.post(reverse('customer_feedback'), {
            'name': 'Test Reviewer',
            'email': 'test@example.com',
            'category': 'General',
            'rating': 5,
            'subject': 'Great platform',
            'message': 'I love YATRALENS!',
            'contact_allowed': 'on',
        })
        self.assertEqual(response.status_code, 302)  # Redirect after success
        self.assertEqual(CustomerFeedback.objects.filter(name='Test Reviewer').count(), 1)

    def test_post_trip_review_submission(self):
        """Verify the post-trip review form creates entries."""
        response = self.client.post(reverse('post_trip_review'), {
            'destination': self.destination.id,
            'reviewer_name': 'New Reviewer',
            'traveler_type': 'Solo Woman',
            'overall_rating': '5',
            'safety_rating': '5',
            'value_rating': '4',
            'title': 'Amazing trip',
            'detailed_notes': 'Truly a once-in-a-lifetime experience.',
            'travel_tips': 'Go early!',
            'would_recommend': 'on',
        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(PostTripReview.objects.filter(reviewer_name='New Reviewer').count(), 1)

    def test_feedback_api(self):
        response = self.client.get(reverse('api_feedback'))
        self.assertEqual(response.status_code, 200)
        self.assertGreaterEqual(len(response.json()), 1)

    def test_feedback_stats_api(self):
        response = self.client.get(reverse('api_feedback_stats'))
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn('total_feedback', data)
        self.assertIn('average_rating', data)
        self.assertIn('rating_distribution', data)

    def test_reviews_api(self):
        response = self.client.get(reverse('api_reviews'))
        self.assertEqual(response.status_code, 200)
        data = response.json()
        # Should only return published + moderated reviews
        self.assertGreaterEqual(len(data), 1)
        self.assertTrue(all(r['is_published'] and r['moderated'] for r in data))

    def test_reviews_stats_api(self):
        response = self.client.get(reverse('api_reviews_stats'))
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIsInstance(data, list)
        self.assertGreaterEqual(len(data), 1)
        self.assertIn('destination', data[0])
        self.assertIn('avg_overall', data[0])

    def test_destination_model_crime_trend_icon(self):
        """Verify the crime_trend_icon property on Destination."""
        self.destination.crime_trend = 'Improving'
        self.assertEqual(self.destination.crime_trend_icon, '📉')
        self.destination.crime_trend = 'Deteriorating'
        self.assertEqual(self.destination.crime_trend_icon, '📈')
        self.destination.crime_trend = 'Stable'
        self.assertEqual(self.destination.crime_trend_icon, '➖')

    def test_tourism_package_price_per_day(self):
        self.assertEqual(self.package.price_per_day, 2750.0)

    def test_post_trip_review_average_rating(self):
        self.assertEqual(self.review.average_rating, 4.5)

    def test_booking_with_multiple_travelers_and_manifest_pdf(self):
        """Test booking flow with multiple travelers, verifying travelers_data and PDF export."""
        User = get_user_model()
        user = User.objects.create_user(username='manifestuser', password='securepass123')
        self.client.force_login(user)

        response = self.client.post(reverse('booking', args=[self.package.slug]), {
            'num_travelers': '2',
            'travel_date': '2026-10-15',
            'contact_email': 'manifestuser@example.com',
            'contact_phone': '+91 9876543210',
            'special_requests': 'Wheelchair assistance requested',
            'traveler_name_0': 'Aarohi Reddy',
            'traveler_age_0': '28',
            'traveler_gender_0': 'Female',
            'traveler_id_type_0': 'Aadhaar Card',
            'traveler_id_number_0': '1234-5678-9012',
            'traveler_diet_0': 'Vegetarian',
            'traveler_phone_0': '+91 9876543210',
            'traveler_name_1': 'Priya Reddy',
            'traveler_age_1': '24',
            'traveler_gender_1': 'Female',
            'traveler_id_type_1': 'Passport',
            'traveler_id_number_1': 'K1234567',
            'traveler_diet_1': 'Jain Meal',
            'traveler_phone_1': '+91 9876543211',
        })
        self.assertEqual(response.status_code, 302)
        booking = Booking.objects.filter(user=user).first()
        self.assertIsNotNone(booking)
        self.assertEqual(booking.num_travelers, 2)
        self.assertEqual(len(booking.travelers_data), 2)
        self.assertEqual(booking.travelers_data[0]['name'], 'Aarohi Reddy')
        self.assertEqual(booking.travelers_data[1]['id_type'], 'Passport')
        self.assertEqual(booking.special_requests, 'Wheelchair assistance requested')

        # Simulate payment success
        booking.status = 'Paid'
        booking.save()

        # Test PDF export with manifest table
        pdf_res = self.client.get(reverse('ticket_pdf', args=[booking.booking_ref]))
        self.assertEqual(pdf_res.status_code, 200)
        self.assertEqual(pdf_res['Content-Type'], 'application/pdf')

    def test_user_memory_creation_and_profile(self):
        """Test creating a memory tied to a user and viewing it on the profile."""
        User = get_user_model()
        user = User.objects.create_user(username='memoryuser', password='securepass123')
        self.client.force_login(user)

        # Create memory via POST to memory_maker
        response = self.client.post(reverse('memory_maker'), {
            'title': 'Sunset at Pushkar Ghat',
            'destination': 'Rajahmundry',
            'traveler_name': 'Memory User',
            'traveler_type': 'Solo Woman Traveler',
            'travel_date': '2026-09-01',
            'favorite_moment': 'Aarti ceremony on the riverbanks.',
            'visited_places': ['Godavari River', 'Kotilingala Ghat'],
            'food_tried': ['Andhra Thali'],
        })
        self.assertEqual(response.status_code, 302)
        memory = TravelMemory.objects.filter(user=user, title='Sunset at Pushkar Ghat').first()
        self.assertIsNotNone(memory)
        self.assertEqual(memory.user, user)

        # View profile and verify memory is displayed
        profile_res = self.client.get(reverse('profile'))
        self.assertEqual(profile_res.status_code, 200)
        self.assertContains(profile_res, 'Sunset at Pushkar Ghat')
        self.assertContains(profile_res, 'Rajahmundry')

        # Delete memory
        del_res = self.client.post(reverse('delete_memory', args=[memory.id]))
        self.assertEqual(del_res.status_code, 302)
        self.assertFalse(TravelMemory.objects.filter(id=memory.id).exists())

    def test_erss_112_cad_sos_trigger(self):
        """Test the real Government ERSS 112 CAD SOS trigger endpoint."""
        response = self.client.post(reverse('api_sos_trigger'), {
            'traveler_name': 'Aarohi Reddy',
            'latitude': 16.9891,
            'longitude': 81.7840,
            'location_name': 'Godavari Pushkar Ghat, Rajahmundry',
            'phone': '+91 98765 43210',
            'emergency_contact': '+91 98765 00000',
            'battery_level': 82
        }, content_type='application/json')
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data['status'], 'SOS_DISPATCHED_ERSS_112')
        self.assertTrue(data['cad_reference_id'].startswith('ERSS-112-IN-'))
        self.assertIn('whatsapp_sos_url', data)
        self.assertIn('sms_sos_url', data)
        self.assertIn('cad_dispatch', data)
        self.assertIn('assigned_jurisdiction', data['cad_dispatch'])
        self.assertEqual(data['cad_dispatch']['assigned_jurisdiction']['police_station'], 'Rajahmundry I Town Police Station (Control Division)')

    def test_erss_cad_status_update(self):
        """Test updating CAD status by law enforcement/authority."""
        from .models import GovernmentDispatchLog
        log = GovernmentDispatchLog.objects.create(
            cad_reference_id="ERSS-112-IN-TEST-001",
            traveler_name="Test Traveler",
            latitude=16.9891,
            longitude=81.7840,
            dispatch_status="DISPATCHED_TO_PCR"
        )
        # Update to PCR_EN_ROUTE
        res = self.client.post(reverse('api_erss_cad_status', args=[log.cad_reference_id]), {
            'status': 'PCR_EN_ROUTE'
        }, content_type='application/json')
        self.assertEqual(res.status_code, 200)
        log.refresh_from_db()
        self.assertEqual(log.dispatch_status, 'PCR_EN_ROUTE')

    def test_offline_sos_sync_api(self):
        """Test syncing offline queued emergency alerts."""
        res = self.client.post(reverse('api_offline_sync_sos'), {
            'id': 'OFFLINE-SOS-9999',
            'timestamp': '2026-09-02T18:00:00Z',
            'traveler_name': 'Offline Solo Explorer',
            'latitude': 16.9891,
            'longitude': 81.7840,
            'battery_level': 75
        }, content_type='application/json')
        self.assertEqual(res.status_code, 201)
        data = res.json()
        self.assertEqual(data['status'], 'OFFLINE_SOS_SYNCED')
        self.assertTrue(data['cad_reference_id'].startswith('ERSS-112-IN-'))

    def test_emergency_offline_bundle_api(self):
        """Test fetching the offline emergency data bundle for Service Worker caching."""
        res = self.client.get(reverse('api_emergency_offline_bundle'))
        self.assertEqual(res.status_code, 200)
        data = res.json()
        self.assertIn('national_helplines', data)
        self.assertIn('jurisdictions', data)
        self.assertIn('services', data)
        self.assertIn('destinations', data)

    def test_pwa_manifest_and_sw_views(self):
        """Test PWA manifest, service worker, and offline hub endpoints."""
        manifest_res = self.client.get(reverse('manifest_json'))
        self.assertEqual(manifest_res.status_code, 200)
        self.assertIn('application/manifest+json', manifest_res['Content-Type'])

        sw_res = self.client.get(reverse('service_worker'))
        self.assertEqual(sw_res.status_code, 200)
        self.assertIn('application/javascript', sw_res['Content-Type'])

        offline_res = self.client.get(reverse('offline_hub'))
        self.assertEqual(offline_res.status_code, 200)
        self.assertContains(offline_res, 'Offline Emergency Hub')
