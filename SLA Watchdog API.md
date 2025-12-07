----SLA Watchdog API---

A simple API that tracks ticket deadlines and automatically alerts when an SLA is close to being missed or already missed.

This project demonstrates:

A FastAPI backend

SQLAlchemy ORM models

Background scheduling to run SLA checks

Asynchronous endpoints

Clean project structure

---Project Structure----
sla-watchdog/
│
├── main.py              # FastAPI app + scheduler lifespan
├── models.py            # SQLAlchemy models + DB config
├── watchdog.py          # SLA checking logic
├── requirements.txt
└── README.md

---- How It Works----

The user creates a ticket with:

title

description

sla_deadline (UTC datetime)

The system stores it in a database.

The background scheduler runs every 60 seconds:

Checks tickets

Prints an alert if:

SLA will be missed in 15 minutes

SLA is already missed

All API calls interact with the database asynchronously.

----Running the Project-----
1. Install dependencies
pip install -r requirements.txt


-----Requirements------

fastapi
uvicorn
sqlalchemy
asyncpg
apscheduler
python-dotenv

2. Run the API server
uvicorn main:app --reload


You should see:

Scheduler started...


and FastAPI docs at:

 http://127.0.0.1:8000/docs

http://127.0.0.1:8000/redoc

Curl Examples

Below are real working curl commands you can paste into a terminal.

 Create a Ticket
curl -X POST "http://127.0.0.1:8000/tickets" \
     -H "Content-Type: application/json" \
     -d '{
           "title": "Payment outage",
           "description": "Payments not going through",
           "sla_deadline": "2025-01-05T14:00:00Z"
         }'

Get All Tickets
curl "http://127.0.0.1:8000/tickets"

Get a Ticket by ID
curl "http://127.0.0.1:8000/tickets/1"

Update a Ticket
curl -X PUT "http://127.0.0.1:8000/tickets/1" \
    -H "Content-Type: application/json" \
     -d '{
           "title": "Updated title",
           "description": "Updated description",
           "sla_deadline": "2025-01-06T12:00:00Z"
         }'

Delete a Ticket
curl -X DELETE "http://127.0.0.1:8000/tickets/1"

SLA Checking Logic

Runs every 60 seconds:

if now + 15 minutes >= sla_deadline:
    print("Ticket 1 is about to miss SLA!")

if now >= sla_deadline:
    print("Ticket 1 has MISSED the SLA!")