import json
from datetime import datetime
import pytest
from unittest.mock import patch, MagicMock
from restaurant.models import Booking

@pytest.mark.django_db
def test_bookings_post_creates_booking(client):
    """
    Test POST to bookings() view when the booking does NOT already exist.
    """
    data = {
        "first_name": "Alice",
        "reservation_date": "2025-08-15",
        "reservation_slot": "18:00"
    }

    # Patch the Booking.objects.filter(...).exists() call
    with patch('restaurant.views.Booking.objects.filter') as mock_filter:
        mock_queryset = MagicMock()
        mock_queryset.filter.return_value.exists.return_value = False
        mock_filter.return_value = mock_queryset

        # Patch save method
        with patch('restaurant.views.Booking.save') as mock_save:
            response = client.post('/bookings/', data=json.dumps(data), content_type='application/json')

    assert response.status_code == 200
    assert 'application/json' in response['Content-Type']


@pytest.mark.django_db
def test_bookings_post_already_exists(client):
    """
    Test POST to bookings() view when the booking already exists.
    """
    data = {
        "first_name": "Bob",
        "reservation_date": "2025-08-15",
        "reservation_slot": "19:00"
    }

    with patch('restaurant.views.Booking.objects.filter') as mock_filter:
        mock_queryset = MagicMock()
        mock_queryset.filter.return_value.exists.return_value = True
        mock_filter.return_value = mock_queryset

        response = client.post('/bookings/', data=json.dumps(data), content_type='application/json')

    assert response.status_code == 200
    assert response.content == b"{'error':1}"


@pytest.mark.django_db
def test_bookings_get_returns_json(client):
    """
    Test GET to bookings() view returns JSON list of bookings.
    """
    date = datetime.today().date().isoformat()

    # Create a test booking in DB
    Booking.objects.create(
        first_name="Charlie",
        reservation_date=date,
        reservation_slot="20:00"
    )

    response = client.get(f'/bookings/?date={date}')

    assert response.status_code == 200
    assert 'application/json' in response['Content-Type']

    data = json.loads(response.content)
    assert isinstance(data, list)
    assert data[0]['fields']['first_name'] == "Charlie"
