"""Ticket module.

Generates ticket IDs and assembles the final e-ticket. ``generate_ticket_id``
is a clean pure function for Unit Testing; ``create_ticket`` ties the booking
data together and is exercised during Integration Testing.
"""

_counter = {"value": 0}


def generate_ticket_id(number):
    """Format a ticket sequence number as a ticket ID, e.g. 1 -> 'TCK001'.

    Raises:
        ValueError: If number is not a positive integer.
    """
    if not isinstance(number, int) or number <= 0:
        raise ValueError("number must be a positive integer")
    return "TCK%03d" % number


def next_ticket_id():
    """Increment the internal counter and return the next ticket ID."""
    _counter["value"] += 1
    return generate_ticket_id(_counter["value"])


def create_ticket(flight, seat, amount, passenger="Guest"):
    """Build a confirmed e-ticket from the booking details.

    Args:
        flight: The flight dict (as returned by ``flight_service``).
        seat: The reserved seat code.
        amount: The amount paid.
        passenger: Passenger name.

    Returns:
        A dict describing the issued e-ticket.
    """
    if not flight:
        raise ValueError("flight is required")

    return {
        "ticket_id": next_ticket_id(),
        "passenger": passenger,
        "flight_code": flight["code"],
        "airline": flight["airline"],
        "route": "%s -> %s" % (flight["origin"], flight["destination"]),
        "depart_time": flight["depart_time"],
        "seat": seat,
        "amount": amount,
        "status": "CONFIRMED",
    }


def reset_counter():
    """Reset the ticket counter. Useful for tests."""
    _counter["value"] = 0
