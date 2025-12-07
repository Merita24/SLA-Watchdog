from fastapi import FastAPI,HTTPException
from pydantic import BaseModel
from datetime import datetime,timezone
from sqlalchemy import create_engine,Column,Integer,String,DateTime
from sqlalchemy.orm import sessionmaker,declarative_base

app=FastAPI()

#DATABASE SETUP 

DATABASE_URL="sqlite:///./sla_watchdog.db"
engine=create_engine(DATABASE_URL,connect_args={"check_same_thread":False})
SessionLocal=sessionmaker(autocommit=False,autoflush=False,bind=engine)
Base=declarative_base()

#DATABASE MODEL FOR SLA TICKETS

class SLATickets(Base):
    __tablename__="tickets"
    
    ticket_id=Column(Integer,primary_key=True,index=True)
    title=Column(String)
    created_at=Column(DateTime,default=datetime.now(timezone.utc))
    sla_deadline=Column(DateTime)
    status=Column(String,default="open")
    time_remaining=Column(Integer) #in minutes
    
    


    
