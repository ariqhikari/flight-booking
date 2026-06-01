"""FlyNow - Flight Booking Mini App.

A small Flask application used as the codebase for the Software Testing
Levels challenge. It deliberately keeps logic in separate service modules so
that students can practice:

  * Unit Testing        -> pure functions in services/*
  * Integration Testing -> the Search -> Seat -> Payment -> Ticket flow
  * System Testing       -> the HTTP endpoints (/search, /api/search, ...)

No database, no login, in-memory data only.
"""

import os

from flask import Flask, render_template, request, redirect, url_for, jsonify

from services import flight_service, seat_service, payment_service, ticket_service

app = Flask(__name__)


@app.route("/")
def home():
    return render_template(
        "home.html",
        routes=flight_service.list_routes(),
        flights=None,
        origin="",
        destination="",
    )


@app.route("/search", methods=["GET", "POST"])
def search():
    origin = request.values.get("origin", "")
    destination = request.values.get("destination", "")
    flights = flight_service.search_flights(origin, destination)
    return render_template(
        "home.html",
        routes=flight_service.list_routes(),
        flights=flights,
        origin=origin,
        destination=destination,
    )


@app.route("/select-seat")
def select_seat():
    code = request.values.get("flight", "")
    flight = flight_service.get_flight(code)
    if not flight:
        return redirect(url_for("home"))
    seats = seat_service.get_seats(code)
    return render_template("seats.html", flight=flight, seats=seats)


@app.route("/payment", methods=["GET", "POST"])
def payment():
    code = request.values.get("flight", "")
    seat = request.values.get("seat", "")
    flight = flight_service.get_flight(code)
    if not flight or not seat:
        return redirect(url_for("home"))

    travel_class = seat_service.seat_class(seat)
    price = payment_service.calculate_ticket_price(
        flight["base_price"], travel_class
    )
    return render_template(
        "payment.html",
        flight=flight,
        seat=seat,
        travel_class=travel_class,
        price=price,
    )


@app.route("/ticket", methods=["POST"])
def ticket():
    code = request.form.get("flight", "")
    seat = request.form.get("seat", "")
    method = request.form.get("method", "credit_card")
    passenger = request.form.get("passenger", "Guest") or "Guest"

    flight = flight_service.get_flight(code)
    if not flight or not seat:
        return redirect(url_for("home"))

    if not seat_service.reserve_seat(code, seat):
        return render_template(
            "ticket.html",
            error="Seat %s is no longer available. Please choose another seat."
            % seat,
            flight=flight,
        )

    travel_class = seat_service.seat_class(seat)
    price = payment_service.calculate_ticket_price(flight["base_price"], travel_class)
    result = payment_service.process_payment(price, method)

    if result["status"] != "PAID":
        seat_service.release_seat(code, seat)
        return render_template(
            "ticket.html",
            error="Payment failed: %s" % result["reason"],
            flight=flight,
        )

    issued = ticket_service.create_ticket(flight, seat, price, passenger)
    return render_template("ticket.html", ticket=issued, error=None)


@app.route("/api/search")
def api_search():
    origin = request.args.get("origin", "")
    destination = request.args.get("destination", "")
    flights = flight_service.search_flights(origin, destination)
    return jsonify(flights)


@app.route("/healthz")
def healthz():
    return {"status": "ok"}


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
