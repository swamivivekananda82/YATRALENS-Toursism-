from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse
from django.utils import timezone
from datetime import timedelta
from .models import Destination, SafetyZone, VerifiedHotel, EmergencyService, TravelMemory, LiveShareSession
from .models import TourismPackage, CustomerFeedback, PostTripReview, CrimeStatistic
from .ai_service import generate_travel_story, generate_smart_itinerary, ai_travel_assistant_reply, calculate_safe_routes

class SafeTripCoreTests(TestCase):
    def setUp(self):
        self.client = Client()
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

        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)

        response = self.client.post(reverse('login'), {
            'username': 'demo',
            'password': 'securepass123',
        }, follow=True)
        self.assertTrue(response.context['user'].is_authenticated)
        self.assertRedirects(response, reverse('profile'))

        response = self.client.post(reverse('logout'), follow=True)
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
        self.assertEqual(data['status'], 'SOS_DISPATCHED')
        self.assertIn('112', data['helplines']['national_emergency'])

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
