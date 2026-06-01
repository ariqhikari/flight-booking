"""Flight search module.

Holds the in-memory flight catalogue and the logic for searching flights
by route. The pure functions here (``search_flights``, ``get_flight``) are
good candidates for Unit Testing.
"""

FLIGHTS = [
    {
        "code": "GA101",
        "airline": "Garuda Indonesia",
        "origin": "Jakarta",
        "destination": "Bali",
        "depart_time": "08:00",
        "base_price": 850000,
    },
    {
        "code": "GA102",
        "airline": "Garuda Indonesia",
        "origin": "Jakarta",
        "destination": "Bali",
        "depart_time": "13:30",
        "base_price": 920000,
    },
    {
        "code": "JT201",
        "airline": "Lion Air",
        "origin": "Jakarta",
        "destination": "Bali",
        "depart_time": "17:45",
        "base_price": 690000,
    },
    {
        "code": "QZ305",
        "airline": "AirAsia",
        "origin": "Jakarta",
        "destination": "Surabaya",
        "depart_time": "09:15",
        "base_price": 540000,
    },
]


def search_flights(origin, destination):
    """Return all flights matching the given origin and destination.

    The comparison is case-insensitive and ignores surrounding whitespace.
    Returns an empty list when no flight matches.
    """
    if not origin or not destination:
        return []

    origin = origin.strip().lower()
    destination = destination.strip().lower()

    return [
        flight
        for flight in FLIGHTS
        if flight["origin"].lower() == origin
        and flight["destination"].lower() == destination
    ]


def get_flight(code):
    """Return a single flight by its code, or ``None`` if not found."""
    if not code:
        return None

    code = code.strip().upper()
    for flight in FLIGHTS:
        if flight["code"] == code:
            return flight
    return None


def list_routes():
    """Return the unique list of available (origin, destination) routes."""
    routes = []
    for flight in FLIGHTS:
        route = (flight["origin"], flight["destination"])
        if route not in routes:
            routes.append(route)
    return routes
