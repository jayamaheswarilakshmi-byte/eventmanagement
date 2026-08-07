import json
from datetime import datetime

from django.contrib import messages
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from .models import ContactMessage

from .models import Event, EventBooking, InstantCallRequest
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import CallLog
from django.core.mail import send_mail
from django.conf import settings



def home(request):
    return render(request, "home.html")


def events(request):
    return render(request, "events.html")


def services(request):
    return render(request, "services.html")


def about(request):
    return render(request, "about.html")


def contact(request):
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        phone = request.POST.get("phone")
        subject = request.POST.get("subject")
        message = request.POST.get("message")

        # Save to database or send an email notification here
        messages.success(request, "Your message has been sent successfully!")
        return redirect("contact")

    return render(request, "contact.html")


def event_detail(request, pk):
    event = get_object_or_404(Event, pk=pk)
    context = {
        "event": event,
    }
    return render(request, "event_detail.html", context)

from django.shortcuts import render, redirect
from django.contrib import messages
from .models import EventBooking

def book_event(request, event_id=None):
    if request.method == "POST":
        name = request.POST.get("name", "").strip()
        phone = request.POST.get("phone", "").strip()
        email = request.POST.get("email", "").strip()
        event_type = request.POST.get("event_type", "").strip()
        event_date = request.POST.get("event_date", "").strip()
        location = request.POST.get("location", "").strip()
        user_message = request.POST.get("message", "").strip()

        # Input Validation
        if not all([name, phone, email, event_type, event_date, location]):
            messages.error(request, "Please fill in all required fields.")
            return render(request, "book_event.html", {
                "name": name,
                "phone": phone,
                "email": email,
                "location": location,
                "user_message": user_message,  # <-- Renamed key
            })

        # Save record to Database
        EventBooking.objects.create(
            name=name,
            phone=phone,
            email=email,
            event_type=event_type,
            event_date=event_date,
            location=location,
            message=user_message,
        )

        messages.success(request, "Your event booking request has been submitted successfully!")
        return redirect("book_event")

    return render(request, "book_event.html")
def log_instant_call(request):
    if request.method == "POST":
        # Parse payload sent via JavaScript fetch API
        try:
            data = json.loads(request.body) if request.body else {}
        except json.JSONDecodeError:
            data = {}

        # 1. Extract ALL fields sent from JavaScript
        name = data.get("name", "").strip()
        phone_number = data.get("phone_number") or data.get("phone", "+1234567890")
        email = data.get("email", "").strip()
        event_type = data.get("event_type", "").strip()

        # Extract client IP address
        x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
        if x_forwarded_for:
            ip = x_forwarded_for.split(",")[0].strip()
        else:
            ip = request.META.get("REMOTE_ADDR")

        # 2. Save ALL extracted fields to the database
        try:
            InstantCallRequest.objects.create(
                name=name,
                phone_number=phone_number,
                email=email,
                event_type=event_type,
                user_ip=ip
            )
            return JsonResponse({"status": "success"})
        except Exception as e:
            return JsonResponse({"status": "error", "reason": str(e)}, status=400)

    return JsonResponse({"status": "error", "reason": "Invalid HTTP method"}, status=405)
def contact(request):
    if request.method == "POST":
        name = request.POST.get("name", "").strip()
        sender_email = request.POST.get("email", "").strip()
        phone = request.POST.get("phone", "").strip()
        subject = request.POST.get("subject", "").strip()
        user_message = request.POST.get("message", "").strip()

        # Validation check for required fields
        if not name or not sender_email or not user_message:
            messages.error(request, "Please fill in all required fields.")
            return render(request, "contact.html")

        # 1. SAVE TO DATABASE
        ContactMessage.objects.create(
            name=name,
            email=sender_email,
            phone=phone,
            subject=subject,
            message=user_message,
        )

        # Fallback for subject line if empty
        if not subject:
            subject = f"New Contact Form Submission from {name}"

        # 2. FORMAT AND SEND EMAIL
        email_body = f"""
You have received a new message from your website contact form:

Name: {name}
Email: {sender_email}
Phone: {phone if phone else 'N/A'}
Subject: {subject}

Message:
{user_message}
        """

        # Replace with your actual recipient email address(es)
        recipient_list = ["admin@yourdomain.com", "info@ultimateevents.com"]

        try:
            send_mail(
                subject=f"[Contact Form] {subject}",
                message=email_body,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=recipient_list,
                fail_silently=False,
            )
            messages.success(
                request, "Your message has been sent successfully!"
            )
        except Exception as e:
            # Data is already saved to DB, so notify user about email issue
            messages.warning(
                request,
                "Your message was saved, but email notification failed.",
            )

        return redirect("contact")

    return render(request, "contact.html")
@csrf_exempt
def track_call(request):
    if request.method == "POST":
        phone_number = request.POST.get("phone_number", "+1-555-123-4567")
        user_agent = request.META.get("HTTP_USER_AGENT", "")

        # Save the click event to the database
        CallLog.objects.create(
            phone_number=phone_number, user_agent=user_agent
        )

        return JsonResponse(
            {"status": "success", "message": "Call logged successfully"}
        )

    return JsonResponse(
        {"status": "error", "message": "Invalid request"}, status=400
    )