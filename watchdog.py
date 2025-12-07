from datetime import datetime, timedelta,timezone
from apscheduler.schedulers.background import BackgroundScheduler
import logging
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import SessionLocal, Ticket

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(message)s")
scheduler = BackgroundScheduler()
THRESHOLD = timedelta(minutes=5)


def check_sla():
    now = datetime.now(timezone.utc)
    db = SessionLocal()

    tickets = db.query(Ticket).all()

    for t in tickets:
        time_left = t.sla_deadline - now

        if time_left.total_seconds() < 0:
            t.status = "breached"
            logging.warning(f"Ticket {t.ticket_id} SLA breached!")
        elif timedelta(0) < time_left <= THRESHOLD:
            t.status = "warning"
            logging.info(f"Ticket {t.ticket_id} SLA approaching ({time_left}).")
        else:
            t.status = "ok"

    db.commit()
    db.close()


def start_watchdog():
    scheduler.add_job(check_sla, "interval", seconds=15)
    scheduler.start()
    logging.info("SLA Watchdog Started.")
