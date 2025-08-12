from django.test import TestCase
from restaurant.models import Booking, Menu
from datetime import date

class BookingModelTest(TestCase):

    def test_booking_creation(self):
        booking = Booking.objects.create(
            first_name="Alice",
            reservation_date=date.today(),
            reservation_slot=5
        )
        self.assertEqual(str(booking), "Alice")
        self.assertEqual(booking.reservation_slot, 5)

class MenuModelTest(TestCase):

    def test_menu_creation(self):
        menu = Menu.objects.create(
            name="Pizza",
            price=15,
            menu_item_description="Delicious cheese pizza"
        )
        self.assertEqual(str(menu), "Pizza")
        self.assertEqual(menu.price, 15)
