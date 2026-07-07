"""FlyNow - Flight Booking Mini App.

A small Flask application used as the codebase for the Software Testing
Levels challenge. It deliberately keeps logic in separate service modules so
that students can practice:

  * Unit Testing        -> pure functions in services/*
  * Integration Testing -> the Search -> Seat -> Payment -> Ticket flow
  * System Testing       -> the HTTP endpoints (/search, /api/search, ...)

No database, in-memory data only.
"""

import os
from datetime import datetime, timedelta, timezone

import jwt

from flask import Flask, render_template, request, redirect, url_for, jsonify

from services import flight_service, seat_service, payment_service, ticket_service

app = Flask(__name__)
app.config["JWT_SECRET_KEY"] = os.environ.get("JWT_SECRET_KEY", "flynow-dev-secret")
app.config["JWT_ALGORITHM"] = os.environ.get("JWT_ALGORITHM", "HS256")
app.config["JWT_ACCESS_TOKEN_EXPIRES_MINUTES"] = int(
    os.environ.get("JWT_ACCESS_TOKEN_EXPIRES_MINUTES", "60")
)
app.config["LOGIN_USERNAME"] = os.environ.get("LOGIN_USERNAME", "admin")
app.config["LOGIN_PASSWORD"] = os.environ.get("LOGIN_PASSWORD", "admin123")


def api_success(message, data=None, status_code=200):
    return (
        jsonify(
            {
                "success": True,
                "message": message,
                "data": data,
                "errors": None,
            }
        ),
        status_code,
    )


def api_error(message, errors=None, status_code=400):
    return (
        jsonify(
            {
                "success": False,
                "message": message,
                "data": None,
                "errors": errors,
            }
        ),
        status_code,
    )


def create_access_token(username):
    now = datetime.now(timezone.utc)
    payload = {
        "sub": username,
        "iat": now,
        "exp": now
        + timedelta(minutes=app.config["JWT_ACCESS_TOKEN_EXPIRES_MINUTES"]),
    }
    return jwt.encode(
        payload,
        app.config["JWT_SECRET_KEY"],
        algorithm=app.config["JWT_ALGORITHM"],
    )


def get_bearer_token():
    authorization = request.headers.get("Authorization", "")
    if not authorization.startswith("Bearer "):
        return None
    return authorization.split(" ", 1)[1].strip() or None


def verify_access_token(token):
    try:
        decoded = jwt.decode(
            token,
            app.config["JWT_SECRET_KEY"],
            algorithms=[app.config["JWT_ALGORITHM"]],
        )
        return decoded.get("sub")
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None


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
    return api_success(
        "Flights retrieved successfully",
        {"items": flights},
    )


@app.route("/api/login", methods=["POST"])
def api_login():
    payload = request.get_json(silent=True)
    if not payload:
        return api_error(
            "Validation failed",
            {
                "username": "Username is required",
                "password": "Password is required",
            },
            422,
        )

    username = str(payload.get("username", "")).strip()
    password = str(payload.get("password", "")).strip()

    if not username:
        return api_error(
            "Validation failed",
            {"username": "Username is required"},
            422,
        )

    if not password:
        return api_error(
            "Validation failed",
            {"password": "Password is required"},
            422,
        )

    if username != app.config["LOGIN_USERNAME"]:
        return api_error(
            "Invalid username or password",
            None,
            401,
        )

    if password != app.config["LOGIN_PASSWORD"]:
        return api_error(
            "Invalid username or password",
            None,
            401,
        )

    token = create_access_token(username)
    return api_success(
        "Login successful",
        {
            "user": {
                "id": "USR001",
                "name": "FlyNow User",
                "username": username,
                "role": "user",
            },
            "token": {
                "access_token": token,
                "token_type": "Bearer",
                "expires_in": app.config["JWT_ACCESS_TOKEN_EXPIRES_MINUTES"] * 60,
            },
        },
        200,
    )


@app.route("/api/book-seat", methods=["POST"])
def api_book_seat():
    token = get_bearer_token()
    if not token or not verify_access_token(token):
        return api_error(
            "Unauthorized access",
            None,
            401,
        )

    payload = request.get_json(silent=True)
    if not payload:
        return api_error(
            "Validation failed",
            {
                "flight": "Flight ID is required",
                "seat": "Seat is required",
            },
            422,
        )

    flight_code = str(payload.get("flight", "")).strip().upper()
    seat = str(payload.get("seat", "")).strip().upper()
    passenger = str(payload.get("passenger", "Guest")).strip() or "Guest"

    if not flight_code:
        return api_error(
            "Validation failed",
            {"flight": "Flight ID is required"},
            422,
        )

    if not seat:
        return api_error(
            "Validation failed",
            {"seat": "Seat is required"},
            422,
        )

    flight = flight_service.get_flight(flight_code)
    if not flight:
        return api_error(
            "Flight not found",
            None,
            404,
        )

    if not seat_service.is_seat_available(flight_code, seat):
        return api_error(
            "Seat already booked",
            {
                "seat": "Seat %s is already booked for flight %s" % (seat, flight_code)
            },
            409,
        )

    reserved = seat_service.reserve_seat(flight_code, seat)
    if not reserved:
        return api_error(
            "Seat already booked",
            {
                "seat": "Seat %s is already booked for flight %s" % (seat, flight_code)
            },
            409,
        )

    booking = {
        "booking_id": ticket_service.next_ticket_id(),
        "passenger": passenger,
        "flight": {
            "code": flight["code"],
            "airline": flight["airline"],
            "origin": flight["origin"],
            "destination": flight["destination"],
            "depart_time": flight["depart_time"],
        },
        "seat": seat,
        "status": "CONFIRMED",
    }

    return api_success(
        "Booking created successfully",
        booking,
        201,
    )


@app.route("/healthz")
def healthz():
    return api_success("Service is healthy", {"status": "ok"})


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
