from django.db import models
from django.conf import settings


class Location(models.Model):
    city = models.CharField(max_length=100, unique=True)
    state = models.CharField(max_length=100)
    country = models.CharField(max_length=100, default="India")
    status = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["city"]
        verbose_name = "Location"
        verbose_name_plural = "Locations"

    def __str__(self):
        return f"{self.city}, {self.state}"


class Event(models.Model):
    title = models.CharField(max_length=200)
    tagline = models.CharField(
        max_length=255, 
        help_text="Short description directly below title"
    )
    banner_image = models.ImageField(upload_to="events/banners/")
    description = models.TextField(help_text="Main full detail paragraph")

    # Highlights / Quick Stats
    attendees_count = models.CharField(max_length=50, default="500+ Attendees")
    speakers_count = models.CharField(max_length=50, default="30+ Speakers")
    duration = models.CharField(max_length=50, default="2-Day Event")
    location_name = models.CharField(max_length=100, default="Downtown Convention Center")

    # Pricing text
    pricing_description = models.TextField(
        default=(
            "Pricing varies based on the services selected and the scale of the "
            "event. Contact us for a detailed quote tailored to your specific needs."
        )
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Event"
        verbose_name_plural = "Events"

    def __str__(self):
        return self.title


class EventService(models.Model):
    event = models.ForeignKey(
        Event, 
        related_name="services", 
        on_delete=models.CASCADE
    )
    title = models.CharField(max_length=100)  # e.g., "Keynote Speakers", "Interactive Workshops"

    class Meta:
        verbose_name = "Event Service"
        verbose_name_plural = "Event Services"

    def __str__(self):
        return f"{self.event.title} - {self.title}"


class EventEnquiry(models.Model):
    event = models.ForeignKey(
        Event, 
        related_name="enquiries", 
        on_delete=models.CASCADE
    )
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    message = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Event Enquiry"
        verbose_name_plural = "Event Enquiries"

    def __str__(self):
        return f"Enquiry by {self.name} for {self.event.title}"

class EventBooking(models.Model):
    name = models.CharField(max_length=150)
    phone = models.CharField(max_length=20)
    email = models.EmailField()
    event_type = models.CharField(max_length=100)
    event_date = models.DateField()
    location = models.CharField(max_length=200)
    message = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Event Booking"
        verbose_name_plural = "Event Bookings"

    def __str__(self):
        return f"{self.name} - {self.event_type} on {self.event_date}"

class InstantCallRequest(models.Model):
    name = models.CharField(max_length=100, blank=True, null=True)
    phone_number = models.CharField(max_length=20)
    email = models.EmailField(blank=True, null=True)
    event_type = models.CharField(max_length=100, blank=True, null=True)
    user_ip = models.GenericIPAddressField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"Call request from {self.name or 'Anonymous'} ({self.phone_number})"
class ContactMessage(models.Model):
    name = models.CharField(max_length=150)
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True, null=True)
    subject = models.CharField(max_length=200, blank=True, null=True)
    message = models.TextField()
    user_ip = models.GenericIPAddressField(blank=True, null=True)  # <-- Add this field
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message from {self.name}"
class CallLog(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    phone_number = models.CharField(max_length=20)
    page_source = models.CharField(max_length=100, blank=True, null=True)
    user_agent = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Call Log"
        verbose_name_plural = "Call Logs"

    def __str__(self):
        user_name = self.user.username if self.user else "Anonymous"
        return f"Call request by {user_name} from {self.page_source}"