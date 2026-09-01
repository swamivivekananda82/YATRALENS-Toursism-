import math
import random

def generate_travel_story(title, destination, traveler_name, places, foods, facts, favorite_moment):
    """
    AI Travel Story Generator:
    Combines Location + Photos + Timeline + Food + Activities + Historical Facts + Favorite Moment
    into a cohesive, evocative travel narrative.
    """
    places_str = ", ".join(places) if places else destination
    foods_str = ", ".join(foods) if foods else "delightful local cuisine"
    
    # Contextual narratives tailored to destinations
    if "Rajahmundry" in destination or "Godavari" in str(places):
        story = (
            f"🌄 My Day in {destination}\n\n"
            f"My unforgettable journey through {destination} began along the tranquil and holy banks of the sacred Godavari River. "
            f"As dawn broke, I visited {places_str}, taking in the awe-inspiring engineering and rich history that defines this cultural capital. "
            f"Standing at the historic Dowleswaram Barrage, built by Sir Arthur Cotton, I marveled at how this mighty waterway transformed the entire delta into the rice bowl of Andhra.\n\n"
            f"Between exploring historical landmarks and soaking in the vibrant spiritual atmosphere, I treated my tastebuds to authentic {foods_str}, "
            f"including traditional Andhra thali and melting Pootharekulu sweets.\n\n"
            f"The absolute highlight of my trip was {favorite_moment}. "
            f"With the safety features guiding my path through well-lit, police-patrolled heritage trails, I felt completely secure as a solo traveler. "
            f"Rajahmundry gifted me memories of serenity, heritage, and warm hospitality that will stay in my heart forever."
        )
    elif "Jaipur" in destination:
        story = (
            f"👑 Royal Exploration in {destination}\n\n"
            f"My adventure in the vibrant Pink City of {destination} was an enchanting journey through time. "
            f"I explored {places_str}, marveling at the intricate Rajput architecture and centuries of regal heritage. "
            f"Throughout the day, I savored {foods_str}, delighting in the spicy, rich aromas of Rajasthani culture.\n\n"
            f"My favorite moment was {favorite_moment}. Navigating through verified tourist corridors with real-time safety tracking gave me complete peace of mind to soak in every royal corridor."
        )
    elif "Goa" in destination:
        story = (
            f"🌊 Coastal Serenade in {destination}\n\n"
            f"The golden coast of {destination} offered a harmonious blend of scenic coastlines, Portuguese heritage, and vibrant energy. "
            f"Visiting {places_str} while enjoying {foods_str} created unforgettable moments.\n\n"
            f"My most cherished memory was {favorite_moment}. Traveling along verified safe coastal routes made this solo journey deeply rejuvenating and peaceful."
        )
    else:
        story = (
            f"✨ An Unforgettable Journey to {destination}\n\n"
            f"Traveling to {destination} as {traveler_name} was an exhilarating and heartwarming experience. "
            f"I explored remarkable destinations including {places_str}, learning fascinating historical stories along every step.\n\n"
            f"Food was a major highlight: tasting {foods_str} connected me deeply with the local culture and traditions.\n\n"
            f"The defining memory of my journey was {favorite_moment}. "
            f"Guided by intelligent safety routes, verified accommodations, and responsive emergency support, I explored with pure freedom and confidence."
        )
    
    return story.strip()


def generate_smart_itinerary(destination_name, duration_days, budget, traveler_type, interests):
    """
    Generates an hour-by-hour, safety-first personalized itinerary
    designed specifically with solo women & traveler safety protocols.
    """
    duration = max(1, min(int(duration_days), 5))
    budget_val = float(budget)
    
    # Destination-specific day templates
    if "rajahmundry" in destination_name.lower():
        days_data = [
            {
                "day": 1,
                "theme": "Godavari Heritage, Holy Ghats & Barrage Marvels",
                "safety_advisory": "🟢 All locations are verified high-density tourist zones with 24/7 police kiosks. Safe return to hotel recommended by 08:30 PM.",
                "schedule": [
                    {
                        "time": "08:30 AM",
                        "activity": "Morning Aarti & Sacred Riverfront Walk",
                        "location": "Kotilingala Ghat & Pushkar Ghat, Rajahmundry",
                        "safety_tag": "🟢 Well-Lit Tourist Zone | Police Booth Available",
                        "cost": "Free",
                        "description": "Start the day with peaceful views of the Godavari River and fresh air among local morning walkers."
                    },
                    {
                        "time": "10:30 AM",
                        "activity": "Historical Heritage Visit",
                        "location": "Sri Markandeyeshwara Swamy Temple",
                        "safety_tag": "🟢 Verified Heritage Site | Female Security Staff",
                        "cost": "₹50 (Darshan)",
                        "description": "Explore ancient Dravidian architecture and serene temple courtyards with strict crowd management."
                    },
                    {
                        "time": "01:00 PM",
                        "activity": "Traditional Andhra Lunch & Rest",
                        "location": "SafeStay Recommended: Hotel RiverBay Restaurant",
                        "safety_tag": "🟢 Verified Dining | CCTV Monitored",
                        "cost": "₹350",
                        "description": "Savor authentic Andhra vegetarian thali or Godavari specialties in a family and solo-friendly environment."
                    },
                    {
                        "time": "03:30 PM",
                        "activity": "Engineering Marvel & Sir Arthur Cotton Museum",
                        "location": "Dowleswaram Barrage & Cotton Museum",
                        "safety_tag": "🟢 Safe Public Landmark | Dedicated Security",
                        "cost": "₹30",
                        "description": "Witness the colossal barrage spanning the Godavari River and discover the history of Andhra's agricultural transformation."
                    },
                    {
                        "time": "06:00 PM",
                        "activity": "Golden Sunset Boat Ride & Lighting Spectacular",
                        "location": "Godavari Riverfront Promenade",
                        "safety_tag": "🟢 Patrolled River Promenade | Life Jackets Mandatory",
                        "cost": "₹200",
                        "description": "Spectacular sunset views over the river. Tourist police are actively stationed throughout the promenade."
                    },
                    {
                        "time": "08:00 PM",
                        "activity": "Dinner & Safe Hotel Return",
                        "location": "SafeStay Verified Accommodation",
                        "safety_tag": "🟢 24/7 Reception | Police 0.8 km",
                        "cost": "₹400",
                        "description": "Return to verified hotel before nightfall as per safety best practices for solo travelers."
                    }
                ]
            },
            {
                "day": 2,
                "theme": "Cultural Temples, Sweets & Scenic Godavari Backwaters",
                "safety_advisory": "🟢 Safe organized transport corridor. Recommended to travel with registered tourism cabs or authorized boat rides.",
                "schedule": [
                    {
                        "time": "08:30 AM",
                        "activity": "Spiritual Peace & Beautiful Architecture",
                        "location": "ISKCON Rajahmundry (Gautami Ghat)",
                        "safety_tag": "🟢 Extremely Safe | High Tourist Density",
                        "cost": "Free",
                        "description": "Large peaceful riverside temple with gardens, Vedic exhibitions, and vegetarian breakfast."
                    },
                    {
                        "time": "11:00 AM",
                        "activity": "Scenic River Cruise or Pattiseema Excursion",
                        "location": "Pattiseema Veerabhadra Temple / Papikondalu Foothills Gateway",
                        "safety_tag": "🟢 Authorized AP Tourism Boats Only",
                        "cost": "₹800",
                        "description": "Scenic boat cruise along the tranquil waters of the Godavari hill range."
                    },
                    {
                        "time": "02:00 PM",
                        "activity": "Local Culinary Experience",
                        "location": "Heritage Andhra Mess, Main Road",
                        "safety_tag": "🟢 Verified Eatery | Bustling Market Street",
                        "cost": "₹300",
                        "description": "Enjoy traditional Andhra meals served on banana leaves with homemade gunpowders and ghee."
                    },
                    {
                        "time": "04:00 PM",
                        "activity": "Traditional Craft & Sweet Shopping",
                        "location": "Main Bazaar & Local Pootharekulu Artisan Shops",
                        "safety_tag": "🟡 Busy Commercial Market | Keep Valuables Secure",
                        "cost": "₹500 (Shopping)",
                        "description": "Sample and purchase world-famous paper sweets (Atreyapuram Pootharekulu) and East Godavari handlooms."
                    },
                    {
                        "time": "07:00 PM",
                        "activity": "Evening Reflection & Memory Maker Journaling",
                        "location": "Riverside Cafe / Hotel Lounge",
                        "safety_tag": "🟢 Safe & Well-Lit",
                        "cost": "₹250",
                        "description": "Organize your captured photos, generate your AI Travel Story on SafeTrip Memories, and prepare for departure."
                    }
                ]
            }
        ]
    else:
        # Generic high-quality Indian destination template
        days_data = [
            {
                "day": 1,
                "theme": f"Historic Core & Cultural Highlights of {destination_name}",
                "safety_advisory": "🟢 Verified tourist corridors. Emergency numbers: 112 & 1091 (Women Helpline). Safe return by 08:30 PM.",
                "schedule": [
                    {
                        "time": "09:00 AM",
                        "activity": "Iconic Heritage Monument",
                        "location": f"Main Heritage Complex, {destination_name}",
                        "safety_tag": "🟢 High Security & CCTV",
                        "cost": "₹100",
                        "description": "Explore primary architectural landmarks during cool morning hours with authorized guides."
                    },
                    {
                        "time": "01:00 PM",
                        "activity": "Verified Local Cuisine Lunch",
                        "location": "City Center Verified Restaurant",
                        "safety_tag": "🟢 High Hygiene & Women-Friendly Staff",
                        "cost": "₹400",
                        "description": "Taste regional culinary specialties in a secure, central location."
                    },
                    {
                        "time": "03:30 PM",
                        "activity": "Museum & Cultural Center",
                        "location": f"State Museum / Art Gallery, {destination_name}",
                        "safety_tag": "🟢 Safe Indoor Tourist Spot",
                        "cost": "₹50",
                        "description": "Immerse in local art, handicrafts, and royal relics."
                    },
                    {
                        "time": "06:30 PM",
                        "activity": "Scenic Sunset Viewpoint",
                        "location": "Promenade / Sunset Point",
                        "safety_tag": "🟢 Patrolled Tourist Corridor",
                        "cost": "Free",
                        "description": "Enjoy the evening panorama alongside fellow travelers."
                    },
                    {
                        "time": "08:00 PM",
                        "activity": "Dinner & Verified Safe Hotel Check-in",
                        "location": "Verified SafeStay Hotel",
                        "safety_tag": "🟢 24/7 Guard & Police Proximity",
                        "cost": "₹500",
                        "description": "Conclude the day safely at verified accommodation."
                    }
                ]
            }
        ]
    
    # Return requested number of days
    selected_days = days_data[:duration] if duration <= len(days_data) else days_data
    
    return {
        "destination": destination_name,
        "duration_days": duration,
        "budget": budget_val,
        "traveler_type": traveler_type,
        "interests": interests,
        "estimated_total_cost": f"₹{min(budget_val, duration * 2200):,.0f}",
        "safety_summary": {
            "overall_safety_rating": "🟢 High (Safety Score: 85/100)",
            "women_safety_index": "94% Solo-Female Recommended",
            "recommended_curfew": "08:30 PM for solo exploration",
            "nearest_emergency_hub": "Central Police & General Hospital (within 1.5 km)"
        },
        "days": selected_days
    }


def ai_travel_assistant_reply(message, context=None):
    """
    Intelligent chatbot assistant answering user queries on safety,
    places to visit, hotels, budget, solo women tips, and emergency helplines.
    """
    msg_lower = message.lower()
    
    if any(k in msg_lower for k in ["rajahmundry", "safest places in rajahmundry", "safest place"]):
        return (
            "🛡️ **Safest Places to Visit in Rajahmundry**:\n\n"
            "1. **Kotilingala Ghat & Pushkar Ghat** (Safety Score: 94/100) – High tourist density, brightly illuminated promenade, and 24/7 Tourist Police Kiosk.\n"
            "2. **Dowleswaram Barrage & Cotton Museum** (Safety Score: 90/100) – Highly secure irrigation marvel and park area with dedicated staff.\n"
            "3. **ISKCON Temple (Gautami Ghat)** (Safety Score: 96/100) – Extremely peaceful, highly family & solo woman-friendly with 24/7 security.\n"
            "4. **Markandeyeshwara Temple** (Safety Score: 88/100) – Ancient cultural site right in the heart of town.\n\n"
            "💡 *Safety Tip*: Avoid unlit river canal bypass roads after 9:30 PM. Always use the main Godavari Bund Road which is fully CCTV-monitored."
        )
    elif any(k in msg_lower for k in ["women", "solo female", "solo woman", "female traveler", "safe for women"]):
        return (
            "👩 **Solo Women Traveler Safety Guidelines for SafeTrip**:\n\n"
            "• **Live Location Sharing**: Activate the 'Share Journey' feature in the Women Safety tab to broadcast real-time GPS to your trusted contacts.\n"
            "• **Emergency SOS**: Hold the 🚨 Red SOS button for 3 seconds to immediately alert contacts and dispatch nearest police assistance.\n"
            "• **Verified Stays**: Choose hotels with the 'Women-Friendly' badge (featuring 24/7 reception, female staff on duty, and close proximity to police stations).\n"
            "• **Helplines in India**:\n"
            "  - **112**: All-in-One National Emergency\n"
            "  - **1091 / 1090**: Women Safety Helpline\n"
            "  - **181**: Women in Distress 24/7 Helpline\n"
            "  - **1363**: Ministry of Tourism Tourist Infoline"
        )
    elif any(k in msg_lower for k in ["papikondalu", "hotel near papikondalu", "hotel"]):
        return (
            "🏨 **Safest Hotels & Stays Near Rajahmundry & Papikondalu Gateway**:\n\n"
            "1. **SafeStay Godavari Grand** ⭐ 4.7/5 – 🟢 Verified Women-Friendly | 0.8 km from Central Police Station | 24/7 Reception & CCTV.\n"
            "2. **RiverBay Resort Rajahmundry** ⭐ 4.6/5 – 🟢 Verified Tourist Hub | Direct riverside access with private security.\n"
            "3. **Royal Fort Residency** ⭐ 4.5/5 – 🟢 Verified Safe Stay | 1.1 km from General Hospital.\n\n"
            "All verified hotels include 24/7 security guard presence, keycard locks, and on-call medical assistance."
        )
    elif any(k in msg_lower for k in ["plan", "2-day", "3-day", "itinerary", "2 day"]):
        return (
            "📅 **Quick 2-Day Safe Itinerary for Rajahmundry (Solo/Family)**:\n\n"
            "• **Day 1 (Heritage & Sacred River)**:\n"
            "  - 08:30 AM: Pushkar Ghat & Godavari riverfront walk\n"
            "  - 11:00 AM: Sri Markandeyeshwara Swamy Temple\n"
            "  - 01:00 PM: Andhra Thali at RiverBay\n"
            "  - 04:00 PM: Dowleswaram Barrage & Sir Arthur Cotton Museum\n"
            "  - 06:30 PM: Sunset boat ride & return to hotel by 8:00 PM.\n\n"
            "• **Day 2 (Backwaters & Culture)**:\n"
            "  - 09:00 AM: ISKCON Temple riverside gardens\n"
            "  - 11:30 AM: Pattiseema scenic boat excursion\n"
            "  - 04:30 PM: Main Bazaar for famous Pootharekulu sweets\n"
            "  - 07:00 PM: Travel memory journal synthesis on SafeTrip Memories!\n\n"
            "👉 *You can generate your custom detailed itinerary in the **Trip Planner** tab.*"
        )
    elif any(k in msg_lower for k in ["sos", "emergency", "police", "hospital"]):
        return (
            "🚨 **Emergency Rapid Assistance**:\n\n"
            "If you are facing an emergency right now:\n"
            "1. Press and hold the **EMERGENCY SOS button** in the top navigation or Women Safety portal.\n"
            "2. Direct National Emergency Helpline: **112**\n"
            "3. Women Helpline: **1091** / **1090**\n"
            "4. Rajahmundry Central Police Control: **0883-2471033**\n"
            "5. Govt General Hospital Rajahmundry: **0883-2473456**\n\n"
            "Your live GPS coordinates can be shared instantly with your trusted family contacts."
        )
    else:
        return (
            f"👋 Hello! I am your **SafeTrip AI Travel Assistant**.\n\n"
            f"I can help you with:\n"
            f"• 🛡️ Real-time crime and safety intelligence for destinations\n"
            f"• 👩 Solo women safe routes, timings, and verified hotels\n"
            f"• 📅 Personalized safety-optimized itineraries (like 2-day Rajahmundry tours)\n"
            f"• 📸 Preserving travel stories with our AI Tourist Memory Maker\n"
            f"• 🚨 Instant emergency contacts, police stations, and hospitals\n\n"
            f"Feel free to ask questions like: *'What are the safest places in Rajahmundry?'* or *'Plan a ₹5000 2-day solo trip'*!"
        )


def calculate_safe_routes(start_name, end_name, dest_lat=16.9891, dest_lng=81.7840):
    """
    Calculates 3 route alternatives:
    1. Fastest Route (Direct, but might pass unlit/moderate-risk segments)
    2. Safer Route (⭐ Recommended, prioritizes well-lit, police-patrolled arterial roads)
    3. Balanced Route (Optimal balance of safety and travel time)
    """
    # Base waypoints around Rajahmundry center
    lat, lng = float(dest_lat), float(dest_lng)
    
    fastest_coords = [
        [lat - 0.020, lng - 0.015],
        [lat - 0.010, lng - 0.008],
        [lat, lng],
        [lat + 0.012, lng + 0.010],
        [lat + 0.025, lng + 0.020]
    ]
    
    safest_coords = [
        [lat - 0.020, lng - 0.015],
        [lat - 0.015, lng + 0.005],  # Diverts to Police Patrolled Main Road
        [lat - 0.005, lng + 0.012],  # Passes Central Police Station Kiosk
        [lat + 0.008, lng + 0.015],  # Passes 24/7 Lit Commercial Avenue
        [lat + 0.025, lng + 0.020]
    ]
    
    balanced_coords = [
        [lat - 0.020, lng - 0.015],
        [lat - 0.008, lng - 0.002],
        [lat + 0.005, lng + 0.008],
        [lat + 0.025, lng + 0.020]
    ]
    
    return {
        "start_location": start_name or "Rajahmundry Railway Station / Entry Point",
        "end_location": end_name or "Dowleswaram Barrage / Godavari Riverside",
        "routes": [
            {
                "id": "safer",
                "name": "Safer Route (Recommended ⭐)",
                "recommended": True,
                "duration_mins": 22,
                "distance_km": 6.8,
                "safety_score": 96,
                "safety_level": "🟢 Maximum Safety",
                "lighting": "100% Well-Lit Arterial Road",
                "police_patrol": "Passes 2 Active Police Kiosks & CCTV Grid",
                "risk_exposure": "Avoids isolated canal bypass",
                "coordinates": safest_coords,
                "badge": "⭐ Recommended for Solo & Women Travelers"
            },
            {
                "id": "fastest",
                "name": "Fastest Route",
                "recommended": False,
                "duration_mins": 18,
                "distance_km": 5.4,
                "safety_score": 72,
                "safety_level": "🟡 Moderate Caution",
                "lighting": "Partial lighting on canal stretches",
                "police_patrol": "Standard periodic patrol",
                "risk_exposure": "Passes narrow isolated shortcut",
                "coordinates": fastest_coords,
                "badge": "⚡ Shortest Travel Time"
            },
            {
                "id": "balanced",
                "name": "Balanced Route",
                "recommended": False,
                "duration_mins": 20,
                "distance_km": 6.0,
                "safety_score": 88,
                "safety_level": "🟢 Good Safety",
                "lighting": "Main street lighting",
                "police_patrol": "Regular street patrol",
                "risk_exposure": "Standard city avenue",
                "coordinates": balanced_coords,
                "badge": "⚖️ Balanced Time & Safety"
            }
        ]
    }
