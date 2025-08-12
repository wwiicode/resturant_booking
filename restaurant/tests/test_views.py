from django.test import TestCase
from django.urls import reverse
from restaurant.models import Booking
from datetime import date
import json

class BookingViewTest(TestCase):

    def setUp(self):
        self.booking_data = {
            "first_name": "Bob",
            "reservation_date": str(date.today()),
            "reservation_slot": 3
        }

    def test_post_booking_success(self):
        response = self.client.post(
            "/bookings/",
            data=json.dumps(self.booking_data),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Booking.objects.count(), 1)
        self.assertEqual(Booking.objects.first().first_name, "Bob")

    def test_post_booking_duplicate(self):
        # Create initial booking
        self.client.post(
            "/bookings/",
            data=json.dumps(self.booking_data),
            content_type='application/json'
        )
        # Try to create a duplicate
        response = self.client.post(
            "/bookings/",
            data=json.dumps(self.booking_data),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 409)

    def test_get_bookings(self):
        Booking.objects.create(
            first_name="Charlie",
            reservation_date=date.today(),
            reservation_slot=1
        )
        response = self.client.get(f"/bookings/?date={date.today()}")
        self.assertEqual(response.status_code, 200)
        self.assertIn("Charlie", response.content.decode())

