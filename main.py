from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from datetime import datetime

from models import SessionLocal, Ticket, Base, engine
from watchdog import start_watchdog, scheduler

from contextlib import asynccontextmanager



Base.metadata.create_all(bind=engine)



class TicketRequest(BaseModel):
    ticket_id: int
    title: str
    created_at: datetime
    sla_deadline: datetime
    status: str
    time_remaining: int



#   ----ASYNC LIFESPAN HANDLER-----

@asynccontextmanager
async def lifespan(app: FastAPI):
    
    start_watchdog()
    print("SLA Watchdog started.")

    yield

    
    scheduler.shutdown()
    print("SLA Watchdog stopped.")


app = FastAPI(lifespan=lifespan)


# ------ENDPOINTS--------

@app.post("/ticket/")
async def create_or_update_ticket(ticket: TicketRequest):
    db = SessionLocal()
    db_ticket = db.query(Ticket).filter(Ticket.ticket_id == ticket.ticket_id).first()

    if db_ticket:
        
        for key, value in ticket.dict().items():
            setattr(db_ticket, key, value)
    else:
        new_ticket = Ticket(**ticket.dict())
        db.add(new_ticket)

    db.commit()
    db.close()

    return {"message": "Ticket saved successfully"}


@app.get("/tickets/")
async def get_all_tickets():
    db = SessionLocal()
    data = db.query(Ticket).all()
    db.close()
    return data


@app.get("/ticket/{ticket_id}")
async def get_ticket(ticket_id: int):
    db = SessionLocal()
    ticket = db.query(Ticket).filter(Ticket.ticket_id == ticket_id).first()
    db.close()

    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket Not Found")

    return ticket
