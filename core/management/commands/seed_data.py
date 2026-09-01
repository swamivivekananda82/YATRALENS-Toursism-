from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
from core.models import (
    Destination, SafetyZone, Attraction, VerifiedHotel,
    EmergencyService, SafetyAlert, LiveShareSession,
    TravelMemory, IncidentReport,
    TourismPackage, CustomerFeedback, PostTripReview, CrimeStatistic
)

class Command(BaseCommand):
    help = "Seeds comprehensive tourism safety and memory data for SafeTrip Memories"

    def handle(self, *args, **options):
        self.stdout.write("Starting database seeding...")

        # Clear existing data
        Destination.objects.all().delete()
        SafetyZone.objects.all().delete()
        Attraction.objects.all().delete()
        VerifiedHotel.objects.all().delete()
        EmergencyService.objects.all().delete()
        SafetyAlert.objects.all().delete()
        LiveShareSession.objects.all().delete()
        TravelMemory.objects.all().delete()
        IncidentReport.objects.all().delete()
        TourismPackage.objects.all().delete()
        CustomerFeedback.objects.all().delete()
        PostTripReview.objects.all().delete()
        CrimeStatistic.objects.all().delete()

        # 1. DESTINATION: RAJAHMUNDRY (Primary Focus)
        rjy = Destination.objects.create(
            name="Rajahmundry",
            state="Andhra Pradesh",
            tagline="Cultural Capital of Andhra Pradesh & Holy Godavari City",
            description="Perched majestically on the banks of the sacred Godavari River, Rajahmundry is the cultural heartland of Andhra Pradesh. Renowned for its magnificent bridges, historic Dowleswaram Barrage, vibrant river ghats, ancient temples, and exquisite traditional cuisine.",
            latitude=16.9891,
            longitude=81.7840,
            safety_score=82,
            risk_level="Low Risk",
            crime_rate_index=14.2,
            theft_reports=9,
            harassment_reports=1,
            violent_crime_reports=1,
            crime_data_source="Real-Time",
            last_crime_update=timezone.now() - timedelta(hours=4),
            crime_trend="Improving",
            theft_change_pct=-12.5,
            harassment_change_pct=-25.0,
            night_safety_score=84,
            tourist_density="High Density",
            emergency_accessibility_score=92,
            police_accessibility_score=90,
            hospital_accessibility_score=94,
            accident_prone_areas="Caution on narrow turns near the old canal bypass road after 9:30 PM. River steps can be slippery during high tide.",
            image_url="https://images.unsplash.com/photo-1627894006066-b4578896085a?auto=format&fit=crop&w=1200&q=80",
            banner_image_url="https://images.unsplash.com/photo-1544620347-c4fd4a3d5957?auto=format&fit=crop&w=1600&q=80",
            popular=True
        )

        # Safety Zones for Rajahmundry
        SafetyZone.objects.create(
            destination=rjy,
            name="Godavari Pushkar Ghat Tourist Zone",
            zone_type="Tourist Area",
            risk_level="Low Risk",
            latitude=16.9940,
            longitude=81.7780,
            radius_meters=700,
            lighting_status="100% LED Bright Illumination",
            police_patrol="24/7 Dedicated Tourist Police Outpost & Mobile Patrol",
            cctv_coverage="360° Smart City High-Definition CCTV Grid",
            safety_notes="Safest zone in the city. High tourist density, active evening pedestrian promenade, and frequent female police officer patrols."
        )

        SafetyZone.objects.create(
            destination=rjy,
            name="Dowleswaram Barrage & Cotton Museum Complex",
            zone_type="Tourist Area",
            risk_level="Low Risk",
            latitude=16.9400,
            longitude=81.7700,
            radius_meters=900,
            lighting_status="Well-Lit Public Park & Bridge Illumination",
            police_patrol="Regular Hourly Police Checkpoints",
            cctv_coverage="Monitored Entrance & Parking Security Cams",
            safety_notes="Excellent safety record. Park closes at 07:30 PM with private security and official tourism guards on duty."
        )

        SafetyZone.objects.create(
            destination=rjy,
            name="Main Bazaar & Stadium Market Area",
            zone_type="Main Market",
            risk_level="Moderate Risk",
            latitude=17.0010,
            longitude=81.7830,
            radius_meters=800,
            lighting_status="Commercial Bright Lighting until 10:00 PM",
            police_patrol="Foot Patrols by Local Police",
            cctv_coverage="Shop-front & Street Traffic CCTV",
            safety_notes="Heavy crowds during peak evening hours (05:00 PM - 08:30 PM). Keep wallets and phones secured from petty pickpockets."
        )

        SafetyZone.objects.create(
            destination=rjy,
            name="NH16 Highway Junction & Outskirt Corridor",
            zone_type="Highway Area",
            risk_level="Moderate Risk",
            latitude=17.0250,
            longitude=81.8100,
            radius_meters=1200,
            lighting_status="Moderate Sodium Highway Lighting",
            police_patrol="Highway Patrol Van (Vehicle 112)",
            cctv_coverage="Highway Toll & Speed Enforcement Cameras",
            safety_notes="Fast-moving intercity heavy vehicles. Solo travelers should use verified app cabs or registered auto-rickshaws when traversing at night."
        )

        SafetyZone.objects.create(
            destination=rjy,
            name="Old Canal Industrial Bypass Lane",
            zone_type="Isolated Area",
            risk_level="High Risk",
            latitude=16.9650,
            longitude=81.7600,
            radius_meters=600,
            lighting_status="Dim / Intermittent Street Lights",
            police_patrol="Night Periodic Patrol Only",
            cctv_coverage="Low / Sparse Coverage",
            safety_notes="Isolated industrial and canal road with minimal pedestrian traffic after 09:00 PM. SafeTrip navigation automatically re-routes travelers along the main bund arterial road."
        )

        # Attractions for Rajahmundry
        Attraction.objects.create(
            destination=rjy,
            name="Dowleswaram Barrage & Sir Arthur Cotton Museum",
            category="Historical",
            latitude=16.9400,
            longitude=81.7700,
            description="A monumental irrigation marvel spanning across the Godavari river, built under the guidance of British engineer Sir Arthur Cotton, featuring panoramic river views and a rich museum.",
            historical_fact="Engineered between 1847 and 1852 by Sir Arthur Cotton, this 3.6-kilometer barrage transformed the drought-hit Godavari delta into the prosperous 'Rice Bowl of Andhra Pradesh'.",
            best_visiting_hours="08:00 AM - 06:30 PM",
            safety_rating=4.9,
            women_safety_certified=True,
            entry_fee="₹30 (Museum)",
            image_url="https://images.unsplash.com/photo-1544620347-c4fd4a3d5957?auto=format&fit=crop&w=800&q=80"
        )

        Attraction.objects.create(
            destination=rjy,
            name="Godavari Pushkar Ghat & Riverfront Promenade",
            category="Riverfront & Nature",
            latitude=16.9940,
            longitude=81.7780,
            description="The premier spiritual and recreational riverfront of Rajahmundry with wide bathing ghats, evening arti ceremonies, and boating docks.",
            historical_fact="One of the holiest riverfronts in India, host to the grand Godavari Maha Pushkaram which occurs once every 144 years and regular Pushkaram every 12 years.",
            best_visiting_hours="05:30 AM - 08:30 PM",
            safety_rating=4.9,
            women_safety_certified=True,
            entry_fee="Free",
            image_url="https://images.unsplash.com/photo-1506744038136-46273834b3fb?auto=format&fit=crop&w=800&q=80"
        )

        Attraction.objects.create(
            destination=rjy,
            name="Sri Markandeyeshwara Swamy Temple",
            category="Temple & Culture",
            latitude=16.9910,
            longitude=81.7820,
            description="An ancient temple dedicated to Lord Shiva, celebrated for its Dravidian architectural stone carvings and spiritual sanctity.",
            historical_fact="Excavated from ruins in 1818, archaeological research links this temple to centuries of Chola and Eastern Chalukya patronage.",
            best_visiting_hours="06:00 AM - 12:00 PM, 04:30 PM - 08:00 PM",
            safety_rating=4.7,
            women_safety_certified=True,
            entry_fee="Free (Special Darshan ₹50)",
            image_url="https://images.unsplash.com/photo-1582510003544-4d00b7f74220?auto=format&fit=crop&w=800&q=80"
        )

        Attraction.objects.create(
            destination=rjy,
            name="ISKCON Temple (Gautami Ghat)",
            category="Temple & Culture",
            latitude=16.9850,
            longitude=81.7750,
            description="South India's prominent ISKCON campus located on the banks of Gautami Godavari, featuring serene landscaped gardens and Vedic heritage dioramas.",
            historical_fact="Built over a two-acre serene site where saint Sri Chaitanya Mahaprabhu met Ramananda Raya during his historic pilgrimage to the South.",
            best_visiting_hours="07:30 AM - 01:00 PM, 04:00 PM - 08:30 PM",
            safety_rating=5.0,
            women_safety_certified=True,
            entry_fee="Free",
            image_url="https://images.unsplash.com/photo-1609766857041-ed402ea8069a?auto=format&fit=crop&w=800&q=80"
        )

        Attraction.objects.create(
            destination=rjy,
            name="Papikondalu River Cruise Gateway",
            category="Eco-Tourism",
            latitude=17.0200,
            longitude=81.7500,
            description="The gateway for world-famous river cruises sailing through the breathtaking gorge of Papikondalu hills on the Godavari river.",
            historical_fact="The name Papikondalu originates from the Telugu word 'Paidi Kondalu' (hills that resemble a woman's hair partition), celebrated in classic Telugu literature.",
            best_visiting_hours="06:00 AM - 05:00 PM (Pre-booked cruise)",
            safety_rating=4.8,
            women_safety_certified=True,
            entry_fee="₹850 - ₹1,500 (Full Day Boat Package)",
            image_url="https://images.unsplash.com/photo-1507525428034-b723cf961d3e?auto=format&fit=crop&w=800&q=80"
        )

        # Verified Hotels for Rajahmundry
        VerifiedHotel.objects.create(
            destination=rjy,
            name="SafeStay Godavari Grand Residency",
            rating=4.7,
            price_range="₹2,600 - ₹4,200/night",
            verified=True,
            women_friendly=True,
            reception_24_7=True,
            cctv_security=True,
            dist_city_center=0.8,
            dist_police_station=0.6,
            dist_hospital=1.1,
            latitude=16.9920,
            longitude=81.7810,
            contact_number="+91 883 245 9901",
            address="Main Bund Road, Near Pushkar Ghat, Rajahmundry",
            amenities="24/7 Security Guard, Verified Female Staff, Keycard Access, In-room Safety Locker, Free Wi-Fi, Emergency Doctor on Call",
            image_url="https://images.unsplash.com/photo-1566073771259-6a8506099945?auto=format&fit=crop&w=800&q=80"
        )

        VerifiedHotel.objects.create(
            destination=rjy,
            name="RiverBay Luxury Resort & Suites",
            rating=4.6,
            price_range="₹3,400 - ₹5,800/night",
            verified=True,
            women_friendly=True,
            reception_24_7=True,
            cctv_security=True,
            dist_city_center=1.5,
            dist_police_station=0.9,
            dist_hospital=1.4,
            latitude=16.9830,
            longitude=81.7760,
            contact_number="+91 883 247 8888",
            address="Gautami Ghat Road, Morampudi Junction, Rajahmundry",
            amenities="Riverside Dining, 24/7 CCTV Surveillance, Safe Airport/Station Cab Transfer, Female Guest Concierge Desk",
            image_url="https://images.unsplash.com/photo-1582719478250-c89cae4dc85b?auto=format&fit=crop&w=800&q=80"
        )

        VerifiedHotel.objects.create(
            destination=rjy,
            name="Royal Fort SafeStay Hotel",
            rating=4.5,
            price_range="₹1,800 - ₹2,900/night",
            verified=True,
            women_friendly=True,
            reception_24_7=True,
            cctv_security=True,
            dist_city_center=0.5,
            dist_police_station=0.4,
            dist_hospital=0.8,
            latitude=16.9960,
            longitude=81.7850,
            contact_number="+91 883 246 1122",
            address="Station Road, Opp. Central Plaza, Rajahmundry",
            amenities="Rapid Check-in, 24/7 Reception, Safe Luggage Vault, CCTV on Every Floor, Solo Traveler Verified",
            image_url="https://images.unsplash.com/photo-1542314831-068cd1dbfeeb?auto=format&fit=crop&w=800&q=80"
        )

        # Emergency Services for Rajahmundry
        EmergencyService.objects.create(
            destination=rjy,
            name="Rajahmundry Central Police Station",
            service_type="Police",
            phone="0883-2471033",
            latitude=16.9930,
            longitude=81.7820,
            address="Station Road, Near Town Hall, Rajahmundry",
            is_24_7=True,
            distance_km=0.6
        )

        EmergencyService.objects.create(
            destination=rjy,
            name="Women Safety Police Station & Disha Helpdesk",
            service_type="Police",
            phone="1091 / 0883-2471090",
            latitude=16.9915,
            longitude=81.7805,
            address="Pushkar Ghat Circle, Rajahmundry",
            is_24_7=True,
            distance_km=0.7
        )

        EmergencyService.objects.create(
            destination=rjy,
            name="Government General Hospital & Trauma Center",
            service_type="Hospital",
            phone="0883-2473456",
            latitude=16.9880,
            longitude=81.7890,
            address="Hospital Road, Danavaipeta, Rajahmundry",
            is_24_7=True,
            distance_km=1.2
        )

        EmergencyService.objects.create(
            destination=rjy,
            name="Apollo 24/7 Pharmacy & Emergency Care",
            service_type="Pharmacy",
            phone="0883-2422244",
            latitude=16.9950,
            longitude=81.7835,
            address="Main Road, Near Syamala Theater, Rajahmundry",
            is_24_7=True,
            distance_km=0.5
        )

        EmergencyService.objects.create(
            destination=rjy,
            name="108 Emergency Ambulance Pushkar Station",
            service_type="Ambulance",
            phone="108",
            latitude=16.9945,
            longitude=81.7785,
            address="Pushkar Ghat Parking Area, Rajahmundry",
            is_24_7=True,
            distance_km=0.4
        )

        EmergencyService.objects.create(
            destination=rjy,
            name="HP 24/7 Smart Fuel & EV Fast Charger",
            service_type="Fuel",
            phone="0883-2457890",
            latitude=17.0020,
            longitude=81.7870,
            address="Morampudi Road, Rajahmundry",
            is_24_7=True,
            distance_km=0.9
        )

        # 2. OTHER MAJOR INDIAN DESTINATIONS
        jaipur = Destination.objects.create(
            name="Jaipur",
            state="Rajasthan",
            tagline="The Royal Pink City & UNESCO World Heritage Landmark",
            description="Famous for majestic palaces, rugged hill forts, vibrant pink-hued architecture, and rich Rajasthani royal history.",
            latitude=26.9124,
            longitude=75.7873,
            safety_score=86,
            risk_level="Low Risk",
            crime_rate_index=16.0,
            theft_reports=14,
            harassment_reports=2,
            violent_crime_reports=2,
            crime_data_source="Real-Time",
            last_crime_update=timezone.now() - timedelta(hours=6),
            crime_trend="Stable",
            theft_change_pct=2.1,
            harassment_change_pct=0.0,
            night_safety_score=88,
            tourist_density="Very High Density",
            emergency_accessibility_score=94,
            police_accessibility_score=92,
            hospital_accessibility_score=95,
            accident_prone_areas="Caution in narrow crowded lanes of Johari Bazaar during peak festive season.",
            image_url="https://images.unsplash.com/photo-1599661046289-e31897846e41?auto=format&fit=crop&w=1200&q=80",
            popular=True
        )

        goa = Destination.objects.create(
            name="Goa",
            state="Goa",
            tagline="Sun, Sand, Serenity & Portuguese Heritage",
            description="India's celebrated tropical paradise featuring golden beaches, historic churches, lively flea markets, and safe coastal tourism corridors.",
            latitude=15.2993,
            longitude=74.1240,
            safety_score=88,
            risk_level="Low Risk",
            crime_rate_index=12.5,
            theft_reports=10,
            harassment_reports=1,
            violent_crime_reports=1,
            crime_data_source="Real-Time",
            last_crime_update=timezone.now() - timedelta(hours=2),
            crime_trend="Improving",
            theft_change_pct=-8.0,
            harassment_change_pct=-10.0,
            night_safety_score=90,
            tourist_density="High Density",
            emergency_accessibility_score=90,
            police_accessibility_score=89,
            hospital_accessibility_score=91,
            accident_prone_areas="Caution on coastal scooter curves between Calangute and Anjuna after midnight.",
            image_url="https://images.unsplash.com/photo-1512343879784-a960bf40e7f2?auto=format&fit=crop&w=1200&q=80",
            popular=True
        )

        varanasi = Destination.objects.create(
            name="Varanasi",
            state="Uttar Pradesh",
            tagline="The Spiritual Capital of India & Sacred Ganga Ghats",
            description="One of the world's oldest continuously inhabited cities, world-famous for holy Ganga Aarti, ancient alleyways, and silk weaving.",
            latitude=25.3176,
            longitude=82.9739,
            safety_score=78,
            risk_level="Moderate Risk",
            crime_rate_index=19.4,
            theft_reports=22,
            harassment_reports=3,
            violent_crime_reports=2,
            crime_data_source="Statistical",
            last_crime_update=timezone.now() - timedelta(days=7),
            crime_trend="Deteriorating",
            theft_change_pct=8.5,
            harassment_change_pct=12.0,
            night_safety_score=76,
            tourist_density="Extremely High Density",
            emergency_accessibility_score=86,
            police_accessibility_score=85,
            hospital_accessibility_score=88,
            accident_prone_areas="Congested ghat alleys and unguided evening boat boarding zones.",
            image_url="https://images.unsplash.com/photo-1561361513-2d000a50f0dc?auto=format&fit=crop&w=1200&q=80",
            popular=True
        )

        mysore = Destination.objects.create(
            name="Mysore",
            state="Karnataka",
            tagline="City of Royal Palaces, Sandalwood & Silk",
            description="A clean, green heritage city known for the grand Mysore Palace, Chamundi Hill, vibrant Devaraja Market, and rich heritage arts.",
            latitude=12.2958,
            longitude=76.6394,
            safety_score=91,
            risk_level="Low Risk",
            crime_rate_index=9.8,
            theft_reports=6,
            harassment_reports=0,
            violent_crime_reports=0,
            crime_data_source="Real-Time",
            last_crime_update=timezone.now() - timedelta(hours=3),
            crime_trend="Improving",
            theft_change_pct=-15.0,
            harassment_change_pct=-50.0,
            night_safety_score=92,
            tourist_density="Moderate to High",
            emergency_accessibility_score=95,
            police_accessibility_score=94,
            hospital_accessibility_score=96,
            accident_prone_areas="Minor congestion near Suburban Bus Stand during Dasara.",
            image_url="https://images.unsplash.com/photo-1600100397608-f010e42e12a6?auto=format&fit=crop&w=1200&q=80",
            popular=True
        )

        # 3. SAFETY ALERTS
        SafetyAlert.objects.create(
            title="Safe Corridor Active: Godavari Pushkar Ghat",
            alert_type="Safety Alert",
            message="Additional female police personnel and illuminated helpdesks stationed at Pushkar Ghat for evening riverfront visitors.",
            severity="Low",
            destination=rjy,
            is_active=True
        )

        SafetyAlert.objects.create(
            title="Pleasant River Breeze & Sunny Climate",
            alert_type="Weather Warning",
            message="Optimal sightseeing conditions across Rajahmundry. Clear skies with cool evening breeze along the Godavari bank.",
            severity="Low",
            destination=rjy,
            is_active=True
        )

        # 4. PRE-SEEDED TRAVEL MEMORY
        TravelMemory.objects.create(
            title="🌅 My Day in Rajahmundry",
            destination="Rajahmundry",
            traveler_name="Aarohi Reddy",
            traveler_type="Solo Woman Traveler",
            places_visited=[
                "Godavari River & Pushkar Ghat",
                "Dowleswaram Barrage & Sir Arthur Cotton Museum",
                "Sri Markandeyeshwara Swamy Temple",
                "ISKCON Gautami Ghat"
            ],
            food_tried=[
                "Authentic Andhra Vegetarian Thali with Gongura Pachadi",
                "Atreyapuram Ghee Pootharekulu",
                "Godavari Fresh Filter Coffee"
            ],
            historical_facts=[
                "Dowleswaram Barrage was engineered by Sir Arthur Cotton across the Godavari River, transforming the delta into India's green heartland.",
                "Rajahmundry Pushkar Ghat is revered as one of the oldest riverfront pilgrimage centers in India dating back centuries."
            ],
            favorite_moment="Standing by the massive Dowleswaram Barrage watching the sun melt into the sacred Godavari River while feeling completely safe and independent.",
            photos=[
                {
                    "url": "https://images.unsplash.com/photo-1627894006066-b4578896085a?auto=format&fit=crop&w=800&q=80",
                    "caption": "Golden sunset reflections over the majestic Godavari River",
                    "time": "06:15 PM",
                    "location": "Pushkar Ghat, Rajahmundry"
                },
                {
                    "url": "https://images.unsplash.com/photo-1544620347-c4fd4a3d5957?auto=format&fit=crop&w=800&q=80",
                    "caption": "Dowleswaram Barrage - A marvel of 19th century hydraulic engineering",
                    "time": "03:45 PM",
                    "location": "Dowleswaram, Rajahmundry"
                },
                {
                    "url": "https://images.unsplash.com/photo-1582510003544-4d00b7f74220?auto=format&fit=crop&w=800&q=80",
                    "caption": "Sacred calmness and Dravidian stone architecture at Markandeyeshwara Temple",
                    "time": "11:20 AM",
                    "location": "Temple Street, Rajahmundry"
                }
            ],
            generated_story=(
                "My journey began along the beautiful Godavari River. I visited Dowleswaram Barrage and explored the local attractions. "
                "I enjoyed traditional Andhra food including authentic Gongura pachadi and mouth-watering Atreyapuram Pootharekulu, "
                "and captured several memorable moments throughout the day.\n\n"
                "Standing by the massive Dowleswaram Barrage watching the sun melt into the sacred Godavari River was my favorite moment. "
                "The live safety tracking and verified safe routes provided me with the ultimate peace of mind as a solo woman traveler."
            )
        )

        # 5. LIVE SHARE SESSION
        LiveShareSession.objects.create(
            session_token="share-mom-rjy-2026",
            traveler_name="Priya Sharma",
            trusted_contact_name="Mom (Mrs. Sunita Sharma)",
            trusted_contact_phone="+91 98765 43210",
            current_location_name="Godavari Pushkar Ghat Promenade, Rajahmundry",
            current_latitude=16.9940,
            current_longitude=81.7780,
            battery_level=86,
            status="Active"
        )

        # =====================================================================
        # 6. CRIME STATISTICS — Historical & real-time trend data per destination
        # =====================================================================
        today = timezone.now().date()
        crime_periods = [
            ("Q1 2025", today.replace(month=3, day=31)),
            ("Q2 2025", today.replace(month=6, day=30)),
            ("Q3 2025", today.replace(month=9, day=30)),
            ("Q4 2025", today.replace(month=12, day=31)),
            ("Q1 2026", today.replace(month=3, day=31) if today.month >= 3 else today.replace(year=today.year-1, month=3, day=31)),
            ("Q2 2026", today.replace(month=6, day=30) if today.month >= 6 else today.replace(year=today.year-1, month=6, day=30)),
        ]

        # Crime profiles per destination
        crime_profiles = {
            rjy:  [(12, 3, 2, 1), (10, 2, 1, 1), (9, 2, 1, 0), (8, 1, 1, 0), (7, 1, 0, 0), (5, 1, 0, 0)],
            jaipur:[(18, 4, 3, 1), (16, 3, 2, 1), (15, 3, 2, 1), (14, 2, 2, 1), (13, 2, 1, 1), (12, 2, 1, 1)],
            goa:   [(15, 3, 2, 0), (12, 2, 2, 0), (11, 2, 1, 0), (10, 1, 1, 0), (9, 1, 0, 0), (7, 1, 0, 0)],
            varanasi:[(25, 6, 4, 2), (23, 5, 3, 2), (22, 4, 3, 1), (21, 3, 2, 1), (20, 3, 2, 1), (18, 2, 1, 1)],
            mysore:[(8, 1, 1, 0), (7, 1, 0, 0), (6, 0, 0, 0), (5, 0, 0, 0), (4, 0, 0, 0), (3, 0, 0, 0)],
        }

        for dest, profile in crime_profiles.items():
            for (label, dt), (theft, harass, violent, other) in zip(crime_periods, profile):
                CrimeStatistic.objects.create(
                    destination=dest,
                    period_label=label,
                    recorded_at=dt,
                    theft_cases=theft,
                    harassment_cases=harass,
                    violent_crime_cases=violent,
                    other_cases=other,
                    population_estimate=350000,
                    data_source="Local Police Records" if dest != rjy else "Smart City Surveillance + Police Records",
                    notes=f"{label} aggregate crime data for {dest.name}.",
                )

        # =====================================================================
        # 7. TOURISM PACKAGES — Curated experiences across destinations
        # =====================================================================
        TourismPackage.objects.create(
            title="Godavari Heritage & Sacred Ghats — 2 Day Escape",
            slug="godavari-heritage-2d",
            subtitle="Explore Rajahmundry's iconic riverfront, ancient temples, and engineering marvels in 2 curated days.",
            description=(
                "A premium 2-day cultural escape that takes you through the soul of Rajahmundry — from the sacred "
                "Pushkar Ghat and majestic Dowleswaram Barrage to ancient Dravidian temples and the ISKCON riverside. "
                "Includes verified safe stays, escorted sightseeing, and authentic Andhra cuisine."
            ),
            package_type="Cultural",
            destination=rjy,
            price=5499,
            duration_days=2,
            rating=4.8,
            review_count=128,
            highlights=[
                "Sunset boat ride on the Godavari",
                "Dowleswaram Barrage & Cotton Museum",
                "ISKCON riverside darshan",
                "Authentic Andhra thali lunch",
            ],
            inclusions=[
                "1 night at a verified SafeStay hotel",
                "Daily breakfast & 1 traditional thali lunch",
                "AC transport for all sightseeing",
                "Licensed tour escort & entry fees",
                "YATRALENS SOS & live-share access",
            ],
            exclusions=[
                "Personal expenses & tips",
                "Travel insurance (recommended)",
                "Camera fees at monuments",
            ],
            itinerary_summary=[
                {"theme": "Godavari Heritage Tour", "description": "Pushkar Ghat → Markandeyeshwara Temple → Sunset boat ride"},
                {"theme": "Engineering Marvel & Culture", "description": "Dowleswaram Barrage → ISKCON → Pootharekulu shopping"},
            ],
            image_url="https://images.unsplash.com/photo-1627894006066-b4578896085a?auto=format&fit=crop&w=1200&q=80",
            is_featured=True,
            is_available=True,
            max_group_size=8,
            age_from=10,
            age_to=70,
            difficulty="Easy",
        )

        TourismPackage.objects.create(
            title="Pink City Royal Weekend — 3 Days in Jaipur",
            slug="pink-city-weekend-3d",
            subtitle="A curated 3-day royal experience through majestic forts, palaces, and bazaars of Jaipur.",
            description=(
                "Step into royalty with our 3-day Jaipur package — Hawa Mahal, Amber Fort, City Palace, and a curated "
                "bazaar experience. Verified women-friendly hotels, royal Rajasthani dinners, and cultural evenings included."
            ),
            package_type="Weekend",
            destination=jaipur,
            price=12500,
            duration_days=3,
            rating=4.7,
            review_count=243,
            highlights=[
                "Amber Fort evening light show",
                "Hawa Mahal & City Palace guided tour",
                "Traditional Rajasthani thali dinner",
                "Johari Bazaar shopping experience",
            ],
            inclusions=[
                "2 nights at a verified heritage hotel",
                "Daily breakfast + 2 traditional dinners",
                "AC transport & licensed guide",
                "All monument entry fees",
            ],
            exclusions=["Personal shopping", "Travel to/from Jaipur"],
            itinerary_summary=[
                {"theme": "Royal Arrival & Pink City Walk", "description": "Hawa Mahal → City Palace → Bapu Bazaar"},
                {"theme": "Amber Fort & Nahargarh Sunset", "description": "Amber Fort → Jal Mahal → Nahargarh"},
                {"theme": "Cultural Morning & Departure", "description": "Albert Hall → shopping → departure"},
            ],
            image_url="https://images.unsplash.com/photo-1599661046289-e31897846e41?auto=format&fit=crop&w=1200&q=80",
            is_featured=True,
            is_available=True,
            max_group_size=10,
            age_from=8,
            age_to=75,
            difficulty="Easy",
        )

        TourismPackage.objects.create(
            title="Goa Coastal Serenity — 4 Day Beach Retreat",
            slug="goa-coastal-4d",
            subtitle="Sun, sand, and Portuguese heritage with verified beach-side stays.",
            description=(
                "A leisurely 4-day Goa retreat — from North Goa beaches to Old Goa churches. Includes a sunset "
                "cruise on the Mandovi, Portuguese culinary walk, and an evening at a beach shack."
            ),
            package_type="Luxury",
            destination=goa,
            price=18999,
            duration_days=4,
            rating=4.9,
            review_count=312,
            highlights=[
                "Beach sunset cruise",
                "Old Goa church heritage walk",
                "Spice plantation visit",
                "Beach shack dinner experience",
            ],
            inclusions=[
                "3 nights at a verified beach resort",
                "Daily breakfast + 2 specialty dinners",
                "Sunset cruise & spice plantation entry",
                "AC transport & travel desk support",
            ],
            exclusions=["Water sports (bookable on-site)", "Personal expenses"],
            itinerary_summary=[
                {"theme": "Beaches & Sunset Cruise", "description": "Calangute → Baga → Mandovi sunset cruise"},
                {"theme": "Old Goa Heritage", "description": "Basilica of Bom Jesus → Spice Plantation → Fontainhas"},
                {"theme": "Leisure & Water Sports", "description": "Free morning → optional water sports → beach shack"},
                {"theme": "Departure", "description": "Souvenir shopping → airport transfer"},
            ],
            image_url="https://images.unsplash.com/photo-1512343879784-a960bf40e7f2?auto=format&fit=crop&w=1200&q=80",
            is_featured=True,
            is_available=True,
            max_group_size=12,
            age_from=12,
            age_to=80,
            difficulty="Easy",
        )

        TourismPackage.objects.create(
            title="Mysore Royal Palace Weekend — 2 Day Heritage",
            slug="mysore-palace-2d",
            subtitle="A clean, green, heritage-rich weekend in the City of Palaces.",
            description=(
                "Mysore is one of India's safest and cleanest cities. This 2-day package covers the grand Mysore "
                "Palace, Chamundi Hills, Devaraja Market, and the famous Dasara illumination (seasonal)."
            ),
            package_type="Weekend",
            destination=mysore,
            price=6999,
            duration_days=2,
            rating=4.8,
            review_count=156,
            highlights=[
                "Mysore Palace guided tour",
                "Chamundi Hills sunset",
                "Devaraja Market walk",
                "Mysore Pak tasting",
            ],
            inclusions=[
                "1 night at a verified heritage hotel",
                "Daily breakfast + royal lunch",
                "AC transport & licensed guide",
                "Palace entry & museum tickets",
            ],
            exclusions=["Personal shopping", "Camera fees"],
            itinerary_summary=[
                {"theme": "Palace & Heritage Walk", "description": "Mysore Palace → Jaganmohana → Devaraja Market"},
                {"theme": "Chamundi Hills & Departure", "description": "Chamundi Hills → St. Philomena's → Mysore Pak"},
            ],
            image_url="https://images.unsplash.com/photo-1600100397608-f010e42e12a6?auto=format&fit=crop&w=1200&q=80",
            is_featured=True,
            is_available=True,
            max_group_size=8,
            age_from=6,
            age_to=80,
            difficulty="Easy",
        )

        TourismPackage.objects.create(
            title="Spiritual Varanasi — 3 Day Ganga Aarti Experience",
            slug="spiritual-varanasi-3d",
            subtitle="A guided spiritual journey through the ghats and alleys of India's oldest living city.",
            description=(
                "Varanasi is intense and spiritual. This 3-day package includes sunrise boat rides on the Ganga, "
                "evening aarti at Dashashwamedh Ghat, Sarnath excursion, and silk-weaving workshop visit."
            ),
            package_type="Cultural",
            destination=varanasi,
            price=8999,
            duration_days=3,
            rating=4.5,
            review_count=89,
            highlights=[
                "Sunrise boat ride on the Ganga",
                "Evening Ganga Aarti at Dashashwamedh",
                "Sarnath Buddhist excursion",
                "Banarasi silk weaving workshop",
            ],
            inclusions=[
                "2 nights at a verified SafeStay",
                "Daily breakfast + 1 traditional dinner",
                "AC transport & licensed guide",
                "Boat ride & Sarnath entry",
            ],
            exclusions=["Personal donations", "Silk shopping"],
            itinerary_summary=[
                {"theme": "Ghats & Aarti", "description": "Sunrise boat → Vishwanath → Evening Aarti"},
                {"theme": "Sarnath Buddhist Trail", "description": "Sarnath → Museum → Deer Park"},
                {"theme": "Silk Weaving & Departure", "description": "Weaving workshop → Banarasi silk market → departure"},
            ],
            image_url="https://images.unsplash.com/photo-1561361513-2d000a50f0dc?auto=format&fit=crop&w=1200&q=80",
            is_featured=False,
            is_available=True,
            max_group_size=8,
            age_from=15,
            age_to=70,
            difficulty="Moderate",
        )

        TourismPackage.objects.create(
            title="Women-Safe Solo: YATRALENS Curated Solo Trip — 4 Days",
            slug="yatralens-solo-women-4d",
            subtitle="A curated women-only solo trip package with verified women-friendly stays and 24/7 safety escort.",
            description=(
                "Designed specifically for solo women travelers. This 4-day itinerary across Rajahmundry and the "
                "Godavari delta includes women-only transfers, verified women-managed stays, and a 24/7 safety escort "
                "with live GPS sharing and SOS access through YATRALENS."
            ),
            package_type="WomenSafe",
            destination=rjy,
            price=11999,
            duration_days=4,
            rating=4.9,
            review_count=67,
            highlights=[
                "Women-managed SafeStay hotel",
                "Female tour escort throughout",
                "24/7 SOS & live-share activation",
                "Curated solo-friendly experiences",
            ],
            inclusions=[
                "3 nights at a verified women-managed hotel",
                "All meals (breakfast, lunch, dinner)",
                "Female tour escort & AC transport",
                "YATRALENS SOS device & live-share",
                "All entry fees & experiences",
            ],
            exclusions=["Personal shopping", "Optional spa services"],
            itinerary_summary=[
                {"theme": "Arrival & Pushkar Ghat", "description": "Airport pickup → hotel check-in → evening Pushkar Ghat"},
                {"theme": "Heritage & Barrage", "description": "Temple tour → Dowleswaram → cultural evening"},
                {"theme": "Papikondalu Boat", "description": "Full-day river cruise with female crew"},
                {"theme": "Souvenirs & Departure", "description": "Pootharekulu shopping → airport drop"},
            ],
            image_url="https://images.unsplash.com/photo-1506744038136-46273834b3fb?auto=format&fit=crop&w=1200&q=80",
            is_featured=True,
            is_available=True,
            max_group_size=6,
            age_from=18,
            age_to=65,
            difficulty="Easy",
        )

        TourismPackage.objects.create(
            title="Adventure Andhra — Trek & River Rafting — 3 Days",
            slug="adventure-andhra-3d",
            subtitle="An adrenaline-fueled 3-day adventure through Eastern Ghats and Godavari rapids.",
            description=(
                "For thrill-seekers, this 3-day adventure package combines Eastern Ghats treks, Godavari river "
                "rapids (seasonal), and campfire nights. Includes certified adventure guides and full safety gear."
            ),
            package_type="Adventure",
            destination=rjy,
            price=9999,
            duration_days=3,
            rating=4.6,
            review_count=42,
            highlights=[
                "Eastern Ghats day trek",
                "Godavari rapids (seasonal)",
                "Certified adventure guides",
                "Campfire & stargazing night",
            ],
            inclusions=[
                "2 nights (1 hotel + 1 campsite)",
                "All meals & camping gear",
                "Certified adventure guide & safety equipment",
                "AC transport from Rajahmundry",
            ],
            exclusions=["Personal travel insurance", "Extra snacks"],
            itinerary_summary=[
                {"theme": "Eastern Ghats Trek", "description": "Morning trek → waterfall → campsite"},
                {"theme": "River Adventure", "description": "Rapids (seasonal) → kayaking → bonfire"},
                {"theme": "Return & Reflection", "description": "Sunrise → breakfast → Rajahmundry return"},
            ],
            image_url="https://images.unsplash.com/photo-1507525428034-b723cf961d3e?auto=format&fit=crop&w=1200&q=80",
            is_featured=False,
            is_available=True,
            max_group_size=10,
            age_from=16,
            age_to=55,
            difficulty="Challenging",
        )

        TourismPackage.objects.create(
            title="Budget Backpacker: 5-Day Across South India",
            slug="budget-backpacker-5d",
            subtitle="A budget-friendly 5-day backpacker trail covering Mysore, Goa, and Gokarna.",
            description=(
                "For budget-conscious travelers. Hostel stays, public transport, and curated free experiences. "
                "Includes verified backpacker hostels and group activities."
            ),
            package_type="Budget",
            destination=mysore,
            price=4999,
            duration_days=5,
            rating=4.4,
            review_count=98,
            highlights=[
                "Verified backpacker hostels",
                "Group trekking & meet-ups",
                "Local food walks",
                "Public transport passes",
            ],
            inclusions=[
                "4 nights in verified hostels",
                "Daily breakfast",
                "Curated group experiences",
                "24/7 trip coordinator support",
            ],
            exclusions=["Inter-city travel tickets", "Personal expenses"],
            itinerary_summary=[
                {"theme": "Mysore Arrival", "description": "Hostel check-in → Palace walk → group dinner"},
                {"theme": "Mysore to Goa", "description": "Train to Goa → Calangute hostel → beach"},
                {"theme": "Goa Exploration", "description": "Old Goa → Anjuna → beach shack evening"},
                {"theme": "Goa to Gokarna", "description": "Bus to Gokarna → beach trek → camping"},
                {"theme": "Return", "description": "Sunrise → return to Goa → departure"},
            ],
            image_url="https://images.unsplash.com/photo-1542314831-068cd1dbfeeb?auto=format&fit=crop&w=1200&q=80",
            is_featured=False,
            is_available=True,
            max_group_size=15,
            age_from=18,
            age_to=35,
            difficulty="Moderate",
        )

        # =====================================================================
        # 8. CUSTOMER FEEDBACK — Public platform feedback entries
        # =====================================================================
        CustomerFeedback.objects.create(
            name="Priya Sharma",
            email="priya@example.com",
            category="Safety",
            rating=5,
            subject="Real-time crime data was a game-changer",
            message=(
                "I used the YATRALENS crime intelligence feature before booking my Rajahmundry trip. "
                "The real-time theft/harassment counts and the safety score gave me the confidence to travel solo. "
                "The data matched my actual experience — I felt safe the entire time."
            ),
            destination=rjy,
            contact_allowed=True,
            is_resolved=True,
        )
        CustomerFeedback.objects.create(
            name="Arjun Mehta",
            category="Package",
            rating=5,
            subject="Pink City Weekend was worth every rupee",
            message=(
                "The Jaipur package was perfectly curated. The hotel was women-friendly, the guide was knowledgeable, "
                "and YATRALENS live-share kept my family reassured throughout. Highly recommend."
            ),
            destination=jaipur,
            is_resolved=True,
        )
        CustomerFeedback.objects.create(
            name="Anonymous",
            category="General",
            rating=4,
            subject="Loved the post-trip review section",
            message=(
                "Reading verified post-trip reviews before booking really helped me set expectations. "
                "I appreciate that reviews include both pros AND cons — feels honest."
            ),
            is_resolved=True,
        )
        CustomerFeedback.objects.create(
            name="Sneha Iyer",
            category="Destination",
            rating=5,
            subject="Mysore was cleaner than I expected",
            message=(
                "The YATRALENS crime stats showed Mysore as the safest destination on the platform, and the city "
                "lived up to it. Police presence was visible and the city was well-lit even late at night."
            ),
            destination=mysore,
            contact_allowed=False,
        )
        CustomerFeedback.objects.create(
            name="Ravi Kumar",
            category="App",
            rating=4,
            subject="Some minor UX improvements needed",
            message=(
                "The platform is genuinely useful. I'd love to see a map view of all packages in the future — "
                "and maybe a price calendar so I can see cheaper days to travel."
            ),
            contact_allowed=True,
        )

        # =====================================================================
        # 9. POST-TRIP REVIEWS — Detailed user reflections
        # =====================================================================
        PostTripReview.objects.create(
            destination=rjy,
            reviewer_name="Aarohi Reddy",
            traveler_type="Solo Woman",
            overall_rating=5.0,
            safety_rating=5.0,
            value_rating=4.5,
            title="An Unforgettable Godavari Sunset Trip",
            detailed_notes=(
                "I spent 2 days in Rajahmundry as a solo woman traveler and felt completely safe throughout. "
                "The Pushkar Ghat evening aarti was mesmerizing. The Dowleswaram Barrage museum was surprisingly "
                "well-curated. I had Andhra thali and Pootharekulu sweets. The YATRALENS live-share let my mom track "
                "me in real-time. I'd absolutely go back."
            ),
            pros=[
                "Excellent safety infrastructure",
                "Affordable verified hotels",
                "Beautiful sunset boat ride",
                "Helpful local police presence",
            ],
            cons=[
                "Limited public transport after 9 PM",
                "Auto-rickshaws can overcharge tourists",
            ],
            travel_tips=(
                "Pre-book hotels on YATRALENS. Use the YATRALENS safe-route feature for autos. "
                "Carry cash for the bazaar. Sunscreen is a must."
            ),
            would_recommend=True,
            is_published=True,
            moderated=True,
        )
        PostTripReview.objects.create(
            destination=jaipur,
            reviewer_name="Karthik Nair",
            traveler_type="Friends",
            overall_rating=4.5,
            safety_rating=4.0,
            value_rating=4.5,
            title="Pink City Weekend with Friends — Highly Recommended",
            detailed_notes=(
                "We did the 3-day Pink City package. Amber Fort was the highlight, and the evening sound-and-light "
                "show was magical. Johari Bazaar is great for souvenirs. The hotel was centrally located and women-friendly. "
                "Some areas felt crowded — be careful with phones and wallets."
            ),
            pros=["Heritage hotels", "Affordable food", "Iconic monuments"],
            cons=["Crowded bazaars", "Aggressive shopkeepers in some lanes"],
            travel_tips="Visit Amber Fort early morning. Bargain in bazaars. Carry a water bottle.",
            would_recommend=True,
            is_published=True,
            moderated=True,
        )
        PostTripReview.objects.create(
            destination=goa,
            reviewer_name="Riya & Aman",
            traveler_type="Couple",
            overall_rating=5.0,
            safety_rating=5.0,
            value_rating=4.5,
            title="Honeymoon in Goa — Paradise",
            detailed_notes=(
                "We spent 4 days in Goa for our honeymoon. The beach resort was excellent and the sunset cruise "
                "was romantic. Old Goa's churches are stunning. The spice plantation visit was a highlight. "
                "We felt completely safe as a couple traveling together."
            ),
            pros=["Romantic settings", "Beach resorts", "Great seafood"],
            cons=["Expensive in peak season", "Some beaches can be crowded"],
            travel_tips="Book sunset cruises in advance. Rent a scooter for flexibility. Try the local feni.",
            would_recommend=True,
            is_published=True,
            moderated=True,
        )
        PostTripReview.objects.create(
            destination=mysore,
            reviewer_name="Deepa Krishnan",
            traveler_type="Family",
            overall_rating=5.0,
            safety_rating=5.0,
            value_rating=5.0,
            title="A Perfect Family Weekend in Mysore",
            detailed_notes=(
                "We took our kids (ages 8 and 12) to Mysore. The city is incredibly clean and safe. "
                "Mysore Palace amazed the kids. Chamundi Hills offered great views. The Devaraja Market is colorful. "
                "YATRALENS crime data showed Mysore as the safest — and it absolutely was."
            ),
            pros=["Family-friendly", "Very clean city", "Affordable"],
            cons=["Limited nightlife (which is a pro for families)"],
            travel_tips="Buy Mysore Pak from Guru Sweets. Visit the Palace illumination on Sundays.",
            would_recommend=True,
            is_published=True,
            moderated=True,
        )
        PostTripReview.objects.create(
            destination=varanasi,
            reviewer_name="Manish Tiwari",
            traveler_type="Solo Man",
            overall_rating=4.0,
            safety_rating=3.5,
            value_rating=4.5,
            title="Spiritual but Intense — Varanasi in 3 Days",
            detailed_notes=(
                "Varanasi is overwhelming — both spiritually and in terms of sensory experience. The Ganga Aarti "
                "is genuinely life-changing. However, the alleys can be confusing, and you do need to be alert. "
                "I felt safe with YATRALENS live-share active. Pre-book a guide for the alley walks."
            ),
            pros=["Spiritual depth", "Affordable", "Photogenic"],
            cons=["Crowded alleys", "Aggressive touts in some areas"],
            travel_tips="Pre-book Ganga Aarti viewing seats. Carry a printed map. Be respectful at ghats.",
            would_recommend=True,
            is_published=True,
            moderated=True,
        )

        self.stdout.write(self.style.SUCCESS("Successfully seeded YATRALENS database!"))
