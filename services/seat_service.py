"""Seat selection module.

Manages seat availability per flight and the seat-class rules. Functions
like ``is_seat_available`` and ``seat_class`` are simple to Unit Test, while
``reserve_seat`` mutates the in-memory seat map and is useful for
Integration Testing.
"""

DEFAULT_SEATS = ["A1", "A2", "A3", "A4"]

_seat_map = {}


def _ensure_flight(flight_code):
    """Lazily create the seat map for a flight on first access."""
    flight_code = flight_code.strip().upper()
    if flight_code not in _seat_map:
        _seat_map[flight_code] = {seat: True for seat in DEFAULT_SEATS}
    return flight_code


def get_seats(flight_code):
    """Return a dict of ``{seat: is_available}`` for the given flight."""
    flight_code = _ensure_flight(flight_code)
    return dict(_seat_map[flight_code])


def is_seat_available(flight_code, seat):
    """Return ``True`` if the seat exists and is still free."""
    flight_code = _ensure_flight(flight_code)
    seat = seat.strip().upper() if seat else ""
    return _seat_map[flight_code].get(seat, False)


def reserve_seat(flight_code, seat):
    """Reserve a seat. Returns ``True`` on success, ``False`` if unavailable."""
    flight_code = _ensure_flight(flight_code)
    seat = seat.strip().upper() if seat else ""
    if not is_seat_available(flight_code, seat):
        return False
    _seat_map[flight_code][seat] = False
    return True


def release_seat(flight_code, seat):
    """Release a previously reserved seat, making it available again."""
    flight_code = _ensure_flight(flight_code)
    seat = seat.strip().upper() if seat else ""
    if seat in _seat_map[flight_code]:
        _seat_map[flight_code][seat] = True
        return True
    return False


def seat_class(seat):
    """Return the travel class for a seat.

    Row 1 seats (A1, B1, ...) are 'business'; all others are 'economy'.
    """
    if not seat:
        raise ValueError("seat is required")
    seat = seat.strip().upper()
    row = "".join(ch for ch in seat if ch.isdigit())
    if row == "1":
        return "business"
    return "economy"


def reset_seats():
    """Clear all reservations. Useful for tests to start from a clean state."""
    _seat_map.clear()
