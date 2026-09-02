from django.urls import path
from . import views

urlpatterns = [
    # Pages — Landing & Tourism Packages
    path('', views.index_view, name='index'),
    path('packages/', views.tourism_package_list_view, name='tourism_packages'),
    path('packages/<slug:package_slug>/', views.tourism_package_detail_view, name='package_detail'),

    # Pages — Safety & Crime Intelligence
    path('safety/', views.safety_intelligence_view, name='safety_intelligence'),
    path('safety/<str:destination_name>/', views.safety_intelligence_view, name='safety_intelligence_dest'),

    # Pages — Women Safe Tourism
    path('women-safety/', views.women_safety_view, name='women_safety'),

    # Pages — Verified Hotels
    path('hotels/', views.verified_hotels_view, name='verified_hotels'),

    # Pages — Emergency Map
    path('emergency/', views.emergency_map_view, name='emergency_map'),

    # Pages — AI Assistant
    path('ai-assistant/', views.ai_assistant_view, name='ai_assistant'),

    # Pages — Trip Planner
    path('trip-planner/', views.trip_planner_view, name='trip_planner'),

    # Pages — Memory Maker & Stories
    path('memories/', views.memory_maker_view, name='memory_maker'),
    path('memories/<int:memory_id>/', views.memory_detail_view, name='memory_detail'),
    path('memories/<int:memory_id>/pdf/', views.export_memory_pdf_view, name='export_memory_pdf'),
    path('memories/<int:memory_id>/delete/', views.delete_memory_view, name='delete_memory'),
    path('track/<str:token>/', views.live_tracker_view, name='live_tracker'),

    # Pages — Customer Feedback System
    path('feedback/', views.customer_feedback_view, name='customer_feedback'),

    # Pages — Post-Trip Review Module
    path('reviews/', views.post_trip_review_view, name='post_trip_review'),
    path('reviews/<str:destination_name>/', views.reviews_by_destination_view, name='reviews_by_destination'),

    # Pages — Profile & Admin
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('profile/', views.profile_view, name='profile'),
    path('logout/', views.logout_view, name='logout'),
    path('admin-dashboard/', views.admin_dashboard_view, name='admin_dashboard'),

    # Pages — Booking & Online Payment
    path('booking/<slug:package_slug>/', views.booking_view, name='booking'),
    path('booking/<str:booking_ref>/ticket-pdf/', views.export_ticket_pdf_view, name='ticket_pdf'),
    path('payment/<str:booking_ref>/', views.payment_view, name='payment'),
    path('payment/success/<str:booking_ref>/', views.payment_success_view, name='payment_success'),
    path('bookings/', views.booking_history_view, name='booking_history'),

    # REST APIs — Destinations & Safety
    path('api/destinations/', views.api_destinations, name='api_destinations'),
    path('api/destinations/<str:name>/', views.api_destination_detail, name='api_destination_detail'),
    path('api/safe-route/', views.api_safe_route, name='api_safe_route'),
    path('api/crime-stats/<str:destination_name>/', views.api_crime_stats, name='api_crime_stats'),

    # REST APIs — Tourism Packages
    path('api/packages/', views.api_packages, name='api_packages'),
    path('api/packages/<slug:slug>/', views.api_package_detail, name='api_package_detail'),

    # REST APIs — Customer Feedback
    path('api/feedback/', views.api_feedback, name='api_feedback'),
    path('api/feedback/stats/', views.api_feedback_stats, name='api_feedback_stats'),

    # REST APIs — Post-Trip Reviews
    path('api/reviews/', views.api_reviews, name='api_reviews'),
    path('api/reviews/stats/', views.api_reviews_stats, name='api_reviews_stats'),

    # REST APIs — SOS & Emergency
    path('api/sos/trigger/', views.api_sos_trigger, name='api_sos_trigger'),
    path('api/live-share/create/', views.api_live_share_create, name='api_live_share_create'),
    path('api/live-share/<str:token>/', views.api_live_share_detail, name='api_live_share_detail'),

    # REST APIs — AI Assistant
    path('api/ai/chat/', views.api_ai_chat, name='api_ai_chat'),
    path('api/ai/generate-itinerary/', views.api_generate_itinerary, name='api_generate_itinerary'),

    # REST APIs — Memory Maker
    path('api/memories/generate-story/', views.api_generate_story, name='api_generate_story'),
    path('api/memories/save/', views.api_save_memory, name='api_save_memory'),

    # Pages — Offline Emergency Hub & PWA Shell
    path('offline/', views.offline_hub_view, name='offline_hub'),
    path('manifest.json', views.manifest_view, name='manifest_json'),
    path('sw.js', views.service_worker_view, name='service_worker'),

    # REST APIs — Incidents & Admin
    path('api/incidents/report/', views.api_report_incident, name='api_report_incident'),
    path('api/admin/broadcast-alert/', views.api_admin_broadcast_alert, name='api_admin_broadcast_alert'),
    path('api/admin/toggle-hotel/', views.api_admin_toggle_hotel, name='api_admin_toggle_hotel'),

    # REST APIs — Government ERSS 112 CAD & Offline Sync
    path('api/erss/cad/<str:cad_id>/', views.api_erss_cad_status, name='api_erss_cad_status'),
    path('api/sos/sync-offline/', views.api_offline_sync_sos, name='api_offline_sync_sos'),
    path('api/emergency/offline-bundle/', views.api_emergency_offline_bundle, name='api_emergency_offline_bundle'),
]
