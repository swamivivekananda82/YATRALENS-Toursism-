# 🌐 YATRALENS — Intelligent Tourism & Safety Companion
> **Tagline**: *Discover India. Plan Safely. Remember Forever.*  
> **Pitch**: *"YATRALENS is the intelligent travel companion that helps you discover curated tourism packages, assess real-time crime risk, share live GPS, write detailed post-trip reviews, and turn every journey into a digital memory."*

---

## 🎯 Architecture: A Professional Tourism Platform

YATRALENS is a Django-based full-stack tourism platform that combines three powerful paradigms:

1. **Curated Tourism Packages** — Weekend, adventure, cultural, luxury, budget, and women-safe solo packages
2. **Real-Time / Statistical Crime Intelligence** — Live safety scores, crime statistics, heatmaps, zone-level risk meters, and trend analytics
3. **Traveler Community** — Customer feedback system, detailed post-trip reviews, AI-generated memory storybooks, and PDF export

The professional landing page at `/` introduces the **YATRALENS** brand, showcases featured packages, and provides a one-stop entry point to seamless exploration of tourism packages.

---

## 🚀 Modules & Capabilities

| Module | Features & Capabilities |
| :--- | :--- |
| **🏠 YATRALENS Landing Page** | Professional hero, package showcase, crime intelligence snapshot, live safety advisories, recent post-trip reviews, and a "Submit Feedback" call-to-action. |
| **📦 Curated Tourism Packages** | 6+ pre-seeded packages (Weekend, Adventure, Cultural, Luxury, Budget, Women-Safe Solo) with filters by destination, type, price, rating, and search. |
| **🛡️ Real-Time Crime Intelligence** | Per-destination crime data source, last-update timestamp, trend (📉 Improving / ➖ Stable / 📈 Deteriorating), and historical `CrimeStatistic` records for trend charting. |
| **🗺️ Destination Crime Heatmap** | Leaflet.js interactive map with zone breakdown: Tourist Areas, Main Markets, Highways, Isolated Areas, and Residential Zones. |
| **💬 Customer Feedback System** | Structured form with category, rating, subject, message, destination/package linking, follow-up consent, and public feedback display with aggregate stats. |
| **⭐ Post-Trip Review Module** | Detailed post-trip reviews with overall/safety/value ratings, pros, cons, travel tips, recommendation flag, and destination-grouped aggregate statistics. |
| **📊 Crime Statistics & Trend Charts** | Historical `CrimeStatistic` records per destination (theft, harassment, violent crime) with auto-computed `crime_rate_per_100k` for Chart.js trend visualization. |
| **🏛️ Official Government ERSS 112 CAD** | Ministry of Home Affairs (MHA) Computer-Aided Dispatch (CAD) engine with automated police jurisdiction resolution, PCR arrival ETA, and official CAD reference numbers. |
| **📱 Native Mobile Bottom Bar & PWA** | Progressive Web App (`manifest.json`, `sw.js`) with installable mobile app shell, tactile haptic pulses (`navigator.vibrate`), and fixed bottom navigation bar. |
| **🌐 Offline Emergency Hub & Queue** | Zero-data emergency directory (`/offline/`), cached first-aid protocols, and offline SOS beacon queue with automatic synchronization upon network reconnection. |
| **🚨 Real Emergency SOS System** | Real device GPS lock (`navigator.geolocation`), 1-click WhatsApp emergency link, direct SMS emergency intent, audio siren synthesizer, and 3-second hold trigger. |
| **👩 Women Safe Tourism** | Solo Women hub, simulated GPS location sharing ("Share with Mom"), and national helplines (112, 1091, 1090, 181). |
| **🛣️ Safe Route Optimizer** | Compares **Fastest Route (18 min)** vs. **Safer Route (22 min ⭐ Recommended)** vs. **Balanced Route (20 min)**, avoiding unlit spots and routing along police kiosks. |
| **🏨 Verified Safe Hotels** | SafeStay certified accommodations with 24/7 reception, CCTV, female staff, and exact distances to police stations and hospitals. |
| **🚑 Emergency Map & Directory** | Filterable map layers with live "📍 Locate Me" high-accuracy GPS tracker, police station jurisdiction banner, and 24/7 emergency service directory. |
| **🤖 AI Travel Assistant** | Contextual chatbot grounded in safety guidelines, destination advice, budget tips, and opening hours. |
| **📅 Smart Trip Planner** | Budget-optimized (e.g. ₹5,000 / 2-day) hour-by-hour itinerary generator with safe return curfew hours. |
| **📸 Tourist Memory Maker** | Multi-sensory journaling: Places visited, local foods tried, photos, automated historical facts, favorite moment tag. |
| **📖 AI Travel Story Generator** | Synthesizes trip data into personalized narrative with in-browser editing and **ReportLab PDF Album Download**. |
| **📊 Authority Admin Dashboard** | Live ERSS 112 CAD emergency dispatch command feed, tourism footfall analytics, hotel verification toggles, and live safety alert broadcaster. |

---

## 💡 Innovative Features & UX Improvements (Suggestions)

Beyond the three core feature requirements, here are creative additions to elevate the YATRALENS travel-planning experience:

1. **🗺️ Interactive Map View for All Packages** — A geographic map (Leaflet.js) showing every package as a pin on the destination, with click-to-preview cards. Better for visual planners.
2. **📅 Price Calendar & Best-Time-to-Travel** — A 12-month calendar showing historical price-per-day and crowd levels. Travelers can pick cheaper, less-crowded weeks.
3. **🎒 AI Packing List Generator** — Based on destination weather, trip duration, and activity types, generate a tailored packing checklist.
4. **🤝 Group Travel Coordination** — Allow multiple travelers to "join" a package, split costs, and vote on itinerary choices.
5. **🛂 Visa & Document Checklists** — Country/destination-specific document requirements (passport, visa, vaccinations, permits) with validity reminders.
6. **🌦️ Weather-Aware Itinerary Adjustments** — Auto-adjust planned activities if rain or storms are forecasted.
7. **💱 Live Currency Converter & Budget Tracker** — Real-time INR-to-local-currency conversion plus a trip expense tracker with category breakdowns.
8. **🏆 Gamified Travel Badges** — Award badges ("First Solo Trip", "Visited 5 States", "Temple Explorer") that show on a public traveler profile.
9. **📞 In-App Local Guide Connect** — Pre-vetted local guides for hire with verified ratings and language filters.
10. **🌐 Offline Mode (PWA)** — Cache package details, hotel addresses, and emergency numbers for offline access when traveling in low-network areas.
11. **🆘 Smart SOS with Geofencing** — Pre-set "safe zones" (hotel, embassy); if you exit them unexpectedly, an automatic check-in alert fires.
12. **🗣️ Multilingual Reviews & Chat** — Auto-translate reviews to the reader's preferred language using a translation layer.
13. **📰 Personalized Travel Feed** — A TikTok-style feed of short, curated travel videos for each destination.
14. **🤖 AI Travel Concierge** — A more powerful assistant that can plan multi-city trips, optimize train/flight connections, and respect a user's budget.
15. **🧳 Luggage Forwarding Service Integration** — Partner integration for door-to-hotel luggage delivery (common in Japan/Europe).
16. **🛌 Eco-Stay Certification** — A separate badge for environmentally responsible accommodations.
17. **🩺 Travel Health Advisor** — Region-specific health advisories, recommended vaccinations, and pharmacy locations.
18. **👨‍👩‍👧 Family-Friendly Filters** — Filter packages by age-appropriate activities, kid meals, and family-room availability.

---

## 🗃️ Data Model (New in YATRALENS)

### Existing Models (Extended)
- **Destination** — extended with `violent_crime_reports`, `crime_data_source` (Real-Time / Statistical / Manual), `last_crime_update`, `crime_trend` (Improving / Stable / Deteriorating), `theft_change_pct`, `harassment_change_pct`, `banner_image_url`, and computed properties `crime_trend_icon` and `crime_category_breakdown`.

### New Models
- **TourismPackage** — Curated packages with `title`, `slug`, `subtitle`, `description`, `package_type`, `destination`, `price`, `duration_days`, `rating`, `review_count`, `highlights`, `inclusions`, `exclusions`, `itinerary_summary`, `image_url`, `is_featured`, `is_available`, `max_group_size`, `age_from`, `age_to`, `difficulty`, and computed `price_per_day` and `badge_label` properties.
- **CustomerFeedback** — Structured feedback with `name`, `email`, `category`, `rating`, `subject`, `message`, `destination`, `package`, `contact_allowed`, `is_resolved`, `responded_at`.
- **PostTripReview** — Detailed post-trip reflections with `destination`, `package`, `reviewer_name`, `traveler_type`, `overall_rating`, `safety_rating`, `value_rating`, `title`, `detailed_notes`, `pros`, `cons`, `travel_tips`, `would_recommend`, `photos`, `is_published`, `moderated`, and computed `average_rating` property.
- **CrimeStatistic** — Historical crime stats with `destination`, `period_label`, `recorded_at`, `theft_cases`, `harassment_cases`, `violent_crime_cases`, `other_cases`, `population_estimate`, `crime_rate_per_100k` (auto-computed), `data_source`, and `notes`.

---

## 🛠️ Tech Stack

- **Backend**: Python 3.14, Django 5.2, Django REST Framework, ReportLab (PDF Engine)
- **Frontend**: Responsive HTML5, Tailwind CSS, FontAwesome 6, Leaflet.js (OpenStreetMap), Chart.js, HTML2PDF.js
- **Database**: SQLite / Django ORM (Pre-seeded with Rajahmundry, Jaipur, Goa, Varanasi, Mysore)
- **Audio/Web APIs**: Web Audio API (Emergency Siren Synth), Geolocation Simulator, Clipboard API

---

## 🏃 How to Run the Project

1. Navigate to the project directory:
   ```powershell
   cd C:\safetrip_memories
   ```

2. Run database migrations (re-run after the new models):
   ```powershell
   python manage.py makemigrations core
   python manage.py migrate
   ```

3. Seed data (now also seeds tourism packages, feedback, post-trip reviews, and crime statistics):
   ```powershell
   python manage.py seed_data
   ```

4. Run automated tests:
   ```powershell
   python manage.py test core
   ```

5. Start the development server:
   ```powershell
   python manage.py runserver 127.0.0.1:8000
   ```

6. Open your browser and visit:
   - **YATRALENS Landing Page**: [http://127.0.0.1:8000/](http://127.0.0.1:8000/)
   - **Tourism Packages**: [http://127.0.0.1:8000/packages/](http://127.0.0.1:8000/packages/)
   - **Customer Feedback**: [http://127.0.0.1:8000/feedback/](http://127.0.0.1:8000/feedback/)
   - **Post-Trip Reviews**: [http://127.0.0.1:8000/reviews/](http://127.0.0.1:8000/reviews/)
   - **Crime & Safety Intelligence**: [http://127.0.0.1:8000/safety/Rajahmundry/](http://127.0.0.1:8000/safety/Rajahmundry/)
   - **Crime Statistics API**: [http://127.0.0.1:8000/api/crime-stats/Rajahmundry/](http://127.0.0.1:8000/api/crime-stats/Rajahmundry/)
   - **Tourism Packages API**: [http://127.0.0.1:8000/api/packages/](http://127.0.0.1:8000/api/packages/)
   - **Customer Feedback API**: [http://127.0.0.1:8000/api/feedback/](http://127.0.0.1:8000/api/feedback/)
   - **Post-Trip Reviews API**: [http://127.0.0.1:8000/api/reviews/](http://127.0.0.1:8000/api/reviews/)
   - **Women Safe Tourism Hub**: [http://127.0.0.1:8000/women-safety/](http://127.0.0.1:8000/women-safety/)
   - **Verified Hotels**: [http://127.0.0.1:8000/hotels/](http://127.0.0.1:8000/hotels/)
   - **Nearby Emergency Map**: [http://127.0.0.1:8000/emergency/](http://127.0.0.1:8000/emergency/)
   - **AI Trip Planner**: [http://127.0.0.1:8000/trip-planner/](http://127.0.0.1:8000/trip-planner/)
   - **Tourist Memory Maker & Story Synthesizer**: [http://127.0.0.1:8000/memories/](http://127.0.0.1:8000/memories/)
   - **AI Assistant Chatbot**: [http://127.0.0.1:8000/ai-assistant/](http://127.0.0.1:8000/ai-assistant/)
   - **Authority Admin Dashboard**: [http://127.0.0.1:8000/admin-dashboard/](http://127.0.0.1:8000/admin-dashboard/)
   - **Tourist Profile**: [http://127.0.0.1:8000/profile/](http://127.0.0.1:8000/profile/)

---

## 🌐 REST API Endpoints

| Endpoint | Method | Description |
| :--- | :--- | :--- |
| `/api/destinations/` | GET | List/search destinations |
| `/api/destinations/<name>/` | GET | Destination detail with all relations |
| `/api/crime-stats/<name>/` | GET | Real-time + historical crime stats with trend chart data |
| `/api/packages/` | GET | List/search tourism packages (with filters) |
| `/api/packages/<slug>/` | GET | Detailed package info |
| `/api/feedback/` | GET / POST | List public feedback or submit new feedback |
| `/api/feedback/stats/` | GET | Aggregate feedback statistics |
| `/api/reviews/` | GET / POST | List published reviews or submit a new post-trip review |
| `/api/reviews/stats/` | GET | Per-destination review aggregate statistics |
| `/api/safe-route/` | POST | Get 3 safe route alternatives |
| `/api/sos/trigger/` | POST | Trigger SOS alert |
| `/api/incidents/report/` | POST | Report an incident |
| `/api/ai/chat/` | POST | AI travel assistant chat |
| `/api/ai/generate-itinerary/` | POST | Generate AI trip plan |

---

## 🎨 YATRALENS Brand Identity

- **Name**: YATRALENS (Yatra + Lens — "The lens through which you see your journey")
- **Icon**: `fa-compass-drafting` (a compass-drafting tool representing planning & direction)
- **Colors**: Brand teal (#0d9488) → Emerald (#10b981) → Amber (#f59e0b) gradient
- **Tagline**: "Discover • Plan • Remember"
- **Positioning**: A modern, intelligent tourism companion centered on safety, community feedback, and curated experiences.

---

## 📝 License & Credits

This project was developed for the Smart India Hackathon (SIH 2026) to demonstrate an intelligent tourism platform concept. YATRALENS is an evolution of the original SafeTrip Memories prototype, redesigned with:
- A professional landing page experience
- Tourism package exploration
- Real-time crime rate data
- Customer feedback system
- Post-trip review module

© 2026 YATRALENS. Empowering intelligent, safer, and more memorable travel.
