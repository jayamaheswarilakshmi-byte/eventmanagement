from django.contrib import admin
from .models import Event, EventService, EventEnquiry
from .models import EventBooking
from .models import ContactMessage
from .models import CallLog,InstantCallRequest

class EventServiceInline(admin.TabularInline):
    model = EventService
    extra = 3  # Pre-loads 3 empty slots for quick service entry

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'attendees_count', 'duration', 'created_at')
    search_fields = ('title', 'description', 'location_name')
    inlines = [EventServiceInline]

@admin.register(EventEnquiry)
class EventEnquiryAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone', 'event', 'created_at')
    list_filter = ('event', 'created_at')
    search_fields = ('name', 'email', 'phone', 'message')
    readonly_fields = ('created_at',)

@admin.register(EventBooking)
class EventBookingAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone', 'event_type', 'event_date', 'created_at')
    search_fields = ('name', 'email', 'phone', 'location')
    list_filter = ('event_type', 'event_date', 'created_at')
@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone', 'subject', 'created_at', 'user_ip')
    search_fields = ('name', 'email', 'subject', 'message')
    readonly_fields = ('created_at', 'user_ip')
@admin.register(CallLog)
class CallLogAdmin(admin.ModelAdmin):
    list_display = ("user", "phone_number", "page_source", "created_at")
    list_filter = ("page_source", "created_at")
    search_fields = ("user__username", "phone_number", "page_source")
@admin.register(InstantCallRequest)
class InstantCallRequestAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "phone_number",
        "email",
        "event_type",
        "created_at",
    )
    search_fields = ("name", "phone_number", "email")
    list_filter = ("created_at",)
