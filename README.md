# FlyNow — Flight Booking Mini App

A small Flask web application used as the practice codebase for the
**Software Testing Levels** challenge (KPPL). It lets a user:

1. **Search Flight** (e.g. Jakarta → Bali)
2. **Select Seat** (A1–A4)
3. **Pay** (Pay Now)
4. **Get an E-Ticket** (e.g. `TCK001`)

The code is intentionally split into separate modules so you can practice
**Unit Testing**, **Integration Testing**, and **System Testing** on the
same project. No database, no login, in-memory data only.

## Project Structure

```text
flight-booking-mini-app/
├── app.py                  # Flask routes (the HTTP layer)
├── requirements.txt
├── README.md
├── CHALLENGE.md            # The assignment brief
├── services/
│   ├── flight_service.py   # search_flights(), get_flight()
│   ├── seat_service.py     # is_seat_available(), reserve_seat(), seat_class()
│   ├── payment_service.py  # calculate_ticket_price(), process_payment()
│   └── ticket_service.py   # generate_ticket_id(), create_ticket()
├── templates/              # home, seats, payment, ticket pages
└── tests/                  # put your own tests here
```

## Architecture

```text
        Browser
           |
           v
        Flask App  (app.py — the HTTP layer)
           |
   +-------+--------+--------------+--------------+
   |                |              |              |
   v                v              v              v
flight_service  seat_service  payment_service  ticket_service
```

The Flask app only handles HTTP requests and delegates the real work to the
service modules. Each booking step crosses one of these module boundaries,
which is exactly what makes the app useful for practicing the three testing
levels.

## How to Run

You need **Python 3.10+**.

```bash
git clone <repository-url>
cd flight-booking-mini-app

# (optional) create a virtual environment
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate

pip install -r requirements.txt

python app.py
```

Then open:

```text
http://localhost:5000
```

> Try the route **Jakarta → Bali** to see available flights.

### Recommended endpoint for JMeter

```text
http://localhost:5000/api/search?origin=Jakarta&destination=Bali
```

## HTTP Endpoints (useful for System Testing)

| Method   | Path           | Purpose                          |
| -------- | -------------- | -------------------------------- |
| GET      | `/`            | Home / search form               |
| GET/POST | `/search`      | Search flights by origin & dest. |
| GET      | `/select-seat` | Show seats for a flight          |
| GET/POST | `/payment`     | Show price & payment form        |
| POST     | `/ticket`      | Reserve seat, pay, issue ticket  |
| GET      | `/api/search`  | Search flights, returns **JSON** |
| GET      | `/healthz`     | Health check (returns JSON)      |

Example for a load-testing tool (e.g. JMeter):

```text
GET  /search?origin=Jakarta&destination=Bali
GET  /api/search?origin=Jakarta&destination=Bali        (JSON, easy to measure)
GET  /select-seat?flight=GA101
POST /payment        (form: flight=GA101&seat=A2)
POST /ticket         (form: flight=GA101&seat=A2&method=credit_card)
```

> The `/api/search` endpoint returns a clean JSON array, which is easier to
> assert on and measure than the HTML pages — ideal for JMeter.

## Functions Worth Unit Testing

These are pure (or near-pure) functions with clear logic branches:

- `payment_service.calculate_ticket_price(base_price, travel_class, tax_rate)`
- `seat_service.is_seat_available(flight_code, seat)`
- `seat_service.seat_class(seat)`
- `ticket_service.generate_ticket_id(number)`
- `flight_service.search_flights(origin, destination)`

## Integration Flow

```text
Search Flight → Select Seat → Payment → Generate Ticket
```

Each step crosses a module boundary, so the booking flow is a natural target
for Integration Testing.

See **CHALLENGE.md** for the full assignment.
