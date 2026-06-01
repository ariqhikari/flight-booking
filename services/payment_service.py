"""Payment module.

Contains the price calculation rules and a simple payment processor.
``calculate_ticket_price`` is the headline Unit Testing target because it
has several logic branches (class multiplier, tax, validation).
"""

TAX_RATE = 0.11

CLASS_MULTIPLIER = {
    "economy": 1.0,
    "business": 1.5,
}

ACCEPTED_METHODS = ["credit_card", "debit_card", "e_wallet"]


def calculate_ticket_price(base_price, travel_class="economy", tax_rate=TAX_RATE):
    """Calculate the final ticket price including class surcharge and tax.

    Args:
        base_price: The flight's base fare. Must be zero or positive.
        travel_class: 'economy' or 'business'.
        tax_rate: Tax applied on top of the subtotal (default 11%).

    Returns:
        The total price, rounded to the nearest integer.

    Raises:
        ValueError: If base_price is negative or the class is unknown.
    """
    if base_price < 0:
        raise ValueError("base_price cannot be negative")

    travel_class = travel_class.strip().lower()
    if travel_class not in CLASS_MULTIPLIER:
        raise ValueError("unknown travel class: %s" % travel_class)

    subtotal = base_price * CLASS_MULTIPLIER[travel_class]
    total = subtotal * (1 + tax_rate)
    return round(total)


def process_payment(amount, method="credit_card"):
    """Process a payment and return a result dict.

    A payment succeeds when the amount is positive and the method is
    supported. Otherwise it fails with a reason.
    """
    method = method.strip().lower() if method else ""

    if amount is None or amount <= 0:
        return {"status": "FAILED", "reason": "Invalid amount", "amount": amount}

    if method not in ACCEPTED_METHODS:
        return {"status": "FAILED", "reason": "Unsupported method", "amount": amount}

    return {"status": "PAID", "reason": "Payment successful", "amount": amount}
