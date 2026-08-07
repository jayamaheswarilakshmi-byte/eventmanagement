from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
      path('events/', views.events, name='events'),
       path('services/', views.services, name='services'),
       path('about/', views.about, name='about'),
       path('contact/', views.contact, name='contact'),
       path('events/<int:pk>/', views.event_detail, name='event_detail'),
       # Booking Routes
    path('book-event/', views.book_event, name='book_event'),
    path('book-event/<int:event_id>/', views.book_event, name='book_event_with_id'),
    path('log-instant-call/', views.log_instant_call, name='log_instant_call'),
    path("track-call/", views.track_call, name="track_call"),
]